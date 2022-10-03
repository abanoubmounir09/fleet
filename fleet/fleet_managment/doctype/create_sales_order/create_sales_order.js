// Copyright (c) 2021, Dynamic Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Create Sales Order', {
		refresh: function(frm) {
			frappe.model.open_mapped_doc({
			method: "fleet.fleet_managment.doctype.create_sales_order.create_sales_order.make_sales_order",
			frm: frm
		})
		}
});
