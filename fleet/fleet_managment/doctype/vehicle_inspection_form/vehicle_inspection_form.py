# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from fleet.fleet_managment.doctype.maintenance_request.maintenance_request import get_user_by_role

class VehicleInspectionForm(Document):
	def after_insert(self):
		get_all_manger = get_user_by_role("System Manager")
		kwargs={
			"get_all_manger":get_all_manger,
			"document_type":self.doctype,
			"document_name":self.name,
			"date":self.date,
		}
		vechile_inspection_form_alert_manager(**kwargs)

	def on_submit(self):
		if self.passed==1 and self.is_old==0:
			doc=frappe.new_doc('Vehicle')
			doc.vehicle_type=self.vehicle_type
			doc.vehichle_brand=self.vehichle_brand
			doc.model=self.vehichle_model_year
			doc.vehichle_plate_number=self.vehichle_plate_number
			doc.is_passed=1
			doc.vehicle_status="Active"
			doc.no = self.no
			doc.c1 = self.c1
			doc.c2 = self.c2
			doc.c3 = self.c3
			doc.c4 = self.c4
			doc.km_reading=self.mileage_reading
			doc.chassis_no=self.chasis_number
			doc.office=self.office
			doc.area=self.area
			doc.save()
			vehicle_card=frappe.new_doc("Vehicle Card")
			vehicle_card.vehicle=doc.name
			vehicle_card.odometer_reading=self.mileage_reading
			type=frappe.get_doc("Vehicle Type",self.vehicle_type)
			for mm in type.maintainance:
				row=vehicle_card.append("maintainance",{})
				row.maintainance=mm.maintainance
				row.notification_before_km=mm.notification_before_km
				row.period=mm.period
			vehicle_card.save()
		elif self.is_old==1 and self.passed==1:
			doc = frappe.get_doc("Vehicle", self.vehicle)
			doc.is_passed = 0
			doc.vehicle_status = "Active"
			doc.save()
		else:
			if self.passed==0 and self.is_old==1 and self.vehicle:

				try :
					doc=frappe.get_doc("Vehicle",self.vehicle)
					doc.is_passed=0
					doc.vehicle_status="Inactive"
					doc.save()
				except:
					pass


				# doc=frappe.get_doc("Vehicle",self.vehicle)
				# doc.is_passed=0
				# doc.vehicle_status="Inactive"
				# doc.save()
	def validate_plate_no(self):
		if  self.is_old ==0:
			#car is new
			cur_v = frappe.db.get_value("Vehicle",{'vehichle_plate_number':self.vehichle_plate_number},'name')
			if cur_v and not self.is_old:
				frappe.throw(_("Plat Number is Exit with Another Vehicle {}".format(str(cur_v))))
	def validate_vehicle_status(self):
		if self.is_old :
			#car is new
			# if not self.vehicle :
			# 	frappe.throw(_("Vehicle Field is Mandatory"))


			status = frappe.db.get_value("Vehicle",self.vehicle,'vehicle_status') or ''
			if status == "Blacklist":
				frappe.throw(_("Vehicle {} is in Blacklist".format(str(self.vehicle))))

	def validate(self):
		#self.validate_plate_no()
		self.validate_plate_no()
		self.validate_vehicle_status()
	@frappe.whitelist()
	def GetAllType(self,type):

		aspects=frappe.db.sql("select * from `tabInspection Aspects` where aspect_type='{}'".format(type),as_dict=1)
		# for aspect in aspects:
		# 	#frappe.msgprint(aspect.name)
		# 	row=self.append("inspection_aspect",{})
		# 	row.inspection_aspects=aspect.name
		#
		# self.save()
		return aspects
	@frappe.whitelist()
	def getDocStatus(self):
		existing = frappe.db.get_value("Vehicle Inspection Form", self.name, "name")
		if existing:
			return 1
		else:
			return 0
	@frappe.whitelist()
	def ge_all_car_inspections(self):
		
		result = frappe.db.sql("""select name,aspect_name from `tabInspection Aspects` where docstatus=1""", as_dict=1)
		for res in result:
			self.append("inspection_aspect" , {
					'inspection_aspects' : str(res.name),
					'aspect_name' :str(res.aspect_name)


				})
			# row.inspection_aspects = str(res.name)
			# row.aspect_name = str(res.aspect_name)

		return (self.inspection_aspect )
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


def vechile_inspection_form_alert_manager(**kwargs):
	for row in kwargs.get("get_all_manger"):
		owner_name = row.get("parent")
		contact_date = kwargs.get('date')
		notif_doc = frappe.new_doc('Notification Log')
		notif_doc.subject = f"Vehicle Inspection Form With Name {owner_name} was created at {contact_date}"
		notif_doc.email_content = f"Vehicle Inspection Form With Name {owner_name} was created at {contact_date}"
		notif_doc.for_user = owner_name
		notif_doc.type = "Mention"
		notif_doc.document_type = kwargs.get('document_type')
		notif_doc.document_name = kwargs.get('document_name')
		notif_doc.from_user = frappe.session.user
		notif_doc.insert(ignore_permissions=True)
