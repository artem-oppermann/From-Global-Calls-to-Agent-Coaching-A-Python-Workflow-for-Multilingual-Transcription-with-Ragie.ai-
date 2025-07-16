from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
sentiment_pipeline = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",  # 3-way pos/neu/neg
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
    framework="pt"
)
@app.route("/sentiment", methods=["POST"])
def analyze_sentiment():
    payload = request.get_json(force=True)
    text = payload.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    results = sentiment_pipeline(text[:512])
    label = results[0]["label"]
    confidence = results[0]["score"]

    return jsonify({"sentiment": label, "confidence": confidence})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
