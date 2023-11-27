// Copyright (c) 2020, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('vehichle licence', {
	// refresh: function(frm) {

	// }
	refresh:(frm)=>{
		frm.set_query("vehichle_model", function () {
			return {
				filters: {
					brand_name: frm.doc.vehichle_brand
				}
			};
		});
	},
	onload: function (frm) {
		var max = new Date().getFullYear()
		var min = max - 20
		var years = []

		for (var i = max; i >= min; i--) {
			years.push(i)
		}
		frm.set_df_property('model', 'options', years);
	}
});
