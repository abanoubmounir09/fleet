# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import now, getdate, cast_fieldtype
from dateutil.relativedelta import relativedelta

class PreRequest(Document):
	def check_validation_period(self):
		doc=frappe.get_doc("Pre Requisites Type",self.aspect_type)
		if doc.has_period==1:
			return True
		else:
			return False

	def calc_end_date(self):
		start_date=getdate(self.start_date)
		doc = frappe.get_doc("Pre Requisites Type", self.aspect_type)
		end_date = start_date + relativedelta(months=doc.period_in_month)
		self.end_date=end_date
		return True
