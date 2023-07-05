import frappe
from datetime import datetime, timedelta


class HomeDashboard:
    def __init__(self):
        self.result = {}

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
        """
        Get the count of Paid, Unpaid, Return, Overdue, Canceled Sales Invoices
        """
        statuses = ["Paid", "Unpaid", "Return", "Overdue", "Canceled"]
        bar_chart_date = []
        for status in statuses:
            data = {}
            count = frappe.db.count("Sales Invoice", {"status": status})
            data["title"] = status
            data["count"] = count
            bar_chart_date.append(data)

        self.result["bar_chart"] = bar_chart_date

    def get_total_gains(self):
        """Get the sum of grand totals of paid and partly paid sales invoices."""

        past_week_start = datetime.now().date() - timedelta(days=7)
        invoices = frappe.db.sql(
            f"""
            SELECT SUM(grand_total) as total_amount
            FROM `tabSales Invoice`
            WHERE status IN ('Paid', 'Partly Paid')
            AND posting_date >= {past_week_start}
        """,
            as_dict=True,
        )

        total_amount = (
            invoices[0].total_amount if invoices and invoices[0].total_amount else 0
        )
        self.result["total_gains"] = total_amount

    def get_total_loses(self):
        """Get the sum of grand totals of Return sales invoices."""

        past_week_start = datetime.now().date() - timedelta(days=7)
        invoices = frappe.db.sql(
            f"""
            SELECT SUM(grand_total) as total_amount
            FROM `tabSales Invoice`
            WHERE status IN ('Return')
            AND posting_date >= {past_week_start}
        """,
            as_dict=True,
        )

        total_amount = (
            invoices[0].total_amount if invoices and invoices[0].total_amount else 0
        )
        self.result["total_loses"] = total_amount


@frappe.whitelist(methods=["GET"])
def get_home_data():
    hd = HomeDashboard()
    hd.get_user_image()
    hd.get_user_full_name()
    hd.get_bar_chart_data()
    hd.get_total_gains()
    hd.get_total_loses()
    return hd.result
