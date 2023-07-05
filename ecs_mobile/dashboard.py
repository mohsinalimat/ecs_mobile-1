import frappe
import requests


def get_request(url, params):
    response = requests.get(url=url, params=params)
    if response.status_code // 100 == 2:
        return response.json()

    raise Exception(response.text)


PREFIX_URL = "https://mobile.erpcloud.systems/api/method/ecs_mobile"


# drafted 0
# submitted 1
# canceled 2

def get_sales_invoices(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '1'
    params['filters']['is_return'] = '0'
    return get_request(f"{PREFIX_URL}.general.sales_invoices", params['filters'])['data']


def get_returned_sales_invoices(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '1'
    params['filters']['is_return'] = '1'
    return get_request(f"{PREFIX_URL}.general.sales_invoices", params['filters'])['data']


def get_customer_visits(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '0,1'
    return get_request(f"{PREFIX_URL}.general.customer_visits", params['filters'])['data']


def get_payment_entries(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '1'
    return get_request(f"{PREFIX_URL}.general.payment_entries", params['filters'])['data']


def get_stock_entries(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '1'
    params['filters']['is_return'] = '0'
    return get_request(f"{PREFIX_URL}.general.stock_entries", params['filters'])['data']


def get_quotations(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '0,1'
    return get_request(f"{PREFIX_URL}.general.quotations", params['filters'])['data']


def get_delivery_notes(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '0,1'
    return get_request(f"{PREFIX_URL}.general.delivery_notes", params['filters'])['data']


def get_sales_orders(filters):
    params = {
        'filters': filters
    }
    params['filters']['status'] = '0,1'
    return get_request(f"{PREFIX_URL}.general.sales_orders", params['filters'])['data']


@frappe.whitelist(methods=['GET'])
def get_dashboard_data():
    filters = dict(frappe.local.request.args)

    results = {}
    results['sales_invoices'] = get_sales_invoices(filters)
    results['returned_sales_invoices'] = get_returned_sales_invoices(filters)
    results['customer_visits'] = get_customer_visits(filters)
    results['payment_entries'] = get_payment_entries(filters)
    results['stock_entries'] = get_stock_entries(filters)
    results['quotations'] = get_quotations(filters)
    results['delivery_notes'] = get_delivery_notes(filters)
    results['sales_orders'] = get_sales_orders(filters)

    frappe.response['data'] = results
    frappe.response['is_success'] = True

