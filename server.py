from queue import Queue
from threading import Thread
from time import sleep

import logging
import numpy as np
from flask import Flask, send_file, jsonify

app = Flask(__name__)
productsDB = ['beef', 'pizza', 'pasta', 'fondue']  # do not make any size assumption
policyDB = {}  # in memory
broker = Queue(10)
learning_rate = 2.5

logger = logging.getLogger('recommendations')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# ***** Start of your solution *****


def process(element):
    raise NotImplementedError


@app.route('/<string:id>/products')
def products(id):
    raise NotImplementedError


# ***** End of your solution *****


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/<string:id>/buy/<string:product>')
def buy(id, product):
    broker.put(dict(id=id, product=product), block=False)
    # code for shipment, etc.
    return 'ok'


class Worker(Thread):
    def run(self):
        while True:
            element = broker.get(True, timeout=None)
            process(element)
            sleep(2)  # long running process


analysis = Worker()
analysis.daemon = True
analysis.start()
