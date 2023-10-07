#!/usr/bin/env python3

import requests
from flask import Flask, request, render_template

import socket

app = Flask(__name__)

echoForm = '''
    <p> newest deploy :) </p>
    <p>Enter something here!!!</p>
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''
hostaddress = socket.gethostbyname(socket.gethostname())
hostaddress = hostaddress.split('.')
hostaddress[3] = '1'
hostaddress = '.'.join(hostaddress)

@app.route("/")
def main():
    # print(hostaddress)
    # print(type(hostaddress))
    return echoForm

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    if input_text == "a":
        response = requests.get(f"http://{hostaddress}:5050/test_string")
        return "You entered: " + input_text + "\n" + response.text
    try:
        response = requests.get(f"{input_text}/test_string")
    except:
        response = "wrong address. try again."
    # print(response.text)
    # input_text = request.form.get("user_input", "")
    return "You entered: " + input_text + "\n" + response.text

@app.route("/retrieve_id", methods=["GET"])
def retrieve_id():
    response = requests.get("http://34.118.231.185:5050/retrieve_id")
    return response.text
@app.route("/store_id", methods=["GET"])
def store_id():
    response = requests.get("http://34.118.231.185:5050/store_id")
    return response.text

@app.route("/table")
def table():
    return render_template("index.html")

if __name__ == "__main__":
    print("hello")
    app.run(port=5000)
