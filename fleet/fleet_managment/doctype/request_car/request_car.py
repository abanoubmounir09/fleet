# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today 
from frappe.model.document import Document

class RequestCar(Document):
	def validate(self):
		self.set_day_date()
	
	def set_day_date(self):
		self.day_date = today()
