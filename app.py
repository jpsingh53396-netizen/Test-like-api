from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

MAIN_API = "https://like-bot-mera.vercel.app/like"
API_KEY = "saito"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": 1,
        "message": "Like API is running",
        "usage": "/like?uid=2455776873"
    })


@app.route("/like", methods=["GET"])
def like():
    uid = request.args.get("uid")

    if not uid:
        return jsonify({
            "status": 0,
            "error": "uid is required"
        }), 400

    try:
        response = requests.get(
            MAIN_API,
            params={
                "uid": uid,
                "region": "ind",
                "key": API_KEY
            },
            timeout=30
        )

        try:
            data = response.json()
        except ValueError:
            return jsonify({
                "status": 0,
                "error": "Main API returned invalid JSON",
                "response": response.text
            }), 502

        return jsonify(data), response.status_code

    except requests.RequestException as e:
        return jsonify({
            "status": 0,
            "error": "Request to main API failed",
            "details": str(e)
        }), 502

    except Exception as e:
        return jsonify({
            "status": 0,
            "error": "Internal server error",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )
