# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ChangePlateNumber(Document):
	def on_submit(self):
		vehicle=frappe.get_doc("Vehicle",self.vehicle)
		vehicle.c1=self.c1
		vehicle.c2=self.c2
		vehicle.c3 = self.c3
		vehicle.c4 = self.c4
		vehicle.no= self.no
		vehicle.db_set('vehichle_plate_number',self.plate_number)
		frappe.db.commit()
	
	@frappe.whitelist()
	def concat_plate_number(self):
		plate=""
		if self.no:
			plate+=self.no +" "
		if self.c1:
			plate+=self.c1 +" "
		if self.c2:
			plate+=self.c2 +" "
		if self.c3:
			plate+=self.c3 +" "
		if self.c4:
			plate+=self.c4 +" "
		return plate