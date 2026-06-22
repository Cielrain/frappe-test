import frappe

from growth_insights.growth_insights.analytics import build_growth_snapshot


@frappe.whitelist()
def get_dashboard_data():
    return build_growth_snapshot()
