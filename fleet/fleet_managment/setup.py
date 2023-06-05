

import frappe
DOMAINS = frappe.get_active_domains()

def install() :
    pass

def create_vehicle_log_script(doc,*args, **kwargs):
    print("hello world from hook")
    odoreading=doc.odometer or 0
    result=frappe.db.sql("""select type from `tabVehicle Service` where parent='%s' group by type"""%doc.name,as_dict=1)
    card_name = frappe.db.sql("""select name from `tabVehicle Card` where vehicle='%s'""" % doc.license_plate, as_dict=1)
    if card_name:
        print("from card")
        card_doc = frappe.get_doc("Vehicle Card", card_name[0].name)
        for s in result:
            for d in card_doc.maintainance:
                if s.type==d.maintainance and odoreading >d.odometer_reading:
                    print("from last if")
                    d.odometer_reading=odoreading
        card_doc.save()

    change_request_status(doc)


def hook_on_submit(doc,*args, **kwargs):
    if "Fleet" in DOMAINS:
        kwargs['date'] = doc.creation
        kwargs['owner_name'] = doc.applicant_name
        kwargs['document_type'] = doc.doctype
        kwargs['document_name'] = doc.name
        kwargs['subject'] = f"Vechile Log Is Submitted For Driver {doc.applicant_name}  at {doc.modified} status become agree"
        kwargs['email_content'] = f"Vechile Log Is Submitted For Driver {doc.applicant_name}  at {doc.modified} status become agree"
        send_alert_vechile_driver(**kwargs)
        

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
    if doc.maintenance_request:
        min_req_doc = frappe.get_doc("Maintenance Request",doc.maintenance_request)
        min_req_doc.status = doc.status
        min_req_doc.save()