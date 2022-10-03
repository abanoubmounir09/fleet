# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import date
from frappe.model.document import Document

class CreateSalesOrder(Document):
	pass


@frappe.whitelist()
def make_sales_order(source_name):
	doc = frappe.new_doc("Sales Order")
	doc.is_fleet = 1
	doc.ignore_pricing_rule = 1
	doc.transaction_date = date.today()
	doc.delivery_date= date.today()
	return doc



@frappe.whitelist()
def make_fleet_sales_order(args):
	doc = frappe.new_doc("Sales Order")
	doc.is_fleet = 1
	doc.customer = args.get('customer')
	doc.transaction_date = date.today()
	doc.delivery_date=  args.get('date')
	for i in args.get('items'):
		row = doc.append('items',{})
		row.item_code = i.item_code
		row.delivery_date = doc.delivery_date
		row.qty = i.qty
		row.rate = i.price_after_discount
		row.discount_rate = i.discount_rate


	return doc