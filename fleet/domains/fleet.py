from __future__ import unicode_literals
from frappe import _

data = {

    'custom_fields': {
        "Vehicle":[
            {
                "label": "Driver",
                "fieldname": "employee",
                "fieldtype": "Link",
                "insert_after": "vehicle_type",
                "options": "Driver"
            },
            {
                "label": "Make",
                "fieldname": "make",
                "fieldtype": "Data",
                "insert_after": "office",
            },
            {
                "label": "Last Odometer",
                "fieldname": "last_odometer",
                "fieldtype": "Float",
                "insert_after": "make",
                "default": "0",
            }
        ],
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
            
        "Vehicle Log":[
            {
                "label": "Posting Date",
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "insert_after": "status",
                "reqd": "1",
            },
            {
                "label": "Brand",
                "fieldname": "brand",
                "fieldtype": "Link",
                "insert_after": "model",
                "options":"Vehicle Brand",
                "fetch_from":"license_plate.vehichle_brand"
            },
            {
                "label": "Vehicle Type",
                "fieldname": "vehicle_type",
                "fieldtype": "Data",
                "insert_after": "brand",
                # "options":"User",
                "fetch_from":"license_plate.model"
            },
            {
                "label": "Area",
                "fieldname": "area",
                "fieldtype": "Link",
                "insert_after": "vehicle_type",
                "options":"Area",
                "fetch_from":"license_plate.area"
            },
            {
            "label": "Maintenance Request",
            "fieldname": "maintenance_request",
            "fieldtype": "Link",
            "options":"Maintenance Request",
            "insert_after": "employee",
            },
            {
                "label": "Office",
                "fieldname": "office",
                "fieldtype": "Link",
                "insert_after": "maintenance_request",
                "options":"Office",
                # "fetch_from":"license_plate.vehichle_brand"
            },
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
            "fieldname": "employee",
            "property": "reqd",
            "property_type": "Check",
            "value": "0"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "date",
            "property": "reqd",
            "property_type": "Check",
            "value": "0"
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
            "property": "reqd",
            "property_type": "Check",
            "value": "0"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "last_odometer",
            "property": "read_only",
            "property_type": "Check",
            "value": "0"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "odometer",
            "property": "reqd",
            "property_type": "Check",
            "value": "1"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "amended_from",
            "property": "read_only",
            "property_type": "Check",
            "value": "0"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "employee",
            "property": "hidden",
            "property_type": "Check",
            "value": "1"
        },
        {
            "doctype": "Vehicle Log",
            "doctype_or_field": "DocField",
            "fieldname": "make",
            "property": "hidden",
            "property_type": "Check",
            "value": "1"
        },
        
        
    ],
    
    'on_setup': 'fleet.fleet_managment.setup.install'
}
