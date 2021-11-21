from __future__ import unicode_literals
import frappe
import erpnext
from frappe import auth
import datetime
import json, ast
from erpnext.accounts.utils import get_balance_on


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

    quotation = frappe.db.get_list('Quotation', filters={'opportunity': name}, fields=['name'])

    connections = {}
    if quotation and doc_data:
        connections['quotation'] = quotation

    sup_quotation = frappe.db.get_list('Supplier Quotation', filters={'opportunity': name}, fields=['name'])

    if sup_quotation and doc_data:
        connections['sup_quotation'] = sup_quotation

    opp['conn'] = connections

    if doc_data:
        return opp
    else:
        return "لا يوجد فرصة بيعية بهذا الاسم"


@frappe.whitelist()
def customer(name):
    cust = {}
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


    child_data_3 = frappe.db.get_list('Customer Credit Limit', filters={'parent': name},
                                      fields=[
                                          'name',
                                          'company',
                                          'credit_limit',
                                          'bypass_credit_limit_check',
                                      ])

    if child_data_3 and doc_data:
        cust['customer_credit_limit'] = child_data_3


    opportunity = frappe.db.get_list('Opportunity', filters={'party_name': name}, fields=['name'])
    quotation = frappe.db.get_list('Quotation', filters={'party_name': name}, fields=['name'])
    sales_order = frappe.db.get_list('Sales Order', filters={'customer': name}, fields=['name'])
    delivery_note = frappe.db.get_list('Delivery Note', filters={'customer': name}, fields=['name'])
    sales_invoice = frappe.db.get_list('Sales Invoice', filters={'customer': name}, fields=['name'])
    payment_entry = frappe.db.get_list('Payment Entry', filters={'party': name}, fields=['name'])

    connections = {}
    if quotation and doc_data:
        connections['quotation'] = quotation

    if opportunity and doc_data:
        connections['opportunity'] = opportunity

    if sales_order and doc_data:
        connections['sales_order'] = sales_order

    if delivery_note and doc_data:
        connections['delivery_note'] = delivery_note

    if sales_invoice and doc_data:
        connections['sales_invoice'] = sales_invoice

    if payment_entry and doc_data:
        connections['payment_entry'] = payment_entry

    cust['conn'] = connections

    balance = get_balance_on(account=None, date='2021-11-21', party_type='Customer', party=name, company=None, in_account_currency=True, cost_center=None, ignore_account_permission=False)
    cust['balance'] = balance


    if doc_data:
        return cust
    else:
        return "لا يوجد عميل بهذا الاسم"


@frappe.whitelist()
def lead(name):
    led = {}
    doc_data = frappe.db.get_list('Lead', filters={'name': name},
                                  fields=['lead_name',
                                          'company_name',
                                          'lead_owner',
                                          'status',
                                          'source',
                                          'designation',
                                          'email_id',
                                          'gender',
                                          'campaign_name',
                                          'type',
                                          'market_segment',
                                          'territory',
                                          'industry',
                                          'company'

                                          ])
    for x in doc_data:
        led['lead_name'] = x.lead_name
        led['company_name'] = x.company_name
        led['lead_owner'] = x.lead_owner
        led['source'] = x.source
        led['designation'] = x.designation
        led['status'] = x.status
        led['email_id'] = x.email_id
        led['gender'] = x.gender
        led['campaign_name'] = x.campaign_name
        led['type'] = x.type
        led['market_segment'] = x.market_segment
        led['territory'] = x.territory
        led['industry'] = x.industry
        led['company'] = x.company

    quotation = frappe.db.get_list('Quotation', filters={'party_name': name}, fields=['name'])

    connections = {}
    if quotation and doc_data:
        connections['quotation'] = quotation

    opportunity = frappe.db.get_list('Opportunity', filters={'party_name': name}, fields=['name'])

    if opportunity and doc_data:
        connections['opportunity'] = opportunity

    led['conn'] = connections

    if doc_data:
        return led
    else:
        return "لا يوجد عميل محتمل بهذا الاسم"

@frappe.whitelist()
def quotation(name):
    qtn = {}
    doc_data = frappe.db.get_list('Quotation', filters={'name': name},
                                  fields=['quotation_to',
                                          'party_name',
                                          'customer_name',
                                          'amended_from',
                                          'company',
                                          'transaction_date',
                                          'valid_till',
                                          'order_type',
                                          'customer_address',
                                          'address_display',
                                          'contact_person',
                                          'contact_display',
                                          'contact_mobile',
                                          'contact_email',
                                          'shipping_address_name',
                                          'shipping_address',
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
                                          'other_charges_calculation',
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
                                          'enq_det',
                                          'lost_reasons'
                                          ])
    for x in doc_data:
        qtn['quotation_to'] = x.quotation_to
        qtn['party_name'] = x.party_name
        qtn['customer_name'] = x.customer_name
        qtn['amended_from'] = x.amended_from
        qtn['company'] = x.company
        qtn['transaction_date'] = x.transaction_date
        qtn['valid_till'] = x.valid_till
        qtn['order_type'] = x.order_type
        qtn['customer_address'] = x.customer_address
        qtn['address_display'] = x.address_display
        qtn['contact_person'] = x.contact_person
        qtn['contact_display'] = x.contact_display
        qtn['contact_mobile'] = x.contact_mobile
        qtn['contact_email'] = x.contact_email
        qtn['shipping_address_name'] = x.shipping_address_name
        qtn['shipping_address'] = x.shipping_address
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
        qtn['total_net_weight'] = x.total_net_weight
        qtn['tax_category'] = x.tax_category
        qtn['shipping_rule'] = x.shipping_rule
        qtn['taxes_and_charges'] = x.taxes_and_charges
        qtn['other_charges_calculation'] = x.other_charges_calculation
        qtn['base_total_taxes_and_charges'] = x.base_total_taxes_and_charges
        qtn['total_taxes_and_charges'] = x.total_taxes_and_charges
        qtn['coupon_code'] = x.coupon_code
        qtn['referral_sales_partner'] = x.referral_sales_partner
        qtn['apply_discount_on'] = x.apply_discount_on
        qtn['base_discount_amount'] = x.base_discount_amount
        qtn['additional_discount_percentage'] = x.additional_discount_percentage
        qtn['discount_amount'] = x.discount_amount
        qtn['base_grand_total'] = x.base_grand_total
        qtn['base_rounding_adjustment'] = x.base_rounding_adjustment
        qtn['base_in_words'] = x.base_in_words
        qtn['base_rounded_total'] = x.base_rounded_total
        qtn['grand_total'] = x.grand_total
        qtn['rounding_adjustment'] = x.rounding_adjustment
        qtn['rounded_total'] = x.rounded_total
        qtn['in_words'] = x.in_words
        qtn['payment_terms_template'] = x.payment_terms_template
        qtn['tc_name'] = x.tc_name
        qtn['terms'] = x.terms
        qtn['letter_head'] = x.letter_head
        qtn['group_same_items'] = x.group_same_items
        qtn['select_print_heading'] = x.select_print_heading
        qtn['language'] = x.language
        qtn['auto_repeat'] = x.auto_repeat
        qtn['update_auto_repeat_reference'] = x.update_auto_repeat_reference
        qtn['campaign'] = x.campaign
        qtn['source'] = x.source
        qtn['order_lost_reason'] = x.order_lost_reason
        qtn['status'] = x.status
        qtn['enq_det'] = x.enq_det
        qtn['lost_reasons'] = x.lost_reasons

    child_data_1 = frappe.db.get_list('Quotation Item', filters={'parent': name},
                                      fields=[
                                          'name',
                                          'item_code',
                                          'customer_item_code',
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
                                          'discount_and_margin',
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
                                          'pricing_rules',
                                          'stock_uom_rate',
                                          'valuation_rate',
                                          'gross_profit',
                                          'weight_per_unit',
                                          'total_weight',
                                          'weight_uom',
                                          'warehouse',
                                          'prevdoc_doctype',
                                          'prevdoc_docname',
                                          'projected_qty',
                                          'actual_qty',
                                          'stock_balance',
                                          'item_tax_rate',
                                      ])

    child_data_2 = frappe.db.get_list('Pricing Rule Detail', filters={'parent': name},
                                      fields=[
                                          'name',
                                          'pricing_rule',
                                          'item_code',
                                          'margin_type',
                                          'rate_or_discount',
                                          'child_docname',
                                          'rule_applied',
                                      ])

    child_data_3 = frappe.db.get_list('Sales Taxes and Charges', filters={'parent': name},
                                      fields=[
                                          'name',
                                          'charge_type',
                                          'row_id',
                                          'account_head',
                                          'description',
                                          'included_in_print_rate',
                                          'included_in_paid_amount',
                                          'cost_center',
                                          'rate',
                                          'account_currency',
                                          'tax_amount',
                                          'total',
                                          'tax_amount_after_discount_amount',
                                          'base_tax_amount',
                                          'base_total',
                                          'base_tax_amount_after_discount_amount',
                                          'item_wise_tax_detail',
                                          'dont_recompute_tax',
                                      ])

    child_data_4 = frappe.db.get_list('Payment Schedule', filters={'parent': name},
                                      fields=[
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
        cust['allowed_to_transact_with'] = child_data_1

    if child_data_2 and doc_data:
        cust['party_account'] = child_data_2

    if child_data_3 and doc_data:
        cust['customer_credit_limit'] = child_data_3

    if child_data_4 and doc_data:
        cust['sales_team'] = child_data_4

    opportunity = frappe.db.get_list('Opportunity', filters={'party_name': name}, fields=['name'])
    quotation = frappe.db.get_list('Quotation', filters={'party_name': name}, fields=['name'])
    sales_order = frappe.db.get_list('Sales Order', filters={'customer': name}, fields=['name'])
    delivery_note = frappe.db.get_list('Delivery Note', filters={'customer': name}, fields=['name'])
    sales_invoice = frappe.db.get_list('Sales Invoice', filters={'customer': name}, fields=['name'])
    payment_entry = frappe.db.get_list('Payment Entry', filters={'party': name}, fields=['name'])

    connections = {}
    if quotation and doc_data:
        connections['quotation'] = quotation

    if opportunity and doc_data:
        connections['opportunity'] = opportunity

    if sales_order and doc_data:
        connections['sales_order'] = sales_order

    if delivery_note and doc_data:
        connections['delivery_note'] = delivery_note

    if sales_invoice and doc_data:
        connections['sales_invoice'] = sales_invoice

    if payment_entry and doc_data:
        connections['payment_entry'] = payment_entry

    cust['conn'] = connections

    if doc_data:
        return cust
    else:
        return "لا يوجد عميل بهذا الاسم"