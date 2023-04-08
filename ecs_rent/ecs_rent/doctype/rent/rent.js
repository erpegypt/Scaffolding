// Copyright (c) 2023, ECS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rent', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on("Rent", {
	refresh: function(frm, cdt, cdn) {
		if (frm.doc.docstatus == 1){
			frm.add_custom_button(__("Sales Invoice"), function() {
				var child = locals[cdt][cdn];
				frappe.route_options = {
					"rent": frm.doc.name,
					"customer": frm.doc.customer,
					"branch": frm.doc.branch,
					"cost_center": frm.doc.cost_center
				};
				frappe.new_doc("Sales Invoice");
			}, __("Create"));
		}
	}
});

frappe.ui.form.on("Rent", "validate", function(){
    for (var i = 0; i < cur_frm.doc.time_logs.length; i++){
    cur_frm.doc.time_logs[i].uom= cur_frm.doc.rent_type;
    }
    cur_frm.refresh_field('time_logs');
});

frappe.ui.form.on("Rent Detail", "rate", function(frm, doctype, name) { let row = locals[doctype][name]; row.amount = row.rate * row.qty; refresh_field("time_logs"); });



frappe.ui.form.on('Rent',"validate", function(frm, cdt, cdn) {
    $.each(frm.doc.time_logs || [], function(i, d) {

         d.amount = d.qty * d.rate;

    });
});

frappe.ui.form.on("Rent", {
validate:function(frm, cdt, cdn){
var dw = locals[cdt][cdn];
var total = 0;
var total2 = 0;

frm.doc.time_logs.forEach(function(dw) { total += dw.qty; });
frm.set_value("total_qty", total);
refresh_field("total_qty");

frm.doc.time_logs.forEach(function(dw) { total2 += dw.amount; });
frm.set_value("price_per_day_or_month", total2);
refresh_field("price_per_day_or_month");
}, });

