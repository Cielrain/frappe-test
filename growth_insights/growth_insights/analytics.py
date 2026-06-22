from collections import defaultdict

import frappe
from frappe.utils import add_months, flt, get_first_day, getdate, nowdate


LIFECYCLE_DOCTYPE = "Energy Service Lifecycle Event"
NEW_LOGO_EVENTS = {"Signup"}


def get_default_window(months=12):
    end_date = getdate(nowdate())
    start_date = get_first_day(add_months(end_date, -(months - 1)))
    return start_date, end_date


def month_key(date_value):
    return getdate(date_value).strftime("%Y-%m")


def get_events(start_date=None, end_date=None, include_prior=False):
    start_date, end_date = start_date or get_default_window()[0], end_date or get_default_window()[1]
    filters = {"event_date": ["between", [start_date, end_date]]}
    if include_prior:
        filters = {"event_date": ["<=", end_date]}

    return frappe.get_all(
        LIFECYCLE_DOCTYPE,
        filters=filters,
        fields=[
            "name",
            "customer_id",
            "customer_name",
            "event_type",
            "event_date",
            "service_object_type",
            "service_plan",
            "mrr",
            "monthly_swap_quota",
            "vehicle_type",
            "battery_model",
            "station_name",
            "cabinet_count",
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
    start_date = getdate(start_date)
    end_date = getdate(end_date)
    events = get_events(start_date, end_date, include_prior=True)
    months = []
    cursor = get_first_day(start_date)
    while cursor <= getdate(end_date):
        months.append(month_key(cursor))
        cursor = add_months(cursor, 1)

    monthly = {
        key: {
            "month": key,
            "new_customers": 0,
            "activations": 0,
            "reactivations": 0,
            "churned_customers": 0,
            "expansions": 0,
            "new_mrr": 0,
            "reactivation_mrr": 0,
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
    opening_active_customers = 0
    opening_state_captured = False
    window_events = []

    for event in events:
        event_date = getdate(event.event_date)
        in_window = start_date <= event_date <= end_date

        if not opening_state_captured and event_date >= start_date:
            opening_active_customers = _active_customer_count(customer_state)
            opening_state_captured = True

        if in_window:
            window_events.append(event)

        key = month_key(event.event_date)
        row = _monthly_row(monthly, key) if in_window else None

        mrr = flt(event.mrr)
        state = customer_state.get(
            event.customer_id,
            {
                "active": False,
                "mrr": 0,
                "customer_name": event.customer_name,
                "region": event.region,
                "customer_segment": event.service_object_type,
            },
        )

        if event.event_type in NEW_LOGO_EVENTS:
            if in_window:
                row["new_customers"] += 1
                row["new_mrr"] += mrr
                row["net_mrr"] += mrr
                channel[event.channel]["channel"] = event.channel
                channel[event.channel]["new_customers"] += 1
                channel[event.channel]["mrr"] += mrr
            state["active"] = True
            state["mrr"] = mrr
        elif event.event_type == "Activation":
            if in_window:
                row["activations"] += 1
            state["active"] = True
            state["mrr"] = mrr
        elif event.event_type == "Reactivation":
            if in_window:
                row["reactivations"] += 1
                row["reactivation_mrr"] += mrr
                row["net_mrr"] += mrr
            state["active"] = True
            state["mrr"] = mrr
        elif event.event_type == "Expansion":
            if in_window:
                row["expansions"] += 1
                row["expansion_mrr"] += mrr
                row["net_mrr"] += mrr
            state["active"] = True
            state["mrr"] = flt(state.get("mrr")) + mrr
        elif event.event_type == "Churn":
            churn_mrr = flt(state.get("mrr")) or mrr
            if in_window:
                row["churned_customers"] += 1
                row["churn_mrr"] += churn_mrr
                row["net_mrr"] -= churn_mrr
                churn_reason[event.churn_reason or "Unknown"] += 1
            state["active"] = False
            state["mrr"] = 0

        state.update(
            {
                "customer_name": event.customer_name,
                "region": event.region,
                "customer_segment": event.service_object_type,
                "event_type": event.event_type,
            }
        )
        customer_state[event.customer_id] = state

    if not opening_state_captured:
        opening_active_customers = _active_customer_count(customer_state)

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
    total_activations = sum(item["activations"] for item in ordered_monthly)
    total_reactivations = sum(item["reactivations"] for item in ordered_monthly)
    total_churn = sum(item["churned_customers"] for item in ordered_monthly)
    total_new_mrr = sum(item["new_mrr"] for item in ordered_monthly)
    total_reactivation_mrr = sum(item["reactivation_mrr"] for item in ordered_monthly)
    total_expansion_mrr = sum(item["expansion_mrr"] for item in ordered_monthly)
    total_churn_mrr = sum(item["churn_mrr"] for item in ordered_monthly)
    active_mrr = sum(flt(item.get("mrr")) for item in active_customers)
    churn_base = max(opening_active_customers + total_new + total_reactivations, 1)

    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "summary": {
            "active_customers": len(active_customers),
            "churned_customers": len(churned_customers),
            "new_customers": total_new,
            "activations": total_activations,
            "reactivations": total_reactivations,
            "active_mrr": active_mrr,
            "net_new_mrr": total_new_mrr + total_reactivation_mrr + total_expansion_mrr - total_churn_mrr,
            "gross_new_mrr": total_new_mrr,
            "reactivation_mrr": total_reactivation_mrr,
            "expansion_mrr": total_expansion_mrr,
            "churn_mrr": total_churn_mrr,
            "logo_churn_rate": total_churn / churn_base * 100,
        },
        "monthly": ordered_monthly,
        "regions": sorted(region.values(), key=lambda item: item["mrr"], reverse=True),
        "channels": sorted(channel.values(), key=lambda item: item["new_customers"], reverse=True),
        "segments": sorted(segment.values(), key=lambda item: item["mrr"], reverse=True),
        "churn_reasons": [
            {"reason": reason, "count": count}
            for reason, count in sorted(churn_reason.items(), key=lambda item: item[1], reverse=True)
        ],
        "recent_events": list(reversed(window_events[-12:])),
    }


def _monthly_row(monthly, key):
    return monthly.setdefault(
        key,
        {
            "month": key,
            "new_customers": 0,
            "activations": 0,
            "reactivations": 0,
            "churned_customers": 0,
            "expansions": 0,
            "new_mrr": 0,
            "reactivation_mrr": 0,
            "expansion_mrr": 0,
            "churn_mrr": 0,
            "net_mrr": 0,
        },
    )


def _active_customer_count(customer_state):
    return sum(1 for state in customer_state.values() if state.get("active"))
