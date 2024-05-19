# Copyright (c) 2024, Niraj and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
import sys
import traceback

class Subcontracting(Document):
    pass


@frappe.whitelist()
def get_bom_details(data):
    try:
        subcontract_detail = json.loads(data)
        
        raw_materials = []
        
        for each in subcontract_detail.get("subcontracted_item",[]):
            
            bom_doc = frappe.get_cached_doc("BOM", each.get('bom'))
            bom_item_detail = bom_doc.as_dict()
            actual_qty = each.get("qty")
            reserve_warehouse = subcontract_detail.get("set_reserve_warehouse")
            
            for each_item in bom_item_detail.get("items"):
                args = frappe._dict(
                {
                    "main_item_code": each_item.get("item_code"),
                    "rm_item_code":each_item.get("item_code"),
                    "bom_detail_no":each_item.get("parent"),
                    "reserve_warehouse": reserve_warehouse,
                    "required_qty": each_item.get("qty") * actual_qty,
                    "stock_uom":each_item.get("stock_uom"),
                }
                )
    
                raw_materials.append(args)
                
        return raw_materials

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "get_bom_details")



@frappe.whitelist()
def create_stock_entry(data,subcontracting_id):
    
    try:
        subcontracting = frappe.get_doc("Subcontracting", subcontracting_id)
        
        subcontract_detail = json.loads(data)

        for each in subcontract_detail.get("subcontracted_item"):
            
            stock_entry = frappe.new_doc("Stock Entry")
            stock_entry.purpose = "Send to Subcontractor"
            stock_entry.custom_subcontracting_id = subcontracting_id
            stock_entry.company = subcontracting.company
            stock_entry.from_bom = 1
            stock_entry.bom_no = each.get("bom")
            stock_entry.fg_completed_qty = each.get("qty")
            stock_entry.stock_entry_type = "Send to Subcontractor"


            stock_entry.from_warehouse = subcontracting.set_reserve_warehouse
            stock_entry.to_warehouse = subcontracting.supplier_warehouse

            stock_entry.set_stock_entry_type()
            stock_entry.get_items()
            stock_entry.set_serial_no_batch_for_finished_good()
            
            stock_entry.insert()
                    
        else:
            return True
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "create_stock_entry")
        
@frappe.whitelist()       
def creating_purchase_order(data,subcontracting_id):
    try:
        subcontracting = frappe.get_doc("Subcontracting", subcontracting_id)
            
        subcontract_detail = json.loads(data)
        
        items = []
        
        items.append({
            "doctype": "Purchase Order Item",
            "item_code":subcontracting.service_item,
            "qty":1
        })
        
        purchase_order = {
            "doctype": "Purchase Order",
            "supplier":subcontracting.supplier,
            "schedule_date":subcontracting.required_by,
            "custom_subcontracting_id":subcontracting.name,
            "items":items,
        }
        
        new_doc = frappe.get_doc(purchase_order)
        new_doc.insert()
        
        if new_doc.name:
            return True
        else:
            return False

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "creating_purchase_order")
        