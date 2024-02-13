# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate, today, nowdate
import datetime

import inspect

class VehicleCard(Document):
    def validate(self):       
        # frappe.msgprint(str(self.odometer_reading))
        ...
        # if self.last_tire_inspection and float(self.last_tire_inspection or 0) > float(self.odometer_reading or 0):
        #     self.odometer_reading = self.last_tire_inspection
        #     print('\n\n\n-self.last_tire_inspection->',self.last_tire_inspection,'\n\n\n-->')
        # if self.last_tire_change and float(self.last_tire_change or 0) > float(self.odometer_reading or 0):
        #     self.odometer_reading = self.last_tire_change
        #     print('\n\n\n-self.last_tire_change->',self.last_tire_change,'\n\n\n-->')
        # if self.last_tank and float(self.last_tank or 0) > float(self.odometer_reading or 0):
        #     self.odometer_reading = self.last_tank
        #     print('\n\n\n-self.last_tank->',self.last_tank,'\n\n\n-->')
        # for m in self.maintainance:
        #     if float(m.odometer_reading or 0) > float(self.odometer_reading or 0):
        #         self.odometer_reading = m.odometer_reading
        #         print('\n\n\n-for 1->',m.odometer_reading,'\n\n\n-->')
        # if float(self.las_reading or 0) > float(self.odometer_reading or 0):
        #     self.odometer_reading = self.las_reading
        #     print('\n\n\n-self.odometer_reading->',self.odometer_reading,'\n\n\n-->')
        # if self.odometer_reading:
        #     frappe.db.sql(
        #         "update `tabTire Log` set current_reading='{}' where vehicle='{}'".format(self.odometer_reading,
        #                                                                                   self.vehicle))
        #     frappe.db.commit()
        #     frappe.db.sql(
        #         "update `tabTank log` set current_reading='{}' where vehicle='{}'".format(self.odometer_reading,
        #                                                                                   self.vehicle))
        #     frappe.db.commit()
        #     frappe.db.sql(
        #         "update `tabVehicle Log` set odometer='{}' where license_plate='{}'".format(self.odometer_reading,
        #                                                                                     self.vehicle))
        #     frappe.db.commit()

    @frappe.whitelist()
    def get_reading(self):
        tire_log = frappe.db.get_list('Tire Log', filters={'vehicle': ['=', self.vehicle]},
                                      fields=['last_tier_inspection_km', 'last_tier_change_km'])
        tank_log = frappe.db.get_list('Tank log', filters={'vehicle': ['=', self.vehicle]}, fields=['tank_reading'])
        vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
        # vehicle_type=vehicle_doc.vehicle_type
        if vehicle_doc.get("vehicle_type"):
            type_doc = frappe.get_doc("Vehicle Type", vehicle_doc.get("vehicle_type"))
            if type_doc:
                for maintance in type_doc.maintainance:
                    row = self.append("maintainance", {})
                    row.maintainance = maintance.maintainance
                    vehicle_log = frappe.db.sql(
                        """select name from `tabVehicle Log` where license_plate='%s'""" % self.vehicle, as_dict=1)
                    # frappe.db.get_list('Vehicle Log', filters={'license_plate': ['=', self.vehicle]},fields=['name'])
                    if vehicle_log:
                        # frappe.msgprint(str(vehicle_log))
                        maintinance_km = frappe.db.sql("""select odometer_reading from `tabVehicle Service`
						 where type='{}' and parent='{}' order by odometer_reading DESC""".format(
                            maintance.maintainance, vehicle_log[0].name), as_dict=1)
                        if maintinance_km:
                            row.odometer_reading = maintinance_km[0].odometer_reading

        if len(tire_log) > 0:
            self.last_tire_inspection = tire_log[0].last_tier_inspection_km
            self.last_tire_change = tire_log[0].last_tier_change_km
        if len(tank_log):
            self.last_tank = tank_log[0].tank_reading
        return True

    def update_odo_reading(self):
        frappe.db.sql(
            """update `tabTank log` set current_reading='{}' where vehicle='{}'""".format(self.odometer_reading,
                                                                                          self.vehicle))
        frappe.db.commit()
        # frappe.db.sql(
        #     """update `tabVehicle Log` set odometer='{}' where license_plate='{}'""".format(self.odometer_reading,
        #                                                                                     self.vehicle))
        # frappe.db.commit()
        frappe.db.sql(
            """update `tabTire Log` set current_reading='{}' where vehicle='{}'""".format(self.odometer_reading,
                                                                                          self.vehicle))
        frappe.db.commit()

    # tank_log=frappe.db.sql("""select name from `tabTank log` where vehicle='%s'"""%self.vehicle,as_dict=1)
    # vehicle_log = frappe.db.sql("""select name from `tabVehicle Log` where license_plate='%s'""" % self.vehicle, as_dict=1)
    # tire_log = frappe.db.sql("""select name from `tabTire Log` where vehicle='%s'""" % self.vehicle, as_dict=1)
    #
    # if tank_log:
    # 	doc=frappe.get_doc("Tank log",tank_log[0].name)
    # 	doc.current_reading=self.odometer_reading
    # 	doc.save()
    # if vehicle_log:
    # 	doc=frappe.get_doc("Vehicle Log",vehicle_log[0].name)
    # 	doc.odometer=self.odometer_reading
    # 	doc.save()
    # if tire_log:
    # 	doc=frappe.get_doc("Tire Log",tire_log[0].name)
    # 	doc.current_reading=self.odometer_reading
    # 	doc.save()
    @frappe.whitelist()
    def add_tank_log(self, current_reading, no_litre, price, vehicle,date):
        tank_log = frappe.db.sql("""select name from `tabTank log` where vehicle='%s'""" % vehicle, as_dict=1)
        if current_reading > self.odometer_reading:
            self.odometer_reading = current_reading
        self.last_tank = self.odometer_reading
        self.save()
        if tank_log:
            doc = frappe.get_doc("Tank log", tank_log[0].name)
            doc.no_litre = no_litre
            doc.price = price
            doc.current_reading = self.odometer_reading
            doc.date = date
            doc.save()
        else:
            doc = frappe.new_doc("Tank log")
            doc.vehicle = vehicle
            doc.no_litre = no_litre
            doc.price = price
            doc.current_reading = self.odometer_reading
            doc.date = date
            doc.save()
    @frappe.whitelist()
    def add_tire_change(self, current_reading, required_date, change_date, status,valid_from=None,valid_to=None,description=None,*args, **kwargs):
        tire_log = frappe.db.sql("""select name from `tabTire Log` where vehicle='%s'""" % self.vehicle, as_dict=1)
        if current_reading > self.odometer_reading:
            self.odometer_reading = current_reading
        self.last_tire_change = self.odometer_reading
        self.save()
        if tire_log:
            doc = frappe.get_doc("Tire Log", tire_log[0].name)
            doc.valid_from = valid_from
            doc.valid_to = valid_to
            doc.description = description
            # doc.add_ch_r_km=self.odometer_reading
            row = doc.append("tire_change", {})
            row.counter_reading = current_reading  # self.odometer_reading
            row.date = change_date
            row.required_date = required_date
            row.status = status
            row.valid_from = valid_from
            row.valid_to = valid_to
            row.description = description
            doc.save()
        else:
            doc = frappe.new_doc("Tire Log")
            doc.vehicle = self.vehicle
            doc.last_tier_change_date = change_date
            doc.valid_from = valid_from
            doc.valid_to = valid_to
            doc.description = description
            row = doc.append("tire_change", {})
            row.counter_reading = current_reading  # self.odometer_reading
            row.date = change_date
            row.required_date = required_date
            row.status = status
            doc.save()
    @frappe.whitelist()
    def add_tire_inspection(self, current_reading, required_date, change_date, status,valid_from=None,valid_to=None,description=None, *args, **kwargs):
        tire_log = frappe.db.sql("""select name from `tabTire Log` where vehicle='%s'""" % self.vehicle, as_dict=1)
        if current_reading > self.odometer_reading or 0:
            self.odometer_reading = current_reading
        self.last_tire_change = self.odometer_reading
        self.save()
        if tire_log:
            doc = frappe.get_doc("Tire Log", tire_log[0].name)
            # doc.add_ch_r_km=self.odometer_reading
            doc.last_tier_inspection_date = change_date
            doc.valid_from = valid_from
            doc.valid_to = valid_to
            doc.description = description
            row = doc.append("tire_inspection_log", {})
            row.counter_reading = current_reading  # self.odometer_reading
            row.date = change_date
            row.required_date = required_date
            row.status = status
            doc.save()
        else:
            doc = frappe.new_doc("Tire Log")
            doc.vehicle = self.vehicle
            doc.valid_from = valid_from
            doc.valid_to = valid_to
            doc.description = description
            row = doc.append("tire_inspection_log", {})
            row.counter_reading = current_reading  # self.odometer_reading
            row.date = change_date
            row.required_date = required_date
            row.status = status
            row.valid_from = valid_from
            row.valid_to = valid_to
            row.description = description
            doc.save()

    def update_vehicle_status(self):
        if self.vehicle and self.status and self.notes:
            doc = frappe.get_doc("Vehicle", self.vehicle)
            doc.vehicle_status = self.status
            doc.save()
            status_log = frappe.db.sql("select name from `tabVehicle Satus Log` where vehicle='%s'" % self.vehicle,
                                       as_dict=1)
            if status_log:
                update_status_log = frappe.get_doc("Vehicle Satus Log", status_log[0].name)
                row = update_status_log.append("status_log", {})
                row.status = self.status
                row.note = self.notes
                row.date = getdate(nowdate())
                update_status_log.save()
            else:
                doc = frappe.new_doc("Vehicle Satus Log")
                doc.vehicle = self.vehicle
                row = doc.append("status_log", {})
                row.status = self.status
                row.note = self.notes
                row.date = getdate(nowdate())
                doc.save()

            frappe.msgprint("Status updated successfully")
        return True

    def update_gps_status(self):
        vehicle_name = frappe.db.sql("""select name from tabVehicle where name='%s'""" % self.vehicle, as_dict=1)
        if self.vehicle and vehicle_name:
            doc = frappe.get_doc("Vehicle", self.vehicle)
            doc.gps_status = self.gps_status
            doc.url = self.url
            doc.comment = self.comment
            doc.date = self.date
            doc.save()
            status_log = frappe.db.sql("select name from `tabGPS Logs` where vehicle='%s'" % self.vehicle, as_dict=1)
            if status_log:
                update_status_log = frappe.get_doc("GPS Logs", status_log[0].name)
                row = update_status_log.append("status_log", {})
                row.status = self.gps_status
                row.note = self.comment
                row.date = self.date or getdate(nowdate())
                update_status_log.save()
            else:
                doc = frappe.new_doc("GPS Logs")
                doc.vehicle = self.vehicle
                row = doc.append("status_log", {})
                row.status = self.gps_status
                row.note = self.comment
                row.date = self.date or getdate(nowdate())
                doc.save()

            frappe.msgprint("Status updated successfully")
            return True
        return False
    @frappe.whitelist()
    def get_maintenance(self, type):
        maintenance = frappe.db.sql("""select maintainance from `tabMaintainance Child` where parent='%s'""" % type,
                                    as_dict=1)
        return maintenance
    
    @frappe.whitelist()
    def add_maintenance(self,vehicle,reading,date,maintenance_to_date,maintenance,expense,price,description):
        vehicle_log=frappe.new_doc("Vehicle Log")
        vehicle_log.license_plate=vehicle
        #vehicle_log.employee=driver
        vehicle_log.odometer=reading
        #vehicle_log.last_odometer=self.odometer_reading
        vehicle_log.date=date
        vehicle_log.maintenance_to_date=maintenance_to_date
        row=vehicle_log.append("service_detail",{})
        row.type=maintenance
        row.odometer=reading
        row.expense_amount=expense
        row.price=price
        row.description=description
        vehicle_log.flags.ignore_mandatory = True
        vehicle_log.save()
        vehicle_log.docstatus=1
        vehicle_log.save()
    @frappe.whitelist()
    def get_vehicle_driver(self):
        d_list=[]
        vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
        if vehicle_doc:
            if vehicle_doc.get("drivers"):
                for d in vehicle_doc.drivers:
                    d_list.append(d.driver)
        # frappe.msgprint(str(d_list))
        return d_list

# def validae_maintenance(self):
# 	for maint in self.maintainance:

################### Notification ###################


def check_notification(*args, **kwargs):
    cards = frappe.get_list("Vehicle Card",
                            fields=["vehicle", "name", "odometer_reading", "last_tire_inspection", "last_tire_change",
                                    "creation", "vehicle_type"])
    selling_setting = frappe.get_single("Selling Settings")

    # notification_settings = frappe.get_single("Fleet Notification Settings")
    # frappe.msgprint(str(notification_settings.tire_inspection))
    for card in cards:
        vehicle = frappe.get_doc("Vehicle", card.vehicle)
        if not card.vehicle_type:
            return
        vehicle_type = frappe.get_doc("Vehicle Type", card.vehicle_type)
        if vehicle.vehicle_status == "Active":
            if vehicle_type.inspect_after_km + card.last_tire_inspection >= card.odometer_reading - vehicle_type.notification_afterkm:
                sent_notification(subject="tire for vehicle '%s' must be inspected" % card.vehicle,
                                  document_type="Vehicle Card", document_name=card.name)
            if vehicle_type.change_afterkm + card.last_tire_change >= card.odometer_reading - vehicle_type.notification_after:
                sent_notification(subject="tire for vehicle '%s' must be changed" % card.vehicle,
                                  document_type="Vehicle Card", document_name=card.name)
            try:
                diff = str(getdate(today()) - getdate(card.creation))
                period = diff.split(' ')[0]
                if float(period) >= float(vehicle_type.period) * 365:
                    sent_notification(subject="Vehicle  '{}' exceed '{}'".format(card.vehicle, vehicle_type.period),
                                      document_type="Vehicle Card", document_name=card.name)
            except:
                pass

            card_for_mainitinance = frappe.get_doc("Vehicle Card", card.name)
            if vehicle_type.maintainance:
                for veh_maint in card_for_mainitinance.maintainance:
                    for type_maint in vehicle_type.maintainance:
                        if veh_maint.maintainance == type_maint.maintainance:
                            if type_maint.period + veh_maint.odometer_reading >= card.odometer_reading - type_maint.notification_before_km:
                                sent_notification(subject="Vehicle  '{}' need to '{}' ".format(card.vehicle,
                                                                                               veh_maint.maintainance),
                                                  document_type="Vehicle Card", document_name=card.name)
                            # inactive if not do maintinance
                            if (float(card.odometer_reading) or 0) >= (float(type_maint.period) or 0) + (
                                    float(veh_maint.odometer_reading) or 0) + (int(selling_setting.stop_period) or 0):
                                # frappe.msgprint("inactive from maintainance" + card.name)
                                # vehicle = frappe.get_doc("Vehicle", card.vehicle)
                                # vehicle.vehicle_status = "Inactive"
                                # vehicle.save()
                                # frappe.throw("maintenance")
                                frappe.db.sql(
                                    """ update tabVehicle set vehicle_status="Suspended" where name='%s'""" % card.vehicle)
                                frappe.db.commit()

            if vehicle.licences:
                for lic in vehicle.licences:
                    if lic.active == 1:
                        diff = str(getdate(today()) - getdate(lic.end_date))
                        # frappe.msgprint(diff)
                        if diff:
                            try:
                                diff = diff.split(' ')[0]
                                diff = int(diff)
                                if 0 <= diff <= 30:
                                    sent_notification(
                                        subject="'{}' ترخيص السيارة هينتهي في".format(vehicle.name),
                                        # subject=" vehicle '{}' licence  is about to end".format(vehicle.name),
                                        document_type="Vehicle Card", document_name=card.name)
                                if diff > int(selling_setting.stop_period):
                                    # frappe.throw("licence")
                                    # frappe.msgprint("inactive from licence")
                                    # vehicle.vehicle_status="Inactive"
                                    # vehicle.save()
                                    frappe.db.sql(
                                        """ update tabVehicle set vehicle_status="Suspended" where name='%s'""" % card.vehicle)
                                    frappe.db.commit()
                            except:
                                pass
            # inactive if not inspect tire
            # if vehicle_type.inspect_after_km or 0 + card.last_tire_inspection or 0 >= card.odometer_reading + int(selling_setting.stop_period) or 0:
            # frappe.msgprint(str(card.odometer_reading))
            # frappe.msgprint(str(selling_setting.stop_period))
            # frappe.msgprint(str(card.last_tire_inspection))
            # frappe.msgprint(str(vehicle_type.inspect_after_km))
            if float(card.odometer_reading) > float(selling_setting.stop_period) + float(
                    card.last_tire_inspection) + float(vehicle_type.inspect_after_km):
                # frappe.msgprint("inactive from inspect")
                # vehicle.vehicle_status = "Inactive"
                # vehicle.save()
                # frappe.throw("last tire insp")
                frappe.db.sql(""" update tabVehicle set vehicle_status="Suspended" where name='%s'""" % card.vehicle)
                frappe.db.commit()

            # inactive if not change tire
            # 13 > 200000 + 0 +12
            if float(card.odometer_reading) > float(vehicle_type.change_afterkm) + float(card.last_tire_change) + float(
                    selling_setting.stop_period):
                # frappe.msgprint("inactive from change")
                # vehicle.vehicle_status = "Inactive"
                # vehicle.save()
                # frappe.throw("last tire change")
                frappe.db.sql(""" update tabVehicle set vehicle_status="Suspended" where name='%s'""" % card.vehicle)
                frappe.db.commit()


def sent_notification(role="Fleet Manager", subject=None, document_type=None, document_name=None):
    user_lst = frappe.db.sql("""select distinct t1.name
									from `tabUser` t1, `tabHas Role` t2 where t2.role='%s'
									and t2.parent=t1.name and t1.name !='Administrator'
									and t1.name != 'Guest' and t1.docstatus !=2""" % role, as_dict=1)
    try:
        for user in user_lst:
            doc = frappe.new_doc('Notification Log')
            doc.document_type = document_type
            doc.document_name = document_name
            doc.for_user = user.name
            doc.subject = subject
            doc.insert(ignore_permissions=True)
    except:
        pass
