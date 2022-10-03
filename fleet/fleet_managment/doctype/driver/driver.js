// Copyright (c) 2020, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Driver', {
	validate:(frm)=>{
      if(frm.doc.national_id.length !=14){
         // console.log(frm.doc.national_id.length)
          frm.set_value("national_id","")
          frappe.throw(__("National ID mus be 14 character"))
      }
    },
	refresh:(frm)=>{
		if(frm.doc.vehicle) {
			frappe.call({
				method: "checkVehicle",
				doc: frm.doc,
				callback(r) {
					console.log(r.message)
					if (r.message == 2) {
						frm.set_value("vehicle", "")
						frm.set_value("area", "")
						frm.set_value("office", "")
						frm.set_value("account", "")
						frm.save()
					}
				}

			})
		}
	},
	professional_license:(frm)=>{
		if(frm.doc.professional_license ==1){
			frm.set_df_property("licencekind","reqd",1)
		}else {
			frm.set_df_property("licencekind","reqd",0)
		}
	},
	isemployee:function (frm){
	    if(frm.doc.isemployee==1){
	      frm.add_fetch("employeelink", "first_name", "first_name");
	      frm.add_fetch("employeelink", "middle_name", "middle_name");
	      frm.add_fetch("employeelink", "last_name", "last_name");
	      frm.add_fetch("employeelink", "employee_name", "employee_name");
	      frm.add_fetch("employeelink", "arabic_name", "arabic_name");
	      frm.add_fetch("employeelink", "company", "company");
	      frm.add_fetch("employeelink", "status", "status");
	      frm.add_fetch("employeelink", "employee_number", "employee_number");
	      frm.add_fetch("employeelink", "employment_type", "employment_type");
	      frm.add_fetch("employeelink", "national_id", "national_id");
	      frm.add_fetch("employeelink", "gender", "gender");
	      frm.add_fetch("employeelink", "date_of_birth", "date_of_birth");
	      frm.add_fetch("employeelink", "date_of_joining", "date_of_joining");
	      frm.add_fetch("employeelink", "emergency_phone_number", "emergency_phone_number");
	      frm.add_fetch("employeelink", "person_to_be_contacted", "person_to_be_contacted");
	      frm.add_fetch("employeelink", "relation", "relation");
	      frm.add_fetch("employeelink", "user_id", "user_id");
	      frm.add_fetch("employeelink", "department", "department");
	      frm.add_fetch("employeelink", "designation", "designation");
	      frm.add_fetch("employeelink", "reports_to", "reports_to");
	      frm.add_fetch("employeelink", "grade", "grade");
	      frm.add_fetch("employeelink", "branch", "branch");
	      frm.add_fetch("employeelink", "attendance_role", "attendance_role");
	      frm.add_fetch("employeelink", "leave_policy", "leave_policy");
	      frm.add_fetch("employeelink", "attendance_device_id", "attendance_device_id");
	      frm.add_fetch("employeelink", "attendance_role", "attendance_role");
	      frm.add_fetch("employeelink", "enable_overtime", "enable_overtime");
	      frm.add_fetch("employeelink", "total_working_hours_per_day", "total_working_hours_per_day");
	      frm.add_fetch("employeelink", "holiday_list", "holiday_list");
	      frm.add_fetch("employeelink", "default_shift", "default_shift");
	      frm.add_fetch("employeelink", "leave_approver", "leave_approver");
	      frm.add_fetch("employeelink", "salary_mode", "salary_mode");
	      frm.add_fetch("employeelink", "bank_name", "bank_name");
	      frm.add_fetch("employeelink", "bank_ac_no", "bank_ac_no");
	      frm.add_fetch("employeelink", "insured", "insured");
	      frm.add_fetch("employeelink", "medical_insurance_number", "medical_insurance_number");
	      frm.add_fetch("employeelink", "form_111", "form_111");
	      frm.add_fetch("employeelink", "form_date", "form_date");
	      frm.add_fetch("employeelink", "medical_examination", "medical_examination");
	      frm.add_fetch("employeelink", "medical_examination_date", "medical_examination_date");
	      frm.add_fetch("employeelink", "result_of_the_medical_examination", "result_of_the_medical_examination");
	      frm.add_fetch("employeelink", "medical_examination_notes", "medical_examination_notes");
	      frm.add_fetch("employeelink", "cell_number", "cell_number");
	      frm.add_fetch("employeelink", "prefered_contact_email", "prefered_contact_email");
	      frm.add_fetch("employeelink", "prefered_email", "prefered_email");
	      frm.add_fetch("employeelink", "company_email", "company_email");
	      frm.add_fetch("employeelink", "personal_email", "personal_email");
	      frm.add_fetch("employeelink", "unsubscribed", "unsubscribed");
	      frm.add_fetch("employeelink", "permanent_accommodation_type", "permanent_accommodation_type");
	      frm.add_fetch("employeelink", "permanent_address", "permanent_address");
	      frm.add_fetch("employeelink", "current_accommodation_type", "current_accommodation_type");
	      frm.add_fetch("employeelink", "current_address", "current_address");
	      frm.add_fetch("employeelink", "bio", "bio");
	      frm.add_fetch("employeelink", "passport_number", "passport_number");
	      frm.add_fetch("employeelink", "date_of_issue", "date_of_issue");
	      frm.add_fetch("employeelink", "valid_upto", "valid_upto");
	      frm.add_fetch("employeelink", "place_of_issue", "place_of_issue");
	      frm.add_fetch("employeelink", "marital_status", "marital_status");
	      frm.add_fetch("employeelink", "blood_group", "blood_group");
	      frm.add_fetch("employeelink", "family_background", "family_background");
	      frm.add_fetch("employeelink", "health_details", "health_details");
	      frm.add_fetch("employeelink", "resignation_letter_date", "resignation_letter_date");
	      frm.add_fetch("employeelink", "relieving_date", "relieving_date");
	      frm.add_fetch("employeelink", "reason_for_leaving", "reason_for_leaving");
	      frm.add_fetch("employeelink", "leave_encashed", "leave_encashed");
	      frm.add_fetch("employeelink", "encashment_date", "encashment_date");
	      frm.add_fetch("employeelink", "held_on", "held_on");
	      frm.add_fetch("employeelink", "reason_for_resignation", "reason_for_resignation");
	      frm.add_fetch("employeelink", "new_workplace", "new_workplace");
	      frm.add_fetch("employeelink", "feedback", "feedback");
	      frm.add_fetch("employeelink", "lft", "lft");
	      frm.add_fetch("employeelink", "rgt", "rgt");
	      frm.add_fetch("employeelink", "provider", "provider");
	      frm.add_fetch("employeelink", "document", "document");
	      frm.add_fetch("employeelink", "insurance_start_date", "insurance_start_date");
	      frm.add_fetch("employeelink", "medication_card_number", "medication_card_number");
	      frm.add_fetch("employeelink", "medication_card_recieving_date", "medication_card_recieving_date");
	      frm.add_fetch("employeelink", "company_share_ratio", "company_share_ratio");
	      frm.add_fetch("employeelink", "employee_share_ratio", "employee_share_ratio");
	      frm.add_fetch("employeelink", "has_disability", "has_disability");
	      frm.add_fetch("employeelink", "is_consultant", "is_consultant");







        }
    }
});


	  frappe.ui.form.on("Services", "period", function (frm, cdt, cdn) {
	  	console.log("hello")
            var child=locals[cdt][cdn]
            var count=0
            var period=child.period;
            var startdate=child.completationdate;
            var dlist=startdate.split('-')
		  	console.log(dlist)
		 	 var jan312009 = new Date(dlist[0], dlist[1], dlist[2]);
			var endDate  = jan312009.setMonth(jan312009.getMonth()+8);
			var d = new Date(endDate);
			var month = d.getMonth();
			var year=d.getFullYear();
			var day=d.getDate();
			var fulldate=day+"-"+month+"-"+year;
			child.expiredate=fulldate;
		 	 refresh_field("expiredate");

		})