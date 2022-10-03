# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UplaodOdometerReading(Document):
	def validate(self):
		if self.status!="Done":
			# frappe.db.sql("""update `tabVehicle Card` set odometer_reading='{}' ,reading_date='{}' where vehicle='{}' and odometer_reading < '{}'""".format(
			# 	self.reading,
			# 	self.date,
			# 	self.vehicle,
			# 	self.reading
			# ))
			cart_name=frappe.db.sql("""select name from `tabVehicle Card` where vehicle='%s'"""%self.vehicle,as_dict=1)
			if cart_name:
				# frappe.msgprint(cart_name[0].get("name"))
				cart_doc=frappe.get_doc("Vehicle Card",cart_name[0].get("name"))
				if cart_doc.odometer_reading < self.reading:
					cart_doc.odometer_reading=self.reading
					cart_doc.las_reading=self.reading
					cart_doc.reading_date=self.date
					cart_doc.save()
					self.status="Done"
