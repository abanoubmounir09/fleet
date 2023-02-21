// Copyright (c) 2020, Dynamic Technonlgy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Inspection Form', {
	setup:(frm)=>{

		frm.refresh_field("vehichle_model_year")
		 frm.set_query("office", function() {
			return {
				filters: {
                    area:frm.doc.area
				}
			};
		});

	},
	vehicle_type:(frm)=>{
		frm.refresh_field("vehichle_model_year")
	},
    check_if_charachter(c){
		if(c.length >0)
		{
			if(isNaN(c) && c.length==1){
				return true
			}else
			{
				return false
			}
		}
	},
	is_old:(frm)=>{
    	if(frm.doc.is_old==0){
    		frm.set_value("vehicle","")
			frm.set_value("vehichle_brand","")
			 frm.set_df_property("vehichle_brand","read_only",0)
			frm.set_df_property("c1","read_only",0)
			frm.set_value("c1","")
			frm.refresh_field('c1')
			frm.set_df_property("c2","read_only",0)
			frm.set_value("c2","")
			frm.refresh_field('c1')
			frm.set_df_property("c3","read_only",0)
			frm.set_value("c3","")
			frm.set_df_property("c4","read_only",0)
			frm.set_value("c4","")
			frm.set_df_property("no","read_only",0)
			frm.set_value("no","")
			frm.set_value("vehichle_plate_number","")
			// frm.set_df_property("mileage_reading","read_only",0)
			// frm.set_value("mileage_reading","")
			frm.set_df_property("vehichle_model_year","read_only",0)
			frm.set_value("vehichle_model_year","")
		}else{

			frm.set_df_property("vehichle_brand","read_only",1)
			frm.set_df_property("c1","read_only",1)
			frm.set_df_property("c2","read_only",1)
			frm.set_df_property("c3","read_only",1)
			frm.set_df_property("c4","read_only",1)
			frm.set_df_property("no","read_only",1)
			// frm.set_df_property("mileage_reading","read_only",1)
			frm.set_df_property("vehichle_model_year","read_only",1)

		}
	},
	c1:(frm)=>{

			if(!frm.events.check_if_charachter(frm.doc.c1) &&frm.doc.c1 !="" && !frm.doc.vehicle) {
				frm.set_value("c1", "")
				frappe.throw("Please enter Valid Character")
			}

		// if(frm.doc.c1 && frm.doc.c2 &&  frm.doc.no){
		// 	var plate_number=frm.doc.no + " "+ frm.doc.c4  + " " + frm.doc.c3 + " " + frm.doc.c2 + " " +frm.doc.c1
		// 	frm.set_value("vehichle_plate_number",plate_number)
		// 	frm.refresh_field("vehichle_plate_number")
		// }
		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
				}
			}
		})

	},
	c2:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c2) && frm.doc.c2 !="" && !frm.doc.vehicle) {
				frm.set_value("c2", "")
				frappe.throw("Please enter Valid Character")

			}
		// //	if (frm.doc.c1 && frm.doc.c2 &&  frm.doc.no) {
		// 		var plate_number = frm.doc.no + " " + frm.doc.c4 + " "+ frm.doc.c3 + " "+ frm.doc.c2+ " " + frm.doc.c1
		// 		frm.set_value("vehichle_plate_number", plate_number)
		// 		frm.refresh_field("vehichle_plate_number")
		// //	}
		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
				}
			}
		})

	},
	c3:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c3) && frm.doc.c3 !="" && !frm.doc.vehicle) {
				frm.set_value("c3", "")
				frappe.throw("Please enter Valid Character")
			}
		// //	if (frm.doc.c1 && frm.doc.c2 && frm.doc.no) {
		//
		// 		var plate_number = frm.doc.no + " " + frm.doc.c4 + " "+ frm.doc.c3+ " " + frm.doc.c2 + " "+ frm.doc.c1
		// 		frm.set_value("vehichle_plate_number", plate_number)
		// 		frm.refresh_field("vehichle_plate_number")
		// //	}
		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
				}
			}
		})

	},
	c4:(frm)=>{

			if (!frm.events.check_if_charachter(frm.doc.c4) && frm.doc.c4!="" && !frm.doc.vehicle) {
				frm.set_value("c4", "")
				frappe.throw("Please enter Valid Character")
			}
		// //	if (frm.doc.c1 && frm.doc.c2 && frm.doc.no) {
		//
		// 		var plate_number = frm.doc.no + " " + frm.doc.c4 + " "+ frm.doc.c3 + " "+ frm.doc.c2+ " " + frm.doc.c1
		// 		frm.set_value("vehichle_plate_number", plate_number)
		// 		frm.refresh_field("vehichle_plate_number")
		// //	}
		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
				}
			}
		})

	},
	no:(frm)=> {

			if (isNaN(frm.doc.no) && frm.doc.no!="" && !frm.doc.vehicle) {
				frm.set_value("no", "")
				frappe.throw("Please enter valid no")
			}
		// 	//if (frm.doc.c1 && frm.doc.c2 && (frm.doc.c3 || frm.doc.c4) && frm.doc.no) {
		//
		// 	var plate_number = frm.doc.no + " " + frm.doc.c4 + " "+ frm.doc.c3 + " "+ frm.doc.c2 + " "+ frm.doc.c1
		// 	frm.set_value("vehichle_plate_number", " ")
		// 	frm.set_value("vehichle_plate_number", plate_number)
		// 	frm.refresh_field("vehichle_plate_number")
		// //	}
		frappe.call({
			method:"concat_plate_number",
			doc:frm.doc,
			callback(r){
				if(r.message){
					frm.set_value("vehichle_plate_number",r.message)
					// frm.events.get_inseption_forms(frm)
				}
			}
		})

	},
    refresh:function(frm){
		frm.set_query("office", function() {
			return {
				filters: {
                    area:frm.doc.area
				}
			};
		});
		
        frappe.call({
            method:"getDocStatus",
            doc:frm.doc,
            callback(r){
             frm.set_df_property("vehichle_number", "reqd", r.message);
             frm.set_df_property("date", "reqd", r.message);
             frm.set_df_property("vehichle_plate_number", "reqd", r.message);
              // frm.set_df_property("inspection_team", "reqd", r.message);
                frm.set_df_property("passed", "reqd", r.message);
            }
        });
//
//        if(frm.doc.inspection_aspect.length >0){
//            frm.set_df_property("vehichle_number", "reqd", 1);
//             frm.set_df_property("date", "reqd", 1);
//             frm.set_df_property("vehichle_plate_number", "reqd", 1);
//
//
//        }
			frm.refresh_field("vehichle_model_year")
    },


    add_s:function(frm){
    	
    	frm.clear_table("inspection_aspect")
    	refresh_field("inspection_aspect")
    	  frappe.call({
              method:"ge_all_car_inspections",
              doc:frm.doc,
              callback :function(r){
             
                 	// frm.clear_table("inspection_aspect")
                  	// frappe.model.set_value(cdt,cdn,"inspection_aspects",r.message[0])
                  	// frappe.model.set_value(cdt,cdn,"aspect_name","r.message[1]")
                    frm.refresh_field("inspection_aspect")
                    // frm.set_df_property("add_s", "read_only", 1);
                   refresh_field("add_s")
                 
              }
          })
    	// frm.events.get_inseption_forms(frm)
     //    refresh_field("inspection_aspect")

    },

	setup: function(frm ) {
		// frm.events.get_inseption_forms(frm )
		var max = new Date().getFullYear()
		  var min = max - 20
		  var years = []

		  for (var i = max; i >= min; i--) {
			years.push(i)
		  }
			frm.set_df_property('vehichle_model_year', 'options', years);
		  	frm.refresh_field("vehichle_model_year")
	},
	passed:function (frm){
		if(frm.doc.passed==1) {
		for (var i = 0; i < frm.doc.inspection_aspect.length; i++) {
			if (frm.doc.inspection_aspect[i].yes == 0 &&frm.doc.inspection_aspect[i].no == 0) {
			    frm.set_value("passed", 0)
                frappe.throw("You Must Take A Decision")
			}
		}
		}
			if(frm.doc.passed==1) {
				var count = 0
				for (var i = 0; i < frm.doc.inspection_aspect.length; i++) {

					if (frm.doc.inspection_aspect[i].case_failure == 1 &&frm.doc.inspection_aspect[i].no==1) {
						count++;
					}
					if (count > 0) {
						frm.set_value("passed", 0)
						frappe.throw("You cannot accept as there is cause failure aspects")
						refresh_field("passed")
					}
				}
			}
	},
	add_multiple:function (frm){


   			 var d = new frappe.ui.Dialog({
					    title: 'Enter details',
					    fields: [

							 {
					            "label": 'Aspect Type',
					            "fieldname": 'aspect_type',
					            "fieldtype": 'Link',
								 "options":"Aspect Type",
								 "reqd":1,
								    onchange(){
                                   	    frappe.call({
					            		method:"GetAllType",
					            		doc:frm.doc,
					            		args:{
					            			"type":d.get_values().aspect_type
					            		}
					            	}).then(r=>{
					            	//console.log(r.message)
					            	  var txt="<input type='checkbox' class='all' value='All'><label>Add All</label><form><table>";

					            	  for(var i=0;i<r.message.length;i++){
					            	    txt+="<tr><td><input name='items[]' type='checkbox' class='c' value='"+r.message[i].name+"'>"+r.message[i].aspect_name+"</td></tr>";
					            	  }
					            	  txt +="</table>"
					            	  //txt +="<br><input type='submit' id='submit'  name='submit'  value='submit'></input>"
                                       // d.set_df_property("ht","options",txt)
                                        txt +="</form>"

                                        $(d.fields_dict['ht'].wrapper).html(txt);
                                        }
					            	)
                                   }

					            },

					        {

					            "fieldname": 'ht',
					            "fieldtype": 'HTML',
                                 onchange(){
                                 
                                 },


					        },



					    ],
					    primary_action_label: 'Get All',
					    primary_action(values) {console.log("submit")
                            var asd=document.getElementsByClassName("c");//[0].checked;
                            //var args = d.get_values();
                            var all=document.getElementsByClassName("all")[0];
                            if(all.checked==true){
                            	
                                for(var i=0;i<asd.length;i++){
                                    var count=0;
                                     // console.log("from dialog"+asd[i].value)
                                    for(var j=0;j<frm.doc.inspection_aspect.length;j++){
                                       // console.log("from table"+frm.doc.inspection_aspect[j].inspection_aspects)

                                        if(frm.doc.inspection_aspect[j].inspection_aspects==asd[i].value){
                                            count++;
                                        }


                                    }

                                 if(count<1){
                                         var childTable = cur_frm.add_child("inspection_aspect");
								             childTable.inspection_aspects=asd[i].value;
                                       }

                            }
                            }else{
                              if(frm.doc.inspection_aspect.length >0){
                              		c
                            for(var i=0;i<asd.length;i++){
                                 var count=0;
                                    for(var j=0;j<frm.doc.inspection_aspect.length;j++){
                                    	console.log("for loop")
                                        if(frm.doc.inspection_aspect[j].inspection_aspects==asd[i].value){
                                        	console.log("from count if")
                                                        count ++
                                        }
                                    if(asd[i].checked==true && count==0){
                                    	console.log("from secon for")
                                            var childTable = cur_frm.add_child("inspection_aspect");
                                        childTable.inspection_aspects=asd[i].value;
								}

                                    }

                            }
                              }
                              else{
                              			for(var i=0;i<asd.length;i++){
                                  if(asd[i].checked==true){
                             var childTable = cur_frm.add_child("inspection_aspect");
							 childTable.inspection_aspects=asd[i].value;
                                    }   

                            }
                              }
                            }
                            
                            cur_frm.refresh_fields("inspection_aspect");
                            frm.save();

                            //console.log(asd)
//                            frappe.call({
//								method:"GetAllType",
//								doc:frm.doc,
//								args:{
//									"type":values.aspect_type
//								},
//								callback(r){
//									for(var i=0;i<r.message.length;i++){
//										var childTable = cur_frm.add_child("inspection_aspect");
//									childTable.inspection_aspects=r.message[i].aspect_name;
//									}
//
//									cur_frm.refresh_fields("inspection_aspect");
//									frm.save();
//								}
//					        })
                           d.hide();


                           	}
					});

					d.show();

	}


});


//Inspection Grid

