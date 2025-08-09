import requests

BASE_URL = "http://127.0.0.1:5000"

def track_package(tracking_number):
    response = requests.post(f"{BASE_URL}/track", json={"tracking_number": tracking_number})
    return response.json()

def recheck_sms(tracking_number):
    response = requests.post(f"{BASE_URL}/recheck_sms", json={"tracking_number": tracking_number})
    return response.json()

def verify_customs_docs_needed(tracking_number):
    response = requests.post(f"{BASE_URL}/verify_customs_docs_needed", json={"tracking_number": tracking_number})
    return response.json()

def resend_notification(tracking_number):
    response = requests.post(f"{BASE_URL}/resend_notification", json={"tracking_number": tracking_number})
    return response.json()

def provide_est_delivery_window(tracking_number):
    response = requests.post(f"{BASE_URL}/provide_est_delivery_window", json={"tracking_number": tracking_number})
    return response.json()