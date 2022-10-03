// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Card', {
    // refresh:(frm)=>{
    //     if(frm.doc.__islocal && frm.doc.vehicle){
    //         frappe.call({
    //             method:"get_reading",
    //             doc:frm.doc,
    //             callback(r){
    //                 if(r.message){
    //                     // frm.refresh_field("last_tire_inspection")
    //                     cur_frm.refresh_fields("maintainance")
    //                 }
    //             }
    //         })
    //     }
    // },
    setup: (frm) => {
        this.frm.get_field("maintainance").grid.cannot_add_rows = true;
    },
    vehicle: function (frm) {
        if (frm.doc.__islocal && frm.doc.vehicle) {
            frappe.call({
                method: "get_reading",
                doc: frm.doc,
                callback(r) {
                    if (r.message) {
                        // frm.refresh_field("last_tire_inspection")
                        cur_frm.refresh_fields("maintainance")
                    }
                }
            })
        }
    },
    odometer_reading: (frm) => {
        // console.log(frm.doc.odometer_reading)
        frm.set_value("las_reading", frm.doc.odometer_reading)
        // frm.set_value("reading_date","")
        // console.log(frm.doc.las_reading)
        // frappe.call({
        //     method: "update_odo_reading",
        //     doc:frm.doc
        // })
    },
    add_tank_log: (frm) => {
        let d = new frappe.ui.Dialog({
            title: 'Enter details',
            fields: [
                {
                    label: 'Odometer Reading',
                    fieldname: 'current_reading',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Litre',
                    fieldname: 'no_litre',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Price',
                    fieldname: 'price',
                    fieldtype: 'Currency',
                    reqd: 1
                }
            ],
            primary_action_label: 'Save',
            primary_action(values) {
                d.hide();
                var vals = d.get_values()
                if (frm.doc.vehicle) {
                    frappe.call({
                        method: "add_tank_log",
                        doc: frm.doc,
                        args: {
                            "current_reading": vals.current_reading,
                            "no_litre": vals.no_litre,
                            "price": vals.price,
                            "vehicle": frm.doc.vehicle
                        },
                        callback(r) {

                        }
                    })
                }
            }
        });

        d.show();
    },
    add_tire_change: (frm) => {
        let d = new frappe.ui.Dialog({
            title: 'Enter details',
            fields: [
                {
                    label: 'Odometer Reading',
                    fieldname: 'current_reading',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    label: 'Change Date',
                    fieldname: 'change_date',
                    fieldtype: 'Date'
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Required Date',
                    fieldname: 'required_date',
                    fieldtype: 'Date',
                    reqd: 1
                },
                {
                    label: 'Status',
                    fieldname: 'status',
                    fieldtype: 'Select',
                    options: ['Done', 'Not Done']
                }
            ],
            primary_action_label: 'Save',
            primary_action(values) {
                d.hide();
                var vals = d.get_values()
                if (frm.doc.vehicle) {
                    frappe.call({
                        method: "add_tire_change",
                        doc: frm.doc,
                        args: {
                            "current_reading": vals.current_reading ?? 0,
                            "change_date": vals.change_date ?? "",
                            "required_date": vals.required_date ?? 0,
                            "status": vals.status ?? "Not Done"
                        },
                        callback(r) {

                        }
                    })
                }
            }

        });

        d.show();
    },
    add_maintainance: (frm) => {
         var driver_data=[]
        frappe.call({
            method:"get_vehicle_driver",
            doc:frm.doc,
            callback(r){
                if(r.message){
                    driver_data=r.message
                    console.log(driver_data)
                }else {
                    frappe.throw("vehicle doesnt have any driver")
                }
            }
        })
        frappe.call({
            method: "get_maintenance",
            doc: frm.doc,
            args: {
                "type": frm.doc.vehicle_type ?? ""
            },
            callback(r) {
                if (r.message) {
                    var data = r.message
                    var maintenance_list = []
                    for (let i = 0; i < data.length; i++) {
                        maintenance_list.push(data[i]["maintainance"])
                    }
                }

                // dialog

                let d = new frappe.ui.Dialog({
                    title: 'Enter details',
                    fields: [
                        {
                            label: 'Odometer Reading',
                            fieldname: 'maintenance_reading',
                            fieldtype: 'Float',
                            reqd: 1
                        },
                        {
                            label: 'Driver',
                            fieldname: 'driver',
                            fieldtype: 'Select',
                            options: driver_data,
                            reqd: 1
                        },
                        {
                            label: 'Date',
                            fieldname: 'maintenance_date',
                            fieldtype: 'Date',
                             reqd: 1
                        },
                        {
                            label: 'Description',
                            fieldname: 'description',
                            fieldtype: 'Data',
                        },
                        {
                            fieldtype: 'Column Break'
                        },
                        {
                            label: 'Choose Maintenance',
                            fieldname: 'maintenance',
                            fieldtype: 'Select',
                            options: maintenance_list,
                            reqd: 1
                        },
                        {
                            label: 'Expense',
                            fieldname: 'expense',
                            fieldtype: 'Currency',
                        },
                        {
                            label: 'Price',
                            fieldname: 'price',
                            fieldtype: 'Currency',
                        }
                    ],
                    primary_action_label: 'Add',
                    primary_action(values) {
                         d.hide();
                        var vals = d.get_values();
                        frappe.call({
                            method:"add_maintenance",
                            doc:frm.doc,
                            args:{
                                "vehicle":frm.doc.vehicle,
                                "driver":vals.driver,
                                "reading":vals.maintenance_reading,
                                "date":vals.maintenance_date,
                                "maintenance":vals.maintenance,
                                "expense":vals.expense ?? 0,
                                "price":vals.price ?? 0,
                                "description":vals.description ?? "",
                                "driver":vals.driver
                            }
                        })
                    }

                });
                d.show();
            }
        })
    },
    add_tire_inspection: (frm) => {
        let d = new frappe.ui.Dialog({
            title: 'Enter details',
            fields: [
                {
                    label: 'Odometer Reading',
                    fieldname: 'current_reading',
                    fieldtype: 'Float',
                    reqd: 1
                },
                {
                    label: 'Inspection Date',
                    fieldname: 'change_date',
                    fieldtype: 'Date'
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    label: 'Required Date',
                    fieldname: 'required_date',
                    fieldtype: 'Date'
                },
                {
                    label: 'Status',
                    fieldname: 'status',
                    fieldtype: 'Select',
                    options: ['Done', 'Not Done']
                }
            ],
            primary_action_label: 'Save',
            primary_action(values) {
                d.hide();
                var vals = d.get_values();
                // console.log(vals)
                if (frm.doc.vehicle) {
                    frappe.call({
                        method: "add_tire_inspection",
                        doc: frm.doc,
                        args: {
                            "current_reading": vals.current_reading ?? 0,
                            "change_date": vals.change_date ?? "",
                            "required_date": vals.required_date ?? 0,
                            "status": vals.status ?? "Not Done"
                        },
                        callback(r) {

                        }
                    })
                }
            }
        });

        d.show();
    },
    update_status: (frm) => {
        if (!frm.doc.status) {
            frappe.throw("Please enter status")
        }
        if (!frm.doc.notes) {
            frappe.throw("Please enter notes")
        }
        frappe.call({
            method: "update_vehicle_status",
            doc: frm.doc,
            callback(r) {
                if (r.message) {
                    // frm.save()
                }
            }
        })
    },
    update_gps_status: (frm) => {
        if (!frm.doc.date) {
            frappe.throw(__("Please Enter Date"))
        }
        if (!frm.doc.gps_status) {
            frappe.throw(__("Please Enter GPS Status"))
        }
        frappe.call({
            method: "update_gps_status",
            doc: frm.doc,
            callback(r) {
                if (r.message) {
                    frappe.msgprint(__("GPS status updated successfully"))
                }
            }
        })
    }
});
