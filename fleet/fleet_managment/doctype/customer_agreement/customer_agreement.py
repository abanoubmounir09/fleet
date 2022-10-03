# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_address, today, add_years, format_datetime, cstr
class CustomerAgreement(Document):
	def validate(self):
		if getdate(self.to_date) < getdate(self.from_date):
			frappe.throw("To Date Must Be Greate Than From Date")
	# 	for item in self.invoice_details:
	# 		if not frappe.db.get_value("Item", item.vehicle+item.driver, "item_code"):
	# 			self.CreateItem(item.vehicle+item.driver)
	# 			item.item=item.vehicle+item.driver
	#
	#
	#
	# def CreateItem(self,ItemCode):
	# 	doc = frappe.new_doc('Item')
	# 	doc.item_group = "Services"
	# 	doc.item_code =str(ItemCode)
	# 	doc.item_name =str(ItemCode)
	# 	doc.is_stock_item = 0
	# 	doc.include_item_in_manufacturing = 0
	# 	doc.save()
	# 	frappe.db.commit()