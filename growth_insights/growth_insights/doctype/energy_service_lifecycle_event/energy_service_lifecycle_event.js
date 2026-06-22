frappe.ui.form.on("Energy Service Lifecycle Event", {
    refresh(frm) {
        frm.dashboard.add_comment(
            __("Track one service lifecycle movement per rider, fleet, or station account."),
            "blue",
            true
        );
    },

    event_type(frm) {
        frm.toggle_reqd("churn_reason", frm.doc.event_type === "Churn");
        if (frm.doc.event_type !== "Churn") {
            frm.set_value("churn_reason", "");
        }
    }
});
