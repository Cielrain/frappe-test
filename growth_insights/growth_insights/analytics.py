from collections import defaultdict

import frappe
from frappe.utils import add_months, flt, get_first_day, getdate, nowdate


LIFECYCLE_DOCTYPE = "Customer Lifecycle Event"
ACTIVE_EVENTS = {"Signup", "Activation", "Reactivation", "Expansion"}
NEW_LOGO_EVENTS = {"Signup", "Activation", "Reactivation"}


def get_default_window(months=12):
    end_date = getdate(nowdate())
    start_date = get_first_day(add_months(end_date, -(months - 1)))
    return start_date, end_date


def month_key(date_value):
    return getdate(date_value).strftime("%Y-%m")


def get_events(start_date=None, end_date=None):
    start_date, end_date = start_date or get_default_window()[0], end_date or get_default_window()[1]
    return frappe.get_all(
        LIFECYCLE_DOCTYPE,
        filters={
            "event_date": ["between", [start_date, end_date]],
        },
        fields=[
            "name",
            "customer_id",
            "customer_name",
            "event_type",
            "event_date",
            "customer_segment",
            "plan",
            "mrr",
            "seats",
            "region",
            "city",
            "industry",
            "channel",
            "health_score",
            "churn_reason",
        ],
        order_by="event_date asc, creation asc",
    )


def build_growth_snapshot(start_date=None, end_date=None):
    start_date, end_date = start_date or get_default_window()[0], end_date or get_default_window()[1]
    events = get_events(start_date, end_date)
    months = []
    cursor = get_first_day(start_date)
    while cursor <= getdate(end_date):
        months.append(month_key(cursor))
        cursor = add_months(cursor, 1)

    monthly = {
        key: {
            "month": key,
            "new_customers": 0,
            "churned_customers": 0,
            "expansions": 0,
            "new_mrr": 0,
            "expansion_mrr": 0,
            "churn_mrr": 0,
            "net_mrr": 0,
        }
        for key in months
    }

    region = defaultdict(lambda: {"region": "", "active_customers": 0, "mrr": 0})
    channel = defaultdict(lambda: {"channel": "", "new_customers": 0, "mrr": 0})
    segment = defaultdict(lambda: {"segment": "", "active_customers": 0, "mrr": 0})
    churn_reason = defaultdict(int)
    customer_state = {}

    for event in events:
        key = month_key(event.event_date)
        row = monthly.setdefault(
            key,
            {
                "month": key,
                "new_customers": 0,
                "churned_customers": 0,
                "expansions": 0,
                "new_mrr": 0,
                "expansion_mrr": 0,
                "churn_mrr": 0,
                "net_mrr": 0,
            },
        )

        mrr = flt(event.mrr)
        state = customer_state.get(
            event.customer_id,
            {
                "active": False,
                "mrr": 0,
                "customer_name": event.customer_name,
                "region": event.region,
                "customer_segment": event.customer_segment,
            },
        )

        if event.event_type in NEW_LOGO_EVENTS:
            row["new_customers"] += 1
            row["new_mrr"] += mrr
            row["net_mrr"] += mrr
            state["active"] = True
            state["mrr"] = mrr
            channel[event.channel]["channel"] = event.channel
            channel[event.channel]["new_customers"] += 1
            channel[event.channel]["mrr"] += mrr
        elif event.event_type == "Expansion":
            row["expansions"] += 1
            row["expansion_mrr"] += mrr
            row["net_mrr"] += mrr
            state["active"] = True
            state["mrr"] = flt(state.get("mrr")) + mrr
        elif event.event_type == "Churn":
            churn_mrr = flt(state.get("mrr")) or mrr
            row["churned_customers"] += 1
            row["churn_mrr"] += churn_mrr
            row["net_mrr"] -= churn_mrr
            state["active"] = False
            state["mrr"] = 0
            churn_reason[event.churn_reason or "Unknown"] += 1

        state.update(
            {
                "customer_name": event.customer_name,
                "region": event.region,
                "customer_segment": event.customer_segment,
                "event_type": event.event_type,
            }
        )
        customer_state[event.customer_id] = state

    active_customers = []
    churned_customers = []
    for state in customer_state.values():
        if not state.get("active"):
            churned_customers.append(state)
            continue

        active_customers.append(state)
        mrr = flt(state.get("mrr"))
        region[state["region"]]["region"] = state["region"]
        region[state["region"]]["active_customers"] += 1
        region[state["region"]]["mrr"] += mrr
        segment[state["customer_segment"]]["segment"] = state["customer_segment"]
        segment[state["customer_segment"]]["active_customers"] += 1
        segment[state["customer_segment"]]["mrr"] += mrr

    ordered_monthly = [monthly[key] for key in sorted(monthly)]
    total_new = sum(item["new_customers"] for item in ordered_monthly)
    total_churn = sum(item["churned_customers"] for item in ordered_monthly)
    total_new_mrr = sum(item["new_mrr"] for item in ordered_monthly)
    total_expansion_mrr = sum(item["expansion_mrr"] for item in ordered_monthly)
    total_churn_mrr = sum(item["churn_mrr"] for item in ordered_monthly)
    active_mrr = sum(flt(item.get("mrr")) for item in active_customers)

    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "summary": {
            "active_customers": len(active_customers),
            "churned_customers": len(churned_customers),
            "new_customers": total_new,
            "active_mrr": active_mrr,
            "net_new_mrr": total_new_mrr + total_expansion_mrr - total_churn_mrr,
            "gross_new_mrr": total_new_mrr,
            "expansion_mrr": total_expansion_mrr,
            "churn_mrr": total_churn_mrr,
            "logo_churn_rate": (total_churn / total_new * 100) if total_new else 0,
        },
        "monthly": ordered_monthly,
        "regions": sorted(region.values(), key=lambda item: item["mrr"], reverse=True),
        "channels": sorted(channel.values(), key=lambda item: item["new_customers"], reverse=True),
        "segments": sorted(segment.values(), key=lambda item: item["mrr"], reverse=True),
        "churn_reasons": [
            {"reason": reason, "count": count}
            for reason, count in sorted(churn_reason.items(), key=lambda item: item[1], reverse=True)
        ],
        "recent_events": list(reversed(events[-12:])),
    }
