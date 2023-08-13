from urllib import response
from frappe.query_builder.functions import Convert
import frappe
import erpnext
from frappe import auth
import random
import datetime
import json, ast
import time
from decimal import Decimal

@frappe.whitelist(methods=['GET'], allow_guest=True)
def itemGroup(
        search_text="%%",
        con_doc="%%",
        start=0,
        page_length=20,
):
    def get_item_group_with_children(parent_item_group):
        children = frappe.db.get_list(
            "Item Group",
            filters={"parent_item_group": parent_item_group},
            fields=["name", "parent_item_group", "is_group"],
            order_by="name asc",
        )
        for child in children:
            child["child"] = get_item_group_with_children(child["name"])
        return children

    if con_doc == "%%":
        query = frappe.db.get_list(
            "Item Group",
            filters=[{"parent_item_group": ["=", ""]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"item_group_name": ["like", search_text]},
            ],
            fields=["name", "parent_item_group", "is_group"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            for group in query:
                group["child"] = get_item_group_with_children(group["name"])
            return query
        else:
            return "لا يوجد !"
        


# @frappe.whitelist(methods=['GET'], allow_guest=True)
# def itemList(item_name="", start=0, page_length=20):

#   if not item_name.strip():
#     top_level_groups = frappe.db.get_list("Item Group", filters=[{"parent_item_group": ["=", ""]}],  
#                                           fields=["name", "parent_item_group", "is_group"],
#                                           order_by="name asc")
    
#     return top_level_groups

#   else:
#     parent_group = frappe.get_doc("Item Group", item_name)
#     previous_parent = parent_group.parent_item_group or ""

#     query = frappe.db.get_list("Item Group", filters=[{"parent_item_group": ["=", item_name]}],
#                                 fields=["name", "parent_item_group", "is_group"], order_by="name asc",
#                                 start=start, page_length=page_length)

#     if query:
#       for group in query:
#         group["previous_parent"] = previous_parent
      
#       return query
    
#     else:  
#       return {"لا يوجد !"}
    


# @frappe.whitelist(methods=['GET'], allow_guest=True)
# def searchItemGroup(search_text="", start=0, page_length=20):
#     if search_text:
#         query = frappe.db.get_list("Item Group", filters=[{"name": ["like", f"{search_text}%"]}],
#                                    fields=["name", "parent_item_group", "is_group"], order_by="name asc",
#                                    start=start, page_length=page_length)

#         if query:
#             return query
#         else:
#             return {"لا يوجد !"}
#     else:
#         return {"message": "Please provide a search_text parameter."}


@frappe.whitelist(methods=['GET'], allow_guest=True)
def itemList(item_name="", start=0, page_length=20, search_text=""):
    if search_text:
        query = frappe.db.get_list("Item Group", filters=[{"name": ["like", f"{search_text}%"]}],
                                   fields=["name", "parent_item_group", "is_group"], order_by="name asc",
                                   start=start, page_length=page_length)
        if query:
            return query
        else:
            frappe.local.response["http_status_code"] = 404
            return {"لا يوجد !"}
    
    
    if not item_name.strip():
        top_level_groups = frappe.db.get_list("Item Group", filters=[{"parent_item_group": ["=", ""]}],
                                              fields=["name", "parent_item_group", "is_group"],
                                              order_by="name asc")

        return top_level_groups

    else:
        parent_group = frappe.get_doc("Item Group", item_name)
        previous_parent = parent_group.parent_item_group or ""

        query = frappe.db.get_list("Item Group", filters=[{"parent_item_group": ["=", item_name]}],
                                   fields=["name", "parent_item_group", "is_group"], order_by="name asc",
                                   start=start, page_length=page_length)

        if query:
            for group in query:
                group["previous_parent"] = previous_parent

            return query

        else:
            frappe.local.response["http_status_code"] = 404
            return {"لا يوجد !"}
