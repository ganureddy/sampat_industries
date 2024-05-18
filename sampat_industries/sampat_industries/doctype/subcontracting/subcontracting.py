# Copyright (c) 2024, Niraj and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class Subcontracting(Document):
    pass


@frappe.whitelist()
def get_bom_details(data):
    
    subcontract_detail = json.loads(data)
    
    raw_materials = []
    
    for each in subcontract_detail.get("subcontracted_item",[]):
        
        bom_doc = frappe.get_cached_doc("BOM", each.get('bom'))
        bom_item_detail = bom_doc.as_dict()
        actual_qty = each.get("qty")
        reserve_warehouse = subcontract_detail.get("set_reserve_warehouse")
        print(reserve_warehouse,"oooooooooooooooooooo")
        
        for each_item in bom_item_detail.get("items"):
            args = frappe._dict(
			{
				"main_item_code": each_item.get("item_code"),
                "rm_item_code":each_item.get("item_code"),
                "bom_detail_no":each_item.get("parent"),
				"reserve_warehouse": reserve_warehouse,
				"required_qty": each_item.get("qty")*actual_qty,
                "stock_uom":each_item.get("stock_uom"),
			}
            )
   
            raw_materials.append(args)
            
    return raw_materials

    