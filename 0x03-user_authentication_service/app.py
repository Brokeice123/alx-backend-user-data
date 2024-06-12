#!/usr/bin/env python3
"""
Flask app
"""

from flask import Flask, abort, jsonify, make_response, redirect, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """Return a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    session_id = request.cookies.get("session_id")
    if not session_id:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    session_id = request.cookies.get("session_id")
    if not session_id:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)

    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
