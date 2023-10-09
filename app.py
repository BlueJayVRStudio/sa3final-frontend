#!/usr/bin/env python3

import requests
import json
from flask import Flask, request, render_template

import socket

app = Flask(__name__)

dataanalyzer_addr = "http://34.118.238.31:5051/"

@app.route("/")
def main():
    return render_template("table.html", message=None, failed=False)

@app.route("/scrape", methods=["GET"])
def call_scrape():
    try:
        response = requests.get(dataanalyzer_addr + "scrape")
    except:
        return render_template("table.html", message="Data collector component failed to scrape data :(", failed=True)
    
    if response.status_code == 200:
        return render_template("table.html", message="Data successfully scraped by the data collector component!!", failed=False)
    else:
        return render_template("table.html", message="Data collector component failed to scrape data :(", failed=True)

@app.route("/delete_records", methods=["GET"])
def call_delete():
    try:
        response = requests.get(dataanalyzer_addr + "delete_records")
    except:
        return render_template("table.html", message="The data collector component failed to delete data :(", failed=True)
    
    if response.status_code == 200:
        return render_template("table.html", message="All records successfully deleted by the data collector component!!", failed=False)
    else:
        return render_template("table.html", message="The data collector component failed to delete data :(", failed=True)

@app.route("/table")
def table():
    try:
        response = requests.get(dataanalyzer_addr + "retrieve_records")
    except:
        return render_template("table.html", message="Failed to retrieve table :(", failed=True)
    
    if response.status_code == 200:
        rows = json.loads(response.text)
        return render_template("table.html", rows=rows, message="Table retrieved!", failed=False)
    else:
        return render_template("table.html", rows=rows, message="Failed to retrieve table :(", failed=False)


if __name__ == "__main__":
    print("hello world! :D")
    
    # localhost
    dataanalyzer_addr = "http://127.0.0.1:5051/"
    app.run(port=5000)

    # test commit