// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Tools', {
	refresh: function(frm) {
	            frm.get_field("fitems").grid.cannot_add_rows = true;

        if (!frm.is_new())
        {
            // frm.add_custom_button(__('Deliver To Customer'), function() {
			// 	frm.events.deliver_to_customer(frm)
			// }, __('Create'));
        }
	},
    is_driver:function(frm){
        if (frm.doc.is_driver){
            frm.toggle_reqd('driver',frm.doc.is_driver)
        }
    },
    get_data:function(frm){
        frappe.call({
            method:"set_data",
            doc:frm.doc,
            callback:function (r) {
                refresh_field('fitems')
            }
        })
    },
    deliver_to_customer:function(frm){
	   var selected_rows = [];
  		frm.doc.fitems.forEach((row) => {

  			if(row.__checked && row.item_code){
  				selected_rows.push(row.reference);
  			}
  		});
  		console.log(selected_rows)
        if (selected_rows.length <= 0)
            frappe.throw(__("No Item Selected"))


        frappe.call({
            method:"deliver_to_customer",
            doc:frm.doc,
            args:{
                selected : selected_rows
            },
            callback:function (r) {
                refresh_field('fitems')
                refresh_field('items')
            }
        })
    },

});
