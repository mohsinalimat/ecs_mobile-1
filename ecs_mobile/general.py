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
def general_service(doctype, search_text='%%', cur_nam='%%', con_doc='%%', start=0, page_length=20):

############################################ LEAD ############################################

########################### Lead Full List & Search ############################
    if doctype == "Lead" and con_doc == '%%':
        query = frappe.db.get_list('Lead',
           or_filters=[{'name': ['like', search_text]},
                       {'lead_name': ['like', search_text]},
                       {'company_name': ['like', search_text]},
                       {'mobile_no': ['like', search_text]}],
           fields=["name", "lead_name", "company_name", "territory", "source", "market_segment", "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

########################### Quotations Connected With Lead & Search ############################
    if doctype == "Quotation" and con_doc == "Lead":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
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
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

############################################ OPPORTUNITY ############################################

########################### Opportunity Full List & Search ############################
    if doctype == "Opportunity" and con_doc == '%%':
        query = frappe.db.get_list('Opportunity',
           or_filters=[{'name': ['like', search_text]},
                       {'customer_name': ['like', search_text]},
                       {'party_name': ['like', search_text]}],
           fields=["name", "opportunity_from", "customer_name", "transaction_date",
                   "opportunity_type", "sales_stage", "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

########################### Quotations Connected With Opportunity & Search ############################
    if doctype == "Quotation" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, grand_total, status
                from `tabQuotation` where `opportunity` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Supplier Quotations Connected With Opportunity & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name,supplier,transaction_date,valid_till,grand_total,status
                from `tabSupplier Quotation` where `opportunity` = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier like '%{search_text}%' or `tabSupplier Quotation`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

############################################ QUOTATION ############################################

########################### Quotation Full List & Search ############################
    if doctype == "Quotation" and con_doc == '%%':
        query = frappe.db.get_list('Quotation',
           or_filters=[{'name': ['like', search_text]},
                       {'customer_name': ['like', search_text]},
                       {'party_name': ['like', search_text]}],
           fields=["name", "quotation_to", "customer_name", "transaction_date", "grand_total",
                   "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

########################### Sales Orders Connected With Quotation & Search ############################
    if doctype == "Sales Order" and con_doc == "Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                       `tabSales Order`.transaction_date as transaction_date,`tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                from `tabSales Order` join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent
                where `tabSales Order Item`.prevdoc_docname = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

############################################ CUSTOMER ############################################

########################### Customer Full List & Search ############################
    if doctype == "Customer" and con_doc == '%%':
        query = frappe.db.get_list('Customer',
           filters=[{'disabled': ['=', 0]}],
           or_filters=[{'name': ['like', search_text]},
                       {'customer_name': ['like', search_text]},
                       {'mobile_no': ['like', search_text]}],
           fields=["name","customer_name","customer_group","customer_type","territory","mobile_no","tax_id","customer_primary_address","customer_primary_contact","default_currency","default_price_list","payment_terms","default_sales_partner"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

########################### Quotations Connected With Customer & Search ############################
    if doctype == "Quotation" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
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
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Sales Orders Connected With Customer & Search ############################
    if doctype == "Sales Order" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,transaction_date,grand_total,status
                from `tabSales Order` where `customer` = '{cur_nam}' 
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Delivery Notes Connected With Customer & Search ############################
    if doctype == "Delivery Note" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer,territory,posting_date,set_warehouse,status
                from `tabDelivery Note` where `customer` = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Sales Invoices Connected With Customer & Search ############################
    if doctype == "Sales Invoice" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,posting_date,grand_total,status
                from `tabSales Invoice` where `customer` = '{cur_nam}'
                and (`tabSales Invoice`.name like '%{search_text}%' or `tabSales Invoice`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Payment Entries Connected With Customer & Search ############################
    if doctype == "Payment Entry" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,party_name,payment_type,mode_of_payment,posting_date,paid_amount,status
                from `tabPayment Entry` where `party` = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

############################################ SALES ORDER ############################################

########################### Sales Order Full List & Search ############################
    if doctype == "Sales Order" and con_doc == '%%':
        query = frappe.db.get_list('Sales Order',
           or_filters=[{'name': ['like', search_text]},
                       {'customer_name': ['like', search_text]},
                       {'customer': ['like', search_text]}],
           fields=["name", "customer_name", "customer_address", "transaction_date",
                   "grand_total", "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

########################### Sales Invoices Connected With Sales Order & Search ############################
    if doctype == "Sales Invoice" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabSales Invoice`.name as name,`tabSales Invoice`.customer_name as customer_name,`tabSales Invoice`.customer_address as customer_address,
                       `tabSales Invoice`.posting_date as posting_date,`tabSales Invoice`.grand_total as grand_total,`tabSales Invoice`.status as status
                from `tabSales Invoice` join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                where `tabSales Invoice Item`.sales_order = '{cur_nam}'
                and (`tabSales Invoice`.name like '%{search_text}%' or `tabSales Invoice`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Delivery Notes Connected With Sales Order & Search ############################
    if doctype == "Delivery Note" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                       `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse,`tabDelivery Note`.status as status
                from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                where `tabDelivery Note Item`.against_sales_order = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
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
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Purchase Orders Connected With Sales Order & Search ############################
    if doctype == "Purchase Order" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier, `tabPurchase Order`.grand_total as grand_total,
                      `tabPurchase Order`.transaction_date as transaction_date,`tabPurchase Order`.set_warehouse as set_warehouse,`tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                where `tabPurchase Order Item`.sales_order = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%' or `tabPurchase Order`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Quotations Connected With Sales Order & Search ############################
    if doctype == "Quotation" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabQuotation`.name as name, `tabQuotation`.quotation_to as quotation_to, `tabQuotation`.customer_name as customer_name,
                       `tabQuotation`.transaction_date as transaction_date, `tabQuotation`.grand_total as grand_total, `tabQuotation`.status as status
                from `tabQuotation` join `tabSales Order Item` on `tabQuotation`.name = `tabSales Order Item`.prevdoc_docname
                where `tabSales Order Item`.parent = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Payment Entries Connected With Sales Order & Search ############################
    if doctype == "Payment Entry" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                       `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as paid_amount,`tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

############################################ SALES INVOICE ############################################

########################### Sales Invoice Full List & Search ############################
    if doctype == "Sales Invoice" and con_doc == '%%':
        query = frappe.db.get_list('Sales Invoice',
           or_filters=[{'name': ['like', search_text]},
                       {'customer_name': ['like', search_text]},
                       {'customer': ['like', search_text]}],
           fields=["name", "customer_name", "customer_address", "posting_date", "grand_total",
                   "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

########################### Sales Orders Connected With Sales Invoice & Search ############################
    if doctype == "Sales Order" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                    `tabSales Order`.transaction_date as transaction_date,`tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                from `tabSales Order` join `tabSales Invoice Item` on `tabSales Order`.name = `tabSales Invoice Item`.sales_order
                where `tabSales Invoice Item`.parent = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Delivery Notes Connected With Sales Invoice & Search ############################
    if doctype == "Delivery Note" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                       `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse,`tabDelivery Note`.status as status
                from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                where `tabDelivery Note Item`.against_sales_invoice = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

########################### Payment Entries Connected With Sales Invoice & Search ############################
    if doctype == "Payment Entry" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                       `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as paid_amount,`tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(start=start, page_length=page_length, cur_nam=cur_nam, search_text=search_text), as_dict=1)
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

############################################ PAYMENT ENTRY ############################################

########################### Payment Entry Full List & Search ############################
    if doctype == "Payment Entry" and con_doc == '%%':
        query = frappe.db.get_list('Payment Entry',
           or_filters=[{'name': ['like', search_text]},
                       {'party_name': ['like', search_text]},
                       {'mode_of_payment': ['like', search_text]},
                       {'party': ['like', search_text]}],
           fields=["name", "party_name", "payment_type", "mode_of_payment", "posting_date",
                   "paid_amount", "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ LEAD SOURCE ############################################

########################### Lead Source Full List & Search ############################
    if doctype == "Lead Source" and con_doc == '%%':
        query = frappe.db.get_list('Lead Source',
           or_filters=[{'name': ['like', search_text]},
                       {'source_name': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ PROJECT ############################################

########################### Project Segment Full List & Search ############################
    if doctype == "Project" and con_doc == '%%':
        query = frappe.db.get_list('Project',
           filters=[{'is_active': ['=', 'Yes']}],
           or_filters=[{'name': ['like', search_text]},
                       {'project_name': ['like', search_text]}],
           fields=["name", "project_name", "status"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ PAYMENT TERMS TEMPLATE ############################################

########################### Payment Terms Template Full List & Search ############################
    if doctype == "Payment Terms Template" and con_doc == '%%':
        query = frappe.db.get_list('Payment Terms Template',
           or_filters=[{'name': ['like', search_text]},
                       {'template_name': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ MARKET SEGEMENT ############################################

########################### Market Segment Full List & Search ############################
    if doctype == "Market Segment" and con_doc == '%%':
        query = frappe.db.get_list('Market Segment',
           or_filters=[{'name': ['like', search_text]},
                       {'market_segment': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ TERRITORY ############################################

########################### Territory Full List & Search ############################
    if doctype == "Territory" and con_doc == '%%':
        query = frappe.db.get_list('Territory',
           filters=[{'is_group': ['=', 0]}],
           or_filters=[{'name': ['like', search_text]},
                       {'territory_name': ['like', search_text]}],
           fields=["name", "parent_territory"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ WAREHOUSE ############################################

########################### Warehouse Full List & Search ############################
    if doctype == "Warehouse" and con_doc == '%%':
        query = frappe.db.get_list('Warehouse',
           filters=[{'is_group': ['=', 0]}],
           or_filters=[{'name': ['like', search_text]},
                       {'warehouse_name': ['like', search_text]}],
           fields=["name", "warehouse_name", "warehouse_type", "parent_warehouse"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ COUNTRY ############################################

########################### Country Full List & Search ############################
    if doctype == "Country" and con_doc == '%%':
        query = frappe.db.get_list('Country',
           or_filters=[{'name': ['like', search_text]},
                       {'country_name': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ OPPORTUNITY TYPE ############################################

########################### Opportunity Type Full List & Search ############################
    if doctype == "Opportunity Type" and con_doc == '%%':
        query = frappe.db.get_list('Opportunity Type',
           or_filters=[{'name': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ CUSTOMER GROUP ############################################

########################### Customer Group Full List & Search ############################
    if doctype == "Customer Group" and con_doc == '%%':
        query = frappe.db.get_list('Customer Group',
           filters=[{'is_group': ['=', 0]}],
           or_filters=[{'name': ['like', search_text]},
                       {'customer_group_name': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ CAMPAIGN ############################################

########################### Campaign Full List & Search ############################
    if doctype == "Campaign" and con_doc == '%%':
        query = frappe.db.get_list('Campaign',
           or_filters=[{'name': ['like', search_text]},
                       {'campaign_name': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ INDUSTRY TYPE ############################################

########################### Industry Type Full List & Search ############################
    if doctype == "Industry Type" and con_doc == '%%':
        query = frappe.db.get_list('Industry Type',
           or_filters=[{'name': ['like', search_text]},
                       {'industry': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ CURRENCY ############################################

########################### Currency Full List & Search ############################
    if doctype == "Currency" and con_doc == '%%':
        query = frappe.db.get_list('Currency',
           or_filters=[{'name': ['like', search_text]},
                       {'currency_name': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ SALES PARTNER ############################################

########################### Sales Partner Full List & Search ############################
    if doctype == "Sales Partner" and con_doc == '%%':
        query = frappe.db.get_list('Sales Partner',
           or_filters=[{'name': ['like', search_text]},
                       {'partner_name': ['like', search_text]}],
           fields=["name","commission_rate"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ TERMS & CONDITIONS ############################################

########################### Terms and Conditions Full List & Search ############################
    if doctype == "Terms and Conditions" and con_doc == '%%':
        query = frappe.db.get_list('Terms and Conditions',
           or_filters=[{'name': ['like', search_text]},
                       {'title': ['like', search_text]}],
           fields=["name"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ MODE OF PAYMENT ############################################

########################### Mode of Payment Full List & Search ############################
    if doctype == "Mode of Payment" and con_doc == '%%':
        query = frappe.db.get_list('Mode of Payment',
           or_filters=[{'name': ['like', search_text]},
                       {'mode_of_payment': ['like', search_text]}],
           fields=["name", "type"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ PRICE LIST ############################################

########################### Price List Full List & Search ############################
    if doctype == "Price List" and con_doc == '%%':
        query = frappe.db.get_list('Price List',
           or_filters=[{'name': ['like', search_text]},
                       {'price_list_name': ['like', search_text]}],
           fields=["name", "currency"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ COST CENTER ############################################

########################### Cost Center Full List & Search ############################
    if doctype == "Cost Center" and con_doc == '%%':
        query = frappe.db.get_list('Cost Center',
           filters=[{'is_group': ['=', 0]}],
           or_filters=[{'name': ['like', search_text]},
                       {'cost_center_name': ['like', search_text]}],
           fields=["name", "cost_center_name", "parent_cost_center"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ ACCOUNT ############################################

########################### Account Full List & Search ############################
    if doctype == "Account" and con_doc == '%%':
        query = frappe.db.get_list('Account',
           filters=[{'is_group': ['=', 0]}],
           or_filters=[{'name': ['like', search_text]},
                       {'account_name': ['like', search_text]},
                       {'account_number': ['like', search_text]}],
           fields=["name", "account_type", "root_type", "account_currency", "parent_account"],
           order_by='name asc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ ITEM ############################################

########################### Item Full List & Search ############################
    if doctype == "Item" and con_doc == '%%':
        query = frappe.db.get_list('Item',
           or_filters=[{'name': ['like', search_text]},
                       {'item_name': ['like', search_text]},
                       {'item_code': ['like', search_text]}],
           fields=["name", "item_name", "item_group", "stock_uom"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ MATERIAL REQUEST ############################################

########################### Material Request Full List & Search ############################
    if doctype == "Material Request" and con_doc == '%%':
        query = frappe.db.get_list('Material Request',
           or_filters=[{'name': ['like', search_text]},
                       {'title': ['like', search_text]}],
           fields=["name", "material_request_type", "transaction_date", "set_warehouse",
                   "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ STOCK ENTRY ############################################

########################### Stock Entry Full List & Search ############################
    if doctype == "Stock Entry" and con_doc == '%%':
        query = frappe.db.get_list('Stock Entry',
           or_filters=[{'name': ['like', search_text]},
                       {'title': ['like', search_text]}],
           fields=["name", "stock_entry_type", "posting_date", "from_warehouse", "to_warehouse",
                   "docstatus"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ PURCHASE RECEIPT ############################################

########################### Purchase Receipt Full List & Search ############################
    if doctype == "Purchase Receipt" and con_doc == '%%':
        query = frappe.db.get_list('Purchase Receipt',
           or_filters=[{'name': ['like', search_text]},
                       {'title': ['like', search_text]},
                       {'supplier': ['like', search_text]},
                       {'supplier_name': ['like', search_text]}],
           fields=["name", "supplier", "posting_date", "set_warehouse", "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ DELIVERY NOTE ############################################

########################### Delivery Note Full List & Search ############################
    if doctype == "Delivery Note" and con_doc == '%%':
        query = frappe.db.get_list('Delivery Note',
           or_filters=[{'name': ['like', search_text]},
                       {'title': ['like', search_text]},
                       {'customer': ['like', search_text]},
                       {'customer_name': ['like', search_text]}],
           fields=["name", "customer", "territory", "posting_date", "set_warehouse", "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ SUPPLIER ############################################

########################### Supplier Full List & Search ############################
    if doctype == "Supplier" and con_doc == '%%':
        query = frappe.db.get_list('Supplier',
           or_filters=[{'name': ['like', search_text]},
                       {'supplier_name': ['like', search_text]},
                       {'mobile_no': ['like', search_text]}],
           fields=["name", "supplier_name", "supplier_group", "supplier_type", "country",
                   "mobile_no"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ SUPPLIER QUOTATION ############################################

########################### Supplier Quotation Full List & Search ############################
    if doctype == "Supplier Quotation" and con_doc == '%%':
        query = frappe.db.get_list('Supplier Quotation',
           or_filters=[{'name': ['like', search_text]},
                       {'supplier': ['like', search_text]}],
           fields=["name", "supplier", "transaction_date", "valid_till", "grand_total",
                   "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ PURCHASE ORDER ############################################

########################### Purchase Order Full List & Search ############################
    if doctype == "Purchase Order" and con_doc == '%%':
        query = frappe.db.get_list('Purchase Order',
           or_filters=[{'name': ['like', search_text]},
                       {'supplier': ['like', search_text]}],
           fields=["name", "supplier", "transaction_date", "set_warehouse", "grand_total",
                   "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ PURCHASE INVOICE ############################################

########################### Purchase Invoice Full List & Search ############################
    if doctype == "Purchase Invoice" and con_doc == '%%':
        query = frappe.db.get_list('Purchase Invoice',
           or_filters=[{'name': ['like', search_text]},
                       {'supplier': ['like', search_text]}],
           fields=["name", "supplier", "posting_date", "grand_total", "status"],
           order_by='modified desc',
           start=start,
           page_length=page_length
           )
        if query:
            return query
        else:
            return "لا يوجد !"

############################################ ADDRESS ############################################

########################### Filtered Address List & Search ############################
    if doctype == "Address" and con_doc == '%%':
        addresses = frappe.db.get_list('Dynamic Link', filters={'link_name': cur_nam}, fields=['parent'])
        result = []
        for d in addresses:
            query = frappe.db.sql(""" select name as name ,
                                                 address_title as address_title,
                                                 address_line1 as address_line1,
                                                 city as city,
                                                 phone as phone
                                          from tabAddress where name = '{filtered}'
                                          and (address_title like '{search_text}' or address_line1 like '{search_text}'
                                               or city like '{search_text}' or phone like '{search_text}') LIMIT {start},{page_length}
                                      """.format(filtered=d.parent, search_text=search_text, start=start, page_length=page_length,), as_dict=1)
            for x in query:
                data = {
                    'name': x.name,
                    'address_title': x.address_title,
                    'address_line1': x.address_line1,
                    'city': x.city,
                    'phone': x.phone
                }
                result.append(data)

        if result:
            return result
        else:
            return "لا يوجد !"

############################################ CONTACT ############################################

########################### Filtered Contact List & Search ############################
    if doctype == "Contact" and con_doc == '%%':
        contacts = frappe.db.get_list('Dynamic Link', filters={'link_name': cur_nam}, fields=['parent'])
        result = []
        for d in contacts:
            query = frappe.db.sql(""" select name as name ,
                                             email_id as email_id,
                                             mobile_no as mobile_no,
                                             phone as phone,
                                             company_name as company_name
                                      from tabContact where name = '{filtered}'
                                      and (name like '{search_text}' or email_id like '{search_text}'
                                           or mobile_no like '{search_text}' or phone like '{search_text}'
                                           or company_name like '{search_text}') LIMIT {start},{page_length}
                                      """.format(filtered=d.parent, search_text=search_text, start=start, page_length=page_length,), as_dict=1)
            for x in query:
                data = {
                    'name': x.name,
                    'email_id': x.email_id,
                    'mobile_no': x.mobile_no,
                    'company_name': x.company_name,
                    'phone': x.phone
                }
                result.append(data)

        if result:
            return result
        else:
            return "لا يوجد !"

