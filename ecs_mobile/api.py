from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
import json, ast

current_date = datetime.datetime.today().strftime('%Y-%m-%d')
current_user = frappe.session.user

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()

    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key": true,
            "message": "اسم المستخدم او كلمة المرور غير صحيحة !"
        }

        return

    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)
    allowed_modules = frappe.db.sql(""" select `tabMobile user Modules`.modules as modq 
    from `tabMobile user Modules` join `tabMobile User` on `tabMobile user Modules`.parent = `tabMobile User`.name 
    where `tabMobile User`.user = '{user}' or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}'""".format(user=usr),as_dict=1)
    allowed_documents = frappe.db.sql(""" select `tabMobile User Documents`.modules as modq ,
                                        `tabMobile User Documents`.document_name as docq 
                                        from `tabMobile User Documents` join `tabMobile User` on `tabMobile User Documents`.parent = `tabMobile User`.name 
                                        where `tabMobile User`.user = '{user}'  or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}' """.format(user=usr),as_dict=1)
    modules={}
    documents={}
    for module in allowed_modules:
        #modules = {module.modq:"Yes"}
        #modules.update()
        #modules.[module.modq]= 34
        modules.update( {module.modq : "Yes"} )


    for document in allowed_documents:
        documents.update({document.docq:document.modq})


    frappe.response["message"] = {
        "success_key": True,
        "message": "Authentication Success",
        "sid": frappe.session.sid,
        "api_key": user.api_key,
        "api_secret": api_generate,
        "email": user.email,
        "modules": modules,
        "documents": documents,
        "user_type": user.role_profile_name
    }

    return


def generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key

    user_details.api_secret = api_secret
    user_details.save()
    return api_secret

# ------------------------------------------------------------------------------------
