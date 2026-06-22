frappe.ui.form.on("Customer Lifecycle Event", {
    refresh(frm) {
        frm.set_query("event_type", () => ({
            filters: {
                name: ["in", ["Signup", "Activation", "Expansion", "Churn", "Reactivation"]]
            }
        }));
    },

    event_type(frm) {
        frm.toggle_reqd("churn_reason", frm.doc.event_type === "Churn");
        if (frm.doc.event_type !== "Churn") {
            frm.set_value("churn_reason", "");
        }
    }
});
