# Copyright (c) 2024, Niraj and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_colunm(filters)
	return columns, data

def get_data(filters):
	se = frappe.qb.DocType("Stock Entry")
	sub = frappe.qb.DocType("Subcontracting")
	sub_ci = frappe.qb.DocType("Subcontract Item Table")

	query = (
		frappe.qb.from_(se)
		.right_join(sub)
		.on(sub.name == se.custom_subcontracting_id)
		.right_join(sub_ci)
		.on(sub_ci.parent == sub.name)
		.select(
			se.name.as_("stock_entry"),
			se.custom_subcontracting_id.as_("subcontracting_id"),
			sub.supplier,
			sub_ci.item_code,
			sub.supplier_gstn,
			se.posting_date,
			sub_ci.qty,
			sub_ci.amount,

		)
	)
	
	if filters.get("from_date"):
		query = query.where(se.posting_date >= filters.get("from_date"))


	if filters.get("to_date"):
		query =  query.where(se.posting_date <= filters.get("to_date"))

	if filters.get("subcontracting_id"):
		query =  query.where(se.custom_subcontracting_id == filters.get("subcontracting_id"))
		
	data = query.run(as_dict=True)

	return data

def get_colunm(filters):
	columns = [
		{
			"fieldname": "stock_entry",
			"fieldtype": "Link",
			"label": _("DC Number"),
			"options": "Stock Entry",
			"width": 140
		},
		{
			"fieldname": "supplier",
			"fieldtype": "Link",
			"label": _("Job Worker"),
			"options": "Supplier",
			"width": 140
		},
		{
			"fieldname": "supplier_gstn",
			"fieldtype": "Data",
			"label": _("JW GSTN"),
			"options": "Stock Entry",
			"width": 140
		},
		{
			"fieldname": "subcontracting_id",
			"fieldtype": "Data",
			"label": _("Subcontracting ID"),
			"width": 140
		},
		{
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"label": _("DC Date"),
			"width": 140
		},
		# {
		# 	"fieldname": "input_type",
		# 	"fieldtype": "Data",
		# 	"label": _("Input"),
		# 	"default": "input",
		# 	"width": 140
		# },
		{
			"fieldname": "item_code",
			"fieldtype": "Data",
			"label": _("Item Code"),
			"width": 140
		},
		{
			"fieldname": "qty",
			"fieldtype": "Float",
			"label": _("Qty"),
			"width": 140
		},
		{
			"fieldname": "amount",
			"fieldtype": "Currency",
			"label": _("AMount"),
			"width": 140
		},
		
	]
	return columns