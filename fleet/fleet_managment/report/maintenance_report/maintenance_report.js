// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Maintenance Report"] = {
	"filters": [
		{
			fieldname: "vehichle",
			label: __("Vehichle"),
			fieldtype: "Link",
			options:"Vehicle"
		},
		{
			fieldname: "from_date",
			label: __("From date"),
			fieldtype: "Date"
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date"
		}
	]
};
