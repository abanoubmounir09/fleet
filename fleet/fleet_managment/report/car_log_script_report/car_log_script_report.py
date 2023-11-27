# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	data = get_data()
	columns = get_col()

	return columns, data

def get_data():
	data = frappe.db.sql(
		'''
			SELECT * FROM `tabVehicle Log`
			where status <> ''
		'''
	,as_dict=1)
	return data

def get_col():
	return [
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width":300
			# "options": "Maintenance",
		 },
	]

