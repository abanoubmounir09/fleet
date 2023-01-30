// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Return', {
	refresh: function(frm) {
		frm.set_query('moving_register', function(){
			return {
				filters: {
					moving_status:"In Progress"
					// trip_type:"Private Car"
				}
			};
		});
	}
});
