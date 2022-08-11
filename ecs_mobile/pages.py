from __future__ import unicode_literals
import frappe
import erpnext
from frappe import auth
import random
import datetime
import json, ast
from erpnext.accounts.utils import get_balance_on
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from frappe.utils import add_to_date, now, nowdate
from frappe.utils import cstr
from frappe.utils.make_random import get_random


@frappe.whitelist()
def lead(name):
    led = {}
    doc_data = frappe.db.get_list('Lead', filters={'name': name},
                                  fields=['name',
                                          'lead_name',
                                          'organization_lead',
                                          'company_name',
                                          'lead_owner',
                                          'status',
                                          'source',
                                          'email_id',
                                          'mobile_no',
                                          'address_line1',
                                          'city',
                                          'country',
                                          'campaign_name',
                                          'contact_by',
                                          'contact_date',
                                          'notes',
                                          'request_type',
                                          'market_segment',
                                          'territory',
                                          'industry',
                                          'docstatus',
                                          ])
    for x in doc_data:
        led['name'] = x.name
        led['status'] = x.status
        led['lead_name'] = x.lead_name
        led['organization_lead'] = x.organization_lead
        led['company_name'] = x.company_name
        led['industry'] = x.industry
        led['market_segment'] = x.market_segment
        led['territory'] = x.territory
        led['address_line1'] = x.address_line1
        led['city'] = x.city
        led['country'] = x.country
        led['mobile_no'] = x.mobile_no
        led['email_id'] = x.email_id
        led['source'] = x.source
        led['campaign_name'] = x.campaign_name
        led['request_type'] = x.request_type
        led['lead_owner'] = x.lead_owner
        led['contact_by'] = x.contact_by
        led['contact_date'] = x.contact_date
        led['notes'] = x.notes
        led['docstatus'] = x.docstatus

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Lead"
                                    and `tabFile`.attached_to_name = "{name}"
                                """.format(name=name), as_dict=1)

    led['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Lead"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    led['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Lead" and disabled = 0 """, as_dict=1)
    led['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    quotation_count = frappe.db.count('Quotation', filters={'party_name': name})
    opportunity_count = frappe.db.count('Opportunity', filters={'party_name': name})
    #quotation_name = frappe.db.get_list('Quotation', filters={'party_name': name}, fields=['name'])
    #opportunity_name = frappe.db.get_list('Opportunity', filters={'party_name': name}, fields=['name'])

    qtn_connections = {}
    opp_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections['name'] = "Quotation"
        qtn_connections['count'] = quotation_count
        qtn_connections['icon'] = "https://erpcloud.systems/icons/quotation.png"
        connections.append(qtn_connections)

    if opportunity_count > 0 and doc_data:
        opp_connections['name'] = "Opportunity"
        opp_connections['count'] = opportunity_count
        opp_connections['icon'] = "https://erpcloud.systems/icons/opportunity.png"
        connections.append(opp_connections)

    led['conn'] = connections

    if doc_data:
        return led
    else:
        return "لا يوجد عميل محتمل بهذا الاسم"

@frappe.whitelist()
def opportunity(name):
    opp = {}
    doc_data = frappe.db.get_list('Opportunity', filters={'name': name},
                                  fields=['name',
                                          'opportunity_from',
                                          'party_name',
                                          'customer_name',
                                          'source',
                                          'opportunity_type',
                                          'status',
                                          'order_lost_reason',
                                          'contact_by',
                                          'contact_date',
                                          'to_discuss',
                                          'with_items',
                                          'customer_address',
                                          'address_display',
                                          'territory',
                                          'customer_group',
                                          'contact_person',
                                          'contact_email',
                                          'contact_mobile',
                                          'campaign',
                                          'transaction_date',
                                          'docstatus',
                                          ])
    for x in doc_data:
        opp['name'] = x.name
        opp['opportunity_from'] = x.opportunity_from
        opp['party_name'] = x.party_name
        opp['customer_name'] = x.customer_name
        opp['source'] = x.source
        opp['opportunity_type'] = x.opportunity_type
        opp['status'] = x.status
        opp['order_lost_reason'] = x.order_lost_reason
        opp['contact_by'] = x.contact_by
        opp['contact_date'] = x.contact_date
        opp['to_discuss'] = x.to_discuss
        opp['with_items'] = x.with_items
        opp['customer_address'] = x.customer_address
        opp['address_display'] = x.address_display
        opp['territory'] = x.territory
        opp['customer_group'] = x.customer_group
        opp['contact_person'] = x.contact_person
        opp['contact_email'] = x.contact_email
        opp['contact_mobile'] = x.contact_mobile
        opp['campaign'] = x.campaign
        opp['transaction_date'] = x.transaction_date
        opp['docstatus'] = x.docstatus

    child_data = frappe.db.get_list('Opportunity Item', filters={'parent': name}, order_by='idx',
                                    fields=[
                                        'idx',
                                        'name',
                                        'item_code',
                                        'item_name',
                                        'item_group',
                                        'brand',
                                        'description',
                                        'image',
                                        'qty',
                                        'uom',
                                    ])

    if child_data and doc_data:
        opp['items'] = child_data

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Opportunity"
                                    and `tabFile`.attached_to_name = "{name}"
                                """.format(name=name), as_dict=1)

    opp['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Opportunity"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    opp['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Opportunity" and disabled = 0 """, as_dict=1)
    opp['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    quotation_count = frappe.db.count('Quotation', filters={'opportunity': name})
    sup_quotation_count = frappe.db.count('Supplier Quotation', filters={'opportunity': name})
    #quotation_name = frappe.db.get_list('Quotation', filters={'opportunity': name}, fields=['name'])
    #sup_quotation_name = frappe.db.get_list('Supplier Quotation', filters={'opportunity': name}, fields=['name'])

    qtn_connections = {}
    sup_qtn_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections['name'] = "Quotation"
        qtn_connections['count'] = quotation_count
        qtn_connections['icon'] = "https://erpcloud.systems/icons/quotation.png"
        connections.append(qtn_connections)


    if sup_quotation_count > 0 and doc_data:
        sup_qtn_connections['name'] = "Supplier Quotation"
        sup_qtn_connections['count'] = sup_quotation_count
        sup_qtn_connections['icon'] = "https://erpcloud.systems/icons/supplier_quotation.png"
        connections.append(sup_qtn_connections)

    opp['conn'] = connections

    if doc_data:
        return opp
    else:
        return "لا يوجد فرصة بيعية بهذا الاسم"

@frappe.whitelist()
def quotation(name):
    qtn = {}
    doc_data = frappe.db.get_list('Quotation', filters={'name': name},
                                  fields=['name',
                                          'quotation_to',
                                          'party_name',
                                          'customer_name',
                                          'transaction_date',
                                          'valid_till',
                                          'order_type',
                                          'customer_address',
                                          'address_display',
                                          'contact_display',
                                          'contact_mobile',
                                          'contact_email',
                                          'customer_group',
                                          'territory',
                                          'currency',
                                          'conversion_rate',
                                          'selling_price_list',
                                          'price_list_currency',
                                          'plc_conversion_rate',
                                          'ignore_pricing_rule',
                                          'total_qty',
                                          'base_total',
                                          'base_net_total',
                                          'total',
                                          'net_total',
                                          'taxes_and_charges',
                                          'base_total_taxes_and_charges',
                                          'total_taxes_and_charges',
                                          'apply_discount_on',
                                          'base_discount_amount',
                                          'additional_discount_percentage',
                                          'discount_amount',
                                          'base_grand_total',
                                          'base_in_words',
                                          'grand_total',
                                          'in_words',
                                          'payment_terms_template',
                                          'tc_name',
                                          'terms',
                                          'campaign',
                                          'source',
                                          'order_lost_reason',
                                          'status',
                                          'docstatus'
                                          ])

    for x in doc_data:
        qtn['name'] = x.name
        qtn['quotation_to'] = x.quotation_to
        qtn['party_name'] = x.party_name
        qtn['customer_name'] = x.customer_name
        qtn['transaction_date'] = x.transaction_date
        qtn['valid_till'] = x.valid_till
        qtn['order_type'] = x.order_type
        qtn['customer_address'] = x.customer_address
        qtn['address_display'] = x.address_display
        qtn['contact_display'] = x.contact_display
        qtn['contact_mobile'] = x.contact_mobile
        qtn['contact_email'] = x.contact_email
        qtn['customer_group'] = x.customer_group
        qtn['territory'] = x.territory
        qtn['currency'] = x.currency
        qtn['conversion_rate'] = x.conversion_rate
        qtn['selling_price_list'] = x.selling_price_list
        qtn['price_list_currency'] = x.price_list_currency
        qtn['plc_conversion_rate'] = x.plc_conversion_rate
        qtn['ignore_pricing_rule'] = x.ignore_pricing_rule
        qtn['total_qty'] = x.total_qty
        qtn['base_total'] = x.base_total
        qtn['base_net_total'] = x.base_net_total
        qtn['total'] = x.total
        qtn['net_total'] = x.net_total
        qtn['taxes_and_charges'] = x.taxes_and_charges
        qtn['base_total_taxes_and_charges'] = x.base_total_taxes_and_charges
        qtn['total_taxes_and_charges'] = x.total_taxes_and_charges
        qtn['apply_discount_on'] = x.apply_discount_on
        qtn['base_discount_amount'] = x.base_discount_amount
        qtn['additional_discount_percentage'] = x.additional_discount_percentage
        qtn['discount_amount'] = x.discount_amount
        qtn['base_grand_total'] = x.base_grand_total
        qtn['base_in_words'] = x.base_in_words
        qtn['grand_total'] = x.grand_total
        qtn['in_words'] = x.in_words
        qtn['payment_terms_template'] = x.payment_terms_template
        qtn['tc_name'] = x.tc_name
        qtn['terms'] = x.terms
        qtn['campaign'] = x.campaign
        qtn['source'] = x.source
        qtn['order_lost_reason'] = x.order_lost_reason
        qtn['status'] = x.status
        qtn['docstatus'] = x.docstatus

    child_data_1 = frappe.db.get_list('Quotation Item', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'item_code',
                                          'item_name',
                                          'description',
                                          'item_group',
                                          'brand',
                                          'image',
                                          'qty',
                                          'stock_uom',
                                          'uom',
                                          'conversion_factor',
                                          'stock_qty',
                                          'price_list_rate',
                                          'base_price_list_rate',
                                          'margin_type',
                                          'margin_rate_or_amount',
                                          'rate_with_margin',
                                          'discount_percentage',
                                          'discount_amount',
                                          'base_rate_with_margin',
                                          'rate',
                                          'net_rate',
                                          'amount',
                                          'net_amount',
                                          'item_tax_template',
                                          'base_rate',
                                          'base_net_rate',
                                          'base_amount',
                                          'base_net_amount',
                                          'stock_uom_rate',
                                          'valuation_rate',
                                          'gross_profit',
                                          'warehouse',
                                          'prevdoc_doctype',
                                          'prevdoc_docname',
                                          'projected_qty',
                                          'actual_qty',
                                      ])


    child_data_2 = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'charge_type',
                                          'row_id',
                                          'account_head',
                                          'description',
                                          'cost_center',
                                          'rate',
                                          'account_currency',
                                          'tax_amount',
                                          'total',
                                          'tax_amount_after_discount_amount',
                                          'base_tax_amount',
                                          'base_total',
                                          'base_tax_amount_after_discount_amount',
                                      ])

    child_data_3 = frappe.db.get_list('Payment Schedule', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'payment_term',
                                          'description',
                                          'due_date',
                                          'mode_of_payment',
                                          'invoice_portion',
                                          'discount_type',
                                          'discount_date',
                                          'discount',
                                          'payment_amount',
                                          'outstanding',
                                          'paid_amount',
                                          'discounted_amount',
                                          'base_payment_amount',
                                      ])

    if child_data_1 and doc_data:
        qtn['items'] = child_data_1

    if child_data_2 and doc_data:
        qtn['taxes'] = child_data_2

    if child_data_3 and doc_data:
        qtn['payment_schedule'] = child_data_3

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Quotation"
                                    and `tabFile`.attached_to_name = "{name}"
                                """.format(name=name), as_dict=1)

    qtn['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Quotation"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    qtn['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Quotation" and disabled = 0 """, as_dict=1)
    qtn['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    sales_order_name = frappe.db.get_list('Sales Order Item', filters={'prevdoc_docname': name}, fields=['parent'], group_by='parent')
    sales_order_count = len(sales_order_name)

    so_connections = {}
    connections = []

    if sales_order_count > 0 and doc_data:
        so_connections['name'] = "Sales Order"
        so_connections['count'] = sales_order_count
        so_connections['icon'] = "https://erpcloud.systems/icons/sales_order.png"
        connections.append(so_connections)

    qtn['conn'] = connections

    if doc_data:
        return qtn
    else:
        return "لا يوجد عرض سعر بهذا الاسم"

@frappe.whitelist()
def customer(name):
    cust = {}
    balance = get_balance_on(account=None, date=getdate(nowdate()), party_type='Customer', party=name, company=None,
                             in_account_currency=True, cost_center=None, ignore_account_permission=False)
    cust['balance'] = balance
    doc_data = frappe.db.get_list('Customer', filters={'name': name},
                                  fields=['name',
                                          'customer_name',
                                          'disabled',
                                          'customer_type',
                                          'customer_group',
                                          'territory',
                                          'market_segment',
                                          'industry',
                                          'tax_id',
                                          'customer_primary_address',
                                          'primary_address',
                                          'customer_primary_contact',
                                          'mobile_no',
                                          'email_id',
                                          'default_currency',
                                          'default_price_list',
                                          'default_sales_partner',
                                          'docstatus',
                                          ])
    for x in doc_data:
        cust['name'] = x.name
        cust['customer_name'] = x.customer_name
        cust['disabled'] = x.disabled
        cust['customer_type'] = x.customer_type
        cust['customer_group'] = x.customer_group
        cust['territory'] = x.territory
        cust['market_segment'] = x.market_segment
        cust['industry'] = x.industry
        cust['tax_id'] = x.tax_id
        cust['customer_primary_address'] = x.customer_primary_address
        cust['primary_address'] = x.primary_address
        cust['customer_primary_contact'] = x.customer_primary_contact
        cust['mobile_no'] = x.mobile_no
        cust['email_id'] = x.email_id
        cust['default_currency'] = x.default_currency
        cust['default_price_list'] = x.default_price_list
        cust['default_sales_partner'] = x.default_sales_partner
        cust['docstatus'] = x.docstatus

    child_data = frappe.db.get_list('Customer Credit Limit', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'company',
                                          'credit_limit',
                                          'bypass_credit_limit_check',
                                      ])

    if child_data and doc_data:
        cust['credit_limits'] = child_data

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Customer"
                                        and `tabFile`.attached_to_name = "{name}"
                                    """.format(name=name), as_dict=1)

    cust['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Customer"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    cust['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Customer" and disabled = 0 """, as_dict=1)
    cust['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    quotation_count = frappe.db.count('Quotation', filters={'party_name': name})
    opportunity_count = frappe.db.count('Opportunity', filters={'party_name': name})
    sales_order_count = frappe.db.count('Sales Order', filters={'customer': name})
    delivery_note_count = frappe.db.count('Delivery Note', filters={'customer': name})
    sales_invoice_count = frappe.db.count('Sales Invoice', filters={'customer': name})
    payment_entry_count = frappe.db.count('Payment Entry', filters={'party': name})
    #quotation_name = frappe.db.get_list('Quotation', filters={'party_name': name}, fields=['name'])
    #opportunity_name = frappe.db.get_list('Opportunity', filters={'party_name': name}, fields=['name'])
    #sales_order_name = frappe.db.get_list('Sales Order', filters={'customer': name}, fields=['name'])
    #delivery_note_name = frappe.db.get_list('Delivery Note', filters={'customer': name}, fields=['name'])
    #sales_invoice_name = frappe.db.get_list('Sales Invoice', filters={'customer': name}, fields=['name'])
    #payment_entry_name = frappe.db.get_list('Payment Entry', filters={'party': name}, fields=['name'])

    qtn_connections = {}
    opp_connections = {}
    so_connections = {}
    dn_connections = {}
    sinv_connections = {}
    pe_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections['name'] = "Quotation"
        qtn_connections['count'] = quotation_count
        qtn_connections['icon'] = "https://erpcloud.systems/icons/quotation.png"
        connections.append(qtn_connections)

    if opportunity_count > 0 and doc_data:
        opp_connections['name'] = "Opportunity"
        opp_connections['count'] = opportunity_count
        opp_connections['icon'] = "https://erpcloud.systems/icons/opportunity.png"
        connections.append(opp_connections)

    if sales_order_count > 0 and doc_data:
        so_connections['name'] = "Sales Order"
        so_connections['count'] = sales_order_count
        so_connections['icon'] = "https://erpcloud.systems/icons/sales_order.png"
        connections.append(so_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections['name'] = "Delivery Note"
        dn_connections['count'] = delivery_note_count
        dn_connections['icon'] = "https://erpcloud.systems/icons/delivery_note.png"
        connections.append(dn_connections)

    if sales_invoice_count > 0 and doc_data:
        sinv_connections['name'] = "Sales Invoice"
        sinv_connections['count'] = sales_invoice_count
        sinv_connections['icon'] = "https://erpcloud.systems/icons/sales_invoice.png"
        connections.append(sinv_connections)

    if payment_entry_count > 0 and doc_data:
        pe_connections['name'] = "Payment Entry"
        pe_connections['count'] = payment_entry_count
        pe_connections['icon'] = "https://erpcloud.systems/icons/payment_entry.png"
        connections.append(pe_connections)

    cust['conn'] = connections

    if doc_data:
        return cust
    else:
        return "لا يوجد عميل بهذا الاسم"

@frappe.whitelist()
def sales_order(name):
    so = {}
    doc_data = frappe.db.get_list('Sales Order', filters={'name': name},
                                  fields=['name',
                                          'customer',
                                          'customer_name',
                                          'transaction_date',
                                          'delivery_date',
                                          'status',
                                          'tax_id',
                                          'customer_group',
                                          'territory',
                                          'customer_address',
                                          'address_display',
                                          'contact_display',
                                          'contact_mobile',
                                          'contact_email',
                                          'project',
                                          'order_type',
                                          'currency',
                                          'conversion_rate',
                                          'selling_price_list',
                                          'price_list_currency',
                                          'plc_conversion_rate',
                                          'ignore_pricing_rule',
                                          'set_warehouse',
                                          'campaign',
                                          'source',
                                          'tc_name',
                                          'terms',
                                          'taxes_and_charges',
                                          'payment_terms_template',
                                          'sales_partner',
                                          'commission_rate',
                                          'total_commission',
                                          'total_qty',
                                          'base_total',
                                          'base_net_total',
                                          'total',
                                          'net_total',
                                          'base_total_taxes_and_charges',
                                          'total_taxes_and_charges',
                                          'apply_discount_on',
                                          'base_discount_amount',
                                          'additional_discount_percentage',
                                          'discount_amount',
                                          'base_grand_total',
                                          'base_in_words',
                                          'grand_total',
                                          'in_words',
                                          'docstatus'
                                          ])

    for x in doc_data:
        so['name'] = x.name
        so['customer'] = x.customer
        so['customer_name'] = x.customer_name
        so['transaction_date'] = x.transaction_date
        so['delivery_date'] = x.delivery_date
        so['status'] = x.status
        so['tax_id'] = x.order_type
        so['customer_group'] = x.customer_group
        so['territory'] = x.territory
        so['customer_address'] = x.customer_address
        so['address_display'] = x.address_display
        so['contact_display'] = x.contact_display
        so['contact_mobile'] = x.contact_mobile
        so['contact_email'] = x.contact_email
        so['project'] = x.project
        so['order_type'] = x.order_type
        so['currency'] = x.currency
        so['conversion_rate'] = x.conversion_rate
        so['selling_price_list'] = x.selling_price_list
        so['price_list_currency'] = x.price_list_currency
        so['plc_conversion_rate'] = x.plc_conversion_rate
        so['set_warehouse'] = x.set_warehouse
        so['campaign'] = x.campaign
        so['source'] = x.source
        so['tc_name'] = x.tc_name
        so['terms'] = x.terms
        so['taxes_and_charges'] = x.taxes_and_charges
        so['payment_terms_template'] = x.payment_terms_template
        so['sales_partner'] = x.sales_partner
        so['commission_rate'] = x.commission_rate
        so['total_commission'] = x.total_commission
        so['total_qty'] = x.total_qty
        so['base_total'] = x.base_total
        so['base_net_total'] = x.base_net_total
        so['total'] = x.total
        so['net_total'] = x.net_total
        so['base_total_taxes_and_charges'] = x.base_total_taxes_and_charges
        so['total_taxes_and_charges'] = x.total_taxes_and_charges
        so['apply_discount_on'] = x.apply_discount_on
        so['base_discount_amount'] = x.base_discount_amount
        so['additional_discount_percentage'] = x.additional_discount_percentage
        so['discount_amount'] = x.discount_amount
        so['base_grand_total'] = x.base_grand_total
        so['base_in_words'] = x.base_in_words
        so['grand_total'] = x.grand_total
        so['in_words'] = x.in_words
        so['docstatus'] = x.docstatus

    child_data_1 = frappe.db.get_list('Sales Order Item', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'delivery_date',
                                          'item_code',
                                          'item_name',
                                          'description',
                                          'item_group',
                                          'brand',
                                          'image',
                                          'qty',
                                          'stock_uom',
                                          'uom',
                                          'conversion_factor',
                                          'stock_qty',
                                          'price_list_rate',
                                          'base_price_list_rate',
                                          'margin_type',
                                          'margin_rate_or_amount',
                                          'rate_with_margin',
                                          'discount_percentage',
                                          'discount_amount',
                                          'base_rate_with_margin',
                                          'rate',
                                          'net_rate',
                                          'amount',
                                          'item_tax_template',
                                          'net_amount',
                                          'base_rate',
                                          'base_net_rate',
                                          'base_amount',
                                          'base_net_amount',
                                          'billed_amt',
                                          'valuation_rate',
                                          'gross_profit',
                                          'warehouse',
                                          'prevdoc_docname',
                                          'projected_qty',
                                          'actual_qty',
                                          'ordered_qty',
                                          'planned_qty',
                                          'work_order_qty',
                                          'delivered_qty',
                                          'produced_qty',
                                          'returned_qty',
                                          'additional_notes',
                                      ])


    child_data_2 = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'charge_type',
                                          'row_id',
                                          'account_head',
                                          'description',
                                          'cost_center',
                                          'rate',
                                          'account_currency',
                                          'tax_amount',
                                          'total',
                                          'tax_amount_after_discount_amount',
                                          'base_tax_amount',
                                          'base_total',
                                          'base_tax_amount_after_discount_amount',
                                      ])

    child_data_3 = frappe.db.get_list('Payment Schedule', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'payment_term',
                                          'description',
                                          'due_date',
                                          'mode_of_payment',
                                          'invoice_portion',
                                          'discount_type',
                                          'discount_date',
                                          'discount',
                                          'payment_amount',
                                          'outstanding',
                                          'paid_amount',
                                          'discounted_amount',
                                          'base_payment_amount',
                                      ])

    if child_data_1 and doc_data:
        so['items'] = child_data_1

    if child_data_2 and doc_data:
        so['taxes'] = child_data_2

    if child_data_3 and doc_data:
        so['payment_schedule'] = child_data_3

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Sales Order"
                                        and `tabFile`.attached_to_name = "{name}"
                                    """.format(name=name), as_dict=1)

    so['attachments'] = attachments


    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Sales Order"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    so['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Sales Order" and disabled = 0 """, as_dict=1)
    so['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    sales_invoice = frappe.db.get_list('Sales Invoice Item', filters={'sales_order': name}, fields=['parent'], group_by='parent')
    delivery_note = frappe.db.get_list('Delivery Note Item', filters={'against_sales_order': name}, fields=['parent'], group_by='parent')
    material_request = frappe.db.get_list('Material Request Item', filters={'sales_order': name}, fields=['parent'], group_by='parent')
    purchase_order = frappe.db.get_list('Purchase Order Item', filters={'sales_order': name}, fields=['parent'], group_by='parent')
    quotation = frappe.db.get_list('Sales Order Item', filters={'parent': name, 'prevdoc_docname': ["!=", ""]}, fields=['prevdoc_docname'], group_by='prevdoc_docname')
    payment_entry = frappe.db.get_list('Payment Entry Reference', filters={'reference_name': name}, fields=['parent'], group_by='parent')
    sales_invoice_count = len(sales_invoice)
    delivery_note_count = len(delivery_note)
    material_request_count = len(material_request)
    purchase_order_count = len(purchase_order)
    quotation_count = len(quotation)
    payment_entry_count = len(payment_entry)

    sinv_connections = {}
    dn_connections = {}
    mr_connections = {}
    po_connections = {}
    qtn_connections = {}
    pe_connections = {}
    connections = []

    if sales_invoice_count > 0 and doc_data:
        sinv_connections['name'] = "Sales Invoice"
        sinv_connections['count'] = sales_invoice_count
        sinv_connections['icon'] = "https://erpcloud.systems/icons/sales_invoice.png"
        connections.append(sinv_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections['name'] = "Delivery Note"
        dn_connections['count'] = delivery_note_count
        dn_connections['icon'] = "https://erpcloud.systems/icons/delivery_note.png"
        connections.append(dn_connections)

    if material_request_count > 0 and doc_data:
        mr_connections['name'] = "Material Request"
        mr_connections['count'] = material_request_count
        mr_connections['icon'] = "https://erpcloud.systems/icons/material_request.png"
        connections.append(mr_connections)

    if purchase_order_count > 0 and doc_data:
        po_connections['name'] = "Purchase Order"
        po_connections['count'] = purchase_order_count
        po_connections['icon'] = "https://erpcloud.systems/icons/purchase_order.png"
        connections.append(po_connections)

    if quotation_count > 0 and doc_data:
        qtn_connections['name'] = "Quotation"
        qtn_connections['count'] = quotation_count
        qtn_connections['qtn_no']= quotation
        qtn_connections['icon'] = "https://erpcloud.systems/icons/quotation.png"
        connections.append(qtn_connections)

    if payment_entry_count > 0 and doc_data:
        pe_connections['name'] = "Payment Entry"
        pe_connections['count'] = payment_entry_count
        pe_connections['icon'] = "https://erpcloud.systems/icons/payment_entry.png"
        connections.append(pe_connections)

    so['conn'] = connections

    if doc_data:
        return so
    else:
        return "لا يوجد أمر بيع بهذا الاسم"

@frappe.whitelist()
def sales_invoice(name):
    sinv = {}
    doc_data = frappe.db.get_list('Sales Invoice', filters={'name': name},
                                  fields=['name',
                                          'customer',
                                          'customer_name',
                                          'posting_date',
                                          'due_date',
                                          'status',
                                          'is_return',
                                          'tax_id',
                                          'customer_group',
                                          'territory',
                                          'customer_address',
                                          'address_display',
                                          'contact_display',
                                          'contact_mobile',
                                          'contact_email',
                                          'project',
                                          'cost_center',
                                          'currency',
                                          'conversion_rate',
                                          'selling_price_list',
                                          'price_list_currency',
                                          'plc_conversion_rate',
                                          'ignore_pricing_rule',
                                          'set_warehouse',
                                          'set_target_warehouse',
                                          'update_stock',
                                          'campaign',
                                          'source',
                                          'tc_name',
                                          'terms',
                                          'taxes_and_charges',
                                          'payment_terms_template',
                                          'sales_partner',
                                          'commission_rate',
                                          'total_commission',
                                          'total_qty',
                                          'base_total',
                                          'base_net_total',
                                          'total',
                                          'net_total',
                                          'base_total_taxes_and_charges',
                                          'total_taxes_and_charges',
                                          'apply_discount_on',
                                          'base_discount_amount',
                                          'additional_discount_percentage',
                                          'discount_amount',
                                          'base_grand_total',
                                          'base_in_words',
                                          'grand_total',
                                          'in_words',
                                          'docstatus'
                                          ])

    for x in doc_data:
        sinv['name'] = x.name
        sinv['customer'] = x.customer
        sinv['customer_name'] = x.customer_name
        sinv['posting_date'] = x.posting_date
        sinv['due_date'] = x.due_date
        sinv['status'] = x.status
        sinv['is_return'] = x.is_return
        sinv['tax_id'] = x.order_type
        sinv['customer_group'] = x.customer_group
        sinv['territory'] = x.territory
        sinv['customer_address'] = x.customer_address
        sinv['address_display'] = x.address_display
        sinv['contact_display'] = x.contact_display
        sinv['contact_mobile'] = x.contact_mobile
        sinv['contact_email'] = x.contact_email
        sinv['project'] = x.project
        sinv['cost_center'] = x.cost_center
        sinv['currency'] = x.currency
        sinv['conversion_rate'] = x.conversion_rate
        sinv['selling_price_list'] = x.selling_price_list
        sinv['price_list_currency'] = x.price_list_currency
        sinv['plc_conversion_rate'] = x.plc_conversion_rate
        sinv['update_stock'] = x.update_stock
        sinv['set_warehouse'] = x.set_warehouse
        sinv['set_target_warehouse'] = x.set_target_warehouse
        sinv['tc_name'] = x.tc_name
        sinv['terms'] = x.terms
        sinv['taxes_and_charges'] = x.taxes_and_charges
        sinv['payment_terms_template'] = x.payment_terms_template
        sinv['sales_partner'] = x.sales_partner
        sinv['commission_rate'] = x.commission_rate
        sinv['total_commission'] = x.total_commission
        sinv['total_qty'] = x.total_qty
        sinv['base_total'] = x.base_total
        sinv['base_net_total'] = x.base_net_total
        sinv['total'] = x.total
        sinv['net_total'] = x.net_total
        sinv['base_total_taxes_and_charges'] = x.base_total_taxes_and_charges
        sinv['total_taxes_and_charges'] = x.total_taxes_and_charges
        sinv['apply_discount_on'] = x.apply_discount_on
        sinv['base_discount_amount'] = x.base_discount_amount
        sinv['additional_discount_percentage'] = x.additional_discount_percentage
        sinv['discount_amount'] = x.discount_amount
        sinv['base_grand_total'] = x.base_grand_total
        sinv['base_in_words'] = x.base_in_words
        sinv['grand_total'] = x.grand_total
        sinv['in_words'] = x.in_words
        sinv['docstatus'] = x.docstatus


    child_data_1 = frappe.db.get_list('Sales Invoice Item', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'item_code',
                                          'item_name',
                                          'description',
                                          'item_group',
                                          'brand',
                                          'image',
                                          'qty',
                                          'stock_uom',
                                          'uom',
                                          'conversion_factor',
                                          'stock_qty',
                                          'price_list_rate',
                                          'base_price_list_rate',
                                          'margin_type',
                                          'margin_rate_or_amount',
                                          'rate_with_margin',
                                          'discount_percentage',
                                          'discount_amount',
                                          'base_rate_with_margin',
                                          'rate',
                                          'net_rate',
                                          'amount',
                                          'item_tax_template',
                                          'net_amount',
                                          'base_rate',
                                          'base_net_rate',
                                          'base_amount',
                                          'base_net_amount',
                                          'warehouse',
                                          'actual_qty',
                                          'delivered_qty',
                                      ])


    child_data_2 = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'charge_type',
                                          'row_id',
                                          'account_head',
                                          'description',
                                          'cost_center',
                                          'rate',
                                          'account_currency',
                                          'tax_amount',
                                          'total',
                                          'tax_amount_after_discount_amount',
                                          'base_tax_amount',
                                          'base_total',
                                          'base_tax_amount_after_discount_amount',
                                      ])

    child_data_3 = frappe.db.get_list('Payment Schedule', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'payment_term',
                                          'description',
                                          'due_date',
                                          'mode_of_payment',
                                          'invoice_portion',
                                          'discount_type',
                                          'discount_date',
                                          'discount',
                                          'payment_amount',
                                          'outstanding',
                                          'paid_amount',
                                          'discounted_amount',
                                          'base_payment_amount',
                                      ],
                                      )

    if child_data_1 and doc_data:
        sinv['items'] = child_data_1

    if child_data_2 and doc_data:
        sinv['taxes'] = child_data_2

    if child_data_3 and doc_data:
        sinv['payment_schedule'] = child_data_3

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Sales Invoice"
                                        and `tabFile`.attached_to_name = "{name}"
                                    """.format(name=name), as_dict=1)

    sinv['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Sales Invoice"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    sinv['comments'] = comments

    print_formats = frappe.db.sql(""" Select name from `tabPrint Format` where doc_type = "Sales Invoice" and disabled = 0 """, as_dict=1)
    sinv['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    sales_order = frappe.db.get_list('Sales Invoice Item', filters={'parent': name}, fields=['sales_order'], group_by='sales_order')
    delivery_note = frappe.db.get_list('Delivery Note Item', filters={'against_sales_invoice': name}, fields=['parent'], group_by='parent')
    payment_entry = frappe.db.get_list('Payment Entry Reference', filters={'reference_name': name}, fields=['parent'], group_by='parent')
    sales_order_count = len(sales_order)
    delivery_note_count = len(delivery_note)
    payment_entry_count = len(payment_entry)

    so_connections = {}
    dn_connections = {}
    pe_connections = {}
    connections = []

    if sales_order_count > 0 and doc_data:
        so_connections['name'] = "Sales Order"
        so_connections['count'] = sales_order_count
        so_connections['icon'] = "https://erpcloud.systems/icons/sales_order.png"
        connections.append(so_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections['name'] = "Delivery Note"
        dn_connections['count'] = delivery_note_count
        dn_connections['icon'] = "https://erpcloud.systems/icons/delivery_note.png"
        connections.append(dn_connections)

    if payment_entry_count > 0 and doc_data:
        pe_connections['name'] = "Payment Entry"
        pe_connections['count'] = payment_entry_count
        pe_connections['icon'] = "https://erpcloud.systems/icons/payment_entry.png"
        connections.append(pe_connections)

    sinv['conn'] = connections

    if doc_data:
        return sinv
    else:
        return "لا يوجد فاتورة مبيعات بهذا الاسم"


@frappe.whitelist()
def payment_entry(name):
    pe = {}
    doc_data = frappe.db.get_list('Payment Entry', filters={'name': name},
                                  fields=['name',
                                          'party_type',
                                          'party',
                                          'party_name',
                                          'posting_date',
                                          'status',
                                          'reference_no',
                                          'reference_date',
                                          'payment_type',
                                          'mode_of_payment',
                                          'mode_of_payment_2',
                                          'paid_from_account_balance',
                                          'paid_to_account_balance',
                                          'paid_from',
                                          'paid_to',
                                          'paid_amount',
                                          'docstatus'
                                          ])
    for x in doc_data:
        pe['name'] = x.name
        pe['party_type'] = x.party_type
        pe['party'] = x.party
        pe['party_name'] = x.party_name
        pe['posting_date'] = x.posting_date
        pe['status'] = x.status
        pe['reference_no'] = x.reference_no
        pe['reference_date'] = x.reference_date
        pe['payment_type'] = x.payment_type
        pe['mode_of_payment'] = x.mode_of_payment
        pe['mode_of_payment_2'] = x.mode_of_payment_2
        pe['paid_from'] = x.paid_from
        pe['paid_from_account_balance'] = x.paid_from_account_balance
        pe['paid_to'] = x.paid_to
        pe['paid_to_account_balance'] = x.paid_to_account_balance
        pe['paid_amount'] = x.paid_amount
        pe['docstatus'] = x.docstatus


    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Payment Entry"
                                    and `tabFile`.attached_to_name = "{name}"
                                """.format(name=name), as_dict=1)

    pe['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Payment Entry"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    pe['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Payment Entry" and disabled = 0 """, as_dict=1)
    pe['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return pe
    else:
        return "لا يوجد مدفوعات ومقبوضات بهذا الاسم"

@frappe.whitelist()
def item(name):
    item_ = {}
    doc_data = frappe.db.get_list('Item', filters={'name': name},
                                  fields=['name',
                                          'item_code',
                                          'item_name',
                                          'item_group',
                                          'brand',
                                          'stock_uom',
                                          'description',
                                          'image',
                                          'disabled',
                                          'is_stock_item',
                                          'include_item_in_manufacturing',
                                          'is_fixed_asset',
                                          'asset_category',
                                          'is_purchase_item',
                                          'purchase_uom',
                                          'is_sales_item',
                                          'sales_uom',
                                          'docstatus'
                                          ])
    for x in doc_data:
        item_['name'] = x.name
        item_['image'] = x.image
        item_['item_name'] = x.item_name
        item_['item_code'] = x.item_code
        item_['disabled'] = x.disabled
        item_['item_group'] = x.item_group
        item_['brand'] = x.brand
        item_['stock_uom'] = x.stock_uom
        item_['description'] = x.description
        item_['is_stock_item'] = x.is_stock_item
        item_['include_item_in_manufacturing'] = x.include_item_in_manufacturing
        item_['is_fixed_asset'] = x.is_fixed_asset
        item_['asset_category'] = x.asset_category
        item_['is_sales_item'] = x.is_sales_item
        item_['sales_uom'] = x.sales_uom
        item_['is_purchase_item'] = x.is_purchase_item
        item_['purchase_uom'] = x.purchase_uom
        item_['docstatus'] = x.docstatus

    child_data1 = frappe.db.get_list('UOM Conversion Detail', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'uom',
                                          'conversion_factor',
                                      ],
                                      )

    if child_data1 and doc_data:
        item_['uoms'] = child_data1

    child_data2 = frappe.db.get_list('Item Price', filters={'item_code': name, 'selling': 1}, order_by='price_list',
                                    fields=[
                                        'price_list',
                                        'price_list_rate',
                                        'currency',
                                    ],
                                    )

    if child_data2 and doc_data:
        item_['selling_price_lists_rate'] = child_data2


    balances = frappe.db.sql(""" select  
                                     tabBin.warehouse as warehouse,
                                     (select warehouse_type from tabWarehouse where tabWarehouse.name = tabBin.warehouse ) as warehouse_type,
                                     tabBin.actual_qty as actual_qty,
                                     tabBin.reserved_qty as reserved_qty,
                                     tabBin.ordered_qty as ordered_qty,
                                     tabBin.indented_qty as indented_qty,
                                     tabBin.projected_qty as projected_qty
                                from
                                     tabBin 
                                    inner join tabItem on tabBin.item_code = tabItem.item_code
                                where
                                    tabBin.item_code = '{name}'
                                    and tabItem.has_variants = 0
                                    and tabBin.actual_qty >0
                            """.format(name=name), as_dict=1)

    result = []
    for item_dict in balances:
        data = {
            'warehouse': item_dict.warehouse,
            'warehouse_type': item_dict.warehouse_type,
            'actual_qty': item_dict.actual_qty,
            'reserved_qty': item_dict.reserved_qty,
            'ordered_qty': item_dict.ordered_qty,
            'indented_qty': item_dict.indented_qty,
            'projected_qty': item_dict.projected_qty
        }
        result.append(data)

    if result and doc_data:
        item_['stock_balances'] = result

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Item"
                                        and `tabFile`.attached_to_name = "{name}"
                                    """.format(name=name), as_dict=1)

    item_['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Item"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    item_['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Item" and disabled = 0 """, as_dict=1)
    item_['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    quotation = frappe.db.get_list('Quotation Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    sales_order = frappe.db.get_list('Sales Order Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    delivery_note = frappe.db.get_list('Delivery Note Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    sales_invoice = frappe.db.get_list('Sales Invoice Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    material_request = frappe.db.get_list('Material Request Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    supplier_quotation = frappe.db.get_list('Supplier Quotation Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    purchase_order = frappe.db.get_list('Purchase Order Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    purchase_receipt = frappe.db.get_list('Purchase Receipt Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    purchase_invoice = frappe.db.get_list('Purchase Invoice Item', filters={'item_code': name}, fields=['item_code'], group_by='parent')
    stock_entry = frappe.db.get_list('Stock Entry Detail', filters={'item_code': name}, fields=['item_code'], group_by='parent')

    quotation_count = len(quotation)
    sales_order_count = len(sales_order)
    delivery_note_count = len(delivery_note)
    sales_invoice_count = len(sales_invoice)
    material_request_count = len(material_request)
    supplier_quotation_count = len(supplier_quotation)
    purchase_order_count = len(purchase_order)
    purchase_receipt_count = len(purchase_receipt)
    purchase_invoice_count = len(purchase_invoice)
    stock_entry_count = len(stock_entry)

    qtn_connections = {}
    so_connections = {}
    dn_connections = {}
    sinv_connections = {}
    mr_connections = {}
    sup_qtn_connections = {}
    po_connections = {}
    pr_connections = {}
    pinv_connections = {}
    se_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections['name'] = "Quotation"
        qtn_connections['count'] = quotation_count
        qtn_connections['icon'] = "https://erpcloud.systems/icons/quotation.png"
        connections.append(qtn_connections)

    if sales_order_count > 0 and doc_data:
        so_connections['name'] = "Sales Order"
        so_connections['count'] = sales_order_count
        so_connections['icon'] = "https://erpcloud.systems/icons/sales_order.png"
        connections.append(so_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections['name'] = "Delivery Note"
        dn_connections['count'] = delivery_note_count
        dn_connections['icon'] = "https://erpcloud.systems/icons/delivery_note.png"
        connections.append(dn_connections)

    if sales_invoice_count > 0 and doc_data:
        sinv_connections['name'] = "Sales Invoice"
        sinv_connections['count'] = sales_invoice_count
        sinv_connections['icon'] = "https://erpcloud.systems/icons/sales_invoice.png"
        connections.append(sinv_connections)

    if material_request_count > 0 and doc_data:
        mr_connections['name'] = "Material Request"
        mr_connections['count'] = material_request_count
        mr_connections['icon'] = "https://erpcloud.systems/icons/material_request.png"
        connections.append(mr_connections)

    if supplier_quotation_count > 0 and doc_data:
        sup_qtn_connections['name'] = "Supplier Quotation"
        sup_qtn_connections['count'] = supplier_quotation_count
        sup_qtn_connections['icon'] = "https://erpcloud.systems/icons/supplier_quotation.png"
        connections.append(sup_qtn_connections)

    if purchase_order_count > 0 and doc_data:
        po_connections['name'] = "Purchase Order"
        po_connections['count'] = purchase_order_count
        po_connections['icon'] = "https://erpcloud.systems/icons/purchase_order.png"
        connections.append(po_connections)

    if purchase_receipt_count > 0 and doc_data:
        pr_connections['name'] = "Purchase Receipt"
        pr_connections['count'] = purchase_receipt_count
        pr_connections['icon'] = "https://erpcloud.systems/icons/purchase_receipt.png"
        connections.append(pr_connections)

    if purchase_invoice_count > 0 and doc_data:
        pinv_connections['name'] = "Purchase Invoice"
        pinv_connections['count'] = purchase_invoice_count
        pinv_connections['icon'] = "https://erpcloud.systems/icons/purchase_invoice.png"
        connections.append(pinv_connections)

    if stock_entry_count > 0 and doc_data:
        se_connections['name'] = "Stock Entry"
        se_connections['count'] = stock_entry_count
        se_connections['icon'] = "https://erpcloud.systems/icons/stock_entry.png"
        connections.append(se_connections)

    item_['conn'] = connections

    if doc_data:
        return item_
    else:
        return "لا يوجد صنف بهذا الاسم"

@frappe.whitelist()
def stock_entry(name):
    se = {}
    doc_data = frappe.db.get_list('Stock Entry', filters={'name': name},
                                  fields=['name',
                                          'stock_entry_type',
                                          'purpose',
                                          'posting_date',
                                          'docstatus',
                                          'from_warehouse',
                                          'to_warehouse',
                                          'project',
                                          'docstatus'
                                          ])
    for x in doc_data:
        se['name'] = x.name
        se['stock_entry_type'] = x.stock_entry_type
        se['purpose'] = x.purpose
        se['posting_date'] = x.posting_date
        if x.docstatus == 0:
            se['status'] = "Draft"
        if x.docstatus == 1:
            se['status'] = "Submitted"
        if x.docstatus == 2:
            se['status'] = "Cancelled"
        se['from_warehouse'] = x.from_warehouse
        se['to_warehouse'] = x.to_warehouse
        se['project'] = x.project
        se['docstatus'] = x.docstatus


    child_data = frappe.db.get_list('Stock Entry Detail', filters={'parent': name}, order_by='idx',
                                    fields=[
                                        'name',
                                        'idx',
                                        'item_code',
                                        'item_name',
                                        'description',
                                        'item_group',
                                        'image',
                                        'qty',
                                        'transfer_qty',
                                        'stock_uom',
                                        'uom',
                                        'conversion_factor',
                                        's_warehouse',
                                        't_warehouse',
                                        'cost_center',
                                        'project',
                                        'actual_qty',
                                        'transferred_qty',
                                    ])

    if child_data and doc_data:
        se['items'] = child_data

    attachments = frappe.db.sql(""" Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Stock Entry"
                                        and `tabFile`.attached_to_name = "{name}"
                                    """.format(name=name), as_dict=1)

    se['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Stock Entry"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    se['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Stock Entry" and disabled = 0 """, as_dict=1)
    se['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return se
    else:
        return "لا يوجد حركة مخزنية بهذا الاسم"


@frappe.whitelist()
def delivery_note(name):
    dn = {}
    doc_data = frappe.db.get_list('Delivery Note', filters={'name': name},
                                  fields=['name',
                                          'customer',
                                          'customer_name',
                                          'posting_date',
                                          'status',
                                          'is_return',
                                          'tax_id',
                                          'customer_group',
                                          'territory',
                                          'customer_address',
                                          'address_display',
                                          'contact_display',
                                          'contact_mobile',
                                          'contact_email',
                                          'project',
                                          'cost_center',
                                          'currency',
                                          'conversion_rate',
                                          'selling_price_list',
                                          'price_list_currency',
                                          'plc_conversion_rate',
                                          'ignore_pricing_rule',
                                          'set_warehouse',
                                          'set_target_warehouse',
                                          'tc_name',
                                          'sales_partner',
                                          'commission_rate',
                                          'total_commission',
                                          'total_qty',
                                          'base_total',
                                          'base_net_total',
                                          'total',
                                          'net_total',
                                          'base_total_taxes_and_charges',
                                          'total_taxes_and_charges',
                                          'apply_discount_on',
                                          'base_discount_amount',
                                          'additional_discount_percentage',
                                          'discount_amount',
                                          'base_grand_total',
                                          'base_in_words',
                                          'grand_total',
                                          'in_words',
                                          'docstatus'
                                          ])

    for x in doc_data:
        dn['name'] = x.name
        dn['customer'] = x.customer
        dn['customer_name'] = x.customer_name
        dn['posting_date'] = x.posting_date
        dn['status'] = x.status
        dn['is_return'] = x.is_return
        dn['tax_id'] = x.order_type
        dn['customer_group'] = x.customer_group
        dn['territory'] = x.territory
        dn['customer_address'] = x.customer_address
        dn['address_display'] = x.address_display
        dn['contact_display'] = x.contact_display
        dn['contact_mobile'] = x.contact_mobile
        dn['contact_email'] = x.contact_email
        dn['project'] = x.project
        dn['cost_center'] = x.cost_center
        dn['currency'] = x.currency
        dn['conversion_rate'] = x.conversion_rate
        dn['selling_price_list'] = x.selling_price_list
        dn['price_list_currency'] = x.price_list_currency
        dn['plc_conversion_rate'] = x.plc_conversion_rate
        dn['set_warehouse'] = x.set_warehouse
        dn['set_target_warehouse'] = x.set_target_warehouse
        dn['tc_name'] = x.tc_name
        dn['sales_partner'] = x.sales_partner
        dn['commission_rate'] = x.commission_rate
        dn['total_commission'] = x.total_commission
        dn['total_qty'] = x.total_qty
        dn['base_total'] = x.base_total
        dn['base_net_total'] = x.base_net_total
        dn['total'] = x.total
        dn['net_total'] = x.net_total
        dn['base_total_taxes_and_charges'] = x.base_total_taxes_and_charges
        dn['total_taxes_and_charges'] = x.total_taxes_and_charges
        dn['apply_discount_on'] = x.apply_discount_on
        dn['base_discount_amount'] = x.base_discount_amount
        dn['additional_discount_percentage'] = x.additional_discount_percentage
        dn['discount_amount'] = x.discount_amount
        dn['base_grand_total'] = x.base_grand_total
        dn['base_in_words'] = x.base_in_words
        dn['grand_total'] = x.grand_total
        dn['in_words'] = x.in_words
        dn['docstatus'] = x.docstatus


    child_data_1 = frappe.db.get_list('Delivery Note Item', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'item_code',
                                          'item_name',
                                          'description',
                                          'item_group',
                                          'brand',
                                          'image',
                                          'qty',
                                          'stock_uom',
                                          'uom',
                                          'conversion_factor',
                                          'stock_qty',
                                          'price_list_rate',
                                          'base_price_list_rate',
                                          'margin_type',
                                          'margin_rate_or_amount',
                                          'rate_with_margin',
                                          'discount_percentage',
                                          'discount_amount',
                                          'base_rate_with_margin',
                                          'rate',
                                          'net_rate',
                                          'amount',
                                          'item_tax_template',
                                          'net_amount',
                                          'base_rate',
                                          'base_net_rate',
                                          'base_amount',
                                          'base_net_amount',
                                          'warehouse',
                                          'actual_qty',
                                      ])

    child_data_2 = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'charge_type',
                                          'row_id',
                                          'account_head',
                                          'description',
                                          'cost_center',
                                          'rate',
                                          'account_currency',
                                          'tax_amount',
                                          'total',
                                          'tax_amount_after_discount_amount',
                                          'base_tax_amount',
                                          'base_total',
                                          'base_tax_amount_after_discount_amount',
                                      ])

    child_data_3 = frappe.db.get_list('Payment Schedule', filters={'parent': name}, order_by='idx',
                                      fields=[
                                          'idx',
                                          'name',
                                          'payment_term',
                                          'description',
                                          'due_date',
                                          'mode_of_payment',
                                          'invoice_portion',
                                          'discount_type',
                                          'discount_date',
                                          'discount',
                                          'payment_amount',
                                          'outstanding',
                                          'paid_amount',
                                          'discounted_amount',
                                          'base_payment_amount',
                                      ],
                                      )

    if child_data_1 and doc_data:
        dn['items'] = child_data_1

    if child_data_2 and doc_data:
        dn['taxes'] = child_data_2

    if child_data_3 and doc_data:
        dn['payment_schedule'] = child_data_3

    attachments = frappe.db.sql(""" Select file_name, file_url, 
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Delivery Note"
                                        and `tabFile`.attached_to_name = "{name}"
                                    """.format(name=name), as_dict=1)

    dn['attachments'] = attachments

    comments = frappe.db.sql(""" Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Delivery Note"
                                        and `tabComment`.reference_name = "{name}" 
                                        and `tabComment`.comment_type = "Comment"
                                    """.format(name=name), as_dict=1)

    dn['comments'] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Delivery Note" and disabled = 0 """, as_dict=1)
    dn['print_formats'] = print_formats
    pf_standard = {}
    pf_standard['name'] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return dn
    else:
        return "لا يوجد إذن تسليم بهذا الاسم"


@frappe.whitelist()
def default_tax_template():
    tax = {}
    child_data = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': "Default Tax Template"},
                                    fields=[
                                        'charge_type',
                                        'description',
                                        'account_head',
                                    ])

    if child_data:
        tax['sales_taxes_table'] = child_data
        return tax

@frappe.whitelist(allow_guest=True)
def filtered_address(name):
    addresses = frappe.db.get_list('Dynamic Link', filters={'link_name': name}, fields=['parent'])
    result = []
    for item_dict in frappe.db.get_list('Dynamic Link', filters={'link_name': name}, fields=['parent']):
        adddd = frappe.db.get_list('Address', filters={'name': item_dict.parent}, fields=['name','address_title','address_line1','city','phone'])
        for x in adddd:
            data = {
                'name': x.name,
                'address_title': x.address_title,
                'address_line1': x.address_line1,
                'city': x.city,
                'phone': x.phone
            }





            result.append(data)

    if addresses:
        return result
    else:
        return "لا يوجد عنوان !"


@frappe.whitelist()
def filtered_contact(name):
    contacts = frappe.db.get_list('Dynamic Link', filters={'link_name': name}, fields=['parent'])
    result = []
    for item_dict in frappe.db.get_list('Dynamic Link', filters={'link_name': name}, fields=['parent']):
        adddd = frappe.db.get_list('Contact', filters={'name': item_dict.parent},
                                   fields=['name', 'email_id', 'phone', 'mobile_no', 'company_name'])
        for x in adddd:
            data = {
                'name': x.name,
                'email_id': x.email_id,
                'phone': x.phone,
                'mobile_no': x.mobile_no,
                'company_name': x.company_name
            }
            result.append(data)

    if contacts:
        return result
    else:
        return "لا يوجد جهة اتصال !"