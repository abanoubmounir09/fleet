# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_col()

	return columns, data

def get_data(filters):
	conditions = ' 1=1'
	if filters.get('vehichle'):
		conditions += ' AND `tabVehicle Log`.license_plate="%s"'%(filters.get('vehichle'))
	if filters.get('status'):
		conditions += ' AND `tabVehicle Log`.status="%s"'%(filters.get('status'))
	data = frappe.db.sql(
		f'''
			SELECT `tabVehicle Log`.name 
			,`tabVehicle Log`.status
			,`tabVehicle Log`.date
			,`tabVehicle Log`.area
			,`tabVehicle Log`.office
			,`tabVehicle Log`.license_plate
			,`tabVehicle Log`.status
			,`tabVehicle Service`.description
			,`tabVehicle Service`.service_item_name
			,`tabVehicle Service`.service_item
			,`tabVehicle Service`.expense_amount
			FROM `tabVehicle Log`
			INNER JOIN `tabVehicle Service`
			ON `tabVehicle Service`.parent=`tabVehicle Log`.name
			where `tabVehicle Log`.docstatus = 1 AND {conditions}
		'''
	,as_dict=1)
	return data

def get_col():
	return [
		{
			"fieldname": "name",
			"label": _("Id"),
			"fieldtype": "Link",
			"options": "Vehicle Log",
			"width":300,
			# "options": "Maintenance",
		 },
		{
			"fieldname": "license_plate",
			"label": _("License Plate"),
			"fieldtype": "Link",
			"options":"Vehicle",
			"width":100,
			# "options": "Maintenance",
		 },
		 {
			"fieldname": "expense_amount",
			"label": _("Expense"),
			"fieldtype": "Currency",
			"width":100
			# "options": "Maintenance",
		 },
		 {
			"fieldname": "office",
			"label": _("Office"),
			"fieldtype": "Link",
			"options":"Office",
			"width":100
			# "options": "Maintenance",
		 },
		 {
			"fieldname": "description",
			"label": _("Description"),
			"fieldtype": "Data",
			"width":300
			# "options": "Maintenance",
		 },
		 {
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width":100
			# "options": "Maintenance",
		 },
		 {
			"fieldname": "date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width":100
			# "options": "Maintenance",
		 },
		{
			"fieldname": "area",
			"label": _("Area"),
			"fieldtype": "Link",
			"options":"Area",
			"width":100
			# "options": "Maintenance",
		 },
		 {
			"label": _("Service Item Name"),
			"fieldname": "service_item_name",
			"fieldtype": "Link",
			"options":"Service Item",
			"width":300
			# "options": "Maintenance",
		 },
		 {
			"fieldname": "service_item",
			"label": _("Service Item"),
			"fieldtype": "Data",
			"width":300
			# "options": "Maintenance",
		 },
	]

