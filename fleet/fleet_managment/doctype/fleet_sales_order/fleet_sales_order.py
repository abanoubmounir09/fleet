# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import  json
from datetime import date
class FleetSalesOrder(Document):
	def ppp(self):
		return"P"
	def calculate_all_data(self):
		self.total_qty = 0
		self.grand_total =  0
		self.total_discount =  0
		self.net_total = 0

		for i in self.items :
			i.qty = i.qty if i.qty else 0
			i.price = i.price if i.price else 0
			i.price_afte_discount = i.price_afte_discount if i.price_afte_discount else 0
			i.total = i.total if i.total else 0
			i.discount_rate = i.discount_rate if i.discount_rate else 0
			total = 0
			i.discount_amount = 0
			if i.qty and i.price :

				total = float(i.qty or 0 ) * float(i.price or  0) 
				i.price_afte_discount = i.price
				if i.discount_rate > 0 :
					i.discount_amount = (float(i.price or 0) / 30 ) *i.discount_rate
					# price_aftre_discount =  i.price
					# i.price_afte_discount = price_aftre_discount

					total = float(i.qty or 0 ) * float(i.price or  0) -  i.discount_amount
			i.total = total
			self.total_qty += i.qty or 0
			self.grand_total += (i.price *  i.qty)  or 0
			self.total_discount += (i.discount_amount) or 0
			self.net_total += i.total or 0
		return True

			









@frappe.whitelist()
def make_fleet_sales_order(source):
	
	args = frappe.get_doc("Fleet Sales Order",source)
	doc = frappe.new_doc("Sales Order")
	doc.is_fleet = 1
	doc.ignore_pricing_rule = 1
	doc.customer = args.customer
	doc.transaction_date = date.today()
	doc.delivery_date =  args.date
	doc.price_list_currency = doc.currency
	doc.conversion_rate = 0
	doc.plc_conversion_rate = 0

	if args.items:
		for i in args.items:
			item_details = frappe.get_doc('Item',i.item_code)
			row = doc.append('items',{})
			row.item_code = i.item_code
			row.cost_center = i.cost_center
			row.uom = item_details.stock_uom
			row.stock_uom = item_details.stock_uom
			row.conversion_factor = 1
			row.item_name = item_details.item_name
			row.description = item_details.description
			row.delivery_date = args.date
			row.price_list_rate = 0
			# row.delivery_date = doc.delivery_date
			row.qty = i.qty
			row.rate = i.price
			# row.discount_rate = i.discount_rate

			row.discount_amount = i.discount_amount
			row.amount = i.total

	# doc.flags.ignore_validate = True
	doc.save()
	return doc

