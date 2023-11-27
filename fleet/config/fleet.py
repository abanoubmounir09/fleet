
def get_data():
    return [

        {
            "label": _("Fleet Management"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Fleet Supplier Invoice"
                },

                {
                    "type": "doctype",
                    "name": "Fleet Sales Order"
                },
                {
                    "type": "doctype",
                    "name": "Fleet Notification Settings"
                },
            ]
        },
        {
            "label": _("Fleet Operation"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Vehicle Inspection Form"
                },
                {
                    "type": "doctype",
                    "name": "Driver Pre Requisites"
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Card",
                    "label": _("Vehicle Cart")
                },
                {
                    "type": "doctype",
                    "name": "Driver Cart",
                    "label": _("Driver Cart")
                },
                {
                    "type": "doctype",
                    "name": "Tank log"
                },

                {
                    "type": "doctype",
                    "name": "Vehicle Log"
                },

                {
                    "type": "doctype",
                    "name": "Tire Log",
                    "label": _("Tire Log")
                },
                {
                    "type": "doctype",
                    "name": "GPS Logs",
                    "label": _("GPS Log")
                },
                {
                    "type": "doctype",
                    "name": "Driver Violation"
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Contract"
                },
                {
                    "type": "doctype",
                    "name": "Change Plate Number",
                    "label": _("Change Plate Number")
                },


            ]
        },
        {
            "label": _("Driver"),
            "items": [



                {
                    "type": "doctype",
                    "name": "Driver"
                },

                {
                    "type": "doctype",
                    "name": "Pre Requisites Type"
                },
                {
                    "type": "doctype",
                    "name": "Driver Course",
                    "label": _("Driver Course")
                },
                {
                    "label": _("Pre Requisites"),
                    "type": "doctype",
                    "name": "Pre Request"
                },
                {
                    "label": _("Driver Course"),
                    "type": "doctype",
                    "name": "Driver Course"
                },




            ]
        },
        {
            "label": _("Vehichle"),
            "items": [

                {
                    "type": "doctype",
                    "name": "Vehicle"
                },

                {
                    "label": _("Vehichle Licence"),
                    "type": "doctype",
                    "name": "vehichle licence"
                },
                {
                    "type": "doctype",
                    "name": "Aspect Type"
                },
                {
                    "type": "doctype",
                    "name": "Inspection Aspects"
                },
                {
                    "type": "doctype",
                    "name": "Vehichle Model"
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Brand"
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Type"
                },

                {
                    "type": "doctype",
                    "name": "Maintainance",
                    "label": _("Maintainance")
                },
                {
                    "type": "doctype",
                    "name": "Color"
                },
                {
                    "type": "doctype",
                    "name": "Area",
                    "label": _("Area")
                },
                {
                    "type": "doctype",
                    "name": "Uplaod Odometer Reading",
                    "label": _("Uplaod Odometer Reading")
                },
                {
                    "type": "doctype",
                    "name": "Office",
                    "label": _("Office")
                },

            ]
        },
        {
            "label": _("Reports"),
            "items": [
                # {
                #     "type": "report",
                #     "is_query_report": True,
                #     "name": "Vehicle Expenses",
                #     "doctype": "Vehicle"
                # },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Drivers Financial Custodies",
                    "label":_("Drivers Financial Custodies"),
                    "doctype": "Employee Advance"

                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Car Summary",
                    "label": _("Car Summary"),
                    "doctype": "Vehicle"

                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Driver Summary",
                    "label": _("Driver Summary")

                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "D FUP",
                    "label": _("D FUP"),
                    "doctype": "Driver Cart"

                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "C FUP",
                    "label": _("C FUP"),
                    "doctype": "Driver Cart"

                },
            ]
        },

    ]

