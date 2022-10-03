# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_address, today, add_years, format_datetime, cstr
import datetime
from dateutil.relativedelta import relativedelta
class vehichlelicence(Document):
	def validate(self):
		if getdate(self.licence_end_date) < getdate(self.licence_start_date):
			frappe.throw("Invalid End Date")
	def check_licence_dates(self):
		result=frappe.db.sql("""select plate_number,owner_name,licence_end_date from `tabvehichle licence` where CURDATE()-`tabvehichle licence`.licence_end_date >=10""",as_dict=1)
		for res in result:
			frappe.send



