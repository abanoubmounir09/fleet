# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
class MovingRegister(Document):
	# def update_odometer_reading_in_vehichle_card(self):
	# 	sql = f"""select name from `tabVehicle Card` where vehicle ='{self.vehicle}'"""
	# 	r = frappe.db.sql(sql,as_dict=1)
	# 	if len(r)>0:
	# 		card = frappe.db.get("Vehicle Card",r[0].name)
	# 		card.odometer_reading = card.odometer_reading + 
	def on_submit(self):
		doc = frappe.get_doc("Request Trip",self.request_trip)
		if self.type == "Partial":
			doc.completed_percentage = float(doc.completed_percentage or 0) + float(self.percent or 0)
		else:
			doc.completed_percentage = 100
		
		doc.save()
	@frappe.whitelist()
	def get_vehicle_last_reading(self):
		sql = f"""select odometer_reading from `tabVehicle Card` where vehicle ='{self.vehicle}'"""
		res = frappe.db.sql(sql,as_dict=1)
		if len(res)>0:
			return res[0].get("odometer_reading")
		return 0
	@frappe.whitelist()
	def check_remaining_percent(self):
		if self.request_trip:
			doc = frappe.get_doc("Request Trip",self.request_trip)
			remaining =100 - doc.completed_percentage
			if remaining < self.percent:
				#self.percent = 0
				#frappe.msgprint(_("you cant exceed remaing percentage %s"%remaining))
				return {"res":"False","remaining":remaining}
		return
