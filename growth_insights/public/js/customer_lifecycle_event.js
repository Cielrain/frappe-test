frappe.ui.form.on("Energy Service Lifecycle Event", {
    refresh(frm) {
        frm.dashboard.add_comment(
            __("Use one record per rider, station, or fleet service event. Reports reconstruct energy-service growth from this event stream."),
            "blue",
            true
        );
    }
});
