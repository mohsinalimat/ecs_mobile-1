from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
import json, ast


@frappe.whitelist()
def add_quotation(quotation_to,
        party_name,
        customer_name,
        transaction_date,
        valid_till,
        order_type,
        customer_address,
        contact_person,
        customer_group,
        territory,
        currency,
        conversion_rate,
        selling_price_list,
        price_list_currency,
        plc_conversion_rate,
        ignore_pricing_rule,
        apply_discount_on,
        additional_discount_percentage,
        discount_amount,
        tc_name,
        terms,
        payment_terms_template,items,taxes):
    quotation = frappe.get_doc({"doctype": "Quotation",
                                "quotation_to":quotation_to,
                                "party_name":party_name,
                                "customer_name":customer_name,
                                "transaction_date":transaction_date,
                                "valid_till":valid_till,
                                "order_type":order_type,
                                "customer_address":customer_address,
                                "contact_person":contact_person,
                                "customer_group":customer_group,
                                "territory":territory,
                                "currency":currency,
                                "conversion_rate":conversion_rate,
                                "selling_price_list":selling_price_list,
                                "price_list_currency":price_list_currency,
                                "plc_conversion_rate":plc_conversion_rate,
                                "ignore_pricing_rule":ignore_pricing_rule,
                                "apply_discount_on":apply_discount_on,
                                "additional_discount_percentage":additional_discount_percentage,
                                "discount_amount":discount_amount,
                                "tc_name":tc_name,
                                "terms":terms,
                                "payment_terms_template":payment_terms_template,
                                "items":items,
                                "taxes":taxess
                                  })

    quotation.insert()
    quotation_name = quotation.name
    frappe.db.commit()
    if (quotation):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تمت اضافة المعاملة بنجاح !",
            "transaction_id": quotation_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"