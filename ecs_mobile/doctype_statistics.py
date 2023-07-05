import frappe
from frappe.exceptions import DoesNotExistError
from frappe.model.meta import get_meta
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class DocStat(ABC):
    @abstractmethod
    def get_statistics(self) -> list:
        pass


class StatusStat(DocStat):
    def __init__(self, doctype: str) -> None:
        self.doctype = doctype

    def get_statistics(self) -> list:
        response = []
        statuses = get_meta(self.doctype).get_field("status").options.split("\n")
        for status in statuses:
            res_dict = {}
            if status == "":
                continue
            res_dict["title"] = status
            res_dict["count"] = frappe.db.count(self.doctype, {"status": status})
            response.append(res_dict)
        return response


class DisabledStat(DocStat):
    def __init__(self, doctype: str) -> None:
        self.doctype = doctype
        self.disabled = {"0": "Enabled", "1": "Disabled"}

    def get_statistics(self) -> list:
        response = []
        response.append({"title": "Total", "count": frappe.db.count("Item")})

        for status in self.disabled.keys():
            res_dict = {}
            res_dict["title"] = self.disabled.get(status)
            res_dict["count"] = frappe.db.count("Item", {"disabled": int(status)})

            response.append(res_dict)

        return response


class TypeStat(DocStat):
    def __init__(self, doctype: str, field_type: str) -> None:
        self.doctype = doctype
        self.field_type = field_type

    def get_statistics(self) -> list:
        response = []
        response.append({"title": "Total", "count": frappe.db.count(self.doctype)})
        types = get_meta(self.doctype).get_field(self.field_type).options.split("\n")
        for f_type in types:
            if f_type == "":
                continue

            res_dict = {}
            res_dict["title"] = f_type
            res_dict["count"] = frappe.db.count(self.doctype, {self.field_type: f_type})
            response.append(res_dict)

        return response


class DocStatusStat(DocStat):
    def __init__(self, doctype: str) -> None:
        self.doctype = doctype
        self.__docstatus_map = {"Draft": 0, "Submitted": 1, "Canceld": 2}

    def get_statistics(self) -> list:
        response = []
        for status in self.__docstatus_map.keys():
            res_dict = {}
            res_dict["title"] = status
            res_dict["count"] = frappe.db.count(
                self.doctype, {"docstatus": self.__docstatus_map.get(status)}
            )

            response.append(res_dict)
        return response


class DocStatFactory:
    def __init__(self, doctype: str, document_type: Optional[str] = None):
        self.doctype = doctype
        self.document_type = document_type
        self.__status_doctypes = [
            "Task",
            "Project",
            "Timesheet",
            "Issue",
            "Lead",
            "Opportunity",
            "Quotation",
            "Sales Order",
            "Sales Invoice",
            "Payment Entry",
            "Customer Visit",
            "Supplier Quotation",
            "Purchase Order",
            "Purchase Invoice",
            "Material Request",
            "Delivery Note",
            "Purchase Receipt",
            "Leave Application",
            "Employee Advance",
            "Employee",
            "Employee Grievance",
            "Expense Claim",
            "Loan Application",
            "Contact",
        ]
        self.__disabled_field_doctypes = ["Item"]
        self.__type_doctypes_map = {
            "Supplier": "supplier_type",
            "Customer": "customer_type",
            "Address": "address_type",
            "Employee Checkin": "log_type",
        }
        self.__docstatus_doctypes = [
            "Customer Visit",
            "Stock Entry",
            "Attendance Request",
        ]

    def create_doc_stat(self) -> DocStat:
        if self.doctype in self.__status_doctypes:
            return StatusStat(self.doctype)

        if self.doctype in self.__type_doctypes_map.keys():
            type_field = self.__type_doctypes_map.get(self.doctype)
            return TypeStat(self.doctype, type_field)

        if self.doctype in self.__disabled_field_doctypes:
            return DisabledStat(self.doctype)

        if self.doctype in self.__docstatus_doctypes:
            return DocStatusStat(self.doctype)

        frappe.throw("No statistics found for this doctype", DoesNotExistError)


@frappe.whitelist(methods=["GET"])
def doc_stats(doctype: str) -> Dict[str, Any]:
    """Returns statistics for the passed doctype"""

    docstat_factory = DocStatFactory(doctype=doctype)
    docstat = docstat_factory.create_doc_stat()
    return docstat.get_statistics()
