# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RequestTrip(Document):
	pass

@frappe.whitelist()
def create_moving_register(source_name, target_doc=None):
	doc     = frappe.new_doc("Moving Register")
	doc.request_trip = source_name
	return doc

