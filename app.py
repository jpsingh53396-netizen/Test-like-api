from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MAIN_API = "https://like-bot-mera.vercel.app/like"
API_KEY = "saito"


@app.route("/like")
def like():
    uid = request.args.get("uid")

    if not uid:
        return jsonify({
            "status": 0,
            "error": "uid is required"
        }), 400

    try:
        r = requests.get(
            MAIN_API,
            params={
                "uid": uid,
                "region": "ind",
                "key": API_KEY
            },
            timeout=30
        )

        return jsonify(r.json()), r.status_code

    except Exception as e:
        return jsonify({
            "status": 0,
            "error": str(e)
        }), 500


@app.route("/")
def home():
    return jsonify({
        "status": 1,
        "message": "API is running",
        "example": "/like?uid=2455776873"
    })


app.run(host="0.0.0.0", port=5000)
