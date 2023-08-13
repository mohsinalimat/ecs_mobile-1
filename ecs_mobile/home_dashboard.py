import frappe
from datetime import datetime, timedelta
from frappe.utils import getdate


class HomeDashboard:
    def __init__(self, _filters):
        self.result = {}
        self.filters = _filters

    def get_user_image(self):
        user_image = frappe.db.get_value(
            "User", {"name": frappe.session.user}, ["user_image"]
        )
        self.result["user_image"] = user_image

    def get_user_full_name(self):
        user_full_name = frappe.db.get_value(
            "User", {"name": frappe.session.user}, ["full_name"]
        )
        self.result["user_full_name"] = user_full_name

    def get_bar_chart_data(self):
        statuses = ["Paid", "Unpaid", "Return", "Overdue", "Canceled"]
        bar_chart_data = []

        for status in statuses:
            data = {}
            filters = {"status": status}

            if self.filters.get('from_date', None) and self.filters.get('to_date', None):
                filters["posting_date"] = ("BETWEEN", [
                    getdate(self.filters.get('from_date')),
                    getdate(self.filters.get('to_date'))
                ])

            elif self.filters.get('from_date', None):
                filters["posting_date"] = (">=", getdate(self.filters.get('from_date')))

            elif self.filters.get('to_date', None):
                filters["posting_date"] = ("<=", getdate(self.filters.get('to_date')))

            count = frappe.db.count("Sales Invoice", filters)
            data["title"] = status
            data["count"] = count
            bar_chart_data.append(data)

        self.result["bar_chart"] = bar_chart_data

    def get_total_gains(self):
        from_date = self.filters.get('from_date', None)
        to_date = self.filters.get('to_date', None)
        date_condition = ""

        if from_date:
            date_condition += f"AND posting_date >= '{from_date}'"
        if to_date:
            date_condition += f"AND posting_date <= '{to_date}'"

        invoices = frappe.db.sql(
            f"""
            SELECT COALESCE(SUM(grand_total), 0) as total_amount
            FROM `tabSales Invoice`
            WHERE status IN ('Paid', 'Partly Paid')
            {date_condition}
            """,
            as_dict=True,
        )

        self.result["total_gains"] = invoices[0].total_amount if invoices else 0

    def get_total_losses(self):
        from_date = self.filters.get('from_date', None)
        to_date = self.filters.get('to_date', None)
        date_condition = ""

        if from_date:
            date_condition += f"AND posting_date >= '{from_date}'"
        if to_date:
            date_condition += f"AND posting_date <= '{to_date}'"

        invoices = frappe.db.sql(
            f"""
            SELECT COALESCE(SUM(grand_total), 0) as total_amount
            FROM `tabSales Invoice`
            WHERE status = 'Return' 
            {date_condition}
            """,
            as_dict=True,
        )
        self.result["total_losses"] = invoices[0].total_amount if invoices else 0


@frappe.whitelist(methods=["GET"])
def get_home_data(**kwargs):
    hd = HomeDashboard(kwargs)
    hd.get_user_image()
    hd.get_user_full_name()
    hd.get_bar_chart_data()
    hd.get_total_gains()
    hd.get_total_losses()
    return hd.result

