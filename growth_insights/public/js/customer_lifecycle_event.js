frappe.ui.form.on("Energy Service Lifecycle Event", {
    refresh(frm) {
        frm.dashboard.add_comment(
            __("Use one record per rider, station, or fleet service event. Reports reconstruct energy-service growth from this event stream."),
            "blue",
            true
        );

        frm.add_custom_button(__("Growth Report"), () => {
            frappe.set_route("query-report", "User Growth Overview");
        }, __("Open"));

        frm.add_custom_button(__("Operations Dashboard"), () => {
            frappe.set_route("user-growth-dashboard");
        }, __("Open"));
    },

    event_type(frm) {
        frm.toggle_reqd("churn_reason", frm.doc.event_type === "Churn");
        if (frm.doc.event_type !== "Churn") {
            frm.set_value("churn_reason", "");
        }
    }
});
