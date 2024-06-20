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
                    "custom_bom_qty": each_item.get("stock_qty"),
                    "stock_uom":each_item.get("stock_uom"),
                    "custom_bom_uom":each_item.get("uom"),
                }
                )
    
                raw_materials.append(args)
                print(args, "55555555555555555555555555555555")
                
        return raw_materials

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "get_bom_details")



@frappe.whitelist()
def create_stock_entry(data,subcontracting_id,purpose):
    
    try:
        subcontracting = frappe.get_doc("Subcontracting", subcontracting_id)
        
        subcontract_detail = json.loads(data)

        for each in subcontract_detail.get("subcontracted_item"):
            
            stock_entry = frappe.new_doc("Stock Entry")
            stock_entry.purpose = purpose
            stock_entry.custom_subcontracting_id = subcontracting_id
            stock_entry.company = subcontracting.company
            stock_entry.from_bom = 1
            stock_entry.bom_no = each.get("bom")
            stock_entry.custom_fg_item = each.get("item_code")
            stock_entry.custom_total_weight = subcontracting.total_weight
            stock_entry.supplier = subcontracting.supplier
            stock_entry.fg_completed_qty = each.get("qty")
            stock_entry.custom_transaction_type_ = "Outward"
            stock_entry.stock_entry_type = purpose
            stock_entry.custom_item_value = each.get("amount")
            stock_entry.custom_expected_return_date = subcontracting.required_by


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
        
@frappe.whitelist()
def create_stock_entry_as_return(data,subcontracting_id,purpose):
    try:
        subcontracting = frappe.get_doc("Subcontracting", subcontracting_id)
        
        subcontract_detail = json.loads(data)

        for each in subcontract_detail.get("subcontracted_item"):
            
            stock_entry = frappe.new_doc("Stock Entry")
            stock_entry.purpose = purpose
            stock_entry.custom_subcontracting_id = subcontracting_id
            stock_entry.company = subcontracting.company
            stock_entry.stock_entry_type = purpose
            stock_entry.custom_transaction_type_ = "Inward"
            
            if each.get("returned_qty") == 0 and each.get("pending_qty") == 0:   
                stock_entry.append("items", {
                    "item_code":each.get("item_code"),
                    "qty":each.get("qty"),
                    "basic_rate":each.get("rate")
                })
            else:
                if each.get("pending_qty"):
                    stock_entry.append("items", {
                        "item_code":each.get("item_code"),
                        "qty":each.get("pending_qty"),
                        "basic_rate":each.get("rate")
                    })
                else:
                    continue
                
            stock_entry.to_warehouse = subcontracting.set_target_warehouse

            stock_entry.insert()
                    
        else:
            return True
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "create_stock_entry_as_return")
             


def update_check_of_po_created(doc,method=None):
    
    if doc.custom_subcontracting_id:
        subcontracting = frappe.get_doc("Subcontracting", doc.custom_subcontracting_id)
        subcontracting.po_created = 1
        subcontracting.save(ignore_permissions=True)


def update_check_of_stock_entry_created(doc,method=None):
    
    if doc.custom_subcontracting_id and doc.purpose == "Send to Subcontractor":
        subcontracting = frappe.get_doc("Subcontracting", doc.custom_subcontracting_id)
        subcontracting.stock_entry_created = 1
        for each_item_id in subcontracting.get("subcontracted_item", []):
            each_item_id.update({"reference_dc":doc.name})
        subcontracting.save(ignore_permissions=True)
        
    if doc.custom_subcontracting_id and doc.purpose == "Material Receipt":
        subcontracting_1 = frappe.get_doc("Subcontracting", doc.custom_subcontracting_id)
        
        for each_subc_child in subcontracting_1.get("subcontracted_item",[]):
            for each_item in doc.items:
                if each_item.get('item_code') == each_subc_child.get("item_code"):
                    name = each_subc_child.get("name")
                    previous_returned_qty = each_subc_child.get("returned_qty")
                    previous_pending_qty = each_subc_child.get("pending_qty")
                    
                    returned_qty = each_item.get("qty") if previous_returned_qty == 0 else previous_returned_qty + each_item.get("qty")
                    pending_qty = each_subc_child.get("qty")-returned_qty
                    
                    if pending_qty >= 0:
                        each_subc_child.update({
                            "name":name,
                            'returned_qty':returned_qty,
                            "pending_qty":pending_qty
                        })
                        
                    else:
                        frappe.throw("Error")
            
            
        subcontracting_1.material_returned = 1
            
        subcontracting_1.save(ignore_permissions=True)
