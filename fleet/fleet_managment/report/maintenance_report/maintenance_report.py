# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [

		   {
			"fieldname": "maintenance",
			"label": _("Maintenance"),
			"fieldtype": "Data",
			"width":150
			# "options": "Maintenance",
		  },
		  {
			"fieldname": "price",
			"label": _("Price"),
			"fieldtype": "Data",
			"width":150
		  },
		  {
			"fieldname": "date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width":150
		  },
		  {
			"fieldname": "odometer",
			"label": _("Odometer Reading"),
			"fieldtype": "Data",
			"width":150
		  },
		  {
			"fieldname": "vehicle",
			"label": _("Vehicle"),
			"fieldtype": "Link",
			"options":"Vehicle",
			"width":150
		  },
		  {
			"fieldname": "office",
			"label": _("Office"),
			"fieldtype": "Data",
			"width":150
		  },
		  {
			"fieldname": "area",
			"label": _("Area"),
			"fieldtype": "Data",
			"width":150
		  },
		  {
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width":150
		  }

	]


def get_data(filters):
	conditions = " where 1=1 "
	if filters.get("vehichle"):
		conditions +=  " and tv.license_plate ='%s'"%filters.get("vehichle")
	if filters.get("from_date"):
		conditions +=  " and tv.date >= '%s' "%filters.get("from_date")
	if filters.get("to_date"):
		conditions +=  " and tv.date <= '%s' "%filters.get("to_date")
	sql = f"""
		select 
		vs.type  as maintenance
		,vs.expense_amount as price
		,tv.date as date
		,tv.odometer 
		,tv.status 
		,tv.license_plate  as vehicle
		,tv.office 
		,tv.area
		from `tabVehicle Service` vs
		inner join 
		`tabVehicle Log` tv 
		on tv.name  = vs.parent 

		{conditions}
	"""
	print(sql)
	data = frappe.db.sql(sql,as_dict=1)
	return data
