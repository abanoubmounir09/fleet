# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_address, today, add_years, format_datetime, cstr
from fleet.fleet_managment.doctype.vehicle_card.vehicle_card import  sent_notification
from frappe.utils import add_days, getdate, today ,nowdate
import datetime

class DriverCart(Document):
	def update_driver_status(self):
		doc=frappe.get_doc("Driver",self.driver)
		doc.status=self.status
		doc.save()
		return True
	def get_employee_custody(self):
		total_advance_amount=0
		total_paid_amount=0
		total_pending_amount=0
		total_claimed_amount=0
		result=frappe.db.sql("""Select  name,asset_name from tabAsset where driver='%s'"""%self.driver,as_dict=1)
		if result:
			for res in result:
				row=self.append("asset_custody",{})
				row.asset=res.name
		employee_advance=frappe.db.sql("""select advance_amount,paid_amount,pending_amount,claimed_amount,posting_date from `tabEmployee Advance` where driver='%s'"""%self.driver,as_dict=1)
		if employee_advance:
			for adv in employee_advance:
				row=self.append("driver_advance",{})
				row.date=adv.posting_date
				row.advance_amount=adv.advance_amount
				row.paid_amount=adv.paid_amount
				row.pending_amount=adv.pending_amount
				row.claimed_amount=adv.claimed_amount
				total_paid_amount +=adv.paid_amount
				total_advance_amount +=adv.advance_amount
				total_pending_amount +=adv.pending_amount
				total_claimed_amount +=adv.claimed_amount
			self.total_advance_amount=total_advance_amount
			self.total_paid_amount=total_paid_amount
			self.total_pending_amount=total_pending_amount
			self.total_claimed_amount=total_claimed_amount
			self.difference=float(self.total_paid_amount or 0) - float(self.total_claimed_amount or 0)

		items_custody=frappe.db.sql("""
			select `tabEmployee Tools Item`.item_code,`tabEmployee Tools Item`.delivery_date
			from `tabEmployee Tools`
			inner join
				`tabEmployee Tools Item`
			on `tabEmployee Tools Item`.parent=`tabEmployee Tools`.name
			where `tabEmployee Tools`.driver='%s' and status='Delivered'
		"""%self.driver,as_dict=1)
		for item in items_custody:
			row=self.append("items_custody",{})
			row.item_code=item.item_code
			row.delivery_date=item.delivery_date

		return True
	##################### Notification ######################
def check_driver_notification(*args,**kwargs):
	# chech inspections end date

	cards = frappe.get_list("Driver Cart", fields=["name"])
	selling_setting=frappe.get_single("Selling Settings")
	for card in cards:
		s_card=frappe.get_doc("Driver Cart",card)
		driver=frappe.get_doc("Driver",s_card.driver)
		if s_card.inspections and driver.status=="Active":
			#frappe.msgpint("2 if")
			for pre in s_card.inspections:
				pre_req=frappe.get_doc("Pre Request",pre.pre_request)
				pre_request_type=frappe.get_doc("Pre Requisites Type",pre_req.aspect_type)
				if pre_request_type.notification_beforemonh !=0:
					period=pre_request_type.notification_beforemonh
					res=str(getdate(today()) - getdate(pre.end_date))
					if res:
						try:
							res=res.split(' ')[0]
							res=int(res)
							if int(pre_request_type.notification_beforemonh)*30 > res > 0:

								sent_notification(subject="inspection '{}' for driver '{}' is about to end".format(pre.pre_request,s_card.driver),document_type="Driver Cart",document_name=s_card.name)
							if res > int(selling_setting.stop_period) or 0:
								driver.status="Suspended"
								driver.save()
								change_driver_status(driver=cards.driver)

						except:
							pass
		# check driver licence end date	
		diff=str(getdate(today()) - getdate(driver.enddate))
		#frappe.msgprint(diff)
		if diff and driver.status=="Active":
			try:
				# frappe.msgprint(diff)
				diff=diff.split(' ')[0]
				diff=int(diff)
				if  0<= diff <= 30:
					# frappe.msgprint("hello")
					sent_notification(subject=" driver '{}' licence  is about to end".format( s_card.driver),document_type="Driver Cart", document_name=s_card.name)
				if res > int(selling_setting.stop_period):
					driver.status="Suspended"
					driver.save()
					change_driver_status(driver=cards.driver)
			except:
				pass
		# frappe.throw("asd")
		# if card.courses :# and card.status=="Active":
			# frappe.throw("card.courses")
		try:
			for course in s_card.courses:
				diff = str(getdate(course.end_date) - getdate(course.date))
				diff = diff.split(' ')[0]
				diff = int(diff)
				# frappe.msgprint(str(diff))
				if  0<= diff <= 30:
					# frappe.msgprint("diff from if")
					sent_notification(subject=" driver '{}' course for '{}'  is about to end".format( s_card.driver,course.driver_course),document_type="Driver Cart", document_name=s_card.name)
					driver.status = "Suspended"
					driver.save()
					change_driver_status(driver=cards.driver)
		except:
			pass

def change_driver_status(status="Suspended",driver=None):
	frappe.db.sql("""update tabDriver set status="{status}" where name={driver} """.format(
		status=status,
		driver=driver
	),as_dict=1)
	frappe.db.commit()