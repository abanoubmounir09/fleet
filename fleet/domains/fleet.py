from __future__ import unicode_literals
from frappe import _

data = {

    'custom_fields': {
        'Asset': [
            {
                "fieldname": "driver",
                "fieldtype": "Link",
                "insert_after": "department",
                "label": "Driver",
                "options": "Driver"
            }
        ],
        'Employee Advance': [
            {
                "fieldname": "driver",
                "fieldtype": "Link",
                "insert_after": "employee_name",
                "label": "Driver",
                "options": "Driver"
            }
            
            ],
        'Vehicle Service': [
            {
                "fieldname": "description",
                "fieldtype": "Data",
                "insert_after": "expense_amount",
                "label": "Description",
            },
            {
                "label": "Service Item Name",
                "fieldname": "service_item_name",
                "fieldtype": "Link",
                "options":"Service Item",
                "insert_after": "service_item",
                "in_list_view":1,
                "hidden":1
            },
            {
                "label": "Service Item Name",
                "fieldname": "service_item_name_data",
                "fieldtype": "Data",
                "insert_after": "service_item_name",
                "in_list_view":1,
            }
            
            ],
        "Government Inspection":[
            {
                "label": _("To Date"),
                "fieldname": "to_date",
                "fieldtype": "Date",
                "insert_after": "inspection_date",
                "in_list_view":1,
            }
        ],
            'Vehicle Log':[
                {
                "fieldname": "maintenance_request",
                "fieldtype": "Data",
                "insert_after": "service_detail",
                "label": "Maintenance Request",
                "hidden":1
                },
            ],

            "Vehicle Log":[
                 {
                "label": "Delivery Date",
                "fieldname": "delivery_date",
                "fieldtype": "Date",
                "insert_after": "last_odometer",
                
            },
            {
                "label": "Maintenance To Date",
                "fieldname": "maintenance_to_date",
                "fieldtype": "Date",
                "insert_after": "date",
                
            },
            {
                "label": "Applicant Name",
                "fieldname": "applicant_name",
                "fieldtype": "Link",
                "insert_after": "license_plate",
                "options":"User"
                
            },
            {
                "label": "Status",
                "fieldname": "status",
                "fieldtype": "Select",
                "options":"Agree\nIn Progress\nCompleted",
                "insert_after": "column_break_7",
                "in_standard_filter": "1",
                
            },
            ]

    },
    "properties": [
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "employee",
            "property": "options",
            "property_type": "Text",
            "value": "Driver"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "employee",
            "property": "label",
            "property_type": "Text",
            "value": "Driver"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "employee_name",
            "property": "fetch_from",
            "property_type": "Text",
            "value": "employee.driver_name"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "employee_name",
            "property": "label",
            "property_type": "Text",
            "value": "Driver Name"
        },
        {
            "doctype": "Vehicle Service",
            "doctype_or_field": "DocField",
            "fieldname": "type",
            "property": "options",
            "property_type": "Text",
            "value": "Maintainance"
        },
        {
            "doctype": "Vehicle Service",
            "doctype_or_field": "DocField",
            "fieldname": "service_item",
            "property": "reqd",
            "property_type": "Check",
            "value": "0"
        },
        {
            "doctype": "Vehicle Service",
            "doctype_or_field": "DocField",
            "fieldname": "frequency",
            "property": "reqd",
            "property_type": "Check",
            "value": "0"
        },
        {
            "doctype": "Vehicle Service",
            "doctype_or_field": "DocField",
            "fieldname": "service_item",
            "property": "in_list_view",
            "property_type": "Check",
            "value": "0"
        },
         {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "status",
            "property": "in_list_view",
            "property_type": "Check",
            "value": "1"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "refuelling_details",
            "property": "hidden",
            "property_type": "Check",
            "value": "1"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "service_details",
            "property": "collapsible",
            "property_type": "Check",
            "value": "0"
        },
         {
            "doctype": "Vehicle",
            "doctype_or_field": "DocField",
            "fieldname": "area",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1"
        },
         {
            "doctype": "Vehicle",
            "doctype_or_field": "DocField",
            "fieldname": "office",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "1"
        },
         {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "refuelling_details",
            "property": "hidden",
            "property_type": "Check",
            "value": "1"
        },
         {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "service_details",
            "property": "collapsible",
            "property_type": "Check",
            "value": "0"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "last_odometer",
            "reqd": 0,
            "read_only": 0,
            "no_copy": 1,
        },
        
        
    ],
    "property_setters": [

    ],
    'on_setup': 'fleet.fleet_managment.setup.install'
}
