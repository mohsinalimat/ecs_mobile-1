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
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
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
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
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
        items = frappe.db.sql(""" select tabItem.name as name ,
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
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
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
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
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





