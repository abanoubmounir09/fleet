// Copyright (c) 2021, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pre Request', {
    // refresh: function(frm) {

    // }
    // aspect_type: (frm) => {
    //     if (frm.doc.aspect_type) {
    //         frappe.call({
    //             method: "check_validation_period",
    //             doc: frm.doc,
    //             callback(r) {
    //                 if (r.message == true) {
    //                     frm.set_df_property("start_date", "hidden", 0)
    //                     frm.set_df_property("start_date", "reqd", 1)
    //                     frm.refresh_field("start_date")
    //                 }
    //             }
    //         })
    //     }
    // },
    // start_date: (frm) => {
    //     if (frm.doc.start_date) {
    //         frappe.call({
    //             method: "calc_end_date",
    //             doc:frm.doc,
    //             callback(r) {
    //                 if(r.message){
    //                     frm.refresh_field("end_date")
    //                 }
    //             }
    //         })
    //     } else {
    //         frm.set_value("end_date", "")
    //     }
    // }
});
