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
			sub_ci.returned_qty,
			sub_ci.pending_qty,
			sub_ci.amount,
			se.custom_transaction_type_,
			sub.nature_of_process,
			sub_ci.uom,
			se.custom_fg_item,
			se.custom_total_weight,
			se.custom_item_value,
			se.custom_uom,
			se.custom_total_amount_itc_04
		)
		.where(se.docstatus == 1)
	)
	
	if filters.get("from_date"):
		query = query.where(se.posting_date >= filters.get("from_date"))


	if filters.get("to_date"):
		query =  query.where(se.posting_date <= filters.get("to_date"))

	if filters.get("subcontracting_id"):
		query =  query.where(se.custom_subcontracting_id == filters.get("subcontracting_id"))
	
	if filters.get("custom_transaction_type_"):
		query = query.where(se.custom_transaction_type_ == filters.get("custom_transaction_type_"))
		
	data = query.run(as_dict=True)

	return data

def get_colunm(filters):
	columns = [
		{
			"fieldname": "stock_entry",
			"fieldtype": "Link",
			"label": _("DC Challan No."),
			"options": "Stock Entry",
			"width": 160
		},
		{
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"label": _("DC Date"),
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

		# {
		# 	"fieldname": "input_type",
		# 	"fieldtype": "Data",
		# 	"label": _("Input"),
		# 	"default": "input",
		# 	"width": 140
		# },
		{
			"fieldname": "custom_fg_item",
			"fieldtype": "Data",
			"label": _("Item Code"),
			"width": 140
		},
		{
			"fieldname": "custom_uom",
			"fieldtype": "Data",
			"label": _("UOM"),
			"width": 140
		},
		{
			"fieldname": "custom_total_weight",
			"fieldtype": "Float",
			"label": _("Qty"),
			"width": 140
		},
		{
			"fieldname": "returned_qty",
			"fieldtype": "Float",
			"label": _("Returned Qty"),
			"width": 140
		},
				{
			"fieldname": "pending_qty",
			"fieldtype": "Float",
			"label": _("Balanced Qty"),
			"width": 140
		},
		{
			"fieldname": "custom_item_value",
			"fieldtype": "Currency",
			"label": _("Rate"),
			"width": 120
		},
		{
			"fieldname": "custom_total_amount_itc_04",
			"fieldtype": "Currency",
			"label": _("Amount"),
			"width": 140
		},
		{
			"fieldname": "nature_of_process",
			"fieldtype": "Data",
			"label": _("Nature of Process"),
			"width": 140
		},
		{
			"fieldname": "custom_transaction_type_",
			"fieldtype": "Data",
			"label": _("Transaction Type"),
			"width": 140
		},
	]
	return columns