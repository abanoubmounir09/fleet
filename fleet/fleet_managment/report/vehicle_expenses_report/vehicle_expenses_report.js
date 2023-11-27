// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt
/* eslint-disable */
const now = new Date();
frappe.query_reports["Vehicle Expenses Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": new Date(now.getFullYear(), now.getMonth(), 1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": new Date(now.getFullYear(), now.getMonth() + 1, 0),
			"reqd": 1
		},
		{
			"fieldname": "vehicle_type",
			"label": __("Vehicle Type"),
			"fieldtype": "Link",
			"options": "Vehicle Type",
		},
		{
			"fieldname": "vehicle",
			"label": __("Vehicle"),
			"fieldtype": "Link",
			"options": "Vehicle",
		},
		{
			"fieldname": "vehicle_brand",
			"label": __("Vehicle Brand"),
			"fieldtype": "Link",
			"options": "Vehicle Brand",
		}
	]
};
