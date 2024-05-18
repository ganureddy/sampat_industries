// Copyright (c) 2024, Niraj and contributors
// For license information, please see license.txt

frappe.ui.form.on("Subcontracting", {
	refresh: function(frm) {
        console.log("Form Loaded");
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