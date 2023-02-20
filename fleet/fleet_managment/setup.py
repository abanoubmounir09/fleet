
import frappe
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

def change_request_status(doc,*args, **kwargs):
    if doc.maintenance_request:
        min_req_doc = frappe.get_doc("Maintenance Request",doc.maintenance_request)
        min_req_doc.status = doc.status
        min_req_doc.save()