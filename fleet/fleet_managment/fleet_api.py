


import frappe
from frappe import _
from frappe.desk.reportview import get_form_params,make_access_log,append_totals_row,handle_duration_fieldtype_values
from frappe.model.db_query import DatabaseQuery
from six import StringIO, string_types
from six.moves import range
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html
import json

@frappe.whitelist()
@frappe.read_only()
def export_query():
	"""export from report builder"""
	# frappe.throw('heklopnnn')
	title = frappe.form_dict.title
	frappe.form_dict.pop("title", None)
	# print('\n\n\n===>','------xxxx------','\n\n\n\n')
	form_params = get_form_params()
	form_params["limit_page_length"] = None
	form_params["as_list"] = True
	doctype = form_params.doctype
	add_totals_row = None
	file_format_type = form_params["file_format_type"]
	title = title or doctype

	del form_params["doctype"]
	del form_params["file_format_type"]

	if "add_totals_row" in form_params and form_params["add_totals_row"] == "1":
		add_totals_row = 1
		del form_params["add_totals_row"]

	frappe.permissions.can_export(doctype, raise_exception=True)

	if "selected_items" in form_params:
		si = json.loads(frappe.form_dict.get("selected_items"))
		form_params["filters"] = {"name": ("in", si)}
		del form_params["selected_items"]

	make_access_log(
		doctype=doctype,
		file_type=file_format_type,
		report_name=form_params.report_name,
		filters=form_params.filters,
	)

	db_query = DatabaseQuery(doctype)
	ret = db_query.execute(**form_params)

	if add_totals_row:
		ret = append_totals_row(ret)

	data = [["Sr"] + get_labels(db_query.fields, doctype)]
	print('\n\n\n==data 111=>',data,'\n\n\n')
	print('\n\n\n==ret 111=>',ret,'\n\n\n')
	for i, row in enumerate(ret):
		data.append([i + 1] + list(row))

	data = handle_duration_fieldtype_values(doctype, data, db_query.fields)
	print('\n\n\n===>',data,'\n\n\n')
	if file_format_type == "CSV":

		# convert to csv
		import csv

		from frappe.utils.xlsxutils import handle_html

		f = StringIO()
		writer = csv.writer(f)
		for r in data:
			# encode only unicode type strings and not int, floats etc.
			writer.writerow(
				[handle_html(frappe.as_unicode(v)) if isinstance(v, string_types) else v for v in r]
			)

		f.seek(0)
		frappe.response["result"] = cstr(f.read())
		frappe.response["type"] = "csv"
		frappe.response["doctype"] = title

	elif file_format_type == "Excel":

		from frappe.utils.xlsxutils import make_xlsx

		xlsx_file = make_xlsx(data, doctype)

		frappe.response["filename"] = title + ".xlsx"
		frappe.response["filecontent"] = xlsx_file.getvalue()
		frappe.response["type"] = "binary"
                


def get_labels(fields, doctype):
	# frappe.throw('test66')
	"""get column labels based on column names"""
	labels = []
	labels_2 = []
	for key in fields:
		key = key.split(" as ")[0]

		if key.startswith(("count(", "sum(", "avg(")):
			continue

		if "." in key:
			parenttype, fieldname = key.split(".")[0][4:-1], key.split(".")[1].strip("`")
		else:
			parenttype = doctype
			fieldname = fieldname.strip("`")

		df = frappe.get_meta(parenttype).get_field(fieldname)
			
		label = df.label if df else fieldname.title()
		lab1 = _(label)
		if lab1 in labels_2:
			lab1 = doctype + ": " + lab1
		labels_2.append(lab1)
	# print('\n\n\n--labels->',labels)
	# print('\n\n\n--translated-labels_2->',labels_2)
	return labels_2
	# return labels