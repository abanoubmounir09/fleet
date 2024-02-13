

import frappe
from frappe import _
from fleet.fleet_managment.doctype.maintenance_request.maintenance_request import get_user_by_role

DOMAINS = frappe.get_active_domains()

def install() :
	pass

# def create_vehicle_log_script(doc,*args, **kwargs):
#     odoreading=doc.odometer or 0
#     result=frappe.db.sql("""select type from `tabVehicle Service` where parent='%s' group by type"""%doc.name,as_dict=1)
#     card_name = frappe.db.sql("""select name from `tabVehicle Card` where vehicle='%s'""" % doc.license_plate, as_dict=1)
#     if card_name:
#         print("from card")
#         card_doc = frappe.get_doc("Vehicle Card", card_name[0].name)
#         for s in result:
#             for d in card_doc.maintainance:
#                 if s.type==d.maintainance and odoreading > d.odometer_reading:
#                     print("from last if")
#                     d.odometer_reading=odoreading
#         card_doc.save()

	
def vehicle_log_validate(vechile_log,*args, **kwargs):
	update_vechile_card_odometer(vechile_log,*args, **kwargs)

def vehicle_log_on_submit(doc,*args, **kwargs):
	if "Fleet" in DOMAINS:
		update_vechile_card(doc,*args, **kwargs)
		# change_request_status(doc)
		kwargs['date'] = doc.creation
		kwargs['owner_name'] = doc.applicant_name
		kwargs['document_type'] = doc.doctype
		kwargs['document_name'] = doc.name
		status , driver  = str(doc.applicant_name or " "), str(doc.modified or " ")
		kwargs['subject'] = _(f"تم إرسال سجل السيارة إلى السائق {status} بالحالة {driver} وهو مكتمل")
		kwargs['email_content'] = _(f"تم إرسال سجل السيارة إلى السائق {status} بالحالة {driver} وهو مكتمل")
		# kwargs['subject'] = _("Vechile Log Is Submitted For Driver {0} at {1} status become Completed").format(doc.applicant_name, doc.modified)
		# kwargs['email_content'] = _("Vechile Log Is Submitted For Driver {0} at {1} status become Completed").format(doc.applicant_name, doc.modified)
		send_alert_vechile_driver(**kwargs)
		

def update_vechile_card(vechile_log,*args, **kwargs):
	if vechile_log.odometer:
		update_vechile_card_odometer(vechile_log,*args, **kwargs)
		update_vechile_card_notifaction(vechile_log,*args, **kwargs)
		

def update_vechile_card_odometer(vechile_log,*args, **kwargs):
	update_vechile_card_odometer=f"""
		update `tabVehicle Card` card SET card.odometer_reading={vechile_log.odometer}
		WHERE card.vehicle='{vechile_log.license_plate}' and {vechile_log.odometer} >= card.odometer_reading
		"""
	frappe.db.sql(update_vechile_card_odometer)
	frappe.db.commit()

def update_vechile_card_notifaction(vechile_log,*args, **kwargs):
	maintainance_request_type = frappe.db.get_value('Maintenance Request',vechile_log.maintenance_request,'maintainance')
	maintainance_type__doc = frappe.get_doc('Maintainance',maintainance_request_type)
	if not maintainance_type__doc.maintinance_after:
		frappe.throw('Please add Maininace After')
	vehcile_card_name = frappe.db.get_value('Vehicle Card',{'vehicle':vechile_log.license_plate},'name')
	vehcile_card = frappe.get_doc('Vehicle Card',vehcile_card_name)
	#**check if maintennce in table:
	maintainance_flage = False
	if len(vehcile_card.vehicle_notifcation):
		#**check if maintainnce type exist
		print('\n\n\n---add exis->\n\n\n')
		for row in vehcile_card.vehicle_notifcation:
			if row.maintainance == maintainance_request_type:
				maintainance_flage = True
				row.stop_odometer = vehcile_card.odometer_reading +  maintainance_type__doc.maintinance_after
		# vehcile_card.save()
	if not len(vehcile_card.vehicle_notifcation) or  (maintainance_flage==False):
		#**add new row
		# print('\n\n\n---add new--****->\n\n\n')
		new_row = vehcile_card.append('vehicle_notifcation',{
			'maintainance': maintainance_request_type,
			'stop_odometer': vehcile_card.odometer_reading +  maintainance_type__doc.maintinance_after,
			'notifaction_before': maintainance_type__doc.maintinance_before,
		})
	vehcile_card.save()

@frappe.whitelist()
def vehicle_card_notfication_center(**kwargs):
	if "Fleet" in DOMAINS:
		sql_data = """
			SELECT `tabVehicle Notifcation`.parent
			,`tabVehicle Notifcation`.maintainance
			,`tabVehicle Card`.vehicle 
			,`tabVehicle Card`.owner 
			,`tabVehicle Card`.odometer_reading
			, `tabVehicle Notifcation`.stop_odometer
			,`tabVehicle Card`.name
			,`tabVehicle Notifcation`.notifaction_before
			FROM `tabVehicle Notifcation`
			INNER JOIN `tabVehicle Card`
			ON `tabVehicle Notifcation`.parent=`tabVehicle Card`.name
			WHERE ((`tabVehicle Notifcation`.stop_odometer - `tabVehicle Card`.odometer_reading) <= `tabVehicle Notifcation`.notifaction_before)
			"""
		data_notify = frappe.db.sql(sql_data,as_dict=1)
		manager_role= frappe.db.get_single_value('Fleet Vehicle Role', 'manager_role')
		if not manager_role:
			frappe.throw(_("Please Add Manager Role in"))
		get_all_manger=get_user_by_role(manager_role)
		kwargs['cards'] = data_notify
		kwargs['get_all_manger'] = get_all_manger
		send_alert_vechile_manager(**kwargs)

		
@frappe.whitelist()
def alert_vechile_manager__(doc=None,role=None,*args,**kwargs):
	frappe.enqueue(
	method=send_alert_vechile_manager,
	queue="default", 
	timeout=None, 
	is_async=True, # if this is True, method is run in worker
	now=False, # if this is True, method is run directly (not in a worker) 
	at_front=True, # put the job at the front of the queue
	**kwargs,
)

def send_alert_vechile_manager(**kwargs):
	for row in kwargs.get("get_all_manger"):
		if row.parent!='Administrator':
			for vehicle_car in kwargs.get("cards"):
				owner_name = row.get("parent")
				notif_doc = frappe.new_doc('Notification Log')
				notif_doc.subject = _("سجل السياره {0} يحتاج الى صيانه {1}").format(vehicle_car.get('name'), vehicle_car.get('maintainance'))
				notif_doc.email_content = _("سجل السياره {0} يحتاج الى صيانه {1}").format(vehicle_car.get('name'), vehicle_car.get('maintainance'))
				notif_doc.for_user = owner_name
				notif_doc.from_user = frappe.session.user
				notif_doc.type = "Mention"
				notif_doc.document_type = 'Vehicle Card'
				notif_doc.document_name = vehicle_car.get('name')
				notif_doc.insert(ignore_permissions=True)


def send_alert_vechile_driver(**kwargs):
	owner_name = kwargs.get("owner_name")
	notif_doc = frappe.new_doc('Notification Log')
	notif_doc.subject =  kwargs.get("subject")
	notif_doc.email_content =  kwargs.get("email_content")
	notif_doc.for_user = owner_name
	notif_doc.type = "Mention"
	notif_doc.document_type = kwargs.get("document_type")
	notif_doc.document_name = kwargs.get("document_name")
	notif_doc.from_user = frappe.session.user
	notif_doc.insert(ignore_permissions=True)
		
def change_request_status(doc,*args, **kwargs):
	if doc.get("maintenance_request"):
		min_req_doc = frappe.get_doc("Maintenance Request",doc.maintenance_request)
		min_req_doc.db_set('status',"Completed")
		min_req_doc.save()