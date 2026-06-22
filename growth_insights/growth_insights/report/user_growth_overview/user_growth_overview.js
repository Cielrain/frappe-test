frappe.query_reports["User Growth Overview"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.month_start(), -11)
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        }
    ],
    formatter(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (!data) {
            return value;
        }
        if (["Net Revenue", "Churn Revenue"].includes(column.label)) {
            const numeric = Number(data[column.fieldname] || 0);
            const color = numeric < 0 ? "var(--red-600)" : "var(--green-700)";
            return `<span style="color:${color};font-weight:600">${value}</span>`;
        }
        return value;
    }
};
