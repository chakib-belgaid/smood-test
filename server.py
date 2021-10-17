from queue import Queue
from threading import Thread
from time import sleep

import logging
import numpy as np
from flask import Flask, send_file, jsonify

# additional imports
from copy import deepcopy
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
policyDB["default"] = {"products": np.array(productsDB), "probabilities": np.full(
    len(productsDB), 1/len(productsDB))}
# just a test
PageSize = 3
policyDB["ko8w8kdmd"] = {"products": np.array(['beef', 'pizza', 'pasta', 'fondue']),
                         "probabilities": np.array([0.4, 0.3, 0.2, 0.1])}


def add_new_product(user, product):
    """
    Add a new product to the list in a such that it has 50% chance to be picked
    """
    probabilities = policyDB[user]["probabilities"]
    value = 1/(len(probabilities)+1)
    def update_value(x): return x - value/len(probabilities)
    update_value = np.vectorize(update_value)
    probabilities = update_value(probabilities)
    policyDB[user]["probabilities"] = np.append(probabilities, value)
    policyDB[user]["products"] = np.append(policyDB[user]["products"], product)
    logger.info(policyDB[user]["probabilities"])


for user in policyDB.keys():
    add_new_product(user, "potato")


def update_probabilities(probabilities, index, gain):
    loss = gain / (len(probabilities)-1)
    def update_loss(x): return x - loss
    update_loss = np.vectorize(update_loss)
    probabilities = update_loss(probabilities)
    probabilities[index] += gain + loss
    return probabilities


def process(element):
    logger.info(element['id'])
    userPolicyDB = policyDB[element['id']]
    logger.info(userPolicyDB["probabilities"])
    purchasedProduct = element['product']
    purchasedIndex = np.where(
        userPolicyDB["products"] == purchasedProduct)[0][0]
    gain = userPolicyDB["probabilities"][purchasedIndex] * learning_rate/100
    userPolicyDB["probabilities"] = update_probabilities(
        userPolicyDB["probabilities"], purchasedIndex, gain)

    logger.info(sum(userPolicyDB["probabilities"]))


@ app.route('/<string:id>/products')
def products(id):

    if not (id in policyDB.keys()):
        # default configuration we know nothing about the suer
        policyDB[id] = deepcopy(policyDB["default"])

    shownProducts = np.random.choice(
        policyDB[id]["products"], size=PageSize, replace=False, p=policyDB[id]["probabilities"])

    return jsonify(list(shownProducts))


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
