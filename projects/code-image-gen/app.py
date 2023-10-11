from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "03c81118b363e3feaf4b7cc0c7cca9a298c45cf0c4fb5bf975604e67f4bf5856"

PLACEHOLDER_CODE = "print('Hello World!')"


@app.route("/", methods=["GET"])
def code():
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE
    context = {
        "message": "Paste your Python Code 🐍",
        "code": session["code"],
    }
    return render_template("code_input.html", **context)


@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code")
    return redirect(url_for("code"))


@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("code"))
