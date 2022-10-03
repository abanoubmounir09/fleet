// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle', {
	refresh:(frm)=>{
		frm.set_query('contract',function(){
			return{
				filters:{
					"vehicle":frm.doc.name
				}
			}
		})
	},
	on_cancel:(frm)=>{
		console.log("hello")
	},
	setup: function(frm) {
		var max = new Date().getFullYear()
		  var min = max - 20
		  var years = []

		  for (var i = max; i >= min; i--) {
			years.push(i)
		  }
			frm.set_df_property('model', 'options', years);
		       frm.set_query("vehichle_model", function() {
			return {
				filters: {
                    brand_name:frm.doc.vehichle_brand
				}
			};
		});
		 frm.set_query("office", function() {
			return {
				filters: {
                    area:frm.doc.area
				}
			};
		});

	},
	create_contract:function(frm){
		if(frm.doc.__islocal){
			frappe.throw("Save First")
		}
		var d = new frappe.ui.Dialog({

            'fields': [
                {
                	'label':'Start Date',
					'fieldname': 'start_date',
					'fieldtype': 'Date',
					// 'default': frappe.datetime.nowdate(),
					'reqd':1
				},
                 {
                 	'label':'Supplier',
					 'fieldname': 'supplier',
					 'fieldtype': 'Link',
					 'options':'Supplier',
					 'default': frm.doc.supplier,
					 'reqd':1
				 },
                  {
                  	'label':'Vehicle',
					  'fieldname': 'vehicle',
					  'fieldtype': 'Link',
					  'options':'Vehicle',
					  'default':frm.doc.name,
						'reqd':1

                  },
					{
					  'fieldname': 'asd',
					  'fieldtype': 'Column Break',


                  },
				 {
                	'label':'End Date',
					'fieldname': 'end_date',
					'fieldtype': 'Date',
					'reqd':1
				},
				 {
                 	'label':'No drivers',
					 'fieldname': 'no_driver',
					 'fieldtype': 'Int',
					 'reqd':1
				 },
				 {
                 	'label':'Vehicle Rent',
					 'fieldname': 'vehicle_rent',
					 'fieldtype': 'Currency',
					 'reqd':1,
					 'default':frm.doc.vehicle_value
				 },
				{
                 	'label':'No Hours',
					 'fieldname': 'no_hours',
					 'fieldtype': 'Int',
					 'reqd':1,
					'default':frm.doc.no_hours
				 },
            ],
            primary_action: function(){
            	d.hide()
                var args=d.get_values()
				console.log(args)
				frappe.call({
					method:"create_vehicle_contract",
					doc:frm.doc,
					args:{
						"vals":args
					},
					callback(r) {
						if(r.message){
							frm.set_value("contract",r.message)
						}
					}
				})


            }
        });
        d.show();
	},
	check_if_charachter(c){
		if(isNaN(c) && c.length==1){
			return true
		}else
		{
			return false
		}
	},
	c1:(frm)=>{

			if(!frm.events.check_if_charachter(frm.doc.c1) && frm.doc.c1!="" ){
			frm.set_value("c1","")
			frappe.throw("Please enter Valid Character")

		}

		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
					frm.refresh_field("vehichle_plate_number")
				}
			}
		})

	},
	c2:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c2) && frm.doc.c2!="") {
				frm.set_value("c2", "")
				frappe.throw("Please enter Valid Character")

			}

		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
					frm.refresh_field("vehichle_plate_number")
				}
			}
		})

	},
	c3:(frm)=>{

			 if (!frm.events.check_if_charachter(frm.doc.c3) ) {
			 	frm.set_value("c3", "")
			 	frappe.throw("Please enter Valid Character")
			 }

		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
					frm.refresh_field("vehichle_plate_number")
				}
			}
		})

	},
	c4:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c4) ) {
				frm.set_value("c4", "")
				frappe.throw("Please enter Valid Character")
			}

			frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
					frm.refresh_field("vehichle_plate_number")
				}
			}
		})

	},
	no:(frm)=> {

			if (isNaN(frm.doc.no) && frm.doc.no!="" && !frm.doc.vehicle) {
				frm.set_value("no", "")
				frappe.throw("Please enter valid no")
			}
			// if (frm.doc.c1 && frm.doc.c2 && (frm.doc.c3 || frm.doc.c4) && frm.doc.no) {
			// 	var plate_number = frm.doc.no + " " + frm.doc.c4 + frm.doc.c3 + frm.doc.c2 + frm.doc.c1
			// 	frm.set_value("vehichle_plate_number", plate_number)
			// }
		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
					frm.refresh_field("vehichle_plate_number")
				}
			}
		})

	}
});
  frappe.ui.form.on("Licence Grid", "active", function (frm, cdt, cdn) {
  	var child = locals[cdt][cdn]
  		var count =0;
  	  for (var c=0; c< frm.doc.licences.length;c++){
  	  	// console.log(frm.doc.licences[c])
  	  	 if(frm.doc.licences[c].active==1){
  	  	 	count ++

		 }
  	  	 if (count>1){

  	  	 	child.active=0;
  	  	 	refresh_field("licences");
  	  	 	frappe.throw("You Cant Select two licence");
		 }
	  }

	  frappe.call({
		  method: 'checkLicenceValidation',
		  doc: frm.doc,
		  args:{
		  	"endDtae":child.end_date
		  },
		  callback(r) {


				if(r.message=='false'){
					child.active=0;
					frappe.msgprint("This Licence is expired")
					 refresh_field("licences");

				}
		  }

	  });
  })

frappe.ui.form.on("Licence Grid", "licence", function(frm,cdt,cdn){
       var child = locals[cdt][cdn]
         var count=0
		 for (var c=0; c< frm.doc.licences.length;c++){

  	  	 if (child.licence==frm.doc.licences[c].licence ){
			count++
			 if (count>1) {
				 child.licence = "";
				 refresh_field("licences");
				 frappe.throw("Licence Already Exist");
			 }
		 }
	  }

});