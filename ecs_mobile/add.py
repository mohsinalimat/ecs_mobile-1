from __future__ import unicode_literals
import frappe
import traceback
import unicodedata
from frappe import auth
import datetime
import json, ast
from frappe import _
import requests


@frappe.whitelist(allow_guest=True)
def lead(**kwargs):
    lead =frappe.get_doc(kwargs['data'])

    lead.insert()
    lead_name = lead.name
    frappe.db.commit()
    if (lead_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "lead": lead_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def opportunity(**kwargs):
    opportunity =frappe.get_doc(kwargs['data'])

    opportunity.insert()
    opportunity_name = opportunity.name
    frappe.db.commit()
    if (opportunity_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "opportunity": opportunity_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def quotation(**kwargs):
    quotation =frappe.get_doc(kwargs['data'])

    quotation.insert()
    quotation_name = quotation.name
    frappe.db.commit()
    if (quotation_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "quotation": quotation_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def customer(**kwargs):

    customer = frappe.new_doc('Customer')
    customer.customer_name =kwargs['data']['customer_name']
    customer.customer_type =kwargs['data']['customer_type']
    customer.customer_group =kwargs['data']['customer_group']
    customer.territory = kwargs['data']['territory']
    customer.market_segment = kwargs['data']['market_segment']
    customer.industry = kwargs['data']['industry']
    customer.tax_id = kwargs['data']['tax_id']
    customer.default_currency = kwargs['data']['default_currency']
    customer.default_price_list = kwargs['data']['default_price_list']
    customer.default_sales_partner = kwargs['data']['default_sales_partner']
    #customer.credit_limits = kwargs['data']['credit_limits']
    customer.insert()
    customer_name = customer.name

    contact = frappe.new_doc('Contact')
    contact_link = [{
        "link_doctype": "Customer",
        "link_name": customer_name,
        "link_title": customer_name
    }]
    contact.first_name = kwargs['data']['customer_name']
    contact.email_id = kwargs['data']['email_id']
    contact.mobile_no = kwargs['data']['mobile_no']
    contact.is_primary_contact = 1
    contact.is_billing_contact = 1
    #contact.links = contact_link
    contact.insert()

    address = frappe.new_doc('Address')
    address_link = [{
        "link_doctype": "Customer",
        "link_name": customer_name,
        "link_title": customer_name
    }]
    address.address_title = kwargs['data']['customer_name']
    address.address_line1 = kwargs['data']['address_line1']
    address.city = kwargs['data']['city']
    address.country = kwargs['data']['country']
    address.address_type = "Billing"
    address.is_primary_address_type = 1
    address.is_shipping_address_type = 1
    #address.links = address_link
    address.insert()





    #customer =frappe.get_doc(kwargs['data'])

    #customer.insert()

    frappe.db.commit()
    if (customer_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "customer": customer_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def sales_order(**kwargs):
    
    sales_order =frappe.get_doc(kwargs['data'])

    sales_order.insert()
    sales_order_name = sales_order.name
    frappe.db.commit()
    if (sales_order_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "sales_order": sales_order_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def sales_invoice(**kwargs):
    sales_invoice =frappe.get_doc(kwargs['data'])

    sales_invoice.insert()
    sales_invoice_name = sales_invoice.name
    frappe.db.commit()
    if (sales_invoice_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "sales_invoice": sales_invoice_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def payment_entry(**kwargs):
    payment_entry =frappe.get_doc(kwargs['data'])

    payment_entry.insert()
    payment_entry_name = payment_entry.name
    frappe.db.commit()
    if (payment_entry_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "payment_entry": payment_entry_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def item(**kwargs):
    item =frappe.get_doc(kwargs['data'])

    item.insert()
    item_name = item.name
    frappe.db.commit()
    if (item_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة الصنف بنجاح!",
            "item": item_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة الصنف . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def material_request(**kwargs):
    material_request =frappe.get_doc(kwargs['data'])

    material_request.insert()
    material_request_name = material_request.name
    frappe.db.commit()
    if (material_request_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "material_request": material_request_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def stock_entry(**kwargs):
    stock_entry =frappe.get_doc(kwargs['data'])

    stock_entry.insert()
    stock_entry_name = stock_entry.name
    frappe.db.commit()

    if (stock_entry_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "stock_entry": stock_entry_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def delivery_note(**kwargs):
    delivery_note =frappe.get_doc(kwargs['data'])

    delivery_note.insert()
    delivery_note_name = delivery_note.name
    frappe.db.commit()
    if (delivery_note_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "delivery_note": delivery_note_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def purchase_receipt(**kwargs):
    purchase_receipt =frappe.get_doc(kwargs['data'])

    purchase_receipt.insert()
    purchase_receipt_name = purchase_receipt.name
    frappe.db.commit()
    if (purchase_receipt_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_receipt": purchase_receipt_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def comment(**kwargs):
    comment =frappe.get_doc(kwargs['data'])

    comment.insert()
    comment_name = comment.name
    frappe.db.commit()
    if (comment_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة التعليق بنجاح!",
            "comment": comment_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة التعليق . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def add_item_list(**kwargs):
    start = 0
    page_length = 20
    try:
        if kwargs['search_text']:
            items = frappe.db.sql(""" select tabItem.name as name ,
                                                     tabItem.item_code as item_code, 
                                                     tabItem.item_name as item_name, 
                                                     tabItem.item_group as item_group, 
                                                     tabItem.stock_uom as stock_uom, 
                                                     tabItem.image as image,
                                                     tabItem.sales_uom as sales_uom,
                                                     ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                                     ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                                     where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                                     from tabItem  where tabItem.disabled = 0 and tabItem.name like '%{item}%' or tabItem.item_name like '%{item}%' LIMIT {start},{page_length}""".format(start=kwargs['start'], page_length=kwargs['page_length'], price_list=kwargs['price_list'],item=kwargs['search_text']), as_dict=1)
            result = []
            for item_dict in items:
                if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                    net_rate = item_dict.price_list_rate * (1 + (item_dict.tax_percent / 100))
                    vat_value = net_rate - item_dict.price_list_rate 
                    data = {
                        'name': item_dict.name,
                        'item_code': item_dict.item_code,
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
                        'uom': item_dict.stock_uom,
                        'stock_uom': item_dict.stock_uom,
                        'image': item_dict.image,
                        'sales_uom': item_dict.sales_uom,
                        'price_list_rate': item_dict.price_list_rate,
                        'tax_percent': item_dict.tax_percent,
                        'net_rate': net_rate,
                        'vat_value': vat_value
                    }
                    result.append(data)
                else:
                    data = {
                        'name': item_dict.name,
                        'item_code': item_dict.item_code,
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
                        'uom': item_dict.stock_uom,
                        'stock_uom': item_dict.stock_uom,
                        'image': item_dict.image,
                        'sales_uom': item_dict.sales_uom,
                        'price_list_rate': item_dict.price_list_rate,
                        'tax_percent': item_dict.tax_percent,
                        'net_rate': item_dict.price_list_rate
                    }
                    result.append(data)

            if items:
                return result
            else:
                return "لا يوجد منتجات !"


    except:
        items = frappe.db.sql(""" select tabItem.name as name,
                                         tabItem.item_code as item_code,
                                         tabItem.item_name as item_name, 
                                         tabItem.item_group as item_group, 
                                         tabItem.stock_uom as stock_uom, 
                                         tabItem.image as image,
                                         tabItem.sales_uom as sales_uom,
                                         ifnull((select max(price_list_rate) from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                         ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                         where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                         from tabItem where tabItem.disabled = 0 LIMIT {start},{page_length} """.format(start=kwargs['start'], page_length=kwargs['page_length'], price_list=kwargs['price_list']), as_dict=1)

        result = []
        for item_dict in items:
            if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                net_rate = item_dict.price_list_rate * (1 + (item_dict.tax_percent / 100))
                vat_value = net_rate - item_dict.price_list_rate
                data = {
                    'name': item_dict.name,
                    'item_code': item_dict.item_code,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'uom': item_dict.stock_uom,
                    'stock_uom': item_dict.stock_uom,
                    'image': item_dict.image,
                    'sales_uom': item_dict.sales_uom,
                    'price_list_rate': item_dict.price_list_rate,
                    'tax_percent': item_dict.tax_percent,
                    'net_rate': net_rate,
                    'vat_value': vat_value
                }
                result.append(data)
            else:
                data = {
                    'name': item_dict.name,
                    'item_code': item_dict.item_code,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'uom': item_dict.stock_uom,
                    'stock_uom': item_dict.stock_uom,
                    'image': item_dict.image,
                    'sales_uom': item_dict.sales_uom,
                    'price_list_rate': item_dict.price_list_rate,
                    'tax_percent': item_dict.tax_percent,
                    'net_rate': item_dict.price_list_rate
                }
                result.append(data)

        if items:
            return result
        else:
            return "لا يوجد منتجات !"


@frappe.whitelist(allow_guest=True)
def supplier_test(**kwargs):
    supplier = frappe.new_doc('Supplier')
    supplier.supplier_name = kwargs['data']['supplier_name']
    supplier.supplier_type = kwargs['data']['supplier_type']
    supplier.supplier_group = kwargs['data']['supplier_group']
    supplier.tax_id = kwargs['data']['tax_id']
    supplier.default_currency = kwargs['data']['default_currency']
    supplier.default_price_list = kwargs['data']['default_price_list']
    supplier.payment_terms = kwargs['data']['payment_terms']
    supplier.country = kwargs['data']['country']
    supplier.insert()
    supplier_name = supplier.name

    links = [
        {
            "link_doctype": "Supplier",
            "link_name": supplier_name,
            "link_title": supplier_name
        }
    ]

    emails = [
        {
            "email_id": kwargs['data']['email_id'],
            "is_primary": 1
        }
    ]

    contacts = [
        {
            "phone": kwargs['data']['mobile_no'],
            "is_primary_phone": 1,
            "is_primary_mobile_no": 1
        }
    ]

    contact = frappe.get_doc({
        "doctype": "Contact",
        "first_name": kwargs['data']['supplier_name'],
        "links": links,
        "email_ids": emails,
        "phone_nos": contacts,
        "is_primary_contact": 1,
        "is_billing_contact": 1,
    })
    contact.insert()

    address = frappe.get_doc({
        "doctype": "Address",
        "address_title": kwargs['data']['supplier_name'],
        "address_line1": kwargs['data']['address_line1'],
        "city": kwargs['data']['city'],
        "country": kwargs['data']['country'],
        "address_type": "Billing",
        "links": links,
        "is_primary_address_type": 1,
        "is_shipping_address_type": 1,
    })
    address.insert()

    supplier.supplier_primary_address = address.name
    supplier.supplier_primary_contact = contact.name
    supplier.save()

    frappe.db.commit()
    if (supplier_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "name": supplier_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

        

@frappe.whitelist(allow_guest=True)
def supplier_quotation(**kwargs):
    s_quotation =frappe.get_doc(kwargs['data'])

    s_quotation.insert()
    quotation_name = s_quotation.name
    frappe.db.commit()
    if (s_quotation):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "supplier_quotation_name": quotation_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"
        

@frappe.whitelist(allow_guest=True)
def purchase_order(**kwargs):
    p_order =frappe.get_doc(kwargs['data'])

    p_order.insert()
    purchase_order_name = p_order.name
    frappe.db.commit()
    if (purchase_order_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_order_name": purchase_order_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def purchase_invoice(**kwargs):
    purchase_invoice =frappe.get_doc(kwargs['data'])

    purchase_invoice.insert()
    purchase_invoice_name = purchase_invoice.name
    frappe.db.commit()
    if (purchase_invoice_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_invoice_name": purchase_invoice_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"



@frappe.whitelist(allow_guest=True)
def purchsae_receipt(**kwargs):
    purchsae_receipt_data =frappe.get_doc(kwargs['data'])

    purchsae_receipt_data.insert()
    purchsae_receipt_data_name = purchsae_receipt_data.name
    frappe.db.commit()
    if (purchsae_receipt_data_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchsae_receipt_name": purchsae_receipt_data_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"



@frappe.whitelist(allow_guest=True)
def material_request(**kwargs):
    material_request_data =frappe.get_doc(kwargs['data'])

    material_request_data.insert()
    material_request_data_name = material_request_data.name
    frappe.db.commit()
    if (material_request_data_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "material_request_name": material_request_data_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"
        

@frappe.whitelist(allow_guest=True)
def leave_application(**kwargs):
    leave_application_data =frappe.get_doc(kwargs['data'])

    leave_application_data.insert()
    leave_application_data_name = leave_application_data.name
    frappe.db.commit()
    if (leave_application_data_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "leave_application_name": leave_application_data_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"
        
        
@frappe.whitelist(allow_guest=True)
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

@frappe.whitelist(allow_guest=True)
def employee_checkin(**kwargs):
    employee_checkin_data =frappe.get_doc(kwargs['data'])

    employee_checkin_data.insert()
    employee_checkin_data_name = employee_checkin_data.name
    frappe.db.commit()
    if (employee_checkin_data_name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "employee_checkin_data_name": employee_checkin_data_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"
        

