// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Driver Cart', {
	// refresh: function(frm) {

	// }
    refresh:(frm)=>{
        if(!frm.doc.__islocal){

        }
        frm.clear_table("asset_custody")
        frm.clear_table("driver_advance")
        frm.clear_table("items_custody")
      frappe.call({
                method:"get_employee_custody",
                doc:frm.doc,
                callback(r){
                    frm.refresh_fields("asset_custody")
                    frm.refresh_fields("driver_advance")
                    frm.refresh_fields("items_custody")
                }
            })
    },
    change_status:(frm)=>{
        if(frm.doc.driver && frm.doc.status && frm.doc.note){
            frappe.call({
                method:"update_driver_status",
                doc:frm.doc,
                callback(r){
                    if(r.message){
                        frm.save()
                        frappe.msgprint(__("Status updated successfully"))
                    }
                }
            })
        }
    }
});
