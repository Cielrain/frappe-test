app_name = "growth_insights"
app_title = "Zhige Energy Ops"
app_publisher = "Growth Insights Team"
app_description = "Battery swapping service lifecycle tracking, operations reporting, and executive dashboard for Frappe."
app_email = "hello@example.com"
app_license = "MIT"

after_install = "growth_insights.install.after_install"
after_migrate = "growth_insights.install.ensure_navigation"

app_home = "/desk/growth-insights"
home_page = "desk/growth-insights"

app_include_css = [
    "/assets/growth_insights/css/growth_insights.css"
]

doctype_js = {
    "Energy Service Lifecycle Event": "public/js/customer_lifecycle_event.js"
}

fixtures = [
    {
        "dt": "Workspace",
        "filters": [["name", "=", "Growth Insights"]]
    }
]
