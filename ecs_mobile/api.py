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


    frappe.response["message"] = {
        "success_key": True,
        "message": "Authentication Success",
        "sid": frappe.session.sid,
        "api_key": user.api_key,
        "api_secret": api_generate,
        "email": user.email,
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
