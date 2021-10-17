from queue import Queue
from threading import Thread
from time import sleep

import logging
import numpy as np
from flask import Flask, send_file, jsonify

# additional imports
from typing import Dict
# local imports
from user import User
# initial code

app = Flask(__name__)
# do not make any size assumption
productsDB = ['beef', 'pizza', 'pasta', 'fondue']
policyDB = {}  # in memory
broker = Queue(10)
learning_rate = 2.5

logger = logging.getLogger('recommendations')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# ***** Start of your solution *****
# ******* intialisation ******
# Intial policy DB is that each product has 50% chance of getting baught
policyDB = {"ko8w8kdmd": [0.1, 0.5, 0.7, 0.6]}
PageSize = 3


def process(element):
    logger.info(f"processing{element}")


@app.route('/<string:id>/products')
def products(id):

    if id in policyDB.keys():
        pickupProbability = policyDB[id].copy()
    else:
        # new user we give him a new copy of the policy
        pickupProbability = [0.5]*len(productsDB)
        policyDB[id] = pickupProbability.copy()

    shownProducts = []
    i = 0
    while len(shownProducts) < PageSize:
        randomNumber = np.random.rand()
        while i < len(productsDB) and randomNumber > pickupProbability[i]:
            i += 1
        if i < len(productsDB):
            shownProducts.append(productsDB[i])
            pickupProbability[i] = 0
        else:
            # that means the generated number is higher than any probability that we got
            i = 0

    return jsonify(shownProducts)


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
