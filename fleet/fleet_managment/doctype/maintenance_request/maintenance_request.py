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
	notif_doc.subject = _("{0} Has Maintenance Request at {1} status become agree").format(owner_name,contact_date)
	notif_doc.email_content = _("{0} Has Maintenance Request at {1} status become agree").format(owner_name,contact_date)
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
	# print('\n\n\n===>',get_all_manger,'\n\n')
	kwargs={
		"doc":doc,
		"get_all_manger":get_all_manger
	}
	frappe.enqueue(
	method=send_alert_vechile_manager,
	queue="default", 
	timeout=500, 
	is_async=True, # if this is True, method is run in worker
	now=False, # if this is True, method is run directly (not in a worker) 
	at_front=False, # put the job at the front of the queue
	**kwargs,
)

def send_alert_vechile_manager(**kwargs):
	for row in kwargs.get("get_all_manger"):
		to_user = row.get("email")
		contact_date = kwargs.get('doc').date
		notif_doc = frappe.new_doc('Notification Log')
		notif_doc.type = "Mention" #Alert
		notif_doc.document_type = kwargs.get('doc').doctype
		notif_doc.document_name = kwargs.get('doc').name
		notif_doc.subject = _("{0} Has Maintenance Request at {1}").format(frappe.session.user, contact_date)#_(f"{owner_name} Has Maintenance Request at {contact_date}")
		notif_doc.email_content = _("{0} Has Maintenance Request at {1}").format(frappe.session.user, contact_date)
		notif_doc.from_user = frappe.session.user
		notif_doc.for_user = to_user #frappe.session.user
		notif_doc.insert(ignore_permissions=True)
		
def get_user_by_role(role):
	get_all_manger = f"""
	SELECT DISTINCT(has_role.parent),user.email
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
		is_async=True, #! set true after end if this is True, method is run in worker
		now=False, #! set false after end if this is True, method is run directly (not in a worker) 
		at_front=False, # put the job at the front of the queue
		**kwargs,
	)

def send_alert_all_manager(**kwargs):
	print('data==>\n\n\n',kwargs.get("data"),'\n\n')
	for row in kwargs.get("data"):
		for admin in kwargs.get("get_all_manger"):
			if admin.parent != 'Administrator':
				owner_name = admin
				notif_doc = frappe.new_doc('Notification Log')
				subject=''
				mail_msg=''
				if row.doctype=="Maintenance Request":
					subject =_("Maintenance Request With name {0} will be end license at {1}").format(row.get('name'), row.get('end_date'))
					mail_msg =  _("Maintenance Request With name {0} will be end license at {1}").format(row.get('name'),row.get('end_date'))
				elif row.doctype=="Vehicle Contract":
					subject = _("Vehicle Contract With name {0} will be end after 2 months from now {1}").format(row.get('name'),row.get('end_date'))
					mail_msg = _( "Vehicle Contract With name {0} will be end after 2 months from now {1}").format(row.get('name'),row.get('end_date'))
				elif row.doctype=="Tire Log" and row.child=="Tire":
					subject = _("Vehicle  With name {0} will need To Change Tire Name {1}").format(row.get('vehicle'),row.get('name'))
					mail_msg =  _("Vehicle  With name {0} will need To Change Tire Name {1}").format(row.get('vehicle'),row.get('name'))
				elif row.doctype=="Tire Log" and row.child=="Inspection":
					subject = _("Vehicle  With name {0} will need To Change Tire Inspection Name {1}").format(row.get('vehicle'),row.get('name'))
					mail_msg =  _("Vehicle  With name {0} will need To Change Inspection Tire Name {1}").format(row.get('vehicle'),row.get('name'))
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


def insurance_and_goverment_alert():
	if "Fleet" in DOMAINS:
		setup_insurance_alert()
		# set_gov_inspection_alert()


def setup_insurance_alert():
	insqurance_sql = """
	select comment,valid_to ,DATEDIFF(valid_to  ,CURDATE()) diff
	,CONCAT('vechile',' "',parent,'"', ' Insurance Will End At ',valid_to) msg 
	,parent as document_name
	,'Vehicle' as document_type
	,parentfield
	FROM `tabInsurance Table`
	WHERE  (DATEDIFF(valid_to  ,CURDATE()) <= 15)
	"""
	insqurance_data = frappe.db.sql(insqurance_sql,as_dict=1)
	notify_role= frappe.db.get_single_value('Fleet Vehicle Role', 'insurance_inspection_role')
	if insqurance_data and notify_role:
		prepare_insurance_gov_notify(notify_role,insqurance_data,send_insurance_notify)


def set_gov_inspection_alert():
	inspection_sql = """
	select notes,to_date ,DATEDIFF(to_date ,CURDATE()) diff
	,CONCAT('vechile',' "',parent,'"', ' Insurance Will End At ',to_date) msg 
	,parent as document_name
	,'Vehicle' as document_type
	,parentfield
	FROM `tabGovernment Inspection`
	WHERE  (DATEDIFF(to_date  ,CURDATE()) <= 15) 
	"""
	inspection_data = frappe.db.sql(inspection_sql,as_dict=1)
	notify_role= frappe.db.get_single_value('Fleet Vehicle Role', 'insurance_inspection_role')
	if inspection_data and notify_role:
		prepare_insurance_gov_notify(notify_role,inspection_data,send_insurance_notify)

def prepare_insurance_gov_notify(role,data,method):
	get_all_manger = get_user_by_role(role)
	if (data and get_all_manger):
		# get_all_manger = [x['parent'] for x in get_all_manger]
		kwargs={
			"get_all_manger":get_all_manger,
			"data":data,
		}
		frappe.enqueue(
		method=method,
		# job_name="send_insurance_notify",
		queue="default", 
		timeout=500, 
		is_async=True , #! set true after end if this is True, method is run in worker
		now=False, #! set false after end if this is True, method is run directly (not in a worker) 
		at_front=False, # put the job at the front of the queue
		**kwargs,
	)
		
def send_insurance_notify(**kwargs):
	# print('\n\n\n',"in send_insurance_نnotify",'\n\n\n\n')
	# print('\n\n\n-->data',kwargs.get("data"),'\n\n\n\n')
	# print('\n\n\n-->users',kwargs.get("get_all_manger"),'\n\n\n\n')
	for row in kwargs.get("data"):
		for admin in kwargs.get("get_all_manger"):
			owner_name = admin.parent
			notif_doc = frappe.new_doc('Notification Log')
			mail_msg=''
			subject=''
			if row.get('parentfield') == 'insurance_table':
				subject =_("Vechile {0} Insurance Will End {1}").format( row.get('document_name'), row.get('valid_to'))
				mail_msg =  _("Vechile {0} Insurance Will End {1}").format( row.get('document_name'), row.get('valid_to'))
			if row.get('parentfield') == 'government_inspection':
				subject =_("Vechile {0} Of Government Inspection Will End {1}").format( row.get('document_name'), row.get('valid_to'))
				mail_msg =  _("Vechile {0} Of Government Inspection Will End {1}").format( row.get('document_name'), row.get('valid_to'))
			notif_doc.subject = subject
			notif_doc.email_content =mail_msg
			notif_doc.for_user = owner_name
			notif_doc.type = "Mention"
			notif_doc.document_type = row.document_type
			notif_doc.document_name = row.document_name
			notif_doc.from_user = frappe.session.user or ""
			notif_doc.insert(ignore_permissions=True)
			# print('\n\n\n-->notif_doc',notif_doc.__dict__,'\n\n\n\n')

