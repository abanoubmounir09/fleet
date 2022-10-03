# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_address, today, add_years, format_datetime, cstr
from dateutil.relativedelta import relativedelta

class DriverPreRequisites(Document):
	def validate(self):
		self.check_national_id()
		self.check_black_list()
		self.check_if_medical()
	def on_submit(self):
		if self.passed==1 and self.is_old==0:
			doc=frappe.new_doc('Driver')
			doc.first_name=self.driver_name
			doc.driver_name=self.driver_name
			doc.national_id=self.national_id
			doc.is_passed = 1
			doc.save()
			driver_card = frappe.new_doc("Driver Cart")
			driver_card.driver = doc.name
			for insp in self.pre_requests:
				status=0
				if insp.yes:
					status=1
				row =driver_card.append("inspections",{})
				row.pre_request=insp.pre_request
				row.status =status
				row.end_date=insp.end_date
				row.date_of_inspection=getdate(today())
			driver_card.save()
		else:

			if self.driver_link:
				driver_cart = frappe.db.sql(
					"""select name from `tabDriver Cart` where driver='%s'""" %self.driver_link,as_dict=1)
				if driver_cart:
					cart_doc=frappe.get_doc("Driver Cart",driver_cart[0].name)
					doc=frappe.get_doc("Driver",self.driver_link)
					doc.status="Inactive"
					doc.is_passed=0
					doc.save()
					for inspections in self.pre_requests:
						count=0
						for card_inspection in cart_doc.inspections:
							if inspections.pre_request ==card_inspection.pre_request:
								count =count+1
								# frappe.msgprint("hello")
								card_inspection.date_of_inspection=inspections.date
								card_inspection.status=inspections.yes
						if count==0:
							row = cart_doc.append("inspections", {})
							row.pre_request = inspections.pre_request
							row.status = inspections.yes
							row.end_date = inspections.end_date
							row.date_of_inspection = getdate(today())
					cart_doc.save()
	def ge_all_driver_pre_requests(self):
		# frappe.msgprint("hello")
		result=frappe.db.sql("""select name,aspect_name,aspect_type from `tabPre Request`  where docstatus=1""",as_dict=1)
		for res in result:
			row=self.append("pre_requests",{})
			row.pre_request=res.name
			row.pre_requisites_type=res.aspect_type
			row.pre_request_name=res.aspect_name
		return True

	def check_inspection_period(self,inspection,date):
		end_date=None
		pre_request=frappe.get_doc("Pre Request",inspection)
		if pre_request:
			pre_request_type=frappe.get_doc("Pre Requisites Type",pre_request.aspect_type)
			if pre_request_type and pre_request_type.has_period:
				end_date=getdate(date) +relativedelta(months=pre_request_type.period_in_month)
				return end_date
		return end_date
	def check_national_id(self):
		nattional_id=frappe.db.sql("select national_id from tabDriver where national_id='%s'"%self.national_id,as_dict=1)
		if nattional_id and self.is_old==0:
			self.national_id=""
			frappe.throw("National id '%s' already exist"%nattional_id[0].national_id)
	def check_black_list(self):
		if self.is_old==1 and self.driver_link:
			doc=frappe.get_doc("Driver",self.driver_link)
			if doc.status=="Blacklist":
				frappe.throw("Driver in black list")

	def check_if_medical(self):
		for ins in self.pre_requests:
			pre_request = frappe.get_doc("Pre Request", ins.pre_request)
			if pre_request:
				pre_request_type = frappe.get_doc("Pre Requisites Type", pre_request.aspect_type)
				if pre_request_type and pre_request_type.is_medical==1 and  not ins.for_whom:
					frappe.throw("Enter Deliverd To in row '%s'"%ins.idx)

