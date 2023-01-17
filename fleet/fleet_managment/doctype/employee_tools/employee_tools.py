# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class EmployeeTools(Document):
	def save(self):
		self.set('fitems', [])
		super(EmployeeTools, self).save()
	def autoname(self):

		self.name = "{}".format(self.employee_name)
		if self.is_driver :
			self.name = "{}-{}".format(self.employee_name,self.driver_name)

	def set_data (self):
		self.set('fitems',[])
		agreement = self.customer_agreement or ''
		for i in getattr(self,'items',[]):
			customer_agrement = getattr(i,'customer_agrement',None) or ''
			if  agreement == customer_agrement and i.status == self.item_status :
				# row = {}
				# row.update(i.__dict__)
				row = frappe._dict(i.__dict__)
				row.reference = i.name
				row.doctype = 'Employee Tools filtered Item'
				row.parent_field = 'fitems'
				self.append('fitems', row)


	def deliver_to_customer(self,selected):
		if selected and self.customer_agreement:
			self.save()
			agreement = frappe.get_doc('Customer Agrement', self.customer_agreement)

			stock_entry = frappe.new_doc("Stock Entry")

			stock_entry.stock_entry_type = "Material Issue"
			stock_entry.from_warehouse = agreement.warehouse
			stock_entry.from_employee = self.employee
			stock_entry.from_customer_agreement = agreement.name
			for item in getattr(self,'items',[]) :
				if item.name in selected : #and not item.delivered and item.delivered_qty < item.qty:
					se_child = stock_entry.append('items')
					se_child.item_code = item.item_code
					se_child.item_name = item.item_name
					se_child.qty = item.qty
					se_child.s_warehouse = agreement.warehouse
					# in stock uom

					se_child.expense_account = agreement.customer_installment_account
					# se_child.conversion_factor = 1
					# se_child.uom = item.stock_uom
					# se_child.stock_uom = item.stock_uom
			if len(getattr(stock_entry,'items',[])) == 0 :
				frappe.throw(_('All items have been delivered before'))
			stock_entry.insert()
			l = """ <b><a href="#Form/{0}/{1}">{1}</a></b>""".format(stock_entry.doctype, stock_entry.name)
			msg = _("A {} {} is Created for Company {}").format(stock_entry.doctype, l, stock_entry.company)

			frappe.msgprint(msg)

	# names = tuple(selected)
			# sql = """
			# Update `tabEmployee Tools Item` set  stock_entry = '{}' , delivered = 1
			# where delivered <> 1 and stock_entry is null and name in {}
			# """.format(stock_entry.name,names)
			# frappe.db.sql(sql)
			# frappe.db.commit()





