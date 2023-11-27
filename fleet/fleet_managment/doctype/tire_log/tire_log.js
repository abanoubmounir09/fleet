// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tire Log', {
	refresh:(frm)=>{
        if(frm.doc.__islocal){
            frm.add_fetch("vehicle","km_reading","current_reading")
        }
    },
    add_change:(frm)=>{
        frappe.call({
            method:"add_change",
            doc:frm.doc,
            callback(r){
                if(r.message){
                    frm.set_value("add_ch_r_km","")
                    frm.refresh_fields("tire_change")
                }
            }
        })
    },
     add_inspection:(frm)=>{
        frappe.call({
            method:"add_inspection",
            doc:frm.doc,
            callback(r) {
                if(r.message){
                     frm.set_value("add_ins_r_km","")
                     frm.refresh_fields("tire_inspection_log")
                }

            }
        })
    },
});
frappe.ui.form.on('Tier Change Child', {
    status:(frm,cdt,cdn)=> {
        var row = locals[cdt][cdn]
          if(row.status=="Done"){
        frappe.call({
            method: "getDate",
            doc: frm.doc,
            callback(r) {
                if (r.message) {
                    row.date = r.message
                }
            }
        })
    }
    }
});
frappe.ui.form.on('Tire Inspection Child', {
    status:(frm,cdt,cdn)=>{
        var row=locals[cdt][cdn]
        if(row.status=="Done"){
            frappe.call({
            method:"getDate",
            doc:frm.doc,
            callback(r){
                if(r.message){
                    row.date=r.message
                }
            }
        })
        }
    }
})