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
        {"label": _("New Customers"), "fieldname": "new_customers", "fieldtype": "Int", "width": 130},
        {"label": _("Churned Customers"), "fieldname": "churned_customers", "fieldtype": "Int", "width": 150},
        {"label": _("Expansion Events"), "fieldname": "expansions", "fieldtype": "Int", "width": 140},
        {"label": _("New MRR"), "fieldname": "new_mrr", "fieldtype": "Currency", "width": 120},
        {"label": _("Expansion MRR"), "fieldname": "expansion_mrr", "fieldtype": "Currency", "width": 140},
        {"label": _("Churn MRR"), "fieldname": "churn_mrr", "fieldtype": "Currency", "width": 120},
        {"label": _("Net MRR"), "fieldname": "net_mrr", "fieldtype": "Currency", "width": 120},
        {"label": _("Net Logo Growth"), "fieldname": "net_logo_growth", "fieldtype": "Int", "width": 140},
    ]

    data = []
    for row in snapshot["monthly"]:
        item = dict(row)
        item["net_logo_growth"] = item["new_customers"] - item["churned_customers"]
        data.append(item)

    chart = {
        "data": {
            "labels": [item["month"] for item in data],
            "datasets": [
                {"name": _("New Customers"), "values": [item["new_customers"] for item in data]},
                {"name": _("Churned Customers"), "values": [item["churned_customers"] for item in data]},
                {"name": _("Net MRR"), "values": [flt(item["net_mrr"]) for item in data]},
            ],
        },
        "type": "axis-mixed",
        "height": 300,
        "colors": ["#2563eb", "#ef4444", "#16a34a"],
    }

    summary = snapshot["summary"]
    report_summary = [
        {"label": _("Active Customers"), "value": summary["active_customers"], "indicator": "Green"},
        {"label": _("Active MRR"), "value": summary["active_mrr"], "indicator": "Blue", "datatype": "Currency"},
        {"label": _("Net New MRR"), "value": summary["net_new_mrr"], "indicator": "Green", "datatype": "Currency"},
        {"label": _("Logo Churn Rate"), "value": summary["logo_churn_rate"], "indicator": "Red", "datatype": "Percent"},
    ]

    return columns, data, None, chart, report_summary
