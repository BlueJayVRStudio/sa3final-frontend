#!/usr/bin/env python3

import requests
import json
import pika
from flask import Flask, request, render_template
from prometheus_client import start_http_server, Summary, Counter, Gauge

import socket
import time

app = Flask(__name__)

dataanalyzer_addr = "http://34.118.238.31:5051/"

## MONITORING: prometheus metrics
c = Counter('http_scrape_request', 'counter for http request to scrape data')
success = Counter('scrape_success', 'counter for data scrape success events')
s = Summary('request_latency_seconds', 'data scrape function latency')

@app.route("/")
def main():
    return render_template("table.html", message=None, failed=False)

@app.route("/scrape", methods=["GET"])
def call_scrape():
    ## MONITORING: create latency summary for scrape event
    with s.time():

        ## MONITORING: increment request counter
        c.inc()

        try:
            response = requests.get(dataanalyzer_addr + "scrape")
        except:
            return render_template("table.html", message="Data collector component failed to scrape data :(", failed=True)
        
        if response.status_code == 200:
            ## MONITORING: increment request success counter
            success.inc()

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

## MONITORING: health check endpoint
@app.route("/health-check")
def health_check():
    return "very helth"


## MONITORING: start metrics endpoint server at port 9100
start_http_server(9100)


## EVENT COLLABORATION
def create_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='34.27.5.109'))
    channel = connection.channel()
    channel.queue_declare(queue='transactions')
    return (connection, channel)

## EVENT COLLABORATION: signal by message queue to data collector to scrape using
@app.route("/scrape_rabbit")
def scrape_rabbit():    
    conn, channel = create_rabbitmq_connection()
    channel.basic_publish(exchange="", routing_key="scrape_signal", body=json.dumps("scrape signal"))
    return render_template("table.html", message='''Scrape signal sent to data collector. Press "Retrieve Table" to see the result. ''', failed=False)

## EVENT COLLABORATION: signal by message queue to data collector to delete records
@app.route("/delete_rabbit")
def delete_rabbit():    
    conn, channel = create_rabbitmq_connection()
    channel.basic_publish(exchange="", routing_key="scrape_signal", body=json.dumps("delete signal"))
    return render_template("table.html", message='''Delete signal sent to data collector. Press "Retrieve Table" to see the result. ''', failed=False)

if __name__ == "__main__":
    print("hello world! :D")

    # localhost
    dataanalyzer_addr = "http://127.0.0.1:5051/"
    app.run(port=5000)

    # test commit