# Copyright (c) 2023, DTS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from frappe import _

DOMAINS = frappe.get_active_domains()

class MaintenanceRequest(Document):
	def after_insert(self):
		alert_vechile_manager(self)

	def on_submit(self):
		sql = f"""
			UPDATE `tabMaintenance Request` set status = 'Agree' where name = '{self.name}'
		"""
		frappe.db.sql(sql)
		frappe.db.commit()
		self.reload()
		self.create_vehicle_log()
		send_alert_vechile_driver(self)

	def create_vehicle_log(self):
		vehicle_log=frappe.new_doc("Vehicle Log")
		vehicle_log.license_plate = self.vehicle
		vehicle_log.maintenance_request = self.name
		vehicle_log.status = self.status
		vehicle_log.office = self.office
		vehicle_log.area   = self.area
		vehicle_log.applicant_name   = self.applicant_name
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


@frappe.whitelist()
def send_alert_vechile_driver(doc):
	# doc= json.loads(doc)
	owner_name = doc.get("applicant_name")
	contact_date = doc.get("date")
	notif_doc = frappe.new_doc('Notification Log')
	notif_doc.subject = f"{owner_name} Has Maintenance Request at {contact_date} status become agree"
	notif_doc.email_content = f"{owner_name} Has Maintenance Request at {contact_date} status become agree"
	notif_doc.for_user = owner_name
	notif_doc.type = "Mention"
	notif_doc.document_type = doc.get("doctype")
	notif_doc.document_name = doc.get("name")
	notif_doc.from_user = frappe.session.user
	notif_doc.insert(ignore_permissions=True)




@frappe.whitelist()
def alert_vechile_manager(doc,role=None,*args,**kwargs):
	manager_role= frappe.db.get_single_value('Fleet Vehicle Role', 'manager_role')
	if not manager_role:
		frappe.throw(_("Please Add Manager Role in"))
	get_all_manger=get_user_by_role(manager_role)
	kwargs={
		"doc":doc,
		"get_all_manger":get_all_manger
	}
	frappe.enqueue(
	method=send_alert_vechile_manager,
	queue="default", 
	timeout=500, 
	is_async=False, # if this is True, method is run in worker
	now=True, # if this is True, method is run directly (not in a worker) 
	at_front=True, # put the job at the front of the queue
	**kwargs,
)

def send_alert_vechile_manager(**kwargs):
	for row in kwargs.get("get_all_manger"):
		owner_name = row.get("parent")
		contact_date = kwargs.get('doc').date
		notif_doc = frappe.new_doc('Notification Log')
		notif_doc.subject = f"{owner_name} Has Maintenance Request at {contact_date}"
		notif_doc.email_content = f"{owner_name} Has Maintenance Request at {contact_date}"
		notif_doc.for_user = owner_name
		notif_doc.type = "Mention"
		notif_doc.document_type = kwargs.get('doc').doctype
		notif_doc.document_name = kwargs.get('doc').name
		notif_doc.from_user = frappe.session.user
		notif_doc.insert(ignore_permissions=True)
		
def get_user_by_role(role):
	get_all_manger = f"""
	SELECT DISTINCT(has_role.parent)
	FROM
		`tabHas Role` has_role
			LEFT JOIN `tabUser` user
				ON has_role.parent = user.name
	WHERE
		has_role.parenttype = 'User' AND has_role.role='{role}'
	"""
	return frappe.db.sql(get_all_manger,as_dict=1)

@frappe.whitelist()
def cron_job_licence_end_date():
	if "Fleet" in DOMAINS:
		sql="""
		select name,licence_end_date as end_date,'vehichle licence' as doctype
		FROM `tabvehichle licence`
		WHERE (DATE_SUB(licence_end_date , INTERVAL 2 MONTH)=curdate())
		"""
		data = frappe.db.sql(sql,as_dict=1)
		if data:
			alert_all_manger('System Manager',data)

@frappe.whitelist()
def cron_vehicle_contract_end_date():
	if "Fleet" in DOMAINS:
		sql="""
		select name,end_date,'Vehicle Contract' as doctype
		FROM `tabVehicle Contract`
		WHERE (DATE_SUB(end_date , INTERVAL 2 MONTH)=curdate())
		"""
		data = frappe.db.sql(sql,as_dict=1)
		if data:
			alert_all_manger('System Manager',data)


def alert_all_manger(role,data):
	get_all_manger = get_user_by_role(role)
	if (data and get_all_manger):
		get_all_manger = [x['parent'] for x in get_all_manger]
		kwargs={
			"get_all_manger":get_all_manger,
			"data":data,
		}
		frappe.enqueue(
		method=send_alert_all_manager,
		queue="default", 
		timeout=500, 
		is_async=False, #! set true after end if this is True, method is run in worker
		now=True, #! set false after end if this is True, method is run directly (not in a worker) 
		at_front=True, # put the job at the front of the queue
		**kwargs,
	)

def send_alert_all_manager(**kwargs):
	for row in kwargs.get("data"):
		for admin in kwargs.get("get_all_manger"):
			owner_name = admin
			notif_doc = frappe.new_doc('Notification Log')
			subject=''
			mail_msg=''
			if row.doctype=="Maintenance Request":
				subject =_(f"Maintenance Request With name {row.get('name')} will be end license at {row.get('end_date')}")
				mail_msg =  _(f"Maintenance Request With name {row.get('name')} will be end license at {row.get('end_date')}")
			elif row.doctype=="Vehicle Contract":
				subject = _(f"Vehicle Contract With name {row.get('name')} will be end after 2 months from now {row.get('end_date')}")
				mail_msg = _( f"Vehicle Contract With name {row.get('name')} will be end after 2 months from now {row.get('end_date')}")
			elif row.doctype=="Tire Log" and row.child=="Tire":
				subject = _(f"Vehicle  With name {row.get('vehicle')} will need To Change Tire Name {row.get('name')}")
				mail_msg =  _(f"Vehicle  With name {row.get('vehicle')} will need To Change Tire Name {row.get('name')}")
			elif row.doctype=="Tire Log" and row.child=="Inspection":
				subject = _(f"Vehicle  With name {row.get('vehicle')} will need To Change Tire Inspection Name {row.get('name')}")
				mail_msg =  _(f"Vehicle  With name {row.get('vehicle')} will need To Change Inspection Tire Name {row.get('name')}")
			notif_doc.subject = subject
			notif_doc.email_content =mail_msg
			notif_doc.for_user = owner_name
			notif_doc.type = "Mention"
			notif_doc.document_type = row.doctype
			notif_doc.document_name = row.name
			notif_doc.from_user = frappe.session.user or ""
			notif_doc.insert(ignore_permissions=True)


@frappe.whitelist()
def cron_tire_log_alert():
	if "Fleet" in DOMAINS:
		sql="""
		select tire.vehicle,tire.name,'Tire Log' as doctype,
		'Tire' as child
		FROM `tabTire Log` tire
		INNER JOIN `tabTier Change Child` tire_child
		ON tire_child.parent = tire.name
		WHERE (DATE_SUB(tire_child.valid_to , INTERVAL 2 MONTH)=curdate())
		"""
		data = frappe.db.sql(sql,as_dict=1)
		if data:
			alert_all_manger('System Manager',data)

@frappe.whitelist()
def cron_inspection_log_alert():
	if "Fleet" in DOMAINS:
		sql="""
		select tire.vehicle,tire.name,tire_child.counter_reading,'Tire Log' as doctype ,
		'Inspection' as child
		FROM `tabTire Log` tire
		INNER JOIN `tabTire Inspection Child` tire_child
		ON tire_child.parent = tire.name
		WHERE (DATE_SUB(tire_child.valid_to , INTERVAL 2 MONTH)=curdate())
		"""
		data = frappe.db.sql(sql,as_dict=1)
		if data:
			alert_all_manger('System Manager',data)
