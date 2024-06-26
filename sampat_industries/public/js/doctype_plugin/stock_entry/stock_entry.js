frappe.ui.form.on("Stock Entry", {
  refresh: function (frm) {
    console.log("Accessing Stock Entry");
    // refresh_field("items");
  },
});

frappe.ui.form.on('Stock Entry', {
	custom_total_weight(frm) {
	    let get_item_value = cur_frm.doc.custom_item_value;
	    console.log(get_item_value,"2345678");
	    let get_item_qty = cur_frm.doc.custom_total_weight;
	    let cal_total_amount = get_item_value * get_item_qty;
	    frm.set_value("custom_total_amount_itc_04", cal_total_amount);
	},
	custom_item_value(frm){
	    let get_item_value = cur_frm.doc.custom_item_value;
	    let get_item_qty = cur_frm.doc.custom_total_weight;
	    let cal_total_amount = get_item_value * get_item_qty;
	    frm.set_value("custom_total_amount_itc_04", cal_total_amount);
	}
});
// frappe.ui.form.on("Stock Entry Detail", {
//   refresh: function (frm, cdt, cdn) {
//     frappe.model.set_value(cdt, cdn, "allow_zero_valuation_rate", "1");
//     console.log("entered");
//     refresh_field("items");
//   },
// });
