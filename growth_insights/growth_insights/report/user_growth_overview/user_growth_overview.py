from frappe import _
from frappe.utils import flt

from growth_insights.growth_insights.analytics import build_growth_snapshot, get_default_window


def execute(filters=None):
    filters = filters or {}
    default_start, default_end = get_default_window()
    snapshot = build_growth_snapshot(
        filters.get("from_date") or default_start,
        filters.get("to_date") or default_end,
    )

    columns = [
        {"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 110},
        {"label": _("New Signups"), "fieldname": "new_customers", "fieldtype": "Int", "width": 130},
        {"label": _("Activations"), "fieldname": "activations", "fieldtype": "Int", "width": 120},
        {"label": _("Reactivations"), "fieldname": "reactivations", "fieldtype": "Int", "width": 130},
        {"label": _("Churned Accounts"), "fieldname": "churned_customers", "fieldtype": "Int", "width": 150},
        {"label": _("Expansion Events"), "fieldname": "expansions", "fieldtype": "Int", "width": 140},
        {"label": _("New Service Revenue"), "fieldname": "new_mrr", "fieldtype": "Currency", "width": 170},
        {"label": _("Reactivation Revenue"), "fieldname": "reactivation_mrr", "fieldtype": "Currency", "width": 170},
        {"label": _("Expansion Revenue"), "fieldname": "expansion_mrr", "fieldtype": "Currency", "width": 160},
        {"label": _("Churn Revenue"), "fieldname": "churn_mrr", "fieldtype": "Currency", "width": 150},
        {"label": _("Net Revenue"), "fieldname": "net_mrr", "fieldtype": "Currency", "width": 130},
        {"label": _("Net Account Growth"), "fieldname": "net_logo_growth", "fieldtype": "Int", "width": 160},
    ]

    data = []
    for row in snapshot["monthly"]:
        item = dict(row)
        item["net_logo_growth"] = item["new_customers"] + item["reactivations"] - item["churned_customers"]
        data.append(item)

    chart = {
        "data": {
            "labels": [item["month"] for item in data],
            "datasets": [
                {"name": _("New Signups"), "chartType": "bar", "values": [item["new_customers"] for item in data]},
                {"name": _("Reactivations"), "chartType": "bar", "values": [item["reactivations"] for item in data]},
                {"name": _("Churned Accounts"), "chartType": "bar", "values": [item["churned_customers"] for item in data]},
                {"name": _("Net Revenue"), "chartType": "line", "values": [flt(item["net_mrr"]) for item in data]},
            ],
        },
        "type": "axis-mixed",
        "height": 300,
        "colors": ["#2563eb", "#22c55e", "#ef4444", "#16a34a"],
    }

    summary = snapshot["summary"]
    report_summary = [
        {"label": _("Active Service Accounts"), "value": summary["active_customers"], "indicator": "Green"},
        {"label": _("New Signups"), "value": summary["new_customers"], "indicator": "Blue"},
        {"label": _("Reactivations"), "value": summary["reactivations"], "indicator": "Green"},
        {"label": _("Active Service Revenue"), "value": summary["active_mrr"], "indicator": "Blue", "datatype": "Currency"},
        {"label": _("Net New Revenue"), "value": summary["net_new_mrr"], "indicator": "Green", "datatype": "Currency"},
        {"label": _("Account Churn Rate"), "value": summary["logo_churn_rate"], "indicator": "Red", "datatype": "Percent"},
    ]

    return columns, data, None, chart, report_summary
