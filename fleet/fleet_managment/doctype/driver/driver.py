# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Driver(Document):
	def on_submit(self):
		if not self.national_id:
			frappe.throw("Please enter national id")
		if not self.gender:
			frappe.throw("Please enter gender")
		if not self.date_of_birth:
			frappe.throw("Please enter date of birth")
		if not self.date_of_joining:
			frappe.throw("Please enter date of joining")
	def validate(self):
		self.update_vehicle_card()
		try:
			self.driver_name = self.first_name + " " + self.last_name
		except:
			print("error")

	def update_vehicle_card(self):
		if self.vehicle:
			try:
				driver_cart=frappe.db.sql("""select name from `tabDriver Cart` where driver='%s'"""%self.name,as_dict=1)
				# frappe.msgprint(str(driver_cart))
				if driver_cart:
					doc=frappe.get_doc("Driver Cart",driver_cart[0].name)
					# frappe.msgprint(str(doc))
					if doc:
						doc.vehicle=self.vehicle
						doc.save()
			except:
				pass
	# 1 if exist ,2 if not exist
	@frappe.whitelist()
	def checkVehicle(self):
		if self.vehicle:
			doc=frappe.get_doc("Vehicle",self.vehicle)
			if doc.drivers:
				for d in doc.drivers:
					if d.driver==self.name:
						return 1

			else: return 2
		return 2

	def on_cancel(self):
		self.vehicle=''
		frappe.db.sql("""delete from `tabDriver Violation` where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""delete from `tabVehicle Drivers` where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabVehicle Log` set employee='' where employee='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabInvoice Details` set driver='' where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabCustomer Invoice Details` set driver='' where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabDelivery Note` set driver='' where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabEmployee Advance` set driver='' where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update `tabExpense Claim` set driver='' where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""update tabDeductions set driver='' where driver='%s'"""%self.name)
		frappe.db.commit()
		frappe.db.sql("""delete from `tabDriver Cart` where driver='%s'"""%self.name)
		frappe.db.commit()

