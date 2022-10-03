# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dynamic Technonlgy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ExaminationRequest(Document):
	def getDriver(self):
		drviverList=[]
		drivers=frappe.db.sql("select * from `tabVehicle Drivers` where parent='{}'".format(self.vehicle),as_dict=1)
		for d in drivers:
			drviverList.append(d.driver)
		return drviverList

