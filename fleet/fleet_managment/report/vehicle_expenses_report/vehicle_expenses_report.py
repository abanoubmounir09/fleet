# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    return VehicleExpenses(filters).run()


class VehicleExpenses(object):
    def __init__(self, filters=None):
        self.filters = frappe._dict(filters or {})
        self.from_date = self.filters.get('from_date')
        self.to_date = self.filters.get('to_date')
        self.conditions = self.get_conditions()
        self.maintainances = self.get_maintainances()
        self.columns = self.get_columns()
        self.data = self.get_data()

    def get_maintainances(self):
        maintainances = frappe.db.sql_list(
            " select name from `tabMaintainance` ")
        return maintainances

    def run(self):
        # self.get_columns()
        # self.get_data()
        return self.columns, self.data

    def get_columns(self):
        self.columns = [
            {
                "fieldname": "vehicle_name",
                "fieldtype": "Link",
                "label": _("Vehicle"),
                "options": "Vehicle",
                "width": 150
            },
            {
                "fieldname": "vehicle_type",
                "fieldtype": "Link",
                "label": _("Vehicle Type"),
                "options": "Vehicle Type",
                "width": 120
            },
            {
                "fieldname": "vehicle_brand",
                "fieldtype": "Link",
                "options": "Vehicle Brand",
                "label": _("Vehicle Brand"),
                "width": 120

            },
            {
                "fieldname": "first_odometer",
                "fieldtype": "Float",
                "label": _("First Odometer"),
                "width": 120
            },
            {
                "fieldname": "last_odometer",
                "fieldtype": "Float",
                "label": _("Last Odometer"),
                "width": 120
            },
            {
                "fieldname": "diff_odometer",
                "fieldtype": "Float",
                "label": _("Odometer"),
                "width": 120
            },
            {
                "fieldname": "driver",
                "fieldtype": "Link",
                "label": _("Driver"),
                "options": "Driver",
                "width": 120
            },
            {
                "fieldname": "line",
                "fieldtype": "Data",
                "label": _("Line"),
                "width": 120
            },
            {
                "fieldname": "total_liters",
                "fieldtype": "Float",
                "label": _("Total Liters"),
                "width": 120
            },
            {
                "fieldname": "litres_cost",
                "fieldtype": "Float",
                "label": _("Liters Cost"),
                "width": 120
            },
        ]

        for i in self.maintainances:
            self.columns.append(
                {
                    "fieldname": i,
                    "fieldtype": "Float",
                    "label": _(i),
                    "width": 120
                }
            )

        self.columns.extend([

            {
                "fieldname": "total_cost",
                "fieldtype": "Float",
                "label": _("Total Cost"),
                "width": 120

            },
        ])
        return self.columns

    def get_data(self):
        self.data = []

        columns = ""

        for i in self.maintainances :
            columns += f"""
                , IFNULL((
                 select SUM(IFNULL(service.expense_amount  , 0)) from `tabVehicle Service` service INNER JOIN `tabVehicle Log` log on log.name = service.parent 
                 where log.license_plate = vehicle.name and log.docstatus = 1 and service.`type` ='{i}' and date(log.`date`) BETWEEN date ('{self.from_date}') AND date ('{self.to_date}')
                ),0) as `{i}`
            """
        if not self.maintainances :
            self.maintainances = [0]
        maintainances_str = ",".join([f"'{x}'" for x in self.maintainances ])

        columns += f"""
            , IFNULL((
                select SUM(IFNULL(service.expense_amount  , 0)) from `tabVehicle Service` service INNER JOIN `tabVehicle Log` log on log.name = service.parent 
                where log.license_plate = vehicle.name and log.docstatus = 1 and service.`type` in ({maintainances_str}) and date(log.`date`) BETWEEN date ('{self.from_date}') AND date ('{self.to_date}')
            ),0) as `maintainance_cost`
        """


        sql = f"""
        select 
            * 
            , ABS(ifnull(t.last_odometer,0) - ifnull(t.first_odometer,0)) as diff_odometer
            , (ifnull(t.maintainance_cost,0) + ifnull(t.litres_cost)) as total_cost
        from 
            (
                select
                vehicle.name as vehicle_name
                            ,
                vehicle.vehicle_type 
                            ,
                vehicle.vehichle_brand as vehicle_brand
                            ,
                IFNULL((select max(log.odometer) from `tabVehicle Log` log where log.license_plate = vehicle.name and log.docstatus = 1 and date(log.`date`) <= date ('{self.filters.from_date}') ) , 0 ) as first_odometer 
                            ,
                IFNULL((select max(log.odometer) from `tabVehicle Log` log where log.license_plate = vehicle.name and log.docstatus = 1 and date(log.`date`) BETWEEN date ('{self.filters.from_date}') AND date ('{self.filters.to_date}') ), 0 ) as last_odometer
                ,
                (
                select
                    log.employee
                from
                    `tabVehicle Log` log
                where
                    log.license_plate = vehicle.name
                    and log.docstatus = 1
                    and IFNULL(log.employee, '') <> ''
                        and date(log.`date`) BETWEEN date ('{self.filters.from_date}') AND date ('{self.filters.to_date}')
                    ORDER BY
                        date(log.`date`) desc
                    limit 1 ) as driver
                ,ifnull((
                    select
                        SUM(child.no_litre)
                    from
                        `tabTank log child` child
                    inner join `tabTank log` tank_log on
                        tank_log.name = child.parent
                    where tank_log.vehicle = vehicle.name and date (child.date) BETWEEN date ('{self.filters.from_date}') AND date ('{self.filters.to_date}')
                ),0) as total_liters 
                ,ifnull((
                    select
                        SUM(child.price * child.no_litre)
                    from
                        `tabTank log child` child
                    inner join `tabTank log` tank_log on
                        tank_log.name = child.parent
                    where 
                        tank_log.vehicle = vehicle.name 
                        and date (child.date) BETWEEN date ('{self.filters.from_date}') AND date ('{self.filters.to_date}')

                ),0) as litres_cost 

                {columns}
                
                
	
            from
                tabVehicle vehicle
            where
                1 = 1 
                {self.conditions}
            ) t
        
        """

        self.data = frappe.db.sql(sql, as_dict=1)

        return self.data

    def get_conditions(self):
        conditions = ""

        filters = self.filters

        data = filters.get("vehicle_type")
        if data:
            conditions += f" and vehicle.vehicle_type = '{data}' "

        data = filters.get("vehicle_brand")
        if data:
            conditions += f" and vehicle.vehichle_brand = '{data}' "

        data = filters.get("vehicle")
        if data:
            conditions += f" and vehicle.name = '{data}' "

        return conditions
