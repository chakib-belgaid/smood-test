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
policyDB = {"ko8w8kdmd": {'beef': 0.1,
                          'pizza': 0.5,  'pasta': 0.7,  'fondue': 0.6}}
PageSize = 3


def process(element):
    logger.info(element['id'])
    userPolicyDB = policyDB[element['id']]
    purchasedProduct = element['product']
    for item in userPolicyDB.keys():
        probability = userPolicyDB[item]
        # /200 because since we gain and loose in both wais we use a half step of learning rate
        probability *= (1-learning_rate/200)
        userPolicyDB[item] = probability

# second one to be canceled with later so i don't have to use any conditions inside the loop
    probability = userPolicyDB[purchasedProduct]
    probability /= (1-learning_rate/200)  # we cancel the previous loss
    probability *= (1+learning_rate/200)  # we add a the gain
    if probability > 1:
        probability = 1
    userPolicyDB[purchasedProduct] = probability


@ app.route('/<string:id>/products')
def products(id):

    if not (id in policyDB.keys()):
        # default configuration we know nothing about the suer
        policyDB[id] = {product: 0.5 for product in products(id)}

    pickupProbability = list(policyDB[id].values())
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


@ app.route('/')
def index():
    return send_file('index.html')


@ app.route('/<string:id>/buy/<string:product>')
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
