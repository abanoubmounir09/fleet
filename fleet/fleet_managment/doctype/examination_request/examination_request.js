// Copyright (c) 2020, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Examination Request', {
	vehicle: function(frm) {
		 var driverList=[]
		frappe.call({
				method:"getDriver",
				doc:frm.doc,
				callback(r){

					driverList=r.message

				}
			})
		frm.set_query("driver", function() {



			return {
				filters: [
					["Driver","name", "in", driverList]
				]
			}
		});
	}
});
