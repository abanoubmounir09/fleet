# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MovingRegister(Document):
	def on_submit(self):
		doc = frappe.get_doc("Request Trip",self.request_trip)
		if self.type == "Partial":
			doc.completed_percentage = float(doc.completed_percentage or 0) + float(self.percent or 0)
		else:
			doc.completed_percentage = 100
		
		doc.save()
