# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext.accounts.utils import get_fiscal_year, getdate, nowdate
from frappe.model.document import Document

class TireLog(Document):
	def validate(self):
		for tc in self.tire_change:
			if self.last_tier_change_km:
				if tc.status=="Done" and float(tc.counter_reading) >float(self.last_tier_change_km):
					self.last_tier_change_km=tc.counter_reading
					self.last_tier_change_date = tc.date 

			else:
				if tc.status=="Done":
					self.last_tier_change_km=tc.counter_reading
					#self.last_tier_change_date = tc.date

		for ti in self.tire_inspection_log:
			if self.last_tier_inspection_km:
				if ti.status=="Done" and float(ti.counter_reading) >float(self.last_tier_inspection_km):
					self.last_tier_inspection_km=ti.counter_reading
					self.last_tier_inspection_date = tc.date 
			else:
				if ti.status == "Done":
					self.last_tier_inspection_km = ti.counter_reading
					#self.last_tier_inspection_date = tc.date


		lasttierinspection=self.last_tier_change_km or 0
		lasttierchange = self.last_tier_inspection_km or 0
		currentreading=self.current_reading or 0
		maxreading=max(float(lasttierinspection),float(lasttierchange))
		if maxreading >float(currentreading):
			self.current_reading=maxreading
		card_name = frappe.db.sql("""select name from `tabVehicle Card` where vehicle='%s'""" % self.vehicle, as_dict=1)
		if card_name:
			doc = frappe.get_doc("Vehicle Card", card_name[0].name)
			doc.last_tire_inspection = self.last_tier_inspection_km
			doc.last_tire_change = self.last_tier_change_km
			doc.save()
	def add_change(self):
		row=self.append("tire_change",{})
		# row.date=getdate(nowdate())
		row.required_date=getdate(nowdate())
		row.counter_reading=self.add_ch_r_km
		row.status="Not Done"
		return True

	def add_inspection(self):
		row=self.append("tire_inspection_log",{})
		# row.date=getdate(nowdate())
		row.required_date=getdate(nowdate())
		row.counter_reading=self.add_ins_r_km
		row.status="Not Done"
		return True
	def getDate(self):
		return getdate(nowdate())

