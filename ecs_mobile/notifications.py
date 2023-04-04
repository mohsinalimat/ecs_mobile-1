import requests
import json
import frappe


#------------- External API ----------------#
@frappe.whitelist()
def device_tokens(**kwargs):
    instance = frappe.get_doc(kwargs["data"])
    if instance:
        instance.insert()
    else:
        response = frappe.response["message"] = {
            "success_key": False,
            "message": "Somthing went wrong"
        }

        return response

    response = frappe.response["message"] = {
            "success_key": True,
            "data": instance
        }     
    return response



@frappe.whitelist()
def get_push_notification_details(device_token=None, user_id=None, device_type=None):
        conditions = {}
        if device_token is not None:
            conditions["device_token"] = device_token

        if user_id is not None:
            conditions["user_id"] = user_id

        if device_type is not None:
            conditions["device_type"] = device_type        


        query = frappe.db.get_list(
            "Push Notification Details",
            filters=conditions,
            fields=[
                "name",
            ],
            order_by="modified desc",
        )
        if query:
            return query[0]
        else:
            return "لا يوجد !"

#------------- External API End ----------------#


    


def send_push_notification(tokens, message, subject, doctype, document_name):
    headers = {
        "Authorization": "key=AAAAgRS_puM:APA91bF_sdH4zqFbE6epNz7dO0VbgeskchycwE9pr97LIKMGuWuF2lZ8W3FgTw39qaOMxHkpego6n8KxE9iJJQXrf4P2NmyBVVs1B791JPZAdIY6nzpNPDxI3jka2vC3WJQC6NcsVjcK",
        "Content-Type": "application/json",
    }
    
    body = {
        "registration_ids": tokens,
        "notification": {
            "body": message,
            "title": subject,
            "android_channel_id": "nextapp-notification-channel",
            "image":"https://erpcloud.systems/files/purchase_receipt.png",
            "sound": True
        },
        "data": {
            "doctype": doctype,
            "document_name": document_name  
            }
    }
    url = "https://fcm.googleapis.com/fcm/send"
    data = json.dumps(body)
    response = requests.post(url=url, data=data, headers=headers)

    return response.json()

