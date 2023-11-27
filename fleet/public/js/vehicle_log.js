// Copyright (c) 2023, DTS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vehicle Log", {
	refresh(frm) {
		if(frm.doc.docstatus == 1) {
			frm.remove_custom_button(('Expense Claim'),('Create'));
			frm.add_custom_button(__('Journal Entry'), function() {
				frappe.model.open_mapped_doc({	
					method: "fleet.controllers.vehicle_log.create_journal_entry",
					frm: frm,
				});
			}, __('Create'));
            frm.add_custom_button(__('Purchase Invoice'), function() {
				frappe.model.open_mapped_doc({	
					method: "fleet.controllers.vehicle_log.create_purchase_invoice",
					frm: frm,
				});
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
	},
});