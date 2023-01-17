// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request Trip', {
	refresh: function(frm) {
			if(frm.doc.docstatus ==1 &&    frm.doc.completed_percentage <100){
				frm.add_custom_button(__("Create Moving Register"), function() {
					frappe.model.open_mapped_doc({
						method: "fleet.fleet_managment.doctype.request_trip.request_trip.create_moving_register",
						frm: cur_frm
					})
					// frappe.model.open_mapped_doc({
					// 	method: "fleet.fleet_managment.doctype.",
					// 	frm: frm
					// })
				})
			}
	}

});
