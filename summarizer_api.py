import os
import requests

HF_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

def summarize_via_hf(text: str) -> str:
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    payload = {"inputs": text}
    response = requests.post(HF_MODEL_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")
    data = response.json()
    if isinstance(data, list) and len(data) > 0 and "summary_text" in data[0]:
        return data[0]["summary_text"]
    if "summary_text" in data:
        return data["summary_text"]
    raise Exception("Unexpected API response structure")
