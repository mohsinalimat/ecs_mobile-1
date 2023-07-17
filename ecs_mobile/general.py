from frappe.query_builder.functions import Convert
import frappe
import erpnext
from frappe import auth
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

# Exception Imports
from frappe.exceptions import DoesNotExistError

# local imports
from .doc_connections import project_connections
from .helpers import order_by, remove_html_tags


@frappe.whitelist()
def general_service(
        doctype,
        filter1="%%",
        filter2="%%",
        filter3="%%",
        filter4="%%",
        filter5="%%",
        filter6="%%",
        filter7="%%",
        filter8="%%",
        search_text="%%",
        cur_nam="%%",
        con_doc="%%",
        start=0,
        page_length=20,
        sort_field=None,
        sort_type=None,
):
    from .helpers import remove_html_tags

    # Logs Endpoints
    if doctype == "Error Log":
        query = frappe.db.get_all(
            "Error Log",
            fields=["reference_doctype", "reference_name", "method", "error"],
        )
        if query:
            return query
        frappe.throw("Nothing Found", frappe.exceptions.DoesNotExistError)

    if doctype == "Project Template" and con_doc == "%%":
        query = frappe.db.get_all("Project Template", fields=["name", "project_type"])
        if query:
            for row in query:
                project_temp_tasks = frappe.db.get_all(
                    "Project Template Task",
                    fields=["task", "subject"],
                    filters={"parent": row.name},
                )
                row["tasks"] = project_temp_tasks
            return query
        frappe.throw("No project templates found.", frappe.exceptions.DoesNotExistError)

    if doctype == "DocType" and con_doc == "%%":
        query = frappe.db.get_list(
            "DocType",
            filters={"istable": False},
            fields=["name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Issue Type" and con_doc:
        query = frappe.db.get_all(
            "Issue Type",
            fields=["name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Party Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Party Type",
            fields=["name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Workflow State" and con_doc == "%%":
        query = frappe.db.get_list(
            "Workflow State",
            fields=["name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Workflow Action Master" and con_doc == "%%":
        query = frappe.db.get_list(
            "Workflow Action Master",
            fields=["name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Workflow" and con_doc == "%%":
        conditions = {}

        if filter1 != "%%":
            conditions["document_type"] = filter1

        query = frappe.db.get_list(
            "Workflow",
            filters=conditions,
            fields=["name", "is_active", "document_type"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Mobile Report" and con_doc == "%%":
        conditions = {}

        if filter1 != "%%":
            conditions["module"] = filter1
        if filter2 != "%%":
            conditions["report_name"] = filter2

        query = frappe.db.get_list(
            "Mobile Report",
            filters=conditions,
            fields=[
                "name",
                "report_name",
                "module",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Email Template" and con_doc == "%%":
        conditions = {}

        if filter1 != "%%":
            conditions["module"] = filter1
        if filter2 != "%%":
            conditions["report_name"] = filter2

        query = frappe.db.get_list(
            "Email Template",
            filters=conditions,
            fields=["name", "subject"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Role" and con_doc == "%%":
        conditions = {}
        if filter1 != "%%":
            conditions["module"] = filter1
        if filter2 != "%%":
            conditions["report_name"] = filter2

        query = frappe.db.get_list(
            "Role",
            filters=conditions,
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    # ----------------- Activity Type List View ------------------#
    if doctype == "Activity Type" and con_doc == "%%":
        activity_type = frappe.db.get_all(
            "Activity Type",
            fields=[
                "name",
                "activity_type",
                "costing_rate",
                "billing_rate",
                "disabled",
            ],
        )
        if activity_type:
            return activity_type
        else:
            return "لا يوجد !"
    # ---------------- END Activity Type List View -------------------#

    # ----------------- Project Type List View ------------------#
    if doctype == "Project Type" and con_doc == "%%":
        project_type = frappe.db.get_all(
            "Project Type", fields=["name", "project_type", "description"]
        )
        if project_type:
            return project_type
        else:
            return "لا يوجد !"
    # ---------------- END Project Type List View -------------------#

    # ----------------- Department List View ------------------#
    if doctype == "Department" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["department_name"] = ["like", search_text]

        if filter1 != "%%":
            conditions["company"] = filter1
        if filter2 != "%%":
            conditions["parent_department"] = filter2

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Department",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "department_name",
                "company",
                "parent_department",
                "is_group",
                "disabled",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    # ----------------- END Department List View ------------------#

    # ----------------- Task Type List View ------------------#
    if doctype == "Task Type" and con_doc == "%%":
        task_types = frappe.db.get_all("Task Type", fields=["name", "description"])
        if task_types:
            return task_types
        else:
            return "لا يوجد !"
    # ---------------- Task Type List View -------------------#

    # ----------------- Issue List View ------------------#
    if doctype == "Issue" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["subject"] = ["like", search_text]

        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["priority"] = filter2

        if filter3 != "%%":
            conditions["issue_type"] = filter3

        if filter6 != "%%":
            conditions["customer"] = filter6

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Issue",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "subject",
                "project",
                "status",
                "customer",
                "priority",
                "issue_type",
                "description",
                "opening_date",
                "opening_time",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            for issue in query:
                issue["description"] = remove_html_tags(str(issue["description"]))
            return query
        else:
            return "لا يوجد !"

    # ----------------- END Issue List View ------------------#
    # ------------------ BOM list view ---------------- #
    if doctype == "BOM" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["item"] = ["like", search_text]

        if filter1 != "%%":
            conditions["is_active"] = filter1
        if filter2 != "%%":
            conditions["is_default"] = filter2
        if filter3 != "%%":
            conditions["currency"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "BOM",
            or_filters=conditions1,
            filters=conditions,
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
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    # ------------------ End BOM list view ---------------- #

    # ----------------------------------------- Project List ---------------------------------------- #
    if doctype == "Project" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["project_name"] = ["like", search_text]

        if filter1 != "%%":
            conditions["priority"] = filter1
        if filter2 != "%%":
            conditions["status"] = filter2
        if filter3 != "%%":
            conditions["project_type"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        if filter6 != "%%":
            conditions["department"] = filter6

        query = frappe.db.get_list(
            "Project",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "project_name",
                "priority",
                "status",
                "expected_start_date",
                "expected_end_date",
                "project_type",
                "is_active",
                "department",
                "percent_complete_method",
                "percent_complete",
                "notes",
                "customer",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    # ---------------------------------------- End Project List --------------------------------------#

    # ----------------------------------------- Task List ----------------------------------------#
    if doctype == "Task" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["subject"] = ["like", search_text]

        if filter1 != "%%":
            conditions["project"] = filter1
        if filter2 != "%%":
            conditions["status"] = filter2
        if filter3 != "%%":
            conditions["priority"] = filter3

        query = frappe.db.get_list(
            "Task",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "subject",
                "project",
                "priority",
                "status",
                "type",
                "color",
                "exp_start_date",
                "exp_end_date",
                "progress",
                "expected_time",
                "description",
                "department",
                "company",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            for task in query:
                task["description"] = remove_html_tags(str(task["description"]))
                depends_on = frappe.db.get_all(
                    "Task Depends On",
                    filters={"parent": task["name"]},
                    fields=["task", "project", "subject"],
                )
                task["depends_on"] = depends_on
            return query
        else:
            return "لا يوجد !"
    # ---------------------------------------- End Task List --------------------------------------#

    # ----------------------------------------- Timesheet List ----------------------------------------#
    if doctype == "Timesheet" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["title"] = ["like", search_text]

        if filter1 != "%%":
            conditions["parent_project"] = filter1

        if filter2 != "%%":
            conditions["customer"] = filter2

        query = frappe.db.get_list(
            "Timesheet",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "docstatus",
                "title",
                "customer",
                "currency",
                "exchange_rate",
                "status",
                "parent_project",
                "employee",
                "employee_name",
                "department",
                "start_date",
                "end_date",
                "total_hours",
                "total_billable_hours",
                "base_total_billable_amount",
                "base_total_billed_amount",
                "base_total_costing_amount",
                "total_billed_hours",
                "total_billable_amount",
                "total_billed_amount",
                "total_costing_amount",
                "per_billed",
                "note",
            ],
            order_by="`tabTimesheet`.modified desc",
            start=start,
            page_length=page_length,
        )
        if query:
            for timesheet in query:
                timesheet["note"] = remove_html_tags(str(timesheet["note"]))
                time_logs = frappe.db.get_all(
                    "Timesheet Detail",
                    filters={"parent": timesheet["name"]},
                    fields=[
                        "activity_type",
                        "from_time",
                        "to_time",
                        "project",
                        "project_name",
                    ],
                )
                timesheet["time_logs"] = time_logs
            return query
        else:
            return "لا يوجد !"
    # ---------------------------------------- End Timesheet List --------------------------------------#

    ############################################ LEAD ############################################

    ########################### Lead Full List & Search ############################

    if doctype == "Lead" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["lead_name"] = ["like", search_text]
            conditions1["company_name"] = ["like", search_text]
            conditions1["mobile_no"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["lead_owner"] = filter2
        if filter3 != "%%":
            conditions["organization_lead"] = filter3
        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Lead",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "lead_name",
                "company_name",
                "territory",
                "email_id",
                "mobile_no",
                "source",
                "market_segment",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Quotations Connected With Lead & Search ############################
    if doctype == "Quotation" and con_doc == "Lead":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, currency, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Opportunities Connected With Lead & Search ############################
    if doctype == "Opportunity" and con_doc == "Lead":
        connections = frappe.db.sql(
            """ select name,opportunity_from,customer_name,transaction_date,opportunity_type,sales_stage,status
                from `tabOpportunity` where `party_name` = '{cur_nam}'
                and (`tabOpportunity`.name like '%{search_text}%' or `tabOpportunity`.customer_name like '%{search_text}%' or `tabOpportunity`.party_name like '%{search_text}%' or `tabOpportunity`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ OPPORTUNITY ############################################

    ########################### Opportunity Full List & Search ############################

    if doctype == "Opportunity" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["party_name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["opportunity_from"] = filter2
        if filter3 != "%%":
            conditions["party_name"] = filter3
        if filter4 != "%%":
            conditions["opportunity_type"] = filter4

        if filter5 != "%%" and filter6 == "%%":
            conditions["transaction_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["transaction_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Opportunity",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "opportunity_from",
                "customer_name",
                "transaction_date",
                "opportunity_type",
                "sales_stage",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Quotations Connected With Opportunity & Search ############################
    if doctype == "Quotation" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, currency, grand_total, status
                from `tabQuotation` where `opportunity` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Supplier Quotations Connected With Opportunity & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name,supplier,transaction_date,valid_till,currency,grand_total,status
                from `tabSupplier Quotation` where `opportunity` = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier like '%{search_text}%' or `tabSupplier Quotation`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ QUOTATION ############################################

    ########################### Quotation Full List & Search ############################

    if doctype == "Quotation" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["party_name"] = ["like", search_text]
            conditions1["customer_address"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["quotation_to"] = filter2
        if filter3 != "%%":
            conditions["customer_name"] = filter3
        if filter4 != "%%":
            conditions["order_type"] = filter4

        if filter5 != "%%" and filter6 == "%%":
            conditions["transaction_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["transaction_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Quotation",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "quotation_to",
                "customer_name",
                "transaction_date",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Sales Orders Connected With Quotation & Search ############################
    if doctype == "Sales Order" and con_doc == "Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                       `tabSales Order`.transaction_date as transaction_date,`tabSales Order`.currency as currency,`tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                from `tabSales Order` join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent
                where `tabSales Order Item`.prevdoc_docname = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ CUSTOMER ############################################

    ########################### Customer Full List & Search ############################

    if doctype == "Customer" and con_doc == "%%":
        conditions1 = {}
        conditions = {"disabled": ["=", 0]}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["mobile_no"] = ["like", search_text]
        if filter1 != "%%":
            conditions["customer_group"] = filter1
        if filter2 != "%%":
            conditions["territory"] = filter2
        if filter3 != "%%":
            conditions["customer_type"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Customer",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "customer_name",
                "customer_group",
                "customer_type",
                "territory",
                "mobile_no",
                "tax_id",
                "customer_primary_address",
                "customer_primary_contact",
                "default_currency",
                "default_price_list",
                "payment_terms",
                "default_sales_partner",
                "default_currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Quotations Connected With Customer & Search ############################
    if doctype == "Quotation" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, currency, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Opportunities Connected With Customer & Search ############################
    if doctype == "Opportunity" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,opportunity_from,customer_name,transaction_date,opportunity_type,sales_stage,status
                 from `tabOpportunity` where `party_name` = '{cur_nam}'
                and (`tabOpportunity`.name like '%{search_text}%' or `tabOpportunity`.customer_name like '%{search_text}%' or `tabOpportunity`.party_name like '%{search_text}%' or `tabOpportunity`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Sales Orders Connected With Customer & Search ############################
    if doctype == "Sales Order" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,transaction_date,currency,grand_total,status
                from `tabSales Order` where `customer` = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Delivery Notes Connected With Customer & Search ############################
    if doctype == "Delivery Note" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer,territory,posting_date,set_warehouse,currency,status
                from `tabDelivery Note` where `customer` = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Sales Invoices Connected With Customer & Search ############################
    if doctype == "Sales Invoice" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,posting_date,currency,grand_total,status
                from `tabSales Invoice` where `customer` = '{cur_nam}'
                and (`tabSales Invoice`.name like '%{search_text}%' or `tabSales Invoice`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Customer & Search ############################
    if doctype == "Payment Entry" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,party_name,payment_type,mode_of_payment,posting_date,paid_from_account_currency as currency,paid_amount as base_paid_amount,status
                from `tabPayment Entry` where `party` = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Supplier & Search ############################
    if doctype == "Payment Entry" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select name,party_name,payment_type,mode_of_payment,posting_date,paid_amount as base_paid_amount, paid_from_account_currency as currency,status
                 from `tabPayment Entry` where `party` = '{cur_nam}'
                 and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
             """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ SALES ORDER ############################################

    ########################### Sales Order Full List & Search ############################

    if doctype == "Sales Order" and con_doc == "%%":
        conditions1 = {}
        conditions = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["customer"] = ["like", search_text]
            conditions1["customer_address"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["customer"] = filter2
        if filter3 != "%%":
            conditions["delivery_status"] = filter3
        if filter4 != "%%":
            conditions["billing_status"] = filter4
        if filter5 != "%%" and filter6 == "%%":
            conditions["transaction_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["transaction_date"] = ["between", [filter5, filter6]]
        if filter7 != "%%" and filter8 == "%%":
            conditions["delivery_date"] = [">=", filter7]
        if filter8 != "%%" and filter7 == "%%":
            conditions["delivery_date"] = ["<=", filter8]
        if filter7 != "%%" and filter8 != "%%":
            conditions["delivery_date"] = ["between", [filter7, filter8]]

        query = frappe.db.get_list(
            "Sales Order",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "customer_name",
                "customer_address",
                "transaction_date",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Sales Invoices Connected With Sales Order & Search ############################
    if doctype == "Sales Invoice" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabSales Invoice`.name as name,`tabSales Invoice`.customer_name as customer_name,`tabSales Invoice`.customer_address as customer_address,
                       `tabSales Invoice`.posting_date as posting_date, `tabSales Invoice`.currency as currency, `tabSales Invoice`.grand_total as grand_total,`tabSales Invoice`.status as status
                from `tabSales Invoice` join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                where `tabSales Invoice Item`.sales_order = '{cur_nam}'
                and (`tabSales Invoice`.name like '%{search_text}%' or `tabSales Invoice`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Delivery Notes Connected With Sales Order & Search ############################
    if doctype == "Delivery Note" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                       `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse,`tabDelivery Note`.currency as currency,`tabDelivery Note`.status as status
                from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                where `tabDelivery Note Item`.against_sales_order = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Material Requests Connected With Sales Order & Search ############################
    if doctype == "Material Request" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabMaterial Request`.name as name,`tabMaterial Request`.material_request_type as material_request_type,
                      `tabMaterial Request`.transaction_date as transaction_date,`tabMaterial Request`.set_warehouse as set_warehouse,`tabMaterial Request`.status as status
                from `tabMaterial Request` join `tabMaterial Request Item` on `tabMaterial Request`.name = `tabMaterial Request Item`.parent
                where `tabMaterial Request Item`.sales_order = '{cur_nam}'
                and (`tabMaterial Request`.name like '%{search_text}%' or `tabMaterial Request`.material_request_type like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Orders Connected With Sales Order & Search ############################
    if doctype == "Purchase Order" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier, `tabPurchase Order`.grand_total as grand_total,
                      `tabPurchase Order`.transaction_date as transaction_date,`tabPurchase Order`.set_warehouse as set_warehouse,
                      `tabPurchase Order`.currency as currency, `tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                where `tabPurchase Order Item`.sales_order = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%' or `tabPurchase Order`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Quotations Connected With Sales Order & Search ############################
    if doctype == "Quotation" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabQuotation`.name as name, `tabQuotation`.quotation_to as quotation_to, `tabQuotation`.customer_name as customer_name,
                       `tabQuotation`.transaction_date as transaction_date, `tabQuotation`.currency as currency,`tabQuotation`.grand_total as grand_total, `tabQuotation`.status as status
                from `tabQuotation` join `tabSales Order Item` on `tabQuotation`.name = `tabSales Order Item`.prevdoc_docname
                where `tabSales Order Item`.parent = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Sales Order & Search ############################
    if doctype == "Payment Entry" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                       `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment, `tabPayment Entry`.paid_from_account_currency as currency,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as base_paid_amount,`tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ SALES INVOICE ############################################

    ########################### Sales Invoice Full List & Search ############################

    if doctype == "Sales Invoice" and con_doc == "%%":
        conditions1 = {}
        conditions = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["customer"] = ["like", search_text]
            conditions1["customer_address"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["customer"] = filter2

        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Sales Invoice",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "customer_name",
                "customer_address",
                "posting_date",
                "grand_total",
                "status",
                "currency",
                "creation",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            if filter6 != "%%" and filter2 != "%%":
                filters = [
                    ["Sales Invoice", "customer", "=", filter2],
                    ["Sales Invoice Item", "item_code", "=", filter6],
                ]
                query = frappe.db.get_all(
                    "Sales Invoice",
                    filters=filters,
                    fields=[
                        "name",
                        "customer_name",
                        "customer_address",
                        "posting_date",
                        "grand_total",
                        "status",
                        "currency",
                    ],
                )
            return query
        else:
            return "لا يوجد !"

    ########################### Sales Orders Connected With Sales Invoice & Search ############################
    if doctype == "Sales Order" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                    `tabSales Order`.transaction_date as transaction_date, `tabSales Order`.currency as currency, `tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                from `tabSales Order` join `tabSales Invoice Item` on `tabSales Order`.name = `tabSales Invoice Item`.sales_order
                where `tabSales Invoice Item`.parent = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Delivery Notes Connected With Sales Invoice & Search ############################
    if doctype == "Delivery Note" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                       `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse, `tabDelivery Note`.currency as currency,
                       `tabDelivery Note`.status as status
                from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                where `tabDelivery Note Item`.against_sales_invoice = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Sales Invoice & Search ############################
    if doctype == "Payment Entry" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                       `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as base_paid_amount,
                       `tabPayment Entry`.status as status, `tabPayment Entry`.paid_from_account_currency as currency
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )

        if connections:
            return connections

        else:
            return "لا يوجد روابط !"

    ############################################ PAYMENT ENTRY ############################################

    ########################### Payment Entry Full List & Search ############################

    if doctype == "Payment Entry" and con_doc == "%%":
        conditions1 = {}
        conditions = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["party_name"] = ["like", search_text]
            conditions1["mode_of_payment"] = ["like", search_text]
            conditions1["party"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["payment_type"] = filter2
        if filter3 != "%%":
            conditions["mode_of_payment"] = filter3
        if filter4 != "%%":
            conditions["party_type"] = filter4
        if filter5 != "%%":
            conditions["party"] = filter5
        if filter6 != "%%" and filter7 == "%%":
            conditions["posting_date"] = [">=", filter6]
        if filter7 != "%%" and filter6 == "%%":
            conditions["posting_date"] = ["<=", filter7]
        if filter6 != "%%" and filter7 != "%%":
            conditions["posting_date"] = ["between", [filter6, filter7]]
        query = frappe.db.get_list(
            "Payment Entry",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "party_name",
                "payment_type",
                "mode_of_payment",
                "posting_date",
                "paid_amount as base_paid_amount",
                "paid_from_account_currency as currency",
                "status",
                "company",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )

        """
        for x in range(len(query)):

            currency = frappe.db.get_value("Company", {"name": query[x].company}, "default_currency")

            query[x]["currency"] = currency
        """
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Journal Entry Full List & Search ############################
    if doctype == "Journal Entry" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["title"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["voucher_type"] = filter1
        if filter2 != "%%" and filter3 == "%%":
            conditions["posting_date"] = [">=", filter2]
        if filter3 != "%%" and filter2 == "%%":
            conditions["posting_date"] = ["<=", filter3]
        if filter2 != "%%" and filter3 != "%%":
            conditions["posting_date"] = ["between", [filter2, filter3]]

        query = frappe.db.get_list(
            "Journal Entry",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "docstatus",
                "voucher_type",
                "posting_date",
                "total_debit",
                "total_credit",
                "mode_of_payment",
                "cheque_no",
                "cheque_date",
                "remark",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ############################################ LEAD SOURCE ############################################

    ########################### Lead Source Full List & Search ############################
    if doctype == "Lead Source" and con_doc == "%%":
        query = frappe.db.get_list(
            "Lead Source",
            or_filters=[
                {"name": ["like", search_text]},
                {"source_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ PROJECT ############################################

    ########################### Project Segment Full List & Search ############################

    ############################################ PAYMENT TERMS TEMPLATE ############################################

    ########################### Payment Terms Template Full List & Search ############################
    if doctype == "Payment Terms Template" and con_doc == "%%":
        query = frappe.db.get_list(
            "Payment Terms Template",
            or_filters=[
                {"name": ["like", search_text]},
                {"template_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ MARKET SEGEMENT ############################################

    ########################### Market Segment Full List & Search ############################
    if doctype == "Market Segment" and con_doc == "%%":
        query = frappe.db.get_list(
            "Market Segment",
            or_filters=[
                {"name": ["like", search_text]},
                {"market_segment": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ TERRITORY ############################################

    ########################### Territory Full List & Search ############################
    if doctype == "Territory" and con_doc == "%%":
        query = frappe.db.get_list(
            "Territory",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"territory_name": ["like", search_text]},
            ],
            fields=["name", "parent_territory"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ WAREHOUSE ############################################

    ########################### Warehouse Full List & Search ############################
    if doctype == "Warehouse" and con_doc == "%%":
        query = frappe.db.get_list(
            "Warehouse",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"warehouse_name": ["like", search_text]},
            ],
            fields=["name", "warehouse_name", "warehouse_type", "parent_warehouse"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ COUNTRY ############################################

    ########################### Country Full List & Search ############################
    if doctype == "Country" and con_doc == "%%":
        query = frappe.db.get_list(
            "Country",
            or_filters=[
                {"name": ["like", search_text]},
                {"country_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ OPPORTUNITY TYPE ############################################

    ########################### Opportunity Type Full List & Search ############################
    if doctype == "Opportunity Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Opportunity Type",
            or_filters=[{"name": ["like", search_text]}],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ CUSTOMER GROUP ############################################

    ########################### Customer Group Full List & Search ############################
    if doctype == "Customer Group" and con_doc == "%%":
        query = frappe.db.get_list(
            "Customer Group",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_group_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ ITEM GROUP ############################################

    ########################### Item Group Full List & Search ############################
    if doctype == "Item Group" and con_doc == "%%":
        query = frappe.db.get_list(
            "Item Group",
            or_filters=[
                {"name": ["like", search_text]},
                {"item_group_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ BRAND ############################################

    ########################### Brand Full List & Search ############################
    if doctype == "Brand" and con_doc == "%%":
        query = frappe.db.get_list(
            "Brand",
            or_filters=[
                {"name": ["like", search_text]},
                {"brand": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ UOM ############################################

    ########################### UOM Full List & Search ############################
    if doctype == "UOM" and con_doc == "%%":
        query = frappe.db.get_list(
            "UOM",
            filters=[{"enabled": 1}],
            or_filters=[
                {"name": ["like", search_text]},
                {"uom_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ User ############################################

    ########################### User Full List & Search ############################
    if doctype == "User" and con_doc == "%%":
        query = frappe.db.get_list(
            "User",
            filters=[{"enabled": 1}],
            or_filters=[
                {"name": ["like", search_text]},
                {"full_name": ["like", search_text]},
            ],
            fields=["name", "full_name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ Stock Entry Type ############################################

    ########################### Stock Entry Type Full List & Search ############################
    if doctype == "Stock Entry Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Stock Entry Type",
            or_filters=[
                {"name": ["like", search_text]},
                {"purpose": ["like", search_text]},
            ],
            fields=["name", "purpose"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ CAMPAIGN ############################################

    ########################### Campaign Full List & Search ############################
    if doctype == "Campaign" and con_doc == "%%":
        query = frappe.db.get_list(
            "Campaign",
            or_filters=[
                {"name": ["like", search_text]},
                {"campaign_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ INDUSTRY TYPE ############################################

    ########################### Industry Type Full List & Search ############################
    if doctype == "Industry Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Industry Type",
            or_filters=[
                {"name": ["like", search_text]},
                {"industry": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ CURRENCY ############################################

    ########################### Currency Full List & Search ############################
    if doctype == "Currency" and con_doc == "%%":
        query = frappe.db.get_list(
            "Currency",
            or_filters=[
                {"name": ["like", search_text]},
                {"currency_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ SALES PARTNER ############################################

    ########################### Sales Partner Full List & Search ############################
    if doctype == "Sales Partner" and con_doc == "%%":
        query = frappe.db.get_list(
            "Sales Partner",
            or_filters=[
                {"name": ["like", search_text]},
                {"partner_name": ["like", search_text]},
            ],
            fields=["name", "commission_rate"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ TERMS & CONDITIONS ############################################

    ########################### Terms and Conditions Full List & Search ############################
    if doctype == "Terms and Conditions" and con_doc == "%%":
        query = frappe.db.get_list(
            "Terms and Conditions",
            or_filters=[
                {"name": ["like", search_text]},
                {"title": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ MODE OF PAYMENT ############################################

    ########################### Mode of Payment Full List & Search ############################
    if doctype == "Mode of Payment" and con_doc == "%%":
        query = frappe.db.get_list(
            "Mode of Payment",
            or_filters=[
                {"name": ["like", search_text]},
                {"mode_of_payment": ["like", search_text]},
            ],
            fields=["name", "type"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ PRICE LIST ############################################

    ########################### Price List Full List & Search ############################
    if doctype == "Price List" and con_doc == "%%":
        query = frappe.db.get_list(
            "Price List",
            or_filters=[
                {"name": ["like", search_text]},
                {"price_list_name": ["like", search_text]},
            ],
            filters={"selling": 1},
            fields=["name", "currency"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Buying Price List Full List & Search ############################
    if doctype == "Buying Price List" and con_doc == "%%":
        query = frappe.db.get_list(
            "Price List",
            or_filters=[
                {"name": ["like", search_text]},
                {"price_list_name": ["like", search_text]},
            ],
            filters={"buying": 1},
            fields=["name", "currency"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ COST CENTER ############################################

    ########################### Cost Center Full List & Search ############################
    if doctype == "Cost Center" and con_doc == "%%":
        query = frappe.db.get_list(
            "Cost Center",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"cost_center_name": ["like", search_text]},
            ],
            fields=["name", "cost_center_name", "parent_cost_center"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ ACCOUNT ############################################
    ########################### Account Full List & Search ############################
    if doctype == "Account" and con_doc == "%%":
        conditions = {"is_group": ["=", 0]}
        or_conditions = {}
        if filter1 != "%%":
            conditions["account_type"] = filter1
        if filter2 != "%%":
            conditions["name"] = filter2
        query = frappe.db.get_list(
            "Account",
            filters=conditions,
            or_filters=[
                {"name": ["like", search_text]},
                {"account_name": ["like", search_text]},
                {"account_number": ["like", search_text]},
            ],
            fields=[
                "name",
                "account_type",
                "root_type",
                "account_currency",
                "parent_account",
            ],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ############################################ ITEM ############################################

    ########################### Item Full List & Search ############################

    if doctype == "Item" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["item_name"] = ["like", search_text]
            conditions1["item_code"] = ["like", search_text]
        if filter1 != "%%":
            conditions["item_group"] = filter1
        if filter2 != "%%":
            conditions["brand"] = filter2
        if filter3 != "%%":
            conditions["is_stock_item"] = filter3
        if filter4 != "%%":
            conditions["stock_uom"] = filter4

        query = frappe.db.get_list(
            "Item",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "item_code",
                "item_name",
                "item_group",
                "stock_uom as uom",
                "image",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )

        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ MATERIAL REQUEST ############################################

    ########################### Material Request Full List & Search ############################
    if doctype == "Material Request" and con_doc == "%%":
        conditions = {}
        or_conditions = {}
        if search_text != "%%":
            or_conditions["name"] = ["like", search_text]
            or_conditions["title"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["material_request_type"] = filter2
        if filter3 != "%%":
            conditions["set_warehouse"] = filter3
        if filter4 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["transaction_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["transaction_date"] = ["between", [filter4, filter5]]
        query = frappe.db.get_list(
            "Material Request",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "material_request_type",
                "transaction_date",
                "set_warehouse",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ STOCK ENTRY ############################################

    if doctype == "Supplier Quotation" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabSupplier Quotation`.name as name,`tabSupplier Quotation`.supplier as supplier,
                       `tabSupplier Quotation`.transaction_date as transaction_date, `tabSupplier Quotation`.valid_till as valid_till,
                       `tabSupplier Quotation`.grand_total as grand_total,`tabSupplier Quotation`.status as status,
                       `tabSupplier Quotation`.currency as currency
                    from `tabSupplier Quotation` join `tabSupplier Quotation Item` on `tabSupplier Quotation`.name = `tabSupplier Quotation Item`.parent
                where `tabSupplier Quotation Item`.material_request = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Purchase Order" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                       `tabPurchase Order`.transaction_date as transaction_date, `tabPurchase Order`.set_warehouse as set_warehouse,
                       `tabPurchase Order`.grand_total as grand_total,`tabPurchase Order`.status as status,
                       `tabPurchase Order`.currency as currency
                from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                where `tabPurchase Order Item`.material_request = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Purchase Receipt" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Receipt`.name as name,`tabPurchase Receipt`.supplier as supplier,`tabPurchase Receipt`.posting_date as posting_date		,
                `tabPurchase Receipt`.set_warehouse as set_warehouse,`tabPurchase Receipt`.status as status,
                `tabPurchase Receipt`.currency as currency, `tabPurchase Receipt`.total as total,`tabPurchase Receipt`.total_qty as total_qty,`tabPurchase Receipt`.status as status,
                `tabPurchase Receipt`.currency as currency
                from `tabPurchase Receipt` join `tabPurchase Receipt Item` on `tabPurchase Receipt`.name = `tabPurchase Receipt Item`.parent
                where `tabPurchase Receipt Item`.material_request = '{cur_nam}'
                and (`tabPurchase Receipt`.name like '%{search_text}%' or `tabPurchase Receipt`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Stock Entry" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabStock Entry`.name	 as name,`tabStock Entry`.stock_entry_type as stock_entry_type,
                       `tabStock Entry`.posting_date as posting_date, `tabStock Entry`.from_warehouse as from_warehouse,
                       `tabStock Entry`.to_warehouse as to_warehouse, `tabStock Entry`.docstatus as docstatus
                from `tabStock Entry` join `tabStock Entry Detail` on `tabStock Entry`.name = `tabStock Entry Detail`.parent
                where `tabStock Entry Detail`.material_request = '{cur_nam}'
                and (`tabStock Entry`.name like '%{search_text}%' or `tabStock Entry`.stock_entry_type like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"
    ############################################ STOCK ENTRY ############################################

    ########################### Stock Entry Full List & Search ############################

    if doctype == "Stock Entry" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["docstatus"] = filter1
        if filter2 != "%%":
            conditions["stock_entry_type"] = filter2

        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]
        if filter5 != "%%":
            conditions["from_warehouse"] = filter5
        if filter6 != "%%":
            conditions["to_warehouse"] = filter6

        query = frappe.db.get_list(
            "Stock Entry",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "stock_entry_type",
                "posting_date",
                "from_warehouse",
                "to_warehouse",
                "docstatus",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ PURCHASE RECEIPT ############################################

    ########################### Purchase Receipt Full List & Search ############################
    if doctype == "Purchase Receipt" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2
        if filter3 != "%%":
            conditions["is_return"] = filter3
        if filter4 != "%%":
            conditions["set_warehouse"] = filter4
        if filter5 != "%%" and filter6 == "%%":
            conditions["posting_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["posting_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["posting_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Purchase Receipt",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "posting_date",
                "set_warehouse",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ DELIVERY NOTE ############################################

    ########################### Purchase Order Connected With Purchase Receipt & Search ############################
    if doctype == "Purchase Order" and con_doc == "Purchase Receipt":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                       `tabPurchase Order`.transaction_date as transaction_date,
                       `tabPurchase Order`.set_warehouse as set_warehouse	,`tabPurchase Order`.grand_total as grand_total,
                       `tabPurchase Order`.currency as currency, `tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabPurchase Receipt Item` on `tabPurchase Order`.name = `tabPurchase Receipt Item`.purchase_order
                where `tabPurchase Receipt Item`.parent = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Receipt & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "Purchase Receipt":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Invoice`.name as name,`tabPurchase Invoice`.supplier as supplier,
                       `tabPurchase Invoice`.posting_date as posting_date, `tabPurchase Invoice`.due_date as due_date,
                       `tabPurchase Invoice`.total as total,`tabPurchase Invoice`.grand_total as grand_total,
                       `tabPurchase Invoice`.currency as currency, `tabPurchase Invoice`.status as status
                from `tabPurchase Invoice` join `tabPurchase Invoice Item` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
                where `tabPurchase Invoice Item`.purchase_receipt = '{cur_nam}'
                and (`tabPurchase Invoice`.name like '%{search_text}%' or `tabPurchase Invoice`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Receipt & Search ############################
    if doctype == "Purchase Receipt" and con_doc == "Purchase Receipt":
        connections = frappe.db.sql(
            """ select distinct pr1.name as name, pr1.supplier as supplier,
                       pr1.posting_date as posting_date, pr1.posting_date as posting_date,
                       pr1.set_warehouse as set_warehouse,pr1.status as status,
                       pr1.currency as currency
                from `tabPurchase Receipt` pr1 join `tabPurchase Receipt` pr2 on pr1.name = pr2.amended_from
                where pr2.amended_from = '{cur_nam}'
                and ( pr1.name like '%{search_text}%' or pr1.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ DELIVERY NOTE ############################################

    ########################### Delivery Note Full List & Search ############################

    if doctype == "Delivery Note" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["title"] = ["like", search_text]
            conditions1["customer"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["customer"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]

        if filter5 != "%%":
            conditions["set_warehouse"] = filter5

        query = frappe.db.get_list(
            "Delivery Note",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "customer",
                "territory",
                "posting_date",
                "set_warehouse",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ SUPPLIER ############################################

    ########################### Supplier Full List & Search ############################
    if doctype == "Supplier" and con_doc == "%%":
        conditions1 = {}
        conditions = {"disabled": ["=", 0]}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["supplier_name"] = ["like", search_text]
            conditions1["mobile_no"] = ["like", search_text]
        if filter1 != "%%":
            conditions["supplier_group"] = filter1
        if filter2 != "%%":
            conditions["country"] = filter2
        if filter3 != "%%":
            conditions["supplier_type"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Supplier",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "supplier_name",
                "supplier_group",
                "supplier_type",
                "country",
                "mobile_no",
                "default_currency",
                "default_price_list",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabSupplier Quotation`.name as name,`tabSupplier Quotation`.supplier as supplier,
                       `tabSupplier Quotation`.transaction_date as transaction_date, `tabSupplier Quotation`.valid_till as valid_till,
                       `tabSupplier Quotation`.total as total,`tabSupplier Quotation`.grand_total as grand_total,
                       `tabSupplier Quotation`.currency as currency, `tabSupplier Quotation`.status as status
                from `tabSupplier Quotation` join `tabSupplier` on `tabSupplier`.name = `tabSupplier Quotation`.supplier
                where `tabSupplier Quotation`.supplier = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Order & Search ############################

    if doctype == "Purchase Receipt" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Receipt`.name as name,`tabPurchase Receipt`.supplier as supplier,`tabPurchase Receipt`.set_warehouse as set_warehouse,
                `tabPurchase Receipt`.posting_date as posting_date,`tabPurchase Receipt`.grand_total as grand_total,
                `tabPurchase Receipt`.currency as currency, `tabPurchase Receipt`.total as total,`tabPurchase Receipt`.total_qty as total_qty,`tabPurchase Receipt`.status as status
                from `tabPurchase Receipt` join `tabSupplier` on `tabPurchase Receipt`.supplier = `tabSupplier`.name
                where `tabPurchase Receipt`.supplier = '{cur_nam}'
                and (`tabPurchase Receipt`.name like '%{search_text}%' or `tabPurchase Receipt`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Invoice`.name as name,`tabPurchase Invoice`.supplier as supplier,`tabPurchase Invoice`.currency as currency,
                       `tabPurchase Invoice`.posting_date as posting_date, `tabPurchase Invoice`.due_date as due_date,`tabPurchase Invoice`.grand_total as grand_total,`tabPurchase Invoice`.status as status
                from `tabPurchase Invoice` join `tabSupplier` on `tabPurchase Invoice`.supplier = `tabSupplier`.name
                where `tabPurchase Invoice`.supplier = '{cur_nam}'
                and (`tabPurchase Invoice`.name like '%{search_text}%' or `tabPurchase Invoice`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Order & Search ############################

    ########################### Payment Entry Connected With Purchase Invoice & Search ############################
    if doctype == "Purchase Order" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                `tabPurchase Order`.transaction_date as transaction_date,
                `tabPurchase Order`.set_warehouse as set_warehouse,
                `tabPurchase Order`.grand_total as grand_total,
                `tabPurchase Order`.currency as currency,
                `tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabSupplier` on `tabPurchase Order`.supplier = `tabSupplier`.name
                where `tabPurchase Order`.supplier   = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ SUPPLIER GROUP ############################################

    ########################### Supplier Group Full List & Search ############################
    if doctype == "Supplier Group" and con_doc == "%%":
        query = frappe.db.get_list(
            "Supplier Group",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"supplier_group_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ SUPPLIER QUOTATION ############################################

    ########################### Supplier Quotation Full List & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
            or_conditions["supplier_name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["transaction_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["transaction_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["transaction_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Supplier Quotation",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "transaction_date",
                "valid_till",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Quotation" and con_doc == "Supplier Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabQuotation`.name as name,`tabQuotation`.quotation_to as quotation_to,`tabQuotation`.customer_name as customer_name,
                       `tabQuotation`.transaction_date as transaction_date, `tabQuotation`.currency as currency,
                       `tabQuotation`.grand_total as grand_total,`tabQuotation`.status as status
                from `tabQuotation` join `tabSupplier Quotation` on `tabQuotation`.supplier_quotation = `tabSupplier Quotation`.name
                where `tabQuotation`.supplier_quotation = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.quotation_to like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Orders Connected With Supplier Quotation & Search ############################
    if doctype == "Purchase Order" and con_doc == "Supplier Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                `tabPurchase Order`.currency as currency, `tabPurchase Order`.transaction_date as transaction_date,
                `tabPurchase Order`.status as status, `tabPurchase Order`.set_warehouse as set_warehouse,
                `tabPurchase Order`.grand_total as grand_total
                from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                where `tabPurchase Order Item`.supplier_quotation = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Request Connected With Purchase Invoice & Search ############################
    if doctype == "Material Request" and con_doc == "Supplier Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabMaterial Request`.name as name,`tabMaterial Request`.material_request_type as material_request_type,`tabMaterial Request`.set_warehouse as set_warehouse,
                       `tabMaterial Request`.transaction_date as transaction_date, `tabMaterial Request`.schedule_date as schedule_date,`tabMaterial Request`.status as status
                from `tabMaterial Request` join `tabSupplier Quotation Item` on `tabMaterial Request`.name = `tabSupplier Quotation Item`.material_request
                where `tabSupplier Quotation Item`.parent = '{cur_nam}'
                and (`tabMaterial Request`.name like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ PURCHASE ORDER ############################################

    ########################### Purchase Order Full List & Search ############################
    if doctype == "Purchase Order" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2

        if filter3 != "%%" and filter4 == "%%":
            conditions["transaction_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["transaction_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["transaction_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Purchase Order",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "transaction_date",
                "set_warehouse",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Purchase Receipt" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Receipt`.name as name,`tabPurchase Receipt`.supplier as supplier,
                       `tabPurchase Receipt`.set_warehouse as set_warehouse, `tabPurchase Receipt`.currency as currency,
                       `tabPurchase Receipt`.posting_date as posting_date,`tabPurchase Receipt`.grand_total as grand_total,`tabPurchase Receipt`.status as status
                from `tabPurchase Receipt` join `tabPurchase Receipt Item` on `tabPurchase Receipt`.name = `tabPurchase Receipt Item`.parent
                where `tabPurchase Receipt Item`.purchase_order = '{cur_nam}'
                and (`tabPurchase Receipt`.name like '%{search_text}%' or `tabPurchase Receipt`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Invoice`.name as name,`tabPurchase Invoice`.supplier as supplier,`tabPurchase Invoice`.currency as currency,
                       `tabPurchase Invoice`.posting_date as posting_date, `tabPurchase Invoice`.due_date as due_date,`tabPurchase Invoice`.grand_total as grand_total,`tabPurchase Invoice`.status as status
                from `tabPurchase Invoice` join `tabPurchase Invoice Item` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
                where `tabPurchase Invoice Item`.purchase_order = '{cur_nam}'
                and (`tabPurchase Invoice`.name like '%{search_text}%' or `tabPurchase Invoice`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entry Connected With Purchase Invoice & Search ############################
    if doctype == "Material Request" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabMaterial Request`.name as name,`tabMaterial Request`.material_request_type as material_request_type,`tabMaterial Request`.set_warehouse as set_warehouse,
                       `tabMaterial Request`.transaction_date as transaction_date, `tabMaterial Request`.schedule_date as schedule_date,`tabMaterial Request`.status as status
                from `tabMaterial Request` join `tabPurchase Order Item` on `tabMaterial Request`.name = `tabPurchase Order Item`.material_request
                where `tabPurchase Order Item`.parent = '{cur_nam}'
                and (`tabMaterial Request`.name like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Request Connected With Purchase Invoice & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabSupplier Quotation`.name as name,`tabSupplier Quotation`.supplier as supplier,
                       `tabSupplier Quotation`.currency as currency,
                       `tabSupplier Quotation`.grand_total as grand_total,
                       `tabSupplier Quotation`.transaction_date as transaction_date,
                       `tabSupplier Quotation`.valid_till as valid_till,
                       `tabSupplier Quotation`.status as status
                from `tabSupplier Quotation` join `tabPurchase Order Item` on `tabSupplier Quotation`.name = `tabPurchase Order Item`.supplier_quotation
                where `tabPurchase Order Item`.parent = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Order & Search ############################

    if doctype == "Payment Entry" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.payment_type as payment_type,
                       `tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.paid_from_account_currency as currency,
                       `tabPayment Entry`.paid_amount as base_paid_amount,
                       `tabPayment Entry`.posting_date as posting_date, `tabPayment Entry`.party_name as party_name,`tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.contact_email like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ PURCHASE INVOICE ############################################

    ########################### Purchase Invoice Full List & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2
        if filter3 != "%%":
            conditions["is_return"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["posting_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["posting_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["posting_date"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Purchase Invoice",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "posting_date",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Purchase Order Connected With Purchase Invoice & Search ############################

    if doctype == "Purchase Order" and con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,`tabPurchase Order`.currency as currency,
                       `tabPurchase Order`.transaction_date as transaction_date,`tabPurchase Order`.grand_total as grand_total,`tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabPurchase Invoice Item` on `tabPurchase Order`.name = `tabPurchase Invoice Item`.purchase_order
                where `tabPurchase Invoice Item`.parent = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Invoice & Search ############################
    if doctype == con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select  pi_2.name as name, pi_2.supplier as supplier,pi_2.supplier_address as supplier_address,
                       pi_2.posting_date as posting_date,pi_2.due_date as due_date,pi_2.grand_total as grand_total,pi_2.status as status
                from `tabPurchase Invoice` pi_1 join `tabPurchase Invoice` pi_2 on pi_1.name = pi_2.return_against
                where pi_2.return_against = '{cur_nam}'
                and (pi_2.name like '%{search_text}%' or pi_2.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entry Connected With Purchase Invoice & Search ############################
    if doctype == "Payment Entry" and con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.party as party,`tabPayment Entry`.party_name as part_name,
                       `tabPayment Entry`.status as status,
                       `tabPayment Entry`.paid_amount as base_paid_amount,`tabPayment Entry`.paid_from_account_currency as currency
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.party_name like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Request Connected With Purchase Invoice & Search ############################
    if doctype == "Payment Request" and con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Request`.name as name,`tabPayment Request`.payment_request_type as payment_request_type, `tabPayment Request`.mode_of_payment as mode_of_payment,
                      `tabPayment Request`.transaction_date as transaction_date,`tabPayment Request`.party_type as party_type,`tabPayment Request`.party as party,`tabPayment Request`.status as status,
                      `tabPayment Request`.grand_total as grand_total,`tabPayment Request`.currency as currency
                from `tabPayment Request` join `tabPurchase Invoice` on `tabPayment Request`.reference_name = `tabPurchase Invoice`.name
                where `tabPayment Request`.reference_name = '{cur_nam}'
                and (`tabPayment Request`.name like '%{search_text}%' or `tabPayment Request`.party_type like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ ADDRESS ############################################

    ########################### Filtered Address List & Search ############################
    if doctype == "Filtered Address" and con_doc == "%%":
        addresses = frappe.db.get_all(
            "Dynamic Link", filters={"link_name": cur_nam}, fields=["parent"]
        )
        result = []
        for d in addresses:
            query = frappe.db.sql(
                """ select name as name ,
                                                 address_title as address_title,
                                                 address_line1 as address_line1,
                                                 city as city,
                                                 country as country
                                          from tabAddress where name = '{filtered}'
                                          and (address_title like '{search_text}' or address_line1 like '{search_text}'
                                               or city like '{search_text}' or country like '{search_text}') LIMIT {start},{page_length}
                                      """.format(
                    filtered=d.parent,
                    search_text=search_text,
                    start=start,
                    page_length=page_length,
                ),
                as_dict=1,
            )
            for x in query:
                data = {
                    "name": x.name,
                    "address_title": x.address_title,
                    "address_line1": x.address_line1,
                    "city": x.city,
                    "country": x.country,
                }
                result.append(data)

        if result:
            return result
        else:
            return "لا يوجد !"

    ############################################ CONTACT ############################################

    ########################### Filtered Contact List & Search ############################
    if doctype == "Filtered Contact" and con_doc == "%%":
        contacts = frappe.db.get_list(
            "Dynamic Link", filters={"link_name": cur_nam}, fields=["parent"]
        )
        result = []
        for d in contacts:
            query = frappe.db.sql(
                """ select name as name,
                                             first_name as contact_display,
                                             email_id as email_id,
                                             mobile_no as mobile_no,
                                             phone as phone
                                      from tabContact where name = '{filtered}'
                                      and (name like '{search_text}' or email_id like '{search_text}'
                                           or mobile_no like '{search_text}' or phone like '{search_text}'
                                           or company_name like '{search_text}') LIMIT {start},{page_length}
                                      """.format(
                    filtered=d.parent,
                    search_text=search_text,
                    start=start,
                    page_length=page_length,
                ),
                as_dict=1,
            )
            for x in query:
                data = {
                    "name": x.name,
                    "contact_display": str(x.contact_display),
                    "mobile_no": x.mobile_no,
                    "phone": x.phone,
                    "email_id": x.email_id,
                }
                result.append(data)

        if result:
            return result
        else:
            return "لا يوجد !"

    ########################### Leave Ap[plication Full List & Search ############################
    if doctype == "Leave Application" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        from_date = "from_date"
        to_date = "to_date"
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%":
            query = frappe.db.get_list(
                "Leave Application",
                fields=[
                    "name",
                    "employee_name",
                    "leave_approver_name",
                    "leave_approver",
                    "department",
                    "leave_type",
                    "from_date",
                    "to_date",
                    "total_leave_days",
                    "status",
                ],
                order_by=order_by(sort_field, sort_type),
                start=start,
                page_length=page_length,
            )
            response = []
            # return query[0].from_date
            for row in range(len(query)):
                if (
                        time.strptime(str(query[row].from_date), "%Y-%m-%d")
                        <= time.strptime(filter3.split("T")[0], "%Y-%m-%d")
                        <= time.strptime(str(query[row].to_date), "%Y-%m-%d")
                ):
                    response.append(query[row])

            return response

        if filter4 != "%%":
            conditions["department"] = filter4
        if filter5 != "%%":
            conditions["leave_type"] = filter5
        if filter6 != "%%" and filter7 == "%%":
            conditions["posting_date"] = [">=", filter6]
        if filter7 != "%%" and filter6 == "%%":
            conditions["posting_date"] = ["<=", filter7]
        if filter6 != "%%" and filter7 != "%%":
            conditions["posting_date"] = ["between", [filter6, filter7]]

        query = frappe.db.get_list(
            "Leave Application",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "leave_approver_name",
                "leave_approver",
                "department",
                "leave_type",
                "from_date",
                "to_date",
                "total_leave_days",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
            ########################### Attendance Connected With Leave Application & Search ############################

    # if doctype == "Attendance" and con_doc == "Leave Application":
    #     connections = frappe.db.sql(
    #         """ select distinct `tabAttendance`.name as name,`tabAttendance`.employee_name as employee_name,`tabAttendance`.department as department,
    #                    `tabAttendance`.leave_type as leave_type,`tabAttendance`.attendance_date as attendance_date, `tabAttendance`.status as status
    #             from `tabAttendance` join `tabLeave Application` on `tabLeave Application`.name = `Attendance`.leave_application
    #             where `Attendance`.leave_application = '{cur_nam}'
    #             and (`tabAttendance`.name like '%{search_text}%' or `tabAttendance`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
    #         """.format(
    #             start=start,
    #             page_length=page_length,
    #             cur_nam=cur_nam,
    #             search_text=search_text,
    #         ),
    #         as_dict=1,
    #     )
    #     if connections:
    #         return connections
    #     else:
    #         return "لا يوجد روابط !"

    ########################### Purchase Invoice Full List & Search ############################
    if doctype == "Employee" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["gender"] = filter2
        if filter3 != "%%":
            conditions["department"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["date_of_joining"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["date_of_joining"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["date_of_joining"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Employee",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "attendance_device_id",
                "designation",
                "department",
                "leave_approver",
                "branch",
                "company",
                "status",
                "expense_approver",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        for x in range(len(query)):
            currency = frappe.db.get_value(
                "Company", {"name": query[x].company}, "default_currency"
            )

            query[x]["currency"] = currency
            currency = frappe.db.get_value(
                "User", {"email": query[x].leave_approver}, "full_name"
            )

            query[x]["leave_approver_name"] = currency
            advance_account = frappe.db.get_value(
                "Company",
                {"name": query[x].company},
                "default_employee_advance_account",
            )

            query[x]["advance_account"] = advance_account
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Attendance Request" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabAttendance Request`.name as name,`tabAttendance Request`.employee_name as employee_name, `tabAttendance Request`.employee as employee,
                      `tabAttendance Request`.department as department,`tabAttendance Request`.from_date as from_date,`tabAttendance Request`.to_date as to_date,`tabAttendance Request`.reason as reason,`tabAttendance Request`.docstatus as docstatus
                from `tabAttendance Request` join `tabEmployee` on `tabAttendance Request`.employee = `tabEmployee`.name
                where `tabAttendance Request`.employee = '{cur_nam}'
                and (`tabAttendance Request`.name like '%{search_text}%' or `tabAttendance Request`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

            ###########################

    if doctype == "Leave Application" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabLeave Application`.name as name,`tabLeave Application`.employee_name as employee_name, `tabLeave Application`.employee as employee,
                      `tabLeave Application`.department as department,`tabLeave Application`.from_date as from_date,`tabLeave Application`.to_date as to_date,`tabLeave Application`.description as description,`tabLeave Application`.docstatus as docstatus
                from `tabLeave Application` join `tabEmployee` on `tabLeave Application`.employee = `tabEmployee`.name
                where `tabLeave Application`.employee = '{cur_nam}'
                and (`tabLeave Application`.name like '%{search_text}%' or `tabLeave Application`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################################

    if doctype == "Employee Advance" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabEmployee Advance`.name as name,`tabEmployee Advance`.employee_name as employee_name, `tabEmployee Advance`.employee as employee,
                      `tabEmployee Advance`.department as department,`tabEmployee Advance`.posting_date as posting_date,`tabEmployee Advance`.purpose as purpose,`tabEmployee Advance`.advance_amount as advance_amount,`tabEmployee Advance`.status as status
                from `tabEmployee Advance` join `tabEmployee` on `tabEmployee Advance`.employee = `tabEmployee`.name
                where `tabEmployee Advance`.employee = '{cur_nam}'
                and (`tabEmployee Advance`.name like '%{search_text}%' or `tabEmployee Advance`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################################

    if doctype == "Expense Claim" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabExpense Claim`.name as name,`tabExpense Claim`.employee_name as employee_name, `tabExpense Claim`.employee as employee,
                      `tabExpense Claim`.department as department,`tabExpense Claim`.posting_date as posting_date,`tabExpense Claim`.grand_total as grand_total,`tabExpense Claim`.status as status
                from `tabExpense Claim` join `tabEmployee` on `tabExpense Claim`.employee = `tabEmployee`.name
                where `tabExpense Claim`.employee = '{cur_nam}'
                and (`tabExpense Claim`.name like '%{search_text}%' or `tabExpense Claim`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Employee Grievance" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabEmployee Grievance`.name as name, `tabEmployee Grievance`.raised_by as raised_by,
                      `tabEmployee Grievance`.designation as designation,`tabEmployee Grievance`.date as date,`tabEmployee Grievance`.grievance_against_party as grievance_against_party,`tabEmployee Grievance`.grievance_against as grievance_against,
                      `tabEmployee Grievance`.grievance_type as grievance_type, `tabEmployee Grievance`.status as status
                from `tabEmployee Grievance` join `tabEmployee` on `tabEmployee Grievance`.raised_by = `tabEmployee`.name
                where `tabEmployee Grievance`.raised_by = '{cur_nam}'
                and (`tabEmployee Grievance`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"
    if doctype == "Leave Type" and con_doc == "%%":
        conditions = {}
        query = frappe.db.get_list(
            "Leave Type",
            filters=conditions,
            fields=["name", "leave_type_name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Department" and con_doc == "%%":
        conditions = {}
        query = frappe.db.get_list(
            "Department",
            filters=conditions,
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Employee Checkin" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["log_type"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["time"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["time"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["time"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Employee Checkin",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "log_type",
                "time",
                "shift",
                "device_id",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    #################################### Driver ########################
    if doctype == "Driver" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["name"] = ["like", search_text]
            or_conditions["full_name"] = ["like", search_text]

        query = frappe.db.get_list(
            "Driver",
            or_filters=or_conditions,
            fields=[
                "name",
                "full_name",
                "employee",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Gender Full List & Search ############################
    if doctype == "Gender" and con_doc == "%%":
        query = frappe.db.get_list(
            "Gender",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Employment Type Full List & Search ############################
    if doctype == "Employment Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Employment Type",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Company Full List & Search ############################
    if doctype == "Company" and con_doc == "%%":
        query = frappe.db.get_list(
            "Company",
            fields=[
                "name",
                "round_off_cost_center",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ########################### Department Full List & Search ############################
    if doctype == "Department" and con_doc == "%%":
        query = frappe.db.get_list(
            "Department",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### User Full List & Search ############################
    if doctype == "User" and con_doc == "%%":
        query = frappe.db.get_list(
            "User",
            fields=[
                "name",
                "email",
                "full_name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Designation List & Search ############################
    if doctype == "Designation" and con_doc == "%%":
        query = frappe.db.get_list(
            "Designation",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Branch List & Search ############################
    if doctype == "Branch" and con_doc == "%%":
        query = frappe.db.get_list(
            "Branch",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Holiday List List & Search ############################
    if doctype == "Holiday List" and con_doc == "%%":
        query = frappe.db.get_list(
            "Holiday List",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Shift Type List List & Search ############################
    if doctype == "Default Shift" and con_doc == "%%":
        query = frappe.db.get_list(
            "Shift Type",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Attendance Request" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["employee"] = filter1
        if filter2 != "%%":
            conditions["department"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["from_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["from_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["from_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Attendance Request",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "department",
                "from_date",
                "to_date",
                "reason",
                "docstatus",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Employee Advance Full List & Search ############################
    if doctype == "Employee Advance" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%":
            conditions["department"] = filter3
        if filter4 != "%%" and filter5 == "%%":
            conditions["posting_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["posting_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["posting_date"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Employee Advance",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "department",
                "posting_date",
                "purpose",
                "advance_amount",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        for x in range(len(query)):
            company = frappe.db.get_value(
                "Employee", {"name": query[x].employee}, "company"
            )

            query[x]["company"] = company
            advance_account = frappe.db.get_value(
                "Company", {"name": company}, "default_employee_advance_account"
            )

            query[x]["advance_account"] = advance_account
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Payment Entry" and con_doc == "Employee Advance":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name, `tabPayment Entry`.party_name as party_name,
                      `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,`tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.base_paid_amount as base_paid_amount,
                       `tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where  `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Expense Claim" and con_doc == "Employee Advance":
        connections = frappe.db.sql(
            """ select distinct `tabExpense Claim`.name as name, `tabExpense Claim`.employee_name as employee_name,
                      `tabExpense Claim`.employee as employee,`tabExpense Claim`.department as department,`tabExpense Claim`.posting_date as posting_date,`tabExpense Claim`.grand_total as grand_total,
                       `tabExpense Claim`.status as status
                from `tabExpense Claim` join `tabExpense Claim Advance` on `tabExpense Claim`.name = `tabExpense Claim Advance`.parent
                where  `tabExpense Claim Advance`.employee_advance = '{cur_nam}'
                and (`tabExpense Claim`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Branch List & Search ############################

    ########################### Expense Claim Type List & Search ############################
    if doctype == "Expense Claim Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Expense Claim Type",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Expense Claim Full List & Search ############################
    if doctype == "Expense Claim" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%":
            conditions["department"] = filter3
        if filter4 != "%%" and filter5 == "%%":
            conditions["posting_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["posting_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["posting_date"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Expense Claim",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "department",
                "posting_date",
                "grand_total",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Payment Entry" and con_doc == "Expense Claim":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name, `tabPayment Entry`.party_name as party_name,
                      `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,`tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.base_paid_amount as base_paid_amount,
                       `tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where  `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Employee Advance" and con_doc == "Expense Claim":
        connections = frappe.db.sql(
            """ select distinct `tabEmployee Advance`.name as name, `tabEmployee Advance`.employee_name as employee_name,
                      `tabEmployee Advance`.employee as employee,`tabEmployee Advance`.department as department,`tabEmployee Advance`.posting_date as posting_date,`tabEmployee Advance`.purpose as purpose,
                       `tabEmployee Advance`.advance_amount as advance_amount, `tabEmployee Advance`.status as status
                from `tabEmployee Advance` join `tabExpense Claim Advance` on `tabEmployee Advance`.name = `tabExpense Claim Advance`.employee_advance
                where  `tabExpense Claim Advance`.parent = "{cur_nam}"
                and (`tabEmployee Advance`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )

        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Expense Claim Type List & Search ############################
    if doctype == "Loan Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Loan Type",
            fields=[
                "name",
                "rate_of_interest",
                "is_term_loan",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Loan Application Full List & Search ############################
    if doctype == "Loan Application" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["applicant_type"] = filter2
        if filter3 != "%%":
            conditions["applicant"] = filter3
        if filter4 != "%%":
            conditions["loan_type"] = filter4
        if filter5 != "%%" and filter6 == "%%":
            conditions["posting_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["posting_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["posting_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Loan Application",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "applicant_type",
                "applicant_name",
                "applicant",
                "posting_date",
                "loan_type",
                "loan_amount",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )

        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Bank Account List & Search ############################
    if doctype == "Bank Account" and con_doc == "%%":
        query = frappe.db.get_list(
            "Bank Account",
            fields=["name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Customer Visit" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["customer"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["customer"] = filter1
        if filter2 != "%%":
            conditions["customer_address"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]
        if filter5 != "%%":
            conditions["owner"] = filter5

        query = frappe.db.get_list(
            "Customer Visit",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "docstatus",
                "customer",
                "customer_address",
                "posting_date",
                "time",
                "owner",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Address" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["address_title"] = ["like", search_text]
            or_conditions["address_line1"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["address_type"] = filter1
        if filter2 != "%%" and filter3 != "%%":
            address = frappe.qb.DocType("Address")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.address_title,
                    address.address_type,
                    address.address_line1,
                    address.city,
                    address.country,
                )
                .where(dynamic_link.link_doctype == filter2)
                .where(dynamic_link.link_name == filter3)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        if filter2 != "%%":
            address = frappe.qb.DocType("Address")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .inner_join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.address_title,
                    address.address_type,
                    address.address_line1,
                    address.city,
                    address.country,
                )
                .where(dynamic_link.link_doctype == filter2)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        query = frappe.db.get_list(
            "Address",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "address_title",
                "address_type",
                "address_line1",
                "city",
                "country",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        # for x in range(len(query)):

        #     link_doctype = frappe.db.get_value(
        #         "Dynamic Link",
        #         {
        #             "parent": query[x].name,
        #         },
        #         "link_doctype",
        #     )
        #     link_name = frappe.db.get_value(
        #         "Dynamic Link",
        #         {
        #             "parent": query[x].name,
        #         },
        #         "link_name",
        #     )
        #     query[x]["link_doctype"] = link_doctype
        #     query[x]["link_name"] = link_name
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Contact" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["mobile_no"] = ["like", search_text]
            or_conditions["phone"] = ["like", search_text]
            or_conditions["first_name"] = ["like", search_text]
            or_conditions["email_id"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%" and filter3 != "%%":
            address = frappe.qb.DocType("Contact")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.first_name,
                    address.user,
                    address.mobile_no,
                    address.phone,
                    address.email_id,
                )
                .where(dynamic_link.link_doctype == filter2)
                .where(dynamic_link.link_name == filter3)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        if filter2 != "%%":
            address = frappe.qb.DocType("Contact")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .inner_join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.first_name,
                    address.user,
                    address.mobile_no,
                    address.phone,
                    address.email_id,
                )
                .where(dynamic_link.link_doctype == filter2)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        query = frappe.db.get_list(
            "Contact",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "first_name",
                "user",
                "mobile_no",
                "phone",
                "email_id",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        # for x in range(len(query)):

        #     link_doctype = frappe.db.get_value(
        #         "Dynamic Link",
        #         {
        #             "parent": query[x].name,
        #         },
        #         "link_doctype",
        #     )
        #     link_name = frappe.db.get_value(
        #         "Dynamic Link",
        #         {
        #             "parent": query[x].name,
        #         },
        #         "link_name",
        #     )
        #     query[x]["link_doctype"] = link_doctype
        #     query[x]["link_name"] = link_name
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Asset Category Type List & Search ############################
    if doctype == "Asset Category" and con_doc == "%%":
        query = frappe.db.get_list(
            "Asset Category",
            fields=[
                "name",
                "asset_category_name",
                "enable_cwip_accounting",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ##########################    Bin DocType   ####################################
    if doctype == "Bin" and con_doc == "%%":
        conditions1 = {}
        if search_text != "%%":
            conditions1["warehouse"] = ["like", search_text]
        query = frappe.db.get_list(
            "Bin",
            or_filters=conditions1,
            fields=[
                "warehouse",
                "item_code",
                "reserved_qty",
                "actual_qty",
                "ordered_qty",
                "indented_qty",
                "planned_qty",
                "projected_qty",
                "reserved_qty_for_production",
                "reserved_qty_for_sub_contract",
                "stock_uom",
                "valuation_rate",
                "stock_value",
            ],
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ########################     Notification Log    ################################
    if doctype == "Notification Log" and con_doc == "%%":
        conditions = {"for_user": frappe.session.user}
        if filter1 != "%%":
            conditions["read"] = filter1
        query = frappe.db.get_list(
            "Notification Log",
            filters=conditions,
            fields=[
                "name",
                "for_user",
                "from_user",
                "document_name",
                "document_type",
                "read",
                "subject",
                "email_content",
                "type",
            ],
            start=start,
            page_length=page_length,
        )

        if query:
            from .helpers import remove_html_tags

            for notification in query:
                notification["subject"] = remove_html_tags(notification["subject"])
                notification["email_content"] = remove_html_tags(
                    str(notification["email_content"])
                )

            return query
        else:
            return "لا يوجد !"

    # ------------------------------ Project Connections ------------------------------#

    if doctype == "Task" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.task(
            cur_nam,
            search_text,
            filter1,
            filter2,
            filter3,
            filter4,
            filter5,
            filter6,
            filter7,
            start,
            page_length,
        )
        return response

    if doctype == "Timesheet" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.timesheet(
            cur_nam, search_text, filter2, filter3, filter4, filter5, start, page_length
        )
        return response

    if doctype == "Sales Invoice" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.sales_invoice(
            cur_nam, search_text, filter2, filter3, filter4, filter5, start, page_length
        )
        return response

    if doctype == "Purchase Invoice" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.purchase_invoice(
            cur_nam,
            search_text,
            filter1,
            filter2,
            filter3,
            filter4,
            filter5,
            start,
            page_length,
        )
        return response

    if doctype == "Stock Entry" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.stock_entry(
            cur_nam,
            search_text,
            filter1,
            filter2,
            filter3,
            filter4,
            filter5,
            filter6,
            start,
            page_length,
        )
        return response

    if doctype == "Material Request" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.material_request(
            cur_nam,
            search_text,
            filter1,
            filter2,
            filter3,
            filter4,
            filter5,
            start,
            page_length,
        )
        return response

    if doctype == "Sales Order" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.sales_order(
            cur_nam,
            search_text,
            filter1,
            filter2,
            filter3,
            filter4,
            filter5,
            filter6.filter7,
            filter8,
            start,
            page_length,
        )
        return response

    if doctype == "Delivery Note" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.delivery_note(
            cur_nam,
            search_text,
            filter1,
            filter2,
            filter3,
            filter4,
            filter5,
            filter6.filter7,
            filter8,
            start,
            page_length,
        )
        return response

    if doctype == "Issue" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.issue(
            cur_nam, search_text, filter1, filter2, filter3, filter4, start, page_length
        )
        return response

    if doctype == "Expense Claim" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.expense_claim(
            cur_nam,
            search_text,
            filter1,
            filter2,
            filter3,
            filter4,
            filter5,
            start,
            page_length,
        )
        return response

    if doctype == "BOM" and con_doc == "Project" and cur_nam != "%%":
        response = project_connections.bom(cur_nam, start, page_length)
        return response

    # ------------------------ End Project Connections ------------------------- #


@frappe.whitelist(methods=["GET"])
def get_actual_qty(item_code=None, warehouse=None):
    if not (item_code and warehouse):
        response = frappe.response["message"] = {
            "success_key": False,
            "message": "Please Provide a warehouse and an item code",
        }
        return response

    try:
        query = frappe.db.sql(
            f"""
            SELECT actual_qty
            FROM `tabBin`
            WHERE warehouse =  '{warehouse}'
            AND item_code = '{item_code}'
        """
        )
        if query:
            response = frappe.response["message"] = {
                "success_key": True,
                "actual_qty": query[0][0],
            }
            return response
        else:
            response = frappe.response["message"] = {
                "success_key": False,
                "message": "There is no actual quantity for the provided information",
            }
        return response

    except:
        response = frappe.response["message"] = {
            "success_key": False,
            "message": "Something Went Wrong Please Try Again",
        }
        return response


@frappe.whitelist(methods=["GET"])
def get_item_uoms(item_code):
    try:
        item = frappe.get_doc("Item", item_code)
        uoms = []
        for uom in item.uoms:
            uoms.append(
                dict(
                    name=uom.name, uom=uom.uom, conversion_factor=uom.conversion_factor
                )
            )
        response = frappe.response["message"] = uoms
        return response

    except:
        response = frappe.response["message"] = {
            "success": False,
            "error": "Can't found an item with the provided item code",
        }
        return response


@frappe.whitelist(methods=["GET"])
def get_item_list(
        allow_sales=None,
        allow_purchase=None,
        search_text="%%",
        price_list="%%",
        start=0,
        page_length=5,
):
    conditions = ""
    if allow_purchase is not None:
        conditions += f" and tabItem.is_purchase_item = {allow_purchase} "

    if allow_sales is not None:
        conditions += f" and tabItem.is_sales_item = {allow_sales}"

    if search_text != "%%":
        items = frappe.db.sql(
            f""" select tabItem.name as name ,
                                                    tabItem.item_code as item_code,
                                                    tabItem.is_sales_item,
                                                    tabItem.is_purchase_item,
                                                    tabItem.item_name as item_name,
                                                    tabItem.item_group as item_group,
                                                    tabItem.stock_uom as stock_uom,
                                                    tabItem.image as image,
                                                    tabItem.sales_uom as sales_uom,
                                                    ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                                    ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax`
                                                    where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                                    from tabItem
                                                    where tabItem.name like '%{search_text}%'
                                                    or tabItem.item_name like '%{search_text}%'
                                                    {conditions}
                                                    and tabItem.disabled = 0
                                                    LIMIT {start}, {page_length}""",
            as_dict=True,
        )
        result = []
        for item_dict in items:
            if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                net_rate = item_dict.price_list_rate * (
                        1 + (item_dict.tax_percent / 100)
                )
                vat_value = net_rate - item_dict.price_list_rate
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "item_group": item_dict.item_group,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": net_rate,
                    "vat_value": vat_value,
                }
                result.append(data)
            else:
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "item_group": item_dict.item_group,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": item_dict.price_list_rate,
                }
                result.append(data)

        if items:
            return result
        else:
            return "لا يوجد منتجات !"
    else:
        items = frappe.db.sql(
            f""" select tabItem.name as name,
                                        tabItem.item_code as item_code,
                                        tabItem.item_name as item_name,
                                        tabItem.is_sales_item,
                                        tabItem.is_purchase_item,
                                        tabItem.item_group as item_group,
                                        tabItem.stock_uom as stock_uom,
                                        tabItem.image as image,
                                        tabItem.sales_uom as sales_uom,
                                        ifnull((select max(price_list_rate) from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                        ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax`
                                        where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                        from tabItem
                                        where tabItem.disabled = 0
                                        {conditions}
                                        LIMIT {start},{page_length} """,
            as_dict=True,
        )

        result = []
        for item_dict in items:
            if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                net_rate = item_dict.price_list_rate * (
                        1 + (item_dict.tax_percent / 100)
                )
                vat_value = net_rate - item_dict.price_list_rate
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "item_group": item_dict.item_group,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": net_rate,
                    "vat_value": vat_value,
                }
                result.append(data)
            else:
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "item_group": item_dict.item_group,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": item_dict.price_list_rate,
                }
                result.append(data)

        if items:
            return result
        else:
            return "لا يوجد منتجات !"


@frappe.whitelist(methods=["GET"])
def get_reports(module):
    mobile_user = frappe.db.get_all(
        "Mobile User", filters={"user": frappe.session.user}
    )
    if not mobile_user:
        frappe.throw(
            "The logged in user is not a mobile user.",
            frappe.exceptions.ValidationError,
        )

    mobile_user_id = mobile_user[0]["name"]
    mobile_reports = frappe.db.get_all(
        "Mobile Reports Table",
        filters={"parent": mobile_user_id, "module": module},
        fields=["report_name"],
    )

    if mobile_reports:
        return mobile_reports

    frappe.throw("There is no reports to show", frappe.exceptions.DoesNotExistError)


@frappe.whitelist(methods=["GET"])
def get_custom_fields(doctype: str) -> list:
    custom_fields = frappe.db.get_all(
        "Custom Field",
        filters={"dt": doctype},
        fields=[
            "name",
            "dt",
            "label",
            "fieldtype",
            "fieldname",
            "read_only",
            "reqd",
            "default",
            "non_negative",
            "options",
            "fetch_from",
        ],
    )
    if custom_fields:
        return custom_fields
    frappe.throw("No custom fields found!", frappe.exceptions.DoesNotExistError)


@frappe.whitelist(methods=["GET"])
def get_about_us():
    terms_of_service = frappe.get_doc("Terms and Conditions", "About Us")
    if terms_of_service:
        terms_of_service.terms = remove_html_tags(str(terms_of_service.terms))
        return terms_of_service.terms
    return "Please add about us data."


@frappe.whitelist(methods=["GET"])
def get_faqs(tag=None):
    filters = dict(frappe.local.request.args) or {}
    faqs = frappe.get_all("FAQ", fields=["question", "answer", "tag"], filters=filters)

    if not faqs:
        frappe.response['http_status_code'] = 404

    for faq in faqs:
        faq["answer_without_html"] = remove_html_tags(str(faq["answer"]))
    return faqs


@frappe.whitelist()
def get_activity_log():
    filters = frappe.local.request.args or {}
    filters = frappe.parse_json(filters)

    mandatory_filters = ['doctypes', 'from_date', 'to_date', 'length']
    for filter in mandatory_filters:
        if filter not in filters:
            frappe.response['http_status_code'] = 400
            return f"`{filter}` filter is mandatory"

    filters['doctypes'] = ", ".join([f"'{doctype}'" for doctype in filters['doctypes'].split(',')])

    results = frappe.db.sql(f"""
        SELECT 
            reference_doctype as doctype,
            reference_name as id,
            communication_date as `date`
        FROM 
            `tabActivity Log`
        WHERE 
            reference_doctype in ({filters["doctypes"]})
            AND communication_date Between '{filters["from_date"]}' and '{filters["to_date"]}'
        ORDER BY 
            communication_date DESC
        LIMIT {filters['length']}
    """, as_dict=True)

    frappe.response['data'] = results


@frappe.whitelist(methods=['GET'], allow_guest=True)
def sales_invoices():
    """
    response in case failed
    {
        is_success: false,
        message: "dummy message"
    }

    response in case successful
    {

        is_success: true,
        data: {
            count: 342,
            stock_entries: [{}, {}]
        }
    }

    """

    filters = dict(frappe.local.request.args)
    conditions = []
    if filters.get('from'):
        conditions.append(f"posting_date >= '{filters.get('from')}'")

    if filters.get('to'):
        conditions.append(f"posting_date <= '{filters.get('to')}'")

    if filters.get('is_return'):
        conditions.append(f"is_return = {filters.get('is_return')}")

    if filters.get('status'):
        # statuses = "(" + ", ".join([f"{status}" for status in filters.get("status").split(',')]) + ")"
        statuses = f"({filters.get('status')})"
        conditions.append(f"docstatus IN {statuses}")

    conditions = " AND ".join(conditions)

    query = f"""
        SELECT name, grand_total
        FROM `tabSales Invoice`
        WHERE {conditions}
    """

    sales_invoices = frappe.db.sql(query, as_dict=True)

    frappe.response["data"] = {
        "sales_invoices": sales_invoices,
        "count": len(sales_invoices),
        "total": sum(map(lambda x: Decimal(str(x['grand_total'])), sales_invoices))
    }
    frappe.response['is_success'] = True


@frappe.whitelist(methods=['GET'], allow_guest=True)
def customer_visits():
    """
    response in case failed must bve like this
    {
        is_success: false,
        message: "dummy message"
    }

    response in case successful
    {

        is_success: true,
        data: {
            count: 342,
            total: 423,
            customer_visits: [{}, {}]
        }
    }

    """

    filters = dict(frappe.local.request.args)
    conditions = []
    if filters.get('from'):
        conditions.append(f"posting_date >= '{filters.get('from')}'")

    if filters.get('to'):
        conditions.append(f"posting_date <= '{filters.get('to')}'")

    if filters.get('status'):
        statuses = f"({filters.get('status')})"
        conditions.append(f"docstatus IN {statuses}")

    conditions = " AND ".join(conditions)

    customer_visits = frappe.db.sql(f"""
        SELECT name
        FROM `tabCustomer Visit`
        WHERE {conditions}
    """, as_dict=True)

    frappe.response["data"] = {
        "customer_visits": customer_visits,
        "count": len(customer_visits)
    }
    frappe.response['is_success'] = True


@frappe.whitelist(methods=['GET'], allow_guest=True)
def payment_entries():
    """
    response in case failed must bve like this
    {
        is_success: false,
        message: "dummy message"
    }

    response in case successful
    {

        is_success: true,
        data: {
            count: 342,
            total: 423,
            payment_entries: [{}, {}]
        }
    }

    """

    filters = dict(frappe.local.request.args)
    conditions = []
    if filters.get('from'):
        conditions.append(f"posting_date >= '{filters.get('from')}'")

    if filters.get('to'):
        conditions.append(f"posting_date <= '{filters.get('to')}'")

    if filters.get('status'):
        statuses = f"({filters.get('status')})"
        conditions.append(f"docstatus IN {statuses}")

    conditions = " AND ".join(conditions)
    payment_entries = frappe.db.sql(f"""
        SELECT name, paid_amount
        FROM `tabPayment Entry`
        WHERE {conditions}
    """, as_dict=True)

    frappe.response["data"] = {
        "payment_entries": payment_entries,
        "count": len(payment_entries),
        "total": sum(map(lambda x: Decimal(str(x['paid_amount'])), payment_entries)),
    }
    frappe.response['is_success'] = True


@frappe.whitelist(methods=['GET'], allow_guest=True)
def quotations():
    """
    response in case failed must bve like this
    {
        is_success: false,
        message: "dummy message"
    }

    response in case successful
    {

        is_success: true,
        data: {
            count: 342,
            total: 423,
            quotations: [{}, {}]
        }
    }

    """

    filters = dict(frappe.local.request.args)
    conditions = []
    if filters.get('from'):
        conditions.append(f"transaction_date >= '{filters.get('from')}'")

    if filters.get('to'):
        conditions.append(f"transaction_date <= '{filters.get('to')}'")

    if filters.get('status'):
        statuses = f"({filters.get('status')})"
        conditions.append(f"docstatus IN {statuses}")

    conditions = " AND ".join(conditions)

    quotations = frappe.db.sql(f"""
        SELECT name, grand_total
        FROM `tabQuotation`
        WHERE {conditions}
    """, as_dict=True)

    frappe.response["data"] = {
        "quotations": quotations,
        "count": len(quotations),
        "total": sum(map(lambda x: Decimal(str(x['grand_total'])), quotations)),
    }
    frappe.response['is_success'] = True


@frappe.whitelist(methods=['GET'], allow_guest=True)
def sales_orders():
    """
    response in case failed must bve like this
    {
        is_success: false,
        message: "dummy message"
    }

    response in case successful
    {

        is_success: true,
        data: {
            count: 342,
            total: 423,
            sales_orders: [{}, {}]
        }
    }

    """

    filters = dict(frappe.local.request.args)
    conditions = []
    if filters.get('from'):
        conditions.append(f"transaction_date >= '{filters.get('from')}'")

    if filters.get('to'):
        conditions.append(f"transaction_date <= '{filters.get('to')}'")

    if filters.get('status'):
        statuses = f"({filters.get('status')})"
        conditions.append(f"docstatus IN {statuses}")

    conditions = " AND ".join(conditions)

    sales_orders = frappe.db.sql(f"""
        SELECT name, grand_total
        FROM `tabSales Order`
        WHERE {conditions}
    """, as_dict=True)

    frappe.response["data"] = {
        "sales_orders": sales_orders,
        "count": len(sales_orders),
        "total": sum(map(lambda x: Decimal(str(x['grand_total'])), sales_orders)),
    }
    frappe.response['is_success'] = True


@frappe.whitelist(methods=['GET'], allow_guest=True)
def delivery_notes():
    """
        response in case failed must bve like this
        {
            is_success: false,
            message: "dummy message"
        }

        response in case successful
        {

            is_success: true,
            data: {
                count: 342,
                total: 423,
                delivery_notes: [{}, {}]
            }
        }

        """

    filters = dict(frappe.local.request.args)
    conditions = []
    if filters.get('from'):
        conditions.append(f"posting_date >= '{filters.get('from')}'")

    if filters.get('to'):
        conditions.append(f"posting_date <= '{filters.get('to')}'")

    if filters.get('status'):
        statuses = f"({filters.get('status')})"
        conditions.append(f"docstatus IN {statuses}")

    conditions = " AND ".join(conditions)

    delivery_notes = frappe.db.sql(f"""
            SELECT name, grand_total
            FROM `tabDelivery Note`
            WHERE {conditions}
        """, as_dict=True)

    frappe.response["data"] = {
        "delivery_notes": delivery_notes,
        "count": len(delivery_notes),
        "total": sum(map(lambda x: Decimal(str(x['grand_total'])), delivery_notes)),
    }
    frappe.response['is_success'] = True


@frappe.whitelist(methods=['GET'], allow_guest=True)
def stock_entries():
    """
        response in case failed must bve like this
        {
            is_success: false,
            message: "dummy message"
        }

        response in case successful
        {

            is_success: true,
            data: {
                count: 342,
                total: 423,
                stock_entries: [{}, {}]
            }
        }
    """

    filters = dict(frappe.local.request.args)
    conditions = []
    if filters.get('from'):
        conditions.append(f"posting_date >= '{filters.get('from')}'")

    if filters.get('to'):
        conditions.append(f"posting_date <= '{filters.get('to')}'")

    if filters.get('is_return'):
        conditions.append(f"is_return = {filters.get('is_return')}")

    if filters.get('status'):
        statuses = f"({filters.get('status')})"
        conditions.append(f"docstatus IN {statuses}")

    conditions = " AND ".join(conditions)
    stock_entries = frappe.db.sql(f"""
            SELECT name, total_amount
            FROM `tabStock Entry`
            WHERE {conditions}
        """, as_dict=True)

    frappe.response["data"] = {
        "stock_entries": stock_entries,
        "count": len(stock_entries),
        "total": sum(map(lambda x: Decimal(str(x['total_amount'])), stock_entries)),
    }
    frappe.response['is_success'] = True

