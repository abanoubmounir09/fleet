// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["مصروفات صيانه"] = {
	"filters": [
		{
			fieldname: "vehichle",
			label: __("Vehichle"),
			fieldtype: "Link",
			options:"Vehicle"
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options:"\nAgree\nInProgress\nCompleted",
			// "default": "Agree"
		},
		// {
		// 	fieldname: "from_date",
		// 	label: __("From date"),
		// 	fieldtype: "Date"
		// },
		// {
		// 	fieldname: "to_date",
		// 	label: __("To Date"),
		// 	fieldtype: "Date"
		// }
	]
};
