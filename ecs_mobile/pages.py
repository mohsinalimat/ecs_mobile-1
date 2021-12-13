from __future__ import unicode_literals
import frappe
import erpnext
from frappe import auth
import datetime
import json, ast
from erpnext.accounts.utils import get_balance_on
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from frappe.utils import add_to_date, now, nowdate


@frappe.whitelist()
def lead(name):
    led = {}
    doc_data = frappe.db.get_list('Lead', filters={'name': name},
                                  fields=['lead_name',
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
                                          'industry'
                                          ])
    for x in doc_data:
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

    quotation_count = frappe.db.count('Quotation', filters={'party_name': name})
    #quotation_name = frappe.db.get_list('Quotation', filters={'party_name': name}, fields=['name'])

    #connections = {}
    qtn_connections = {}
    opp_connections = {}

    if quotation_count and doc_data:
        #connections['quotation_count'] = quotation_count
        qtn_connections['name'] = "Quotation"
        qtn_connections['count'] = quotation_count
        qtn_connections['icon'] = "https://erpcloud.systems/icons/quotation.png"
    #if quotation_name and doc_data:
    #    connections['quotation_name'] = quotation_name

    opportunity_count = frappe.db.count('Opportunity', filters={'party_name': name})
    #opportunity_name = frappe.db.get_list('Opportunity', filters={'party_name': name}, fields=['name'])

    if opportunity_count and doc_data:
        #connections['opportunity_count'] = opportunity_count
        opp_connections['name'] = "Opportunity"
        opp_connections['count'] = opportunity_count
        opp_connections['icon'] = "https://erpcloud.systems/icons/opportunity.png"
    #if opportunity_name and doc_data:
    #    connections['opportunity_name'] = opportunity_name

    connections = [qtn_connections, opp_connections]
    led['conn'] = connections
    #led['qtn_conn'] = qtn_connections
    #led['opp_conn'] = opp_connections

    if doc_data:
        return led
    else:
        return "لا يوجد عميل محتمل بهذا الاسم"

@frappe.whitelist()
def opportunity(name):
    opp = {}
    doc_data = frappe.db.get_list('Opportunity', filters={'name': name},
                                  fields=['opportunity_from',
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
                                          'transaction_date'
                                          ])
    for x in doc_data:
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

    child_data = frappe.db.get_list('Opportunity Item', filters={'parent': name},
                                    fields=[
                                        'name',
                                        'item_code',
                                        'qty',
                                        'item_group',
                                        'brand',
                                        'uom',
                                        'item_name',
                                        'description',
                                        'image',
                                        'basic_rate',

                                    ])

    if child_data and doc_data:
        opp['items'] = child_data

    quotation_count = frappe.db.count('Quotation', filters={'opportunity': name})
    sup_quotation_count = frappe.db.count('Supplier Quotation', filters={'opportunity': name})

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
                                  fields=['quotation_to',
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
                                          'status'
                                          ])

    for x in doc_data:
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

    child_data_1 = frappe.db.get_list('Quotation Item', filters={'parent': name},
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


    child_data_2 = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': name},
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

    child_data_3 = frappe.db.get_list('Payment Schedule', filters={'parent': name},
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
        qtn['quotation_items'] = child_data_1

    if child_data_2 and doc_data:
        qtn['sales_taxes'] = child_data_2

    if child_data_3 and doc_data:
        qtn['payment_schedule'] = child_data_3

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
                                  fields=['customer_name',
                                          'customer_type',
                                          'lead_name',
                                          'opportunity_name',
                                          'tax_id',
                                          'tax_category',
                                          'customer_group',
                                          'territory',
                                          'account_manager',
                                          'disabled',
                                          'is_internal_customer',
                                          'represents_company',
                                          'default_currency',
                                          'default_price_list',
                                          'customer_primary_contact',
                                          'customer_primary_address',
                                          'mobile_no',
                                          'email_id',
                                          'payment_terms',
                                          'customer_details',
                                          'market_segment',
                                          'industry',
                                          'is_frozen',
                                          'default_sales_partner',
                                          'so_required',
                                          'dn_required',
                                          'tax_withholding_category'
                                          ])
    for x in doc_data:
        cust['customer_name'] = x.customer_name
        cust['customer_type'] = x.customer_type
        cust['lead_name'] = x.lead_name
        cust['opportunity_name'] = x.opportunity_name
        cust['tax_withholding_category'] = x.tax_withholding_category
        cust['tax_id'] = x.tax_id
        cust['tax_category'] = x.tax_category
        cust['customer_group'] = x.customer_group
        cust['territory'] = x.territory
        cust['account_manager'] = x.account_manager
        cust['disabled'] = x.disabled
        cust['is_internal_customer'] = x.is_internal_customer
        cust['represents_company'] = x.represents_company
        cust['default_currency'] = x.default_currency
        cust['default_price_list'] = x.default_price_list
        cust['website'] = x.website
        cust['customer_primary_contact'] = x.customer_primary_contact
        cust['customer_primary_address'] = x.customer_primary_address
        cust['mobile_no'] = x.mobile_no
        cust['email_id'] = x.email_id
        cust['payment_terms'] = x.payment_terms
        cust['customer_details'] = x.customer_details
        cust['market_segment'] = x.market_segment
        cust['industry'] = x.industry
        cust['language'] = x.language
        cust['is_frozen'] = x.is_frozen
        cust['loyalty_program'] = x.loyalty_program
        cust['default_sales_partner'] = x.default_sales_partner
        cust['default_commission_rate'] = x.default_commission_rate
        cust['image'] = x.image
        cust['so_required'] = x.so_required
        cust['dn_required'] = x.dn_required


    child_data = frappe.db.get_list('Customer Credit Limit', filters={'parent': name},
                                      fields=[
                                          'name',
                                          'company',
                                          'credit_limit',
                                          'bypass_credit_limit_check',
                                      ])

    if child_data and doc_data:
        cust['customer_credit_limit'] = child_data

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
                                  fields=['customer',
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
                                          ])

    for x in doc_data:
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

    child_data_1 = frappe.db.get_list('Sales Order Item', filters={'parent': name},
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


    child_data_2 = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': name},
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

    child_data_3 = frappe.db.get_list('Payment Schedule', filters={'parent': name},
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
        so['sales_order_items'] = child_data_1

    if child_data_2 and doc_data:
        so['sales_taxes'] = child_data_2

    if child_data_3 and doc_data:
        so['payment_schedule'] = child_data_3

    sales_invoice = frappe.db.get_list('Sales Invoice Item', filters={'sales_order': name}, fields=['parent'], group_by='parent')
    delivery_note = frappe.db.get_list('Delivery Note Item', filters={'against_sales_order': name}, fields=['parent'], group_by='parent')
    material_request = frappe.db.get_list('Material Request Item', filters={'sales_order': name}, fields=['parent'], group_by='parent')
    purchase_order = frappe.db.get_list('Purchase Order Item', filters={'sales_order': name}, fields=['parent'], group_by='parent')
    quotation = frappe.db.get_list('Sales Order Item', filters={'parent': name}, fields=['prevdoc_docname'], group_by='prevdoc_docname')
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
