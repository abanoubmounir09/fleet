// Copyright (c) 2021, Dynamic Technonlgy and contributors
// For license information, please see license.txt
var Month=[]
frappe.ui.form.on('Vehicle Attendance', {
	refresh(frm){
	cur_frm.fields_dict['attendence_table'].grid.wrapper.find('.grid-remove-rows').hide();
	},
	setup: function(frm) {
		frm.get_field("attendence_table").grid.cannot_add_rows = true;
		
		var max = new Date().getFullYear()
		  var min = max - 5
		  var years = []

		  for (var i = max; i >= min; i--) {
			years.push(i)
		  }

			 Month=["January","February","March","April","May","June","July","August","September","October","November","December"]
			frm.set_df_property('date', 'options', years);
		  	frm.set_df_property('month', 'options', Month);
	},
	month:function (frm){
		frm.clear_table("attendence_table")
		var index=Month.indexOf(frm.doc.month)+1;
		 var noDays=new Date(frm.doc.date,index , 0).getDate()
		 var lisOfDays=[]
		var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
		// console.log(Month.indexOf(frm.doc.month)+1)
			for(var i=1;i<=noDays;i++){
				var n=new Date(frm.doc.date,index-1 , i).getDay()
				cur_frm.add_child("attendence_table",{day:i,day_name:days[n]})
			}
		  // frappe.meta.get_docfield("Vehicle Attendence Child", "day", cur_frm.doc.name).options =lisOfDays;


			frm.refresh_fields();
	},
	calcDays:function (frm){
		var totalAbsent=0;
		var totalPresent=0;
		for (var i=0;i<frm.doc.attendence_table.length;i++){
			if(frm.doc.attendence_table[i]["absent"]==1){
				totalAbsent +=1
			}
			if(frm.doc.attendence_table[i]["present"]==1){
				totalPresent +=1
			}
		}
		frm.set_value("total_number_of_present",totalPresent);
		frm.set_value("total_number_of_absent",totalAbsent);
		frm.refresh_fields();
	}

});
frappe.ui.form.on('Vehicle Attendence Child',{
	// day:function (frm,cdt,cdn){
	// 	var local=locals[cdt][cdn]
	// 	var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	// 	var index=Month.indexOf(frm.doc.month);
	// 	var n=new Date(frm.doc.date,index , local.day).getDay()
	// 	 var dayName = days[n];
	// 	local.day_name=dayName
	//
	//
	// 	frm.refresh_fields();
	//
	// },
	absent:function (frm,cdt,cdn){
		var local=locals[cdt][cdn]
		if(local.absent==1){
			local.present=0
		}
		frm.refresh_fields();
		frm.events.calcDays(frm)
	},
	present:function (frm,cdt,cdn){
		var local=locals[cdt][cdn]
		if(local.present==1){
			local.absent=0
		}
		frm.refresh_fields();
		frm.events.calcDays(frm)
	},

})