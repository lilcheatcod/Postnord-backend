# postnord_backend_client.py
import os
import requests

# Use env if present; otherwise default to your Railway deployment (HTTPS!)
BASE_URL = os.getenv("BACKEND_URL", "https://postnord-backend-production.up.railway.app").rstrip("/")


def _url(path: str) -> str:
    return f"{BASE_URL}{path}"


# ---------------- TTS ----------------
def generate_audio(text: str, timeout: int = 60) -> bytes | None:
    """
    Ask backend /generate-audio for an MP3 of the given text.
    Returns raw MP3 bytes on success, or None on failure.
    """
    try:
        r = requests.post(_url("/generate-audio"), json={"text": text}, timeout=timeout)
        ctype = r.headers.get("content-type", "")
        if r.status_code == 200 and ctype.startswith("audio/"):
            return r.content

        # Not audio? Print the body so you see the error coming from backend.
        print(f"❌ generate_audio failed: {r.status_code} {r.text}")
        return None
    except Exception as e:
        print(f"❌ generate_audio error: {e}")
        return None


# --------------- Health --------------
def ping(timeout: int = 10) -> dict:
    try:
        r = requests.get(_url("/ping"), timeout=timeout)
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --------- Existing tool calls -------
def track_package(tracking_number: str) -> dict:
    response = requests.post(_url("/track"), json={"tracking_number": tracking_number})
    return response.json()

def recheck_sms(tracking_number: str) -> dict:
    response = requests.post(_url("/recheck_sms"), json={"tracking_number": tracking_number})
    return response.json()

def verify_customs_docs_needed(tracking_number: str) -> dict:
    response = requests.post(_url("/verify_customs_docs_needed"), json={"tracking_number": tracking_number})
    return response.json()

def resend_notification(tracking_number: str) -> dict:
    response = requests.post(_url("/resend_notification"), json={"tracking_number": tracking_number})
    return response.json()

def provide_est_delivery_window(tracking_number: str) -> dict:
    response = requests.post(_url("/provide_est_delivery_window"), json={"tracking_number": tracking_number})
    return response.json()