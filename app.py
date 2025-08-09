from flask import Flask, request, jsonify, send_file
from resend_notification import handle_resend_notification
from elevenlabs.client import ElevenLabs
import io
import os

app = Flask(__name__)

from routes.generate_audio import tts_bp
app.register_blueprint(tts_bp)

@app.route("/ping")
def ping():
    return {"message": "✅ Backend is alive!"}, 200

@app.route("/track", methods=["POST"])
def track_package():
    data = request.get_json()
    tracking_number = data.get("tracking_number")

    # 🧪 Mock response for now
    return jsonify({
        "status": "Package is at terminal",
        "last_location": "Gothenburg, Sweden",
        "expected_delivery": "2025-08-10"
    })
@app.route("/recheck_sms", methods=["POST"])
def recheck_sms():
    data = request.get_json()
    tracking_number = data.get("tracking_number", "")
    
    # Just returning mock response for now
    return jsonify({
        "action": "recheck_sms",
        "status": "SMS notification resent",
        "tracking_number": tracking_number
    })

@app.route("/flag_human_support_request", methods=["POST"])
def flag_human_support_request():
    data = request.get_json()
    tracking_number = data.get("tracking_number")
    reason = data.get("reason", "Unclear issue")

    # 📌 Mock response for now
    return jsonify({
        "action": "flag_human_support_request",
        "status": "Human support flagged for follow-up",
        "tracking_number": tracking_number,
        "reason": reason
    })

@app.route("/resend_notification", methods=["POST"])
def resend_notification():
    return handle_resend_notification()

@app.route("/verify_customs_docs_needed", methods=["POST"])
def verify_customs_docs_needed():
    data = request.get_json()
    tracking_number = data.get("tracking_number")

    # 🧪 Mock logic: Simulate that customs documents are missing
    return jsonify({
        "action": "verify_customs_docs_needed",
        "status": "Customs documents required",
        "instructions": "Please upload your ID and invoice at postnord.se/tull within 24 hours to avoid return.",
        "tracking_number": tracking_number
    })

@app.route("/provide_est_delivery_window", methods=["POST"])
def provide_est_delivery_window():
    data = request.get_json()
    tracking_number = data.get("tracking_number")

    # 🧠 Mock response with estimated delivery window
    return jsonify({
        "action": "provide_est_delivery_window",
        "tracking_number": tracking_number,
        "estimated_window": "Between 14:00 - 18:00 on 2025-08-10",
        "status": "Delivery window provided"
    })

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    el_api_key = os.getenv("ELEVEN_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")

    client = ElevenLabs(api_key=el_api_key)

    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            output_format="mp3_44100_128",
            optimize_streaming_latency="2"
        )

        mp3_bytes = b''.join(audio_stream)
        return send_file(
            io.BytesIO(mp3_bytes),
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="response.mp3"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
       