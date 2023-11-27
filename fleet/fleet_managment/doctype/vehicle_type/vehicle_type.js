// Copyright (c) 2020, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Type', {
    setup:function (frm) {
        frm.set_query("item" ,function(frm){
				return {
					filters: {
					    item_group: 'Services'

				}}
			})
    }
    
	// refresh: function(frm) {

	// }
});
