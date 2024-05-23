// Copyright (c) 2024, Niraj and contributors
// For license information, please see license.txt

frappe.ui.form.on("Subcontracting", {
	refresh: function(frm) {
        console.log("Form Loaded");
        
        if(frm.doc.docstatus==1 && frm.doc.stock_entry_created !== 1){

            frm.add_custom_button(__('Create Stock Entry'), function() {
                frappe.call({
                    method: 'sampat_industries.sampat_industries.doctype.subcontracting.subcontracting.create_stock_entry',
                    args: {
                        data: frm.doc,
                        subcontracting_id:frm.doc.name,
                        purpose:"Send to Subcontractor"
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__('Stock Entry successfully'));
                        }else{
                            frappe.msgprint(__('Stock Entry Fail'))
                        }
                    }
                });
            }).addClass('btn-primary');
        }
        if(frm.doc.docstatus==1 && frm.doc.po_created !== 1){

            frm.add_custom_button(__('Create Purchase Order'), function() {
                frappe.call({
                    method: 'sampat_industries.sampat_industries.doctype.subcontracting.subcontracting.creating_purchase_order',
                    args: {
                        data: frm.doc,
                        subcontracting_id:frm.doc.name
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__('Purchase Order successfully'));
                        }else{
                            frappe.msgprint(__('Purchase Order Fail'))
                        }
                    }
                });
            }).addClass('btn-primary');
        }
        if(frm.doc.po_created == 1 && frm.doc.stock_entry_created ==1){

            frm.add_custom_button(__('Create Material Return'), function() {
                frappe.call({
                    method: 'sampat_industries.sampat_industries.doctype.subcontracting.subcontracting.create_stock_entry_as_return',
                    args: {
                        data: frm.doc,
                        subcontracting_id:frm.doc.name,
                        purpose:"Material Receipt"
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__('Material Return successfully'));
                        }else{
                            frappe.msgprint(__('Material Return Fail'))
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    },

    get_materials_for_supplier :function(frm){
        fill_supplier_itmes_table(frm)
    }
    

});

function fill_supplier_itmes_table(frm) {
    if (frm.doc.subcontracted_item?.length > 0) {
        console.log("Fetching Raw Materials Data");
        frappe.call({
            method: 'sampat_industries.sampat_industries.doctype.subcontracting.subcontracting.get_bom_details',
            args: {
                data: frm.doc
            },
            callback: function (r) {
                if (r.message) {
                    update_supplier_child(frm, r.message);
                } else {
                    frm.doc.supplied_items = [];
                    frm.refresh_field('supplied_items');
                }
            }
        });
    } else {
        frm.doc.supplied_items = [];
        frm.refresh_field('supplied_items');
    }
}

function update_supplier_child(frm, data) {
    frm.clear_table('supplied_items');
    let items = data;
    for (let index = 0; index < items.length; index++) {
        let child = frm.add_child('supplied_items');
        child.main_item_code = items[index]['main_item_code'];
        child.rm_item_code = items[index]['rm_item_code'];
        child.bom_detail_no = items[index]['bom_detail_no'];
        child.reserve_warehouse = items[index]['reserve_warehouse'];
        child.required_qty = items[index]['required_qty'];
        child.stock_uom = items[index]['stock_uom'];
    }
    frm.refresh_field('supplied_items');
}

frappe.ui.form.on('Subcontract Item Table', {
	"qty": function(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        item.amount = item.rate * item.qty;
        cur_frm.refresh_fields();
    },
    "rate": function(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        item.amount = item.rate * item.qty;
        cur_frm.refresh_fields();
    }
})