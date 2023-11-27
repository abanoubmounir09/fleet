# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Tanklog(Document):
	def validate(self):
		if  self.no_litre and self.price:
			self.tank_reading=self.current_reading
			row=self.append('tank_log',{})
			row.current_reading=self.current_reading
			row.no_litre=self.no_litre
			row.price=self.price
			row.date = self.date
			self.current_reading=""
			self.no_litre=""
			self.price=""
			#self.date=""
			card_name=frappe.db.sql("""select name from `tabVehicle Card` where vehicle='%s'"""%self.vehicle,as_dict=1)
			if card_name:
				doc=frappe.get_doc("Vehicle Card",card_name[0].name)
				if self.tank_reading and float(self.tank_reading or 0) > float(doc.last_tank or 0):
					doc.last_tank=self.tank_reading
					doc.save()
		else:
			pass
			# frappe.msgprint(_("Please enter missing data"))