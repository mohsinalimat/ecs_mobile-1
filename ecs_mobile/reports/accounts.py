from frappe.utils import flt, getdate
from erpnext.accounts.utils import get_balance_on
import frappe


@frappe.whitelist(methods=["GET"])
def general_ledger(from_date=None, to_date=None, account=None, party_type=None ,party=None, start=0, page_length=20):
    conditions = ""

    if (from_date is not None) and (to_date is not None):
        conditions += f" AND `tabGL Entry`.posting_date BETWEEN '{from_date}' AND '{to_date}'"
    
    if account is not None:
        conditions += f" AND `tabGL Entry`.account = '{account}'"
    
    if party_type is not None:
        conditions += f" AND `tabGL Entry`.party_type = '{party_type}'"
    
    if party is not None:
        conditions += f" AND `tabGL Entry`.party = '{party}'"
    
    query = frappe.db.sql(
        f"""
            SELECT
                name,
                posting_date,
                account,
                party_type,
                party,
                cost_center,
                debit,
                credit,
                against,
                against_voucher_type,
                against_voucher,
                voucher_type,
                voucher_no,
                project,
                remarks,
                account_currency,
                company
            FROM `tabGL Entry`
            WHERE 1=1
            {conditions}
            LIMIT {start}, {page_length}
        """, as_dict=True
    )
    total_credit = 0
    total_debit = 0
    total_balance = 0
    if query:
        for q in query:

            total_credit += q["credit"]
            total_debit += q["debit"]
            balance = flt(get_balance_on(
                account=q["account"],
                date=getdate(["posting_date"]),
                party_type=q["party_type"],
                party=q["party"],
                company=q["company"],
                in_account_currency=q["account_currency"],
                cost_center=q["cost_center"],
                ignore_account_permission=False
            ), 2)

            q["balance"] = balance
            total_balance += balance
       
        response = {
            "data":query,
            "total_debit": flt(total_debit, 2),
            "total_credit": flt(total_credit, 2),
            "total_balance": flt(total_balance, 2)
        }
        return response
    else:
        frappe.throw("No Data", frappe.exceptions.DoesNotExistError)