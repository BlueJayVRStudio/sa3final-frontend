#!/usr/bin/env python3

import requests
from flask import Flask, request, render_template

import socket

app = Flask(__name__)

dataanalyzer_addr = "http://34.118.237.200:5050/"

@app.route("/")
def main():
    # print(hostaddress)
    # print(type(hostaddress))
    return "welcome to my final project!"

@app.route("/retrieve_records", methods=["GET"])
def retrieve_records():
    response = requests.get(dataanalyzer_addr + "retrieve_records")
    return response.text

@app.route("/scrape", methods=["GET"])
def call_scrape():
    response = requests.get(dataanalyzer_addr + "scrape")
    return response.text

@app.route("/delete_records", methods=["GET"])
def call_delete():
    response = requests.get(dataanalyzer_addr + "delete_records")
    return response.text

@app.route("/table")
def table():
    return render_template("index.html")

if __name__ == "__main__":
    print("hello world! :D")
    
    # localhost
    dataanalyzer_addr = "http://127.0.0.1:5051/"
    app.run(port=5000)
