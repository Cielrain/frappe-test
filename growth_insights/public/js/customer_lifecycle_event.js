frappe.ui.form.on("Customer Lifecycle Event", {
    refresh(frm) {
        frm.dashboard.add_comment(
            __("Use one record per lifecycle event. Reports reconstruct customer growth from this event stream."),
            "blue",
            true
        );
    }
});
