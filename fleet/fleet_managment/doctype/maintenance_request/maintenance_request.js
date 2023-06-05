// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Request', {
	// refresh: function(frm) {

	// }
	status:function(frm){
		if(frm.doc.status=="Agree"){
			frm.events.send_notification_fleet(frm)
		}
	},
	send_notification_fleet:function(frm){
		frappe.call({
			method:"fleet.fleet_managment.doctype.maintenance_request.maintenance_request.send_alert_vechile_driver",
			args:{
				doc:frm.doc
			},
			callback:function(frm){

			}
		})
	}
});
