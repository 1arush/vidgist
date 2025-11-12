from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from transcript_util import combine_transcripts
from summarizer_api import summarize_via_hf
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "VidGist-Flask Backend Running Here!"

@app.route("/api/transcripts", methods=["POST"])
def transcripts_endpoint():
    data = request.get_json()
    video_urls = data.get("videoUrls")
    if not isinstance(video_urls, list) or len(video_urls) == 0:
        return jsonify({"success": False, "error": "Provide a list of videoUrls"}), 400

    combined = combine_transcripts(video_urls)
    if not combined.strip():
        return jsonify({"success": False, "error": "No transcripts fetched"}), 500

    return jsonify({"success": True, "transcript": combined})

@app.route("/api/summarize", methods=["POST"])
def summarize_endpoint():
    data = request.get_json()
    video_urls = data.get("videoUrls")
    if not isinstance(video_urls, list) or len(video_urls) == 0:
        return jsonify({"success": False, "error": "Provide a list of videoUrls"}), 400

    combined = combine_transcripts(video_urls)
    if not combined.strip():
        return jsonify({"success": False, "error": "No transcripts fetched"}), 500
    
    # truncation 
    MAX_CHARS = 2000
    if len(combined) > MAX_CHARS:
        combined = combined[:MAX_CHARS]
        print(f"Transcript truncated to {MAX_CHARS} characters") 

    try:
        summary = summarize_via_hf(combined)
        summary = re.sub(r"\s{2,}", " ", summary)
    except Exception as e:
        print(f"Summarization error: {e}")
        return jsonify({"success": False, "error": f"Summarization failed: {e}"}), 500

    return jsonify({"success": True, "summary": summary})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
