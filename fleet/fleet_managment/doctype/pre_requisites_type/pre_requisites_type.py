# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class PreRequisitesType(Document):
	def validate(self):
		if self.has_period and (not self.period_in_month or self.has_period==0):
			frappe.throw(_("Please enter Validation Period"))
