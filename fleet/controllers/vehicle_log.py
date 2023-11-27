import frappe

@frappe.whitelist()
def create_journal_entry(source_name):
    vehicle_log = frappe.get_doc("Vehicle Log",source_name)
    journal_entry = frappe.new_doc("Journal Entry")
    journal_entry.vehicle_log = vehicle_log.name
    return journal_entry

@frappe.whitelist()
def create_purchase_invoice(source_name):
    vehicle_log = frappe.get_doc("Vehicle Log",source_name)
    purchase_invoice = frappe.new_doc("Purchase Invoice")
    purchase_invoice.vehicle_log = vehicle_log.name
    return purchase_invoice