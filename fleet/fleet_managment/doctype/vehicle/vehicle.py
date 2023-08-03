# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_address, today, add_years, format_datetime, cstr
import datetime
from dateutil.relativedelta import relativedelta

class Vehicle(Document):
	def validate(self):
		self.check_vehicle_driver()

	def on_submit(self):
		self.create_vechel_item()
		if not self.vehichle_plate_number:
			frappe.throw("Please enter vehichle plate number")
		if not self.chassis_no:
			frappe.throw("Please enter chassis no")
	@frappe.whitelist()
	def checkLicenceValidation(self, endDtae):
		if getdate(endDtae) > getdate(today()):
			return 'true'
		return 'false'

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

	def check_vehicle_driver(self):
		if self.drivers:
			for driver in self.drivers:
				doc=frappe.get_doc("Driver",driver.driver)
				if driver.status=="Active":
					doc.vehicle=self.name
					doc.area=self.area
					doc.office=self.office
				else:
					doc.vehicle=""
					doc.area = ""
					doc.office = ""
				doc.save()


	def create_vechel_item(self):
		driver_name = ''
		if self.drivers :
			for driver in self.drivers :
				driver_name = driver.driver_name
		if len(driver_name) > 0 :
			item = frappe.new_doc("Item")
			item.item_code = self.concat_plate_number() + driver_name
			item.item_name = self.concat_plate_number() + driver_name
			item.item_group = "Services"
			item.stock_uom = "Nos"
			item.is_stock_item = 0 
			item.save()
			self.item = item.name
			self.save()
	def validate_update_after_submit(self):
		self.check_vehicle_driver()

	def on_cancel(self):
		# try:
		for d in self.drivers:
			doc=frappe.get_doc("Driver",d.driver)
			doc.vehicle=""
			doc.save()
		frappe.db.sql("delete from `tabTire Log` where vehicle='%s'"%self.name)
		frappe.db.commit()
		frappe.db.sql("""delete from `tabTank log` where vehicle='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""delete from `tabVehicle Log` where license_plate='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""delete from `tabVehicle Card` where vehicle='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabDriver Violation` set vehicle='' where vehicle='%s'"""%self.name)
		frappe.db.commit()
		# customer_agreement=frappe.db.sql("""select parent from `tabCustomer Invoice Details` where vehicle='%s'""")
		# if customer_agreement:
		# 	for c_agreement in customer_agreement:
		# 		frappe.db.sql("""delete from `tabCustomer Agreement` where name='%s'"""%c_agreement.parent)
		# except:
		# 	pass
		#customer agreement child
		frappe.db.sql("""update `tabCustomer Invoice Details` set vehicle='' where vehicle='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabInvoice Details` set vehicle='' where vehicle='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""delete from `tabvehichle licence` where vehicle='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""delete from `tabGPS Logs` where vehicle='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabDriver Cart` set vehicle='' where vehicle='%s'"""%self.name)
		frappe.db.commit()



@frappe.whitelist()
def get_edit_vechile_role():
	role = frappe.db.get_single_value('Fleet Vehicle Role','edit_vechile_role')
	user_roles = frappe.get_roles(frappe.session.user)
	if role in user_roles:
		return True
	else:
		return False
