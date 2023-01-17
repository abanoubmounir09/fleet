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
            }]


    },
    "properties": [

    ],
    "property_setters": [

    ],
    'on_setup': 'fleet.fleet_managment.setup.install'
}
