# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceRequest(Document):
	
	def on_submit(self):
		self.create_vehicle_log()
		sql = f"""
			UPDATE `tabMaintenance Request` set status = 'Agree' where name = '{self.name}'
		"""
		frappe.db.sql(sql)
		frappe.db.commit()
		self.reload()

	def create_vehicle_log(self):
		vehicle_log=frappe.new_doc("Vehicle Log")
		vehicle_log.license_plate = self.vehicle
		vehicle_log.maintenance_request = self.name
		vehicle_log.status = self.status
		vehicle_log.office = self.office
		vehicle_log.area   = self.area
		# vehicle_log.odometer=reading
		#vehicle_log.last_odometer=self.odometer_reading
		vehicle_log.date=self.date
		row = vehicle_log.append("service_detail",{})
		row.type=self.maintainance
		row.status = self.status

		# row.odometer=reading
		# row.expense_amount=expense
		# row.price=price
		# row.description=description
		vehicle_log.flags.ignore_mandatory = True
		vehicle_log.save()
		# vehicle_log.docstatus=1
		# vehicle_log.save()
