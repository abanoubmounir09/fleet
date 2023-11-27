// Copyright (c) 2021, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Driver Pre Requisites', {
    setup: function(frm) {
		frm.set_query("pre_request", "pre_requests", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Pre Request', 'docstatus', '=', 1],
				]
			};
		});
	},
    is_old:(frm)=>{
     if(frm.doc.is_old==1){
          frm.set_df_property("driver","read_only",1);
         frm.set_df_property("national_id","read_only",1);
     }else {
         frm.set_df_property("driver","read_only",0);
         frm.set_df_property("national_id","read_only",0);
         frm.set_value("driver_link","")
         frm.set_value("driver","")
         frm.set_value("national_id","")
     }
    },
    validate:(frm)=>{
      if(frm.doc.national_id.length !=14){
         // console.log(frm.doc.national_id.length)
          frm.set_value("national_id","")
          frappe.msgprint(__("National ID mus be 14 character"))
      }
    },
    refresh:function(frm){

      if(frm.doc.__islocal && !frm.doc.pre_requests){
          frappe.call({
              method:"ge_all_driver_pre_requests",
              doc:frm.doc,
              callback(r){
                  if(r.message){
                     frm.refresh_fields("pre_requests")
                  }
              }
          })
      }
    },
    passed: function(frm) {
        if (frm.doc.passed == 1) {
            for (var i = 0; i < frm.doc.pre_requests.length; i++) {
                if (frm.doc.pre_requests[i].yes == 0 && frm.doc.pre_requests[i].no == 0) {
                    frm.set_value("passed", 0)
                    frappe.throw("You Must Take A Decision")
                }
            }
        }
        if (frm.doc.passed == 1) {
            var count = 0
            for (var i = 0; i < frm.doc.pre_requests.length; i++) {

                if (frm.doc.pre_requests[i].case_failure == 1 && frm.doc.pre_requests[i].no == 1) {
                    count++;
                }
                if (count > 0) {
                    frm.set_value("passed", 0)
                    frappe.throw("You cannot accept as there is cause failure pre-requisites ")
                    refresh_field("passed")
                }
            }
        }
    },

});

frappe.ui.form.on("Pre Request Grid", "yes", function(frm, cdt, cdn) {
    var child = locals[cdt][cdn]
    child.no = 0
    refresh_field("pre_requests")

})
frappe.ui.form.on("Pre Request Grid", "no", function(frm, cdt, cdn) {
    var child = locals[cdt][cdn]
    child.yes = 0
    refresh_field("pre_requests")

})

frappe.ui.form.on("Pre Request Grid", "pre_request", function(frm, cdt, cdn) {
    var child = locals[cdt][cdn]
    var count = 0;
    for (var i = 0; i < frm.doc.pre_requests.length; i++) {
        if (frm.doc.pre_requests[i].pre_request == child.pre_request) {
            count++;
        }
    }
    if (count > 1) {
        child.pre_request = "";
        child.pre_request_name = "";
        cur_frm.refresh_fields("pre_requests");
    }


});
frappe.ui.form.on("Pre Request Grid", "date", function(frm, cdt, cdn) {
    var child = locals[cdt][cdn]

    frappe.call({
        method:"check_inspection_period",
        doc:frm.doc,
        args:{
          "inspection": child.pre_request ?? "",
            "date":child.date ?? ""
        },
        callback(r) {
            if(r.message){
                child.end_date=r.message
                frm.refresh_fields("pre_requests")
            }
        }
    })
});

