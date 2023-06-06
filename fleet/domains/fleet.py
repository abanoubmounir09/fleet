from __future__ import unicode_literals

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
            
            ],
            'Vehicle Log':[
                {
                "fieldname": "maintenance_request",
                "fieldtype": "Data",
                "insert_after": "service_detail",
                "label": "Maintenance Request",
                "hidden":1
                }
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
        }
    ],
    "property_setters": [

    ],
    'on_setup': 'fleet.fleet_managment.setup.install'
}
