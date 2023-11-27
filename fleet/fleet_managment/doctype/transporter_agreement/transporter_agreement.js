// Copyright (c) 2020, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transporter Agreement', {

    setup:function (frm){
        frm.set_query("supplier", ()=>{
			return {
				"filters": {
					"is_transporter": 1
				}
			};
		});

        frm.set_query("vehicle", "invoice_details", (doc) => {
			return {
				filters: {
					is_passed:1
				}
			};

		})
        frm.set_query("driver", "invoice_details", (doc) => {
			return {
				filters: {
					is_passed:1
				}
			};

		})

    }

});

	    //  frappe.ui.form.on("Invoice Details", "driver", function (frm, cdt, cdn) {
        //     var child=locals[cdt][cdn]
        //      var dict=frm.doc.salary_structure
		// 	 if(child.driver && child.vehicle){
		// 	     child.item=child.driver +" "+ child.vehicle
        //           refresh_field("driver");
        //      }
        //
        //
		// })


     frappe.ui.form.on("Invoice Details", "price", function (frm, cdt, cdn) {
            var child=locals[cdt][cdn]
             var dict=frm.doc.salary_structure

			     child.amount=child.qty * child.price

                    cur_frm.refresh_fields('invoice_details');



		})

    frappe.ui.form.on("Invoice Details", "qty", function (frm, cdt, cdn) {
            var child=locals[cdt][cdn]
             var dict=frm.doc.salary_structure
                if(child.price){
                     child.amount=child.qty * child.price
                  cur_frm.refresh_fields('invoice_details');
                }




		})

