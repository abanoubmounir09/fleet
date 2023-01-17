// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Moving Register', {
	refresh: function(frm) {
		frm.set_query('request_trip', function(){
			return {
				filters: {
					completed_percentage: ["<","100"],
					docstatus:1
				}
			};
		});
	}
});
