import frappe


def remove_html_tags(text):
    """Remove html tags from a string"""
    
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)



def get_connections(doc_list, fileds, filters, con_filed, con_doc):
    result = {}
    for doc in doc_list:
        data = frappe.db.get_all(doc, fileds[doc], filters[doc])
        result[doc] = data
    return result

def get_timesheet_task_count(task):

    """
    Get the count of the timesheet connected to a certain task
    """
    c = 0
    tss = frappe.db.get_all("Timesheet")
    for i in tss:
        ts = frappe.get_doc("Timesheet", i.name)
        for log in ts.time_logs:
            if log.task == task:
                c += 1
    return c

def order_by(sort_field, sort_type):
    """
        Order the get_list query with sort field and sort type
        provided by the user
    """
    order_by = ""
    if (sort_field is not None) and (sort_type is not None):
        order_by = f"{sort_field} {sort_type}"
    return order_by