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
		frm.set_query('driver', function(){
			return {
				filters: {
					vehicle: frm.doc.vehicle,
					docstatus:1
				}
			};
		});
	},
	vehicle:(frm)=>{
		if(frm.doc.vehicle !=""){
				frappe.call({
					method:"get_vehicle_last_reading",
					doc:frm.doc,
					callback(r){
						if(r.message){
							frm.set_value("checkout_counter",r.message)
						}
					}
				})
		}
	},
	percent:(frm)=>{
		if(frm.doc.percent !=''){
		frappe.call({
			method:"check_remaining_percent",
			doc:frm.doc,
			callback(r){
				let data = r.message;
				console.log(data)
				if(data.res == "False"){
					frappe.msgprint(__("you cant exceed remaing percentage " + data.remaining))
					frm.set_value("percent",0)
					frm.refresh_field("percent")
				}
			}
		})
	}
	}
});
