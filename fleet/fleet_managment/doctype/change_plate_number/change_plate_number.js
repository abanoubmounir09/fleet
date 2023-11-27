// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Change Plate Number', {
	check_if_charachter(c){
		if(isNaN(c) && c.length==1){
			return true
		}else
		{
			return false
		}
	},
	vehicle:(frm) =>{
		cur_frm.refresh_field("old_plate_number")
	},
	c1:(frm)=>{

			if(!frm.events.check_if_charachter(frm.doc.c1) &&frm.doc.c1 !="") {
				frm.set_value("c1", "")
				frappe.throw("Please enter Valid Character")
			}


		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("plate_number",r.message)
				}
			}
		})

	},
	c2:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c2) && frm.doc.c2 !="") {
				frm.set_value("c2", "")
				frappe.throw("Please enter Valid Character")

			}

		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("plate_number",r.message)
				}
			}
		})

	},
	c3:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c3) && frm.doc.c3 !="" ) {
				frm.set_value("c3", "")
				frappe.throw("Please enter Valid Character")
			}

		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("plate_number",r.message)
				}
			}
		})

	},
	c4:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c4) && frm.doc.c4!="" ) {
				frm.set_value("c4", "")
				frappe.throw("Please enter Valid Character")
			}

		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("plate_number",r.message)
				}
			}
		})

	},
	no:(frm)=> {

			if (isNaN(frm.doc.no) && frm.doc.no!="" ) {
				frm.set_value("no", "")
				frappe.throw("Please enter valid no")
			}

		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("plate_number",r.message)
					// frm.events.get_inseption_forms(frm)
				}
			}
		})

	},
});
