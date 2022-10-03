// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fleet Sales Order', {
	refresh: function(frm) {



	},



	calculate_discount :function(frm){
		frappe.call({
			doc :frm.doc ,
			method:"calculate_all_data" ,
			callback:function(r){
				refresh_field("items")
				refresh_field("net_total")
				refresh_field("total_qty")
				refresh_field("total_discount")
				refresh_field("grand_total")
			}

		})
	},

	create_sales_order:function (frm) {
		frm.save()
		frappe.model.open_mapped_doc({

			method: "fleet.fleet_managment.doctype.fleet_sales_order.fleet_sales_order.make_fleet_sales_order",
			frm:frm,
			args:{
				'source' : frm.doc
			},



		})	}


});


frappe.ui.form.on('Fleet Sales Order Item', {
	// refresh: function(frm) {


	// }
	items_add:function(frm ,cdt,cdn){

		frm.events.calculate_discount(frm)

	},
	items_remove:function(frm ,cdt,cdn){

		frm.events.calculate_discount(frm)

	},
	discount_rate:function(frm ,cdt,cdn){
		frm.events.calculate_discount(frm)


	},
	price:function(frm,cdt,cdn){
		frm.events.calculate_discount(frm)

	},
	qty:function(frm,cdt,cdn){
		var loacl = locals[cdt][cdn]
		frm.events.calculate_discount(frm)

	},
	item_code:function(frm,cdt,cdn){
		var loacl = locals[cdt][cdn]
		frm.events.calculate_discount(frm)

	}
});