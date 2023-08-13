import frappe
import traceback
import unicodedata
from frappe import auth
import datetime
import json, ast
from frappe import _
import requests
from frappe.utils import getdate, nowdate
from erpnext.accounts.utils import get_balance_on
from .helpers import remove_html_tags, get_timesheet_task_count
from frappe.query_builder.functions import Convert
import erpnext
import random
import datetime
import json, ast
from erpnext.accounts.utils import get_balance_on
from frappe.desk.form.meta import get_meta
from frappe.utils import (
    flt,
    getdate,
    get_url,
    now,
    nowtime,
    get_time,
    today,
    get_datetime,
    add_days,
)
from frappe.utils import add_to_date, now, nowdate
from frappe.utils import cstr
from frappe.utils.make_random import get_random
import time
from decimal import Decimal
from frappe.exceptions import DoesNotExistError
from .doc_connections import project_connections
from .helpers import order_by, remove_html_tags



@frappe.whitelist()
def addBOM(**kwargs):
    bom = frappe.get_doc(kwargs["data"])
    bom.insert()
    bom_name = bom.name
    frappe.db.commit()
    if bom:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "bom": bom_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"
    

@frappe.whitelist()
def BOMPage(name):
    bom = {}
    doc_data = frappe.db.get_all(
        "BOM",
        filters={"name": name},
        fields=[
            "name",
            "item",
            "item_name",
            "uom",
            "quantity",
            "project",
            "set_rate_of_sub_assembly_item_based_on_bom",
            "allow_alternative_item",
            "is_default",
            "currency",
            "rm_cost_as_per",   
            "with_operations",
            "inspection_required",
            "docstatus",
            "amended_from"
        ],
    )

    for x in doc_data:
        bom["name"] = x.name
        bom["item"] = x.item
        bom["item_name"] = x.item_name
        bom["uom"] = x.uom
        bom["quantity"] = x.quantity
        bom["project"] = x.project
        bom["set_rate_of_sub_assembly_item_based_on_bom"] = x.set_rate_of_sub_assembly_item_based_on_bom
        bom["allow_alternative_item"] = x.allow_alternative_item
        bom["is_default"] = x.is_default
        bom["currency"] = x.currency
        bom["rm_cost_as_per"] = x.rm_cost_as_per
        bom["with_operations"] = x.with_operations
        bom["inspection_required"] = x.inspection_required
        bom["docstatus"] = x.docstatus
        bom["amended_from"] = x.amended_from

    bom_perations = frappe.db.get_all("BOM Operation",
                                      filters={"parent": name},
                                      fields=["operation", "workstation", "fixed_time","operating_cost","time_in_mins"]
                                      )
    bom["bom_perations"] = bom_perations

    attachments = frappe.db.sql(
        f""" Select
                file_name,
                file_url,
                Date_Format(creation,'%d/%m/%Y') as date_added
                from `tabFile`
                where `tabFile`.attached_to_doctype = "BOM"
                and `tabFile`.attached_to_name = "{name}"
                order by `tabFile`.creation
                """, as_dict=True)

    bom["attachments"] = attachments

    comments = frappe.db.sql(
        f""" Select
                creation,
                (Select
                    `tabUser`.full_name
                    from `tabUser`
                    where `tabUser`.name = `tabComment`.owner) as owner, content
                from `tabComment`  where `tabComment`.reference_doctype = "BOM"
                and `tabComment`.reference_name = "{name}"
                and `tabComment`.comment_type = "Comment"
                order by `tabComment`.creation
                """, as_dict=True)

    bom["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name
            from `tabPrint Format`
            where doc_type = "BOM"
            and disabled = 0
        """, as_dict=True)

    bom["print_formats"] = print_formats

    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)
    work_order_connections = {}
    job_card_connections = {}
    bom_connections = {}
    connections = []

    bom_count = len(frappe.get_list("BOM", filters={"project": name}))
    if bom_count > 0:
        bom_connections["name"] = "BOM"
        bom_connections["count"] = bom_count
        bom_connections["icon"] = "https://nextapp.mobi/files/quotation.png"
        connections.append(bom_connections)

    work_order = len(frappe.get_list("Job Card"))
    if work_order > 0:
        connections.append(work_order_connections)

    bom["conn"] = connections
    if doc_data:
        return bom
    else: "there is no bom with that name"


################################## JOB CARD ######################################

@frappe.whitelist()
def addJobCard(**kwargs):
    job = frappe.get_doc(kwargs["data"])
    job.insert()
    job_name = job.name
    frappe.db.commit()
    if job:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة بطاقه العمل بنجاح!",
            "job_card": job_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة بطاقه العمل . برجاء المحاولة مرة اخري!"

@frappe.whitelist()
def jobCardPage(name):
    job_card = {}
    doc_data = frappe.db.get_all(
        "Job Card",
        filters={"name": name},
        fields=[
            "name",
            "item_name",
            "for_quantity",
            "bom_no",
            "project",
            "company",
            "operation",
            "workstation",
            "work_order",
            "wip_warehouse",
            "status",
            "docstatus",
            "amended_from",

        ],
    )

    if doc_data:
        x = doc_data[0]  # Get the first record from doc_data
        job_card["name"] = x.name
        job_card["item_name"] = x.item_name
        job_card["for_quantity"] = x.for_quantity
        job_card["bom_no"] = x.bom_no
        job_card["project"] = x.project
        job_card["company"] = x.company
        job_card["operation"] = x.operation
        job_card["workstation"] = x.workstation
        job_card["work_order"] = x.work_order
        job_card["wip_warehouse"] = x.wip_warehouse,
        job_card["status"] = x.status
        job_card["docstatus"] = x.docstatus
        job_card["amended_from"] = x.amended_from


        # Fetch child table records ('Job Card Time Log' is the child table name)
        time_logs = frappe.get_all(
            "Job Card Time Log",
            filters={"parent": name},
            fields=["employee","from_time","to_time","completed_qty"],
        )
        job_card["time_logs"] = time_logs

        return job_card
    else:
        return "There is no Job Card with that name"


############################## WORK ORDER ##################################
@frappe.whitelist()
def addWorkOrder(**kwargs):
    work = frappe.get_doc(kwargs["data"])
    work.employee = kwargs["data"]["employee"]
    work.insert()
    work_name = work.name
    frappe.db.commit()
    if work:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة أمر التشغيل بنجاح!",
            "Word Order": work_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة أمر التشغيل . برجاء المحاولة مرة اخري!"

@frappe.whitelist()
def workOrderPage(name):
    workOrder = {}
    doc_data = frappe.db.get_all(
        "Work Order",
        filters={"name": name},
        fields=[
            "name",
            "item_name",
            "stock_uom",
            "project",
            "allow_alternative_item",
            "docstatus",
            "amended_from"
        ],
    )

    for x in doc_data:
        workOrder["name"] = x.name
        workOrder["item_name"] = x.item_name
        workOrder["stock_uom"] = x.stock_uom
        workOrder["project"] = x.project
        workOrder["allow_alternative_item"] = x.allow_alternative_item
        workOrder["docstatus"] = x.docstatus
        workOrder["amended_from"] = x.amended_from
    attachments = frappe.db.sql(
        f""" Select
                file_name,
                file_url,
                Date_Format(creation,'%d/%m/%Y') as date_added
                from `tabFile`
                where `tabFile`.attached_to_doctype = "Work Order"
                and `tabFile`.attached_to_name = "{name}"
                order by `tabFile`.creation
                """, as_dict=True)

    workOrder["attachments"] = attachments

    comments = frappe.db.sql(
        f""" Select
                creation,
                (Select
                    `tabUser`.full_name
                    from `tabUser`
                    where `tabUser`.name = `tabComment`.owner) as owner, content
                from `tabComment`  where `tabComment`.reference_doctype = "Work Order"
                and `tabComment`.reference_name = "{name}"
                and `tabComment`.comment_type = "Comment"
                order by `tabComment`.creation
                """, as_dict=True)

    workOrder["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name
            from `tabPrint Format`
            where doc_type = "Work Order"
            and disabled = 0
        """, as_dict=True)

    workOrder["print_formats"] = print_formats

    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)
    
    if doc_data:
        return workOrder
    else: "there is no workOrder with that name"