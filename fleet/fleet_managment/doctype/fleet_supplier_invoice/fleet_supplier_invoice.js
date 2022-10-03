// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fleet Supplier Invoice', {
	refresh: function(frm) {
		if(!frm.doc.supplier){
			frm.set_df_property("items","hidden",1)
			refresh_field("items")

		}else{
			frm.set_df_property("items","hidden",0)
			refresh_field("items")
		}
		if (!frm.is_new() && frm.doc.docstatus <2){
			frm.add_custom_button(__('Create Purchase Invoice'), function() {
						return frm.events.make_purchase_invoice(frm);
			});
		}

	},
	make_purchase_invoice:function(frm){

		 frappe.call({
					method: "make_purchase_invoice",
					"doc": frm.doc,
					callback(r) {
						frm.refresh()
					}
				});
	}
	,
	get_supplier_vehicles:function(frm){
		
		 frappe.call({
					doc: frm.doc,
					method: "add_new_mwthod",
					callback(r) {
						frm.refresh_field('items')
						frm.events.set_totals(frm)
					}
				});
	},
	to_date:function(frm){

		if (frm.doc.from_date && frm.doc.to_date){
			frappe.call({
				doc :frm.doc,
				method:"validate_days",
				callback:function(r){
					frm.refresh()
					// refresh_field("to_date")
					// refresh_field("day_count")
				}
			})
		}
		frm.events.show_items(frm)
		

	},
	from_date:function(frm){
		frm.events.to_date(frm)
		// frm.events.show_items(frm)
	},
	day_count:function(frm){
		frappe.call({
			doc :frm.doc,
			method :"comaper_day_count_with_dates"
		})

		frm.events.show_items(frm)

	},

	supplier:function(frm){
		frm.events.set_query(frm)
		frm.events.show_items(frm)

		
	},
	set_query:function(frm){
		if (frm.doc.supplier){
			frm.set_query('vehicle','items' , function(){
				return {
					filters:{
						supplier:frm.doc.supplier
					}
				}
			})
		}
	},
	calculate_amount:function(frm){
		
		var i = 0 
		for (i = 0 ; i < frm.doc.items.length ; i ++){
			frm.doc.items[i].total_amount = frm.doc.items[i].workin_days * (frm.doc.items[i].rent_amount / 30 )
			

		}
		frm.refresh_field("items")
		frm.events.set_totals(frm)


	},
	set_totals:function(frm ,cdt ,cdn){
		frappe.call({
			doc:frm.doc,
			method :"caculate_total_deduction",
			callback:function(r){
				// refresh_field("deductions")
				// refresh_field("total")
				frm.refresh_field('items')
			}
		})
		refresh_field('items')
		frm.events.update_total_section(frm)
	},


	show_items:function(frm){
		if (frm.doc.supplier && frm.doc.to_date  && frm.doc.from_date ){
			frm.set_df_property("items","hidden",0)
			frm.refresh_field("items")

		}
	},
	validate_item(frm,cdt,cdn){
		var local = locals[cdt][cdn]
		if(local.vehicle){
					frappe.call({

						doc:frm.doc,
						method : "add_items",
						args:{
							"vh":local.vehicle
						},
						callback:function(r){
					refresh_field("items")
					if (r.message) {
						refresh_field("items")
						// frappe.throw(__("Vehicle is Dublicated"))
					}}
					})
		}




	},

	set_deduction_type(frm){

		frappe.call({
			doc :frm.doc ,
			method:"get_deduction_type",
			callback:function(r){
				refresh_field('deductions')
				frm.events.set_totals(frm)
			}
		})

	},


	update_total_section:function(frm){

		frappe.call({
			doc :frm.doc ,
			method:"fetch_totals_section" ,
			callback:function(r){
				frm.refresh_field("vehicle_qty")
				frm.refresh_field("total_amount")
				frm.refresh_field("total_deductions")
				frm.refresh_field("grand_total")
				frm.refresh_field("deductions")
			}
		})
	},
	
	
});
//Fleet Supplier Invoice Items



frappe.ui.form.on('Fleet Supplier Invoice Items', {





	items_add:function(frm ,cdt,cdn){

		if (frm.doc.supplier){
			frm.set_query('vehicle','items' , function(){
				return {
					filters:{
						supplier:frm.doc.supplier
					}
				}
			})
		}
		frappe.model.set_value(cdt,cdn,"from_date" , frm.doc.from_date)
		frappe.model.set_value(cdt,cdn,"to_date" , frm.doc.to_date)
		frm.set_df_property("deductions","hidden",0)
		frm.refresh_field("deductions")
	}
	,
	items_remove:function(frm,cdt,cdn){
		var row=locals[cdt][cdn]
		frm.events.set_totals(frm)
		frm.refresh_field("items")
		frappe.call({
			doc:frm.doc,
			method:"remove_item" ,
			callback:function(r){
				
				frm.refresh_field("deductions")
				frm.refresh_fields("holding_items")
			}
		})
		frm.refresh_field("deductions")
	},
	vehicle:function(frm ,cdt, cdn){

		var local = locals[cdt][cdn]

		frm.events.validate_item(frm,cdt,cdn)
		if (local.vehicle){
		frappe.call({
			"method" : "fleet.fleet_managment.doctype.fleet_supplier_invoice.fleet_supplier_invoice.get_viechle_driver",
			args:{
				"vh" :local.vehicle
			},
			callback:function(r){
				// console.log(r.message)
				if( r.message){
					local.driver = r.message
					frappe.model.set_value(cdt,cdn,"driver" , r.message)

				}

				frappe.model.set_value(cdt,cdn,"from_date" , frm.doc.from_date)
				frappe.model.set_value(cdt,cdn,"workin_days" , frm.doc.day_count)

			frappe.model.set_value(cdt,cdn,"to_date" , frm.doc.to_date)
			frm.events.calculate_amount(frm,cdt,cdn)
				// refresh_field("items")
			frm.events.set_totals(frm)
			frm.events.update_total_section(frm)
			}
		})
	

		}

		
	

	},
	
	

	freeze:function(frm , cdt ,cdn){
		var local = locals[cdt][cdn]
		
		var d = new frappe.ui.Dialog({
			'fields': [
                {
                	'label':'Freez Reason',
					'fieldname': 'freez_reason',
					'fieldtype': 'Small Text',
					'read_only': 0,
					'reqd':1
				},],
				 

				 primary_action: function(){
				 	d.hide()
				 	var args=d.get_values()
				 	frappe.model.set_value(cdt,cdn,"status" , "Hold")
				 	frappe.model.set_value(cdt,cdn,"freez_reason" ,args.freez_reason )

					frappe.call({
						method:"add_hold",
						doc:frm.doc,
						args:{
							"vehicle":local.vehicle ?? "",
							"driver":local.driver ?? "",
							"total_amount":local.total_amount ?? 0,
							"deduction_amount":local.total_deductions ?? 0,
							"note":local.freez_reason,
							"parent_idx":local.idx
						},callback(r){
								frm.refresh_fields("holding_items")
							}
					})

					frm.refresh_field("holding_items")
				 	frm.refresh_field("items")

				 }


			})

		d.show()



	},
	add_deduction:function(frm,cdt,cdn){
	
		var local = locals[cdt][cdn]
		var d = new frappe.ui.Dialog({

            'fields': [

             {
                	'label':'Vehicle Deduction',
					'fieldname': 'vehicle_deduction',
					'fieldtype': 'Link',
					'options' : 'Vehicle Deduction' ,
					'read_only': 0,
					'reqd':1,
					'active' :1

				},
                {
                	'label':'Vehicle',
					'fieldname': 'vehicle',
					'fieldtype': 'Link',
					'options' : 'Vehicle' ,
					'default': local.vehicle,
					'read_only': 1,
					'reqd':1
				},
				 {
                	'label':'Driver',
					'fieldname': 'driver',
					'fieldtype': 'Link',
					'options' : 'Driver' ,
					'default': local.driver,
					'read_only': 1,
					'reqd':1
				},


				{
					'label':'Amout',
					'fieldname': 'amout',
					'fieldtype': 'Float',
					'read_only': 0,
					'reqd':1
				},
				{
					'label':'Notes',
					'fieldname': 'notes',
					'fieldtype': 'Small Text',
					'read_only': 0,
					'reqd':1
				},
                
            ],
            primary_action: function(){
            	d.hide()
                var args=d.get_values()
                var child = frm.add_child("deductions")
				child.vehicle = args.vehicle
				child.driver=args.driver
				
				child.vehicle_deduction = args.vehicle_deduction
				child.amout = args.amout
				frm.refresh_field('deductions')
				frm.events.set_deduction_type(frm)
				refresh_field("items")
				frm.events.set_totals(frm)
				frm.events.update_total_section(frm)
				frm.refresh_field("items")

	},
});

 d.show(); 




	}
	,
	workin_days:function(frm,cdt,cdn){


		frm.events.calculate_amount(frm)
		frm.events.set_totals(frm)
		frm.refresh_field("items")
		
	},

})




//Vehicle Deduction Items


frappe.ui.form.on("Vehicle Deduction Items" , {
	deductions_remove:function(frm){
		frm.events.set_totals(frm)
		frm.events.update_total_section(frm)
	},
	// items_remove(frm,cdt,cdn){
	// 	console.log("hello")
	// }
});
frappe.ui.form.on("Hoding Items" , {
	unhold:function(frm,cdt,cdn){
		var row=locals[cdt][cdn]
		frappe.call({
			method:"update_status",
			doc:frm.doc,
			args:{
				'idx':row.parent_idx
			},callback(r){
				frm.refresh_fields("holding_items")
			}
		})
	},

})