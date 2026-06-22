app_name = "growth_insights"
app_title = "Growth Insights"
app_publisher = "Growth Insights Team"
app_description = "User lifecycle tracking, growth reporting, and executive dashboard for Frappe."
app_email = "hello@example.com"
app_license = "MIT"

after_install = "growth_insights.install.after_install"

app_include_css = [
    "/assets/growth_insights/css/growth_insights.css"
]

doctype_js = {
    "Customer Lifecycle Event": "public/js/customer_lifecycle_event.js"
}

fixtures = [
    {
        "dt": "Workspace",
        "filters": [["name", "=", "Growth Insights"]]
    }
]
