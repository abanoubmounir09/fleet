# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VehicleReturn(Document):
	def on_submit(self):
		self.update_moving_register_status()
		self.update_odometer_reading()
		self.update_vehicle_status()

	def update_moving_register_status(self):
		moving_register_doc = frappe.get_doc("Moving Register",self.moving_register)
		moving_register_doc.moving_status ="Closed"
		moving_register_doc.save()
		

	def update_odometer_reading(self):
		moving_register_doc = frappe.get_doc("Moving Register",self.moving_register)
		if moving_register_doc.vehicle:
			card_name = frappe.db.sql("""select name from `tabVehicle Card` where vehicle='%s'""" % moving_register_doc.vehicle, as_dict=1)
			if len(card_name) > 0:
				card = frappe.get_doc("Vehicle Card",card_name[0].name)
				if  self.retuen_odometer_reading > float(card.odometer_reading or 0):
					card.odometer_reading = self.retuen_odometer_reading
					card.save()


	def update_vehicle_status(self):
		moving_register_doc = frappe.get_doc("Moving Register",self.moving_register)
		if moving_register_doc.vehicle:
			doc = frappe.get_doc("Vehicle",moving_register_doc.vehicle)
			doc.vehicle_status = "Active"
			doc.save()
