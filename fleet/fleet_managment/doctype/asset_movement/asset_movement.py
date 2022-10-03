from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


def on_submit(self):
    if self.reference_doctype == "Custody request" and self.reference_name != None:
        request_custody = frappe.get_doc("Custody request", self.reference_name)
        if request_custody.reference_document_type == "Department":

            for d in self.assets:
                # frappe.throw(request_custody.reference_document_name)
                data = frappe.db.sql("UPDATE `tabAsset` SET  department = '%s' WHERE name ='%s'" % (
                request_custody.reference_document_name, d.asset))
                frappe.db.commit()
        if request_custody.reference_document_type == "Project":
            for d in self.assets:
                # frappe.throw(request_custody.reference_document_name)
                data = frappe.db.sql("UPDATE `tabAsset` SET  project = '%s' WHERE name ='%s'" % (
                request_custody.reference_document_name, d.asset))
                frappe.db.commit()

        final = frappe.db.sql(
            "UPDATE `tabCustody request` SET workflow_state = 'Completed' , docstatus = 1 WHERE name = '%s' " % self.reference_name)
        frappe.db.commit()
    if self.reference_doctype == "Assets Return" and self.reference_name != None:
        asset_return = frappe.get_doc("Assets Return", self.reference_name)
        if asset_return.reference_document_type == "Department":

            for d in self.assets:
                # frappe.throw(request_custody.reference_document_name)
                data = frappe.db.sql(
                    "UPDATE `tabAsset` SET  department = '',custodian = '' , is_driver = 0 ,driver = '' WHERE name ='%s'" % (d.asset))
                frappe.db.commit()
        if asset_return.reference_document_type == "Project":
            for d in self.assets:
                # frappe.throw(request_custody.reference_document_name)
                data = frappe.db.sql("UPDATE `tabAsset` SET  project = '' WHERE name ='%s'" % (d.asset))
                frappe.db.commit()
        if asset_return.reference_document_type == "Employee":
            for d in self.assets:
                frappe.throw(d.asset)
                data = frappe.db.sql("UPDATE `tabAsset` SET  custodian = '' , is_driver = 0 ,driver = '' WHERE name ='%s'" % (d.asset))
                frappe.db.commit()

        final = frappe.db.sql(
            "UPDATE `tabCustody request` SET  workflow_state = 'Completed' ,docstatus = 1 WHERE name = '%s' " % self.reference_name)
        frappe.db.commit()
    self.set_latest_location_in_asset()


def set_latest_location_in_asset(self):



    for d in self.assets:
        current_location, current_employee, current_driver = '', '', ''
        is_driver = 0
        cond = "1=1"
        args = {
            'asset': d.asset,
            'company': self.company
        }

        # latest entry corresponds to current document's location, employee when transaction date > previous dates
        # In case of cancellation it corresponds to previous latest document's location, employee
        latest_movement_entry = frappe.db.sql(
            """
            SELECT asm_item.target_location, asm_item.to_employee , asm_item.to_driver , asm_item.to_is_driver
            FROM `tabAsset Movement Item` asm_item, `tabAsset Movement` asm
            WHERE 
                asm_item.parent=asm.name and
                asm_item.asset=%(asset)s and
                asm.company=%(company)s and 
                asm.docstatus=1 and {0}
            ORDER BY
                asm.transaction_date desc limit 1
            """.format(cond), args)
        if latest_movement_entry:
            current_location = latest_movement_entry[0][0]
            current_employee = latest_movement_entry[0][1]
            current_driver = latest_movement_entry[0][2]
            is_driver = latest_movement_entry[0][3]

        frappe.db.set_value('Asset', d.asset, 'location', current_location)
        frappe.db.set_value('Asset', d.asset, 'custodian', current_employee)
        frappe.db.set_value('Asset', d.asset, 'driver', current_driver)
        frappe.db.set_value('Asset', d.asset, 'is_driver', is_driver)


def validate_location(self):
    for d in self.assets:
        if self.purpose in ['Transfer', 'Issue']:
            if not d.source_location:
                d.source_location = frappe.db.get_value("Asset", d.asset, "location")

            if not d.source_location:
                frappe.throw(_("Source Location is required for the Asset {0}").format(d.asset))

            if d.source_location:
                current_location = frappe.db.get_value("Asset", d.asset, "location")

                if current_location != d.source_location:
                    frappe.throw(_("Asset {0} does not belongs to the location {1}").
                                 format(d.asset, d.source_location))

        if self.purpose == 'Issue':
            if d.target_location:
                frappe.throw(_("Issuing cannot be done to a location. \
					Please enter employee who has issued Asset {0}").format(d.asset),
                             title="Incorrect Movement Purpose")
            if not d.to_employee:
                frappe.throw(_("Employee is required while issuing Asset {0}").format(d.asset))

        if self.purpose == 'Transfer':
            if d.to_employee:
                frappe.throw(_("Transferring cannot be done to an Employee. \
					Please enter location where Asset {0} has to be transferred").format(
                    d.asset), title="Incorrect Movement Purpose")
            if not d.target_location:
                frappe.throw(_("Target Location is required while transferring Asset {0}").format(d.asset))
            if d.source_location == d.target_location:
                frappe.throw(_("Source and Target Location cannot be same"))


        if self.purpose == 'Receipt':
            # only when asset is bought and first entry is made
            if not d.source_location and not (d.target_location or d.to_employee):
                frappe.throw(_("Target Location or To Employee is required while receiving Asset {0}").format(d.asset))
            elif d.source_location:
                # when asset is received from an employee
                if d.target_location and not d.from_employee:
                    frappe.throw(
                        _("From employee is required while receiving Asset {0} to a target location").format(d.asset))
                if d.from_employee and not d.target_location:
                    frappe.throw(
                        _("Target Location is required while receiving Asset {0} from an employee").format(d.asset))
                if d.to_employee and d.target_location:
                    frappe.throw(_("Asset {0} cannot be received at a location and \
						given to employee in a single movement").format(d.asset))

        validate_from_driver(d)
        validate_to_driver(d)


def validate_employee(self):
    for d in self.assets:
        if d.from_employee:
            current_custodian = frappe.db.get_value("Asset", d.asset, "custodian")

            if current_custodian != d.from_employee:
                frappe.throw(_("Asset {0} does not belongs to the custodian {1}").
                             format(d.asset, d.from_employee))

        if d.to_employee and frappe.db.get_value("Employee", d.to_employee, "company") != self.company:
            frappe.throw(_("Employee {0} does not belongs to the company {1}").
                         format(d.to_employee, self.company))
        if d.from__driver:
            current_driver = frappe.db.get_value("Asset", d.asset, "driver")

            if current_driver != d.from__driver:
                frappe.throw(_("Asset {0} does not belongs to the Driver {1}").
                             format(d.asset, d.from__driver))

        if d.to_driver and frappe.db.get_value("Driver", d.to_driver, "company") != self.company:
            frappe.throw(_("Driver {0} does not belongs to the company {1}").
                         format(d.to_driver, self.company))


def validate_from_driver(row):
    if row.from_employee and row.from_is_driver and not row.from__driver:
        frappe.throw(_("Please Set From Driver In Row {} ".format(row.idx)))

def validate_to_driver(row):
    if row.to_employee and row.to_is_driver and not row.to_driver:
        frappe.throw(_("Please Set To Driver In Row {} ".format(row.idx)))

def validate(self,fun=''):
    validate_location(self)


