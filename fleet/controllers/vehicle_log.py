import frappe

@frappe.whitelist()
def create_journal_entry(source_name):
    doc = frappe.get_doc("Vehicle Log",source_name)
    journal_entry = frappe.new_doc("Journal Entry")
    journal_entry.vehicle_log = doc.name
    return journal_entry

@frappe.whitelist()
def create_purchase_invoice(source_name):
    doc = frappe.get_doc("Vehicle Log",source_name)
    journal_entry = frappe.new_doc("Purchase Invoice")
    journal_entry.vehicle_log = doc.name
    return journal_entry