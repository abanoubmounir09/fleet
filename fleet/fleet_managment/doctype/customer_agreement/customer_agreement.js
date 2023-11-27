// Copyright (c) 2021, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Agreement', {
	// refresh: function(frm) {

	// }
});

     frappe.ui.form.on("Customer Invoice Details", "price", function (frm, cdt, cdn) {
            var child=locals[cdt][cdn]
             var dict=frm.doc.salary_structure

			     child.amount=child.qty * child.price

                    cur_frm.refresh_fields('invoice_details');



		})

    frappe.ui.form.on("Customer Invoice Details", "qty", function (frm, cdt, cdn) {
            var child=locals[cdt][cdn]
             var dict=frm.doc.salary_structure
                if(child.price){
                     child.amount=child.qty * child.price
                  cur_frm.refresh_fields('invoice_details');
                }




		})