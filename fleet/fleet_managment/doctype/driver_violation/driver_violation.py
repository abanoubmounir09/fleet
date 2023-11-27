# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DriverViolation(Document):
	def on_submit(self):
		cart_name=frappe.db.sql("""select name from `tabDriver Cart` where driver='%s'"""%self.driver,as_dict=1)
		if cart_name:
			doc=frappe.get_doc("Driver Cart",cart_name[0].name)
			doc.append("driver_violation",{
				"violation":self.name,
				"violation_date":self.violation_date,
				"penality":self.penality,
				"violation_fee":self.violation_fee
			})
			doc.save()

