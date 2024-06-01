// Copyright (c) 2024, Niraj and contributors
// For license information, please see license.txt

frappe.query_reports["ITC-04"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1,
			width: "60px",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
			width: "60px",
		},
		{
			fieldname: "subcontracting_id",
			label: __("subcontracting id"),
			fieldtype: "Link",
			options: "Subcontracting",
			width: "60px",
		},
		{
			fieldname: "custom_transaction_type_",
			label: __("Transaction Type"),
			fieldtype: "Select",
			options: "\nInward\nOutward",
			width: "60px",
		},
		
	]
};
