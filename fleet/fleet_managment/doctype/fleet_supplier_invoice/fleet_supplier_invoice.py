# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime,timedelta,date
from erpnext.controllers.accounts_controller import get_default_taxes_and_charges
import json

class FleetSupplierInvoice(Document):
	@frappe.whitelist()
	def add_new_mwthod(self) :
			frappe.msgprint("Fucking PEro")
	@frappe.whitelist()
	def get_supplier_vehicles(self):
		frappe.msgprint("Fucking PEro")
		# if not getattr(self,'supplier',None):
		# 	frappe.throw(_("Please Select Supplier To Fetch Vehicles"))
		# if not getattr(self,'company',None):
		# 	frappe.throw(_("Please Select Company To Fetch Vehicles"))
		# if not getattr(self,'day_count',None):
		# 	frappe.throw(_("Please Select Day Count To Fetch Vehicles"))
		# self.set('items',[])



		# res = frappe.db.sql("""
		# 	select
		# 		   (select driver  from `tabVehicle Drivers` drivers where drivers.parent = v.name and drivers.status = 'Active' limit 1) as driver
		# 		 , (select status  from `tabVehicle Drivers` drivers where drivers.parent = v.name and drivers.status = 'Active' limit 1) as driver_status
		# 			, v.name as vehicle , v.vehicle_type , v.item , v.vehicle_status , v.payment_method , v.no_hours , v.vehicle_value
		# 	from tabVehicle v
		# 	where supplier = '{}' and docstatus < 2
		
		# """.format(self.supplier),as_dict=1)
		# for i in res :
		# 	row = self.append('items')
		# 	row.vehicle = i.vehicle
		# 	row.vehicle_type = i.vehicle_type
		# 	row.item = i.item
		# 	if i.item  and self.company:
		# 		row.cost_center = frappe.db.get_value('Item Default',
		# 										  fieldname=['buying_cost_center'],
		# 										  filters={
		# 											  'parent': i.item,
		# 											  'parenttype': 'Item',
		# 											  'company': self.company
		# 										  }) or frappe.db.get_value("Company",self.company , "cost_center")
		# 	row.vehicle_satus = i.vehicle_status
		# 	row.payment_method = i.payment_method
		# 	row.driver = i.driver
		# 	row.driver_status = i.driver_status
		# 	row.hrs = i.no_hours
		# 	row.rent_amount = i.vehicle_value or 0
		# 	row .invoiced = 0
		# 	status = 'Active'
		# 	row.from_date = self.from_date
		# 	row.to_date = self.to_date
		# 	row.workin_days = self.day_count or 0
		# 	row.total = row .total_amount =  row.workin_days * (row.rent_amount / 30 )


	@frappe.whitelist()
	def make_purchase_invoice (self):
		self.save()

		# pi_items = frappe.db.sql("""
		# select item as item_code ,sum(total) as rate , cost_center , project from `tabFleet Supplier Invoice Items`  
		#   where parent = '{}' 
		#   and status = 'Active' 
		#   and invoiced <> 1 
		#   group by item
		# """.format(self.name),as_dict=1)

		pi = frappe.new_doc("Purchase Invoice")
		pi.company = self.company
		pi.currency =  frappe.get_cached_value('Company', self.company, "default_currency")
		pi.supplier = self.supplier
		pi.naming_series = 'ACC-PINV-.YYYY.-'
		pi.due_date = date.today()
		pi.posting_date = date.today()
		pi.base_rounded_total = 0
		tax = frappe.db.get_value("Purchase Taxes and Charges Template", {'company': self.company, 'is_default': 1},
								  'name')
		if tax:
			pi.taxes_and_charges = str(tax['taxes_and_charges'])
			pi.set_taxes()

		for i in self.items :
			if i.status not in ("Hold","Invoiced") and not i.invoiced:

				pi.append("items", {
				"item_code": i.item,
				"qty": 1,
				"rate": i.total,
				"amount": i.total,
				"cost_center":i.cost_center,
				"project":i.project,
					"refrenece":i.name
				})
				pi.base_rounded_total += i.total


		if not getattr(pi,'items',None):
			frappe.throw(_('All Items is Invoiced or holded'))
		pi.save()
		for i in self.items:
			if i.status not in ("Hold", "Invoiced") and not i.invoiced:
				i.invoiced = 1
				i.status = "Invoiced"
				i.purchase_invoice = pi.name
				i.purchase_invoice_item = [x.name for x in pi.items if x.refrenece == i.name][0]
		self.save()
		# frappe.msgprint()
		# for i in pi.items:
		# 	frappe.db.sql("""
		# 	update `tabFleet Supplier Invoice Items`
		# 	set invoiced = 1 , status = 'Invoiced' , purchase_invoice = '{}' , purchase_invoice_item = '{}'
		# 	where parent = '{}' and item = '{}' and status = 'Active' and invoiced <> 1
  # 			""".format(pi.name,i.name,self.name,i.item_code))
		msg = "<a href='#Form/Purchase Invoice/{0}'>{0}</a>".format(pi.name)
		frappe.msgprint(_("Done...\nPurchase Invoice {} Was Created".format(msg)),indicator='green')

	def get_cost_center(self,vehicle_type):
		pass
		'''Returns Cost Center for Item or Item Group'''
		# for_item = frappe.db.get_value('Vehicle Type',vehicle_type,'item') or ''
		# cost_center = ''
		# if for_item:
		# 	cost_center = frappe.db.get_value('Item Default',
		# 						   fieldname=['buying_cost_center'],
		# 						   filters={
		# 							   'parent': for_item,
		# 							   'company': self.company
		# 						   })
		# return (for_item,cost_center)

	def validate(self):
		self.validate_days()
		self.caculate_total_deduction()
	

	@frappe.whitelist()
	def validate_days (self):
		if self.from_date and self.to_date :
			if self.from_date > self.to_date :
				self.to_date = ''
				frappe.throw("""From Date is Greater than To Date Please set Valid Dates ! """)
			else :
				# self.day_count = self.get_dat_count()
				if not self.day_count:
					self.day_count = self.get_dat_count()

	def get_dat_count(self):
		from_date =  datetime.strptime(self.from_date, "%Y-%m-%d")
		to_date =  datetime.strptime(self.to_date, "%Y-%m-%d")
		return  (to_date-from_date).days +1

	def comaper_day_count_with_dates(self):
		if self.to_date and self.from_date and self.day_count :
			dif_date = self.get_dat_count()
			if dif_date < self.day_count :
				frappe.msgprint("""The deffirence Betwen From Date And To Date is: %s 
					But you try to add %s """ %(dif_date,  self.day_count))

	def get_deduction_type(self):
		for deduction in self.deductions :
			de_doc = frappe.get_doc("Vehicle Deduction" , deduction.vehicle_deduction)
			deduction.type = de_doc.type
			if de_doc.type == "By Amount" :
				deduction.deduction_amount = deduction.amout
			if de_doc.type == "By Day" :
				vechiel = frappe.get_doc("Vehicle" , deduction.vehicle)
				deduction.deduction_amount = (float(vechiel.vehicle_value)/30)*float(deduction.amout)
			if de_doc.type == "By Hour" :
				vechiel = frappe.get_doc("Vehicle" , deduction.vehicle)
				deduction.deduction_amount = ((float(vechiel.vehicle_value)/30)/float(vechiel.no_hours))*float(deduction.amout)
		self.caculate_total_deduction()
	def caculate_total_deduction(self) :
		for veh in self.items :
			total_deduct = 0 
			for deduct in self.deductions :
				if deduct.vehicle == veh.vehicle :
					total_deduct += float(deduct.deduction_amount or 0)
			veh.total_deductions = total_deduct
			veh.total =  float(veh.total_amount or 0) - float(veh.total_deductions or 0)


	def add_items(self , vh) :
		for t in self.items :
			count = 0 
			for d in self.items :
				
				if d.vehicle == vh :
					count = count + 1
			if count > 1 :
				self.remove(d)
				
				return "duplicated" 


	def remove_item(self):
		vichel = []
		for v in  self.items :
			vichel.append(v.vehicle)
		for d in self.deductions:
			if d.vehicle not in vichel :
				self.remove(d)
		for hold in self.hoding_items:
			if hold.vehicle not in vichel :
				self.remove(hold)

	def fetch_totals_section(self):
		self.remove_item()
		vehicle_qty      = 0
		total_amount     = 0
		total_deductions = 0
		grand_total      = 0
		self.caculate_total_deduction()
		for item in self.items :
			vehicle_qty +=1
			total_amount += float(item.total_amount or 0)
			total_deductions += float(item.total_deductions or  0)
			grand_total += float(item.total or  0)
		

		self.vehicle_qty = vehicle_qty
		self.total_amount = total_amount
		self.total_deductions = total_deductions
		self.grand_total = grand_total

	def add_hold(self,vehicle,driver,total_amount,deduction_amount,parent_idx,note):
		exist=0
		for hold in self.hoding_items:
			if hold.parent_idx==parent_idx:
				exist=1
		if exist==0:
			child=self.append("hoding_items")
			child.vehicle = vehicle
			child.driver = driver
			child.amout = total_amount
			child.deduction_amount = deduction_amount
			child.parent_idx=parent_idx
			child.note=note

	def update_status(self,idx):
		for item in self.items:
			if item.idx==idx:
				item.status="Active"
		for hold in self.hoding_items:
			if hold.parent_idx==idx:
				self.remove(hold)








				
			













	









@frappe.whitelist()
def get_viechle_driver(vh=None):
	if vh :
		drivers = frappe.db.sql(""" SELECT driver FROM `tabVehicle Drivers`
			WHERE parent ='%s' and status='Active' """%vh)
		if len(drivers) > 0 :
			return(drivers[0][0])
	else :
		return None