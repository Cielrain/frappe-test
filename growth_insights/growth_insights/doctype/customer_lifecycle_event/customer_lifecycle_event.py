import frappe
from frappe.model.document import Document
from frappe.utils import flt


class CustomerLifecycleEvent(Document):
    def validate(self):
        if self.event_type == "Churn" and not self.churn_reason:
            frappe.throw("Churn Reason is required for churn events.")

        if self.event_type != "Churn":
            self.churn_reason = None

        self.mrr = flt(self.mrr)
        self.seats = int(self.seats or 0)
