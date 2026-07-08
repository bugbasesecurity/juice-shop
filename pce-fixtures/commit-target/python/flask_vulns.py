from flask import Flask, redirect, request
import os
import subprocess
import sqlite3

import requests


app = Flask(__name__)


@app.route("/admin/run")
def run_admin_task():
    command = request.args.get("cmd", "id")
    subprocess.run(command, shell=True, check=False)
    return "queued"


@app.route("/reports")
def download_report():
    report_name = request.args.get("name", "summary.txt")
    report_path = os.path.join("/srv/reports", report_name)
    with open(report_path, "r", encoding="utf-8") as report_file:
        return report_file.read()


@app.route("/preview")
def preview_url():
    url = request.args.get("url", "https://example.com")
    return requests.get(url, timeout=3).text


@app.route("/search")
def search_customers():
    email = request.args.get("email", "")
    db = sqlite3.connect("customers.db")
    query = "SELECT id, email FROM customers WHERE email = '" + email + "'"
    return str(db.execute(query).fetchall())


@app.route("/logout")
def logout():
    next_url = request.args.get("next", "/")
    return redirect(next_url)
