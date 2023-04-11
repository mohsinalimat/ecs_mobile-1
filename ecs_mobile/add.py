import frappe
import traceback
import unicodedata
from frappe import auth
import datetime
import json, ast
from frappe import _
import requests


@frappe.whitelist()
def bom(**kwargs):
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
def project(**kwargs):
    project = frappe.get_doc(kwargs["data"])
    project.insert()
    project_name = project.name
    frappe.db.commit()
    if project:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "project": project_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist()
def task(**kwargs):
    task = frappe.get_doc(kwargs["data"])
    task.insert()
    task_name = task.name
    frappe.db.commit()
    if task_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "task": task_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist()
def timesheet(**kwargs):
    timesheet = frappe.get_doc(kwargs["data"])
    timesheet.insert()
    timesheet_name = timesheet.name
    frappe.db.commit()
    if timesheet_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "timesheet": timesheet_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist()
def lead(**kwargs):
    lead = frappe.get_doc(kwargs["data"])
    lead.insert()
    lead_name = lead.name
    frappe.db.commit()
    if lead_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "lead": lead_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def opportunity(**kwargs):
    opportunity = frappe.get_doc(kwargs["data"])

    opportunity.insert()
    opportunity_name = opportunity.name
    frappe.db.commit()
    if opportunity_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "opportunity": opportunity_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def quotation(**kwargs):
    quotation = frappe.get_doc(kwargs["data"])
    quotation.insert()
    quotation_name = quotation.name
    frappe.db.commit()
    if quotation_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "quotation": quotation_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def customer(**kwargs):
    customer = frappe.new_doc("Customer")
    customer.customer_name = kwargs["data"].get("customer_name", None)
    customer.lead_name = kwargs["data"].get("lead_name", None)
    customer.customer_type = kwargs["data"].get("customer_type", None)
    customer.customer_group = kwargs["data"].get("customer_group", None)
    customer.territory = kwargs["data"].get("territory", None)
    customer.market_segment = kwargs["data"].get("market_segment", None)
    customer.industry = kwargs["data"].get("industry", None)
    customer.tax_id = kwargs["data"].get("tax_id", None)
    customer.default_currency = kwargs["data"].get("default_currency", None)
    customer.default_price_list = kwargs["data"].get("default_price_list", None)
    customer.default_sales_partner = kwargs["data"].get("default_sales_partner", None)
    customer.longitude = kwargs["data"].get("longitude", None)
    customer.latitude = kwargs["data"].get("latitude", None)
    customer.append("credit_limits", kwargs["data"].get("credit_limits")[0])
    customer.insert()
    customer_name = customer.name

    links = [
        {
            "link_doctype": "Customer",
            "link_name": customer_name,
            "link_title": customer_name,
        }
    ]
    emails = [{"email_id": kwargs["data"].get("email_id"), "is_primary": 1}]

    contacts = [
        {
            "phone": kwargs["data"].get("mobile_no"),
            "is_primary_phone": 1,
            "is_primary_mobile_no": 1,
        }
    ]

    contact = frappe.get_doc(
        {
            "doctype": "Contact",
            "first_name": kwargs["data"]["customer_name"],
            "links": links,
            "email_ids": emails,
            "phone_nos": contacts,
            "is_primary_contact": 1,
            "is_billing_contact": 1,
        }
    )
    if (
        kwargs["data"].get("customer_name")
        and kwargs["data"].get("email_id")
        and kwargs["data"].get("mobile_no")
    ):

        contact.insert()
        customer.customer_primary_contact = contact.name

    address = frappe.new_doc("Address")
    address_link = [
        {
            "link_doctype": "Customer",
            "link_name": customer_name,
            "link_title": customer_name,
        }
    ]
    address.address_title = kwargs["data"].get("customer_name", None)
    address.address_line1 = kwargs["data"].get("address_line1", None)
    address.city = kwargs["data"].get("city", None)
    address.country = kwargs["data"].get("country", None)
    address.address_type = "Billing"
    address.is_primary_address_type = 1
    address.is_shipping_address_type = 1

    if (
        kwargs["data"].get("customer_name")
        and kwargs["data"].get("address_line1")
        and kwargs["data"].get("city")
        and kwargs["data"].get("address_type", "Billing")
    ):
        address.insert()
        customer.customer_primary_address = address.name
    customer.save()
    

    frappe.db.commit()
    if customer_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "customer": customer_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def sales_order(**kwargs):

    sales_order = frappe.get_doc(kwargs["data"])

    sales_order.insert()
    sales_order_name = sales_order.name
    frappe.db.commit()
    if sales_order_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "sales_order": sales_order_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def sales_invoice(**kwargs):
    sales_invoice = frappe.get_doc(kwargs["data"])

    sales_invoice.insert()
    sales_invoice_name = sales_invoice.name
    frappe.db.commit()
    if sales_invoice_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "sales_invoice": sales_invoice_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def payment_entry(**kwargs):
    payment_entry = frappe.get_doc(kwargs["data"])

    payment_entry.insert()
    payment_entry_name = payment_entry.name
    frappe.db.commit()
    if payment_entry_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "payment_entry": payment_entry_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def loan_application(**kwargs):
    loan_application_data = frappe.get_doc(kwargs["data"])
    loan_application_data.insert()
    loan_application_data_name = loan_application_data.name
    frappe.db.commit()
    if loan_application_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "loan_application_data_name": loan_application_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def journal_entry(**kwargs):
    journal_entry_data = frappe.get_doc(kwargs["data"])
    journal_entry_data.insert()
    ejournal_entry_data_name = journal_entry_data.name
    frappe.db.commit()
    if ejournal_entry_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "ejournal_entry_data_name": ejournal_entry_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def issue(**kwargs):
    issue = frappe.get_doc(kwargs["data"])

    issue.insert()
    issue_name = issue.name
    frappe.db.commit()
    if issue_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة الصنف بنجاح!",
            "issue": issue_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة الصنف . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def item(**kwargs):
    item = frappe.get_doc(kwargs["data"])

    item.insert()
    item_name = item.name
    frappe.db.commit()
    if item_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة الصنف بنجاح!",
            "item": item_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة الصنف . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def stock_entry(**kwargs):
    stock_entry = frappe.get_doc(kwargs["data"])
    stock_entry.insert()
    stock_entry_name = stock_entry.name
    frappe.db.commit()

    if stock_entry_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "stock_entry": stock_entry_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def delivery_note(**kwargs):
    delivery_note = frappe.get_doc(kwargs["data"])
    delivery_note.insert()
    delivery_note_name = delivery_note.name
    frappe.db.commit()
    if delivery_note_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "delivery_note": delivery_note_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def purchase_receipt(**kwargs):
    purchase_receipt = frappe.get_doc(kwargs["data"])
    purchase_receipt.insert()
    purchase_receipt_name = purchase_receipt.name
    frappe.db.commit()
    if purchase_receipt_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_receipt": purchase_receipt_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def comment(**kwargs):
    comment = frappe.get_doc(kwargs["data"])

    comment.insert()
    comment_name = comment.name
    frappe.db.commit()
    if comment_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة التعليق بنجاح!",
            "comment": comment_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة التعليق . برجاء المحاولة مرة اخري!"





@frappe.whitelist()
def supplier_test(**kwargs):
    supplier = frappe.new_doc("Supplier")
    supplier.supplier_name = kwargs["data"]["supplier_name"]
    supplier.supplier_type = kwargs["data"]["supplier_type"]
    supplier.supplier_group = kwargs["data"]["supplier_group"]
    supplier.tax_id = kwargs["data"]["tax_id"]
    supplier.default_currency = kwargs["data"]["default_currency"]
    supplier.default_price_list = kwargs["data"]["default_price_list"]
    supplier.payment_terms = kwargs["data"]["payment_terms"]
    supplier.country = kwargs["data"]["country"]
    supplier.insert()
    supplier_name = supplier.name

    links = [
        {
            "link_doctype": "Supplier",
            "link_name": supplier_name,
            "link_title": supplier_name,
        }
    ]

    emails = [{"email_id": kwargs["data"]["email_id"], "is_primary": 1}]

    contacts = [
        {
            "phone": kwargs["data"]["mobile_no"],
            "is_primary_phone": 1,
            "is_primary_mobile_no": 1,
        }
    ]

    contact = frappe.get_doc(
        {
            "doctype": "Contact",
            "first_name": kwargs["data"]["supplier_name"],
            "links": links,
            "email_ids": emails,
            "phone_nos": contacts,
            "is_primary_contact": 1,
            "is_billing_contact": 1,
        }
    )
    contact.insert()

    address = frappe.get_doc(
        {
            "doctype": "Address",
            "address_title": kwargs["data"]["supplier_name"],
            "address_line1": kwargs["data"]["address_line1"],
            "city": kwargs["data"]["city"],
            "country": kwargs["data"]["country"],
            "address_type": "Billing",
            "links": links,
            "is_primary_address_type": 1,
            "is_shipping_address_type": 1,
        }
    )
    address.insert()

    supplier.supplier_primary_address = address.name
    supplier.supplier_primary_contact = contact.name
    supplier.save()

    frappe.db.commit()
    if supplier_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "name": supplier_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def supplier_quotation(**kwargs):
    s_quotation = frappe.get_doc(kwargs["data"])

    s_quotation.insert()
    quotation_name = s_quotation.name
    frappe.db.commit()
    if s_quotation:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "supplier_quotation_name": quotation_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def purchase_order(**kwargs):
    p_order = frappe.get_doc(kwargs["data"])
    p_order.insert()
    purchase_order_name = p_order.name
    frappe.db.commit()
    if purchase_order_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_order_name": purchase_order_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def purchase_invoice(**kwargs):
    purchase_invoice = frappe.get_doc(kwargs["data"])

    purchase_invoice.insert()
    purchase_invoice_name = purchase_invoice.name
    frappe.db.commit()
    if purchase_invoice_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_invoice_name": purchase_invoice_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def purchsae_receipt(**kwargs):
    purchsae_receipt_data = frappe.get_doc(kwargs["data"])

    purchsae_receipt_data.insert()
    purchsae_receipt_data_name = purchsae_receipt_data.name
    frappe.db.commit()
    if purchsae_receipt_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchsae_receipt_name": purchsae_receipt_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def material_request(**kwargs):
    material_request_data = frappe.get_doc(kwargs["data"])
    material_request_data.insert()
    material_request_data_name = material_request_data.name
    frappe.db.commit()
    if material_request_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "material_request_name": material_request_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def leave_application(**kwargs):
    leave_application_data = frappe.get_doc(kwargs["data"])

    leave_application_data.insert()
    leave_application_data_name = leave_application_data.name
    frappe.db.commit()
    if leave_application_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "leave_application_name": leave_application_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def supplier(**kwargs):
    supplier = frappe.new_doc("Supplier")
    supplier.supplier_name = kwargs["data"]["supplier_name"]
    supplier.supplier_type = kwargs["data"]["supplier_type"]
    supplier.supplier_group = kwargs["data"]["supplier_group"]
    if kwargs["data"].get("tax_id"):
        supplier.tax_id = kwargs["data"]["tax_id"]
    if kwargs["data"].get("default_currency"):
        supplier.default_currency = kwargs["data"]["default_currency"]
    if kwargs["data"].get("default_price_list"):
        supplier.default_price_list = kwargs["data"]["default_price_list"]
    if kwargs["data"].get("payment_terms"):
        supplier.payment_terms = kwargs["data"]["payment_terms"]
    if kwargs["data"].get("country"):
        supplier.country = kwargs["data"]["country"]
    supplier.insert()
    supplier_name = supplier.name

    links = [
        {
            "link_doctype": "Supplier",
            "link_name": supplier_name,
            "link_title": supplier_name,
        }
    ]
    emails = [{"email_id": kwargs["data"].get("email_id"), "is_primary": 1}]

    contacts = [
        {
            "phone": kwargs["data"].get("mobile_no"),
            "is_primary_phone": 1,
            "is_primary_mobile_no": 1,
        }
    ]

    contact = frappe.get_doc(
        {
            "doctype": "Contact",
            "first_name": kwargs["data"]["supplier_name"],
            "links": links,
            "email_ids": emails,
            "phone_nos": contacts,
            "is_primary_contact": 1,
            "is_billing_contact": 1,
        }
    )
    if (
        kwargs["data"].get("supplier_name")
        and kwargs["data"].get("email_id")
        and kwargs["data"].get("mobile_no")
    ):

        contact.insert()
        supplier.supplier_primary_contact = contact.name

    if (
        kwargs["data"].get("supplier_name")
        and kwargs["data"].get("address_line1")
        and kwargs["data"].get("city")
        and kwargs["data"].get("address_type", "Billing")
    ):
        address = frappe.get_doc(
            {
                "doctype": "Address",
                "address_title": kwargs["data"]["supplier_name"],
                "address_line1": kwargs["data"]["address_line1"],
                "city": kwargs["data"]["city"],
                "country": kwargs["data"].get("country", None),
                "address_type": kwargs["data"].get("address_type", "Billing"),
                "links": links,
                "is_primary_address_type": 1,
                "is_shipping_address_type": 1,
            }
        )
        address.insert()
        supplier.supplier_primary_address = address.name

    supplier.save()

    frappe.db.commit()
    if supplier_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "name": supplier_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def employee_checkin(**kwargs):
    employee_checkin_data = frappe.get_doc(kwargs["data"])

    employee_checkin_data.insert()
    employee_checkin_data_name = employee_checkin_data.name
    frappe.db.commit()
    if employee_checkin_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "employee_checkin_data_name": employee_checkin_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def employee(**kwargs):
    employee_data = frappe.new_doc("Employee")
    employee_data.first_name = kwargs["data"].get("first_name", None)
    employee_data.last_name = kwargs["data"].get("last_name", None)
    employee_data.gender = kwargs["data"].get("gender", None)
    employee_data.date_of_birth = kwargs["data"].get("date_of_birth", None)
    employee_data.company = kwargs["data"].get("company", None)
    employee_data.status = kwargs["data"].get("status", None)
    employee_data.department = kwargs["data"].get("department", None)
    employee_data.designation = kwargs["data"].get("designation", None)
    employee_data.branch = kwargs["data"].get("branch", None)
    employee_data.employment_type = kwargs["data"].get("employment_type", None)
    employee_data.date_of_joining = kwargs["data"].get("date_of_joining", None)
    employee_data.leave_approver = kwargs["data"].get("leave_approver", None)
    employee_data.expense_approver = kwargs["data"].get("expense_approver", None)
    employee_data.cell_number = kwargs["data"].get("cell_number", None)
    employee_data.company_email = kwargs["data"].get("company_email", None)
    employee_data.personal_email = kwargs["data"].get("personal_email", None)
    employee_data.prefered_email = kwargs["data"].get("prefered_email", None)
    employee_data.current_address = kwargs["data"].get("current_address", None)
    employee_data.permanent_address = kwargs["data"].get("permanent_address", None)
    employee_data.holiday_list = kwargs["data"].get("holiday_list", None)
    employee_data.default_shift = kwargs["data"].get("default_shift", None)
    if kwargs["data"].get("user_id"):
        employee_data.user_id = kwargs["data"].get("user_id")
        employee_data.create_user_permission = 1
    if kwargs["data"].get("attendance_device_id"):
        employee_data.attendance_device_id = kwargs["data"].get("attendance_device_id")
        employee_data.employee_number = kwargs["data"].get("attendance_device_id")
    employee_data.insert()
    employee_data_name = employee_data.name
    frappe.db.commit()
    if employee_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "employee_data_name": employee_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def attendance_request(**kwargs):
    attendance_request_data = frappe.get_doc(kwargs["data"])

    attendance_request_data.insert()
    attendance_request_data_name = attendance_request_data.name
    frappe.db.commit()
    if attendance_request_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "attendance_request_data_name": attendance_request_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def employee_advance(**kwargs):
    employee_advance_data = frappe.get_doc(kwargs["data"])

    employee_advance_data.insert()
    employee_advance_data_name = employee_advance_data.name
    frappe.db.commit()
    if employee_advance_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "employee_advance_data_name": employee_advance_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def expense_claim(**kwargs):
    expense_claim_data = frappe.get_doc(kwargs["data"])
    expense_claim_data.insert()
    expense_claim_data_name = expense_claim_data.name
    frappe.db.commit()
    if expense_claim_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "expense_claim_data_name": expense_claim_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def customer_visit(**kwargs):
    customer_visit_data = frappe.get_doc(kwargs["data"])
    customer_visit_data.insert()
    customer_visit_data_name = customer_visit_data.name
    frappe.db.commit()
    if customer_visit_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "customer_visit_data_name": customer_visit_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def address(**kwargs):
    if kwargs["data"].get("is_primary_address", 0):
        addresses = frappe.db.get_list(
            "Address",
            filters={
                "link_doctype": kwargs["data"]["link_doctype"],
                "link_name": kwargs["data"]["link_name"],
            },
        )
        for row in addresses:
            cur_address = frappe.get_doc("Address", row.name)
            if cur_address.is_primary_address == 1:
                cur_address.is_primary_address = 0
                cur_address.save()

    links = [
        {
            "doctype": "Dynamic Link",
            "link_doctype": kwargs["data"]["link_doctype"],
            "link_name": kwargs["data"]["link_name"],
        }
    ]

    address = frappe.get_doc(
        {
            "doctype": "Address",
            "is_primary_address": kwargs["data"].get("is_primary_address", 0),
            "address_title": kwargs["data"].get("address_title", None),
            "address_type": kwargs["data"].get("address_type", None),
            "address_line1": kwargs["data"].get("address_line1", None),
            "city": kwargs["data"].get("city", None),
            "country": kwargs["data"].get("country", None),
            "longitude": kwargs["data"].get("longitude", None),
            "latitude": kwargs["data"].get("latitude", None),
            "links": links,
        }
    )
    address.insert()
    if (
        kwargs["data"].get("is_primary_address", 0)
        and kwargs["data"]["link_doctype"] == "Customer"
    ):
        customer = frappe.get_doc("Customer", kwargs["data"]["link_name"])
        customer.customer_primary_address = address.name
        customer.save()

    if (
        kwargs["data"].get("is_primary_address", 0)
        and kwargs["data"]["link_doctype"] == "Supplier"
    ):
        customer = frappe.get_doc("Supplier", kwargs["data"]["link_name"])
        customer.supplier_primary_address = address.name
        customer.save()
    address.links = links
    frappe.db.commit()
    address_name = address.name
    if address_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "address_name": address_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def make_primary_address(**kwargs):
    if kwargs["data"].get("is_primary_address", 0):
        addresses = frappe.db.get_list(
            "Address",
            filters={
                "link_doctype": kwargs["data"]["link_doctype"],
                "link_name": kwargs["data"]["link_name"],
            },
        )
        for row in addresses:
            cur_address = frappe.get_doc("Address", row.name)
            if cur_address.is_primary_address == 1:
                cur_address.is_primary_address = 0
                cur_address.save()

    if kwargs["data"]["link_doctype"] == "Customer":
        customer = frappe.get_doc("Customer", kwargs["data"]["link_name"])
        customer.customer_primary_address = kwargs["data"]["name"]
        customer.save()
        customer_name = customer.name
        if customer_name:
            message = frappe.response["message"] = {
                "success_key": True,
                "message": "تم اضافة المعاملة بنجاح!",
                "customer_name": customer_name,
            }
            return message

    if kwargs["data"]["link_doctype"] == "Supplier":
        customer = frappe.get_doc("Supplier", kwargs["data"]["link_name"])
        customer.supplier_primary_address = kwargs["data"]["name"]
        customer.save()
        customer_name = customer.name
        if customer_name:
            message = frappe.response["message"] = {
                "success_key": True,
                "message": "تم اضافة المعاملة بنجاح!",
                "customer_name": customer_name,
            }
            return message
    frappe.db.commit()

    return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def contact(**kwargs):
    contact_data = frappe.get_doc(kwargs["data"])
    contact_data.insert()
    contact_data_name = contact_data.name
    frappe.db.commit()
    if contact_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "contact_data_name": contact_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(methods=["POST"])
def workflow(**kwargs):
    if "data" not in kwargs:
        frappe.throw("data key must be in the body.", frappe.exceptions.ValidationError)

    data = kwargs["data"]
    workflow = frappe.get_doc(data)
    workflow.insert()

    response = {"succss_key": True, "workflow": workflow.name}
    return response