import time
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
error = 1e6
PageSize = 3
# extra logging functions


def timeit(method):
    """decorator to measuere the execution time of a function"""
    def timed_function(*args, **kw):
        tb = time.time_ns()
        result = method(*args, **kw)
        te = time.time_ns()
        logger.info(
            f"the method {method.__name__} has taken {(te-tb)/1e3 :2.2f} us")
        return result
    return timed_function


# ******* intialisation ******
# Intial policy DB is that each product has 50% chance of getting baught
policyDB["default"] = {"products": np.array(productsDB), "probabilities": np.full(
    len(productsDB), 1/len(productsDB))}
# just a test


# mainly for tests
@timeit
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
    logger.info(
        f"Updating the policy of the user {user} after adding the product {product} to the database  ")
    assert 1-error <= sum(policyDB[user]["probabilities"]) <= 1+error


# same here


@timeit
def update_probabilities(probabilities, index, gain):
    # to keep the balance of the probabilities
    loss = gain / (len(probabilities)-1)
    # lambda function
    def update_loss(x): return x - loss if x - loss > 0 else 0
    update_loss = np.vectorize(update_loss)
    probabilities = update_loss(probabilities)
    probabilities[index] += gain + loss
    # assure that always the probabilities are between 0 and 1
    if probabilities[index] > 1:
        probabilities[index] = 1
    # since it is python there is always a marginal error when handling the floats
    assert 1-error <= sum(probabilities) <= 1+error
    return probabilities


def process(element):
    logger.info(
        f"Updating the policy of the user {element['id']} for the product {element['product']}")

    userPolicyDB = policyDB[element['id']]
    purchasedProduct = element['product']
    # get the index of the probability of the baught product
    purchasedIndex = np.where(
        userPolicyDB["products"] == purchasedProduct)[0][0]
    gain = userPolicyDB["probabilities"][purchasedIndex] * learning_rate/100
    try:
        userPolicyDB["probabilities"] = update_probabilities(
            userPolicyDB["probabilities"], purchasedIndex, gain)
    except AssertionError:
        # in case there was an error while calculating the probabilities we assure that the sum of all probabilities is 1
        logger.error(
            "the new probabilities are wrong we will try to correct them ")
        collateralError = (
            userPolicyDB["probabilities"] - 1)/len(userPolicyDB["probabilities"])

        correct_error = np.vectorize(
            lambda x: x - collateralError if x >= collateralError else 0)
        userPolicyDB["probabilities"] = correct_error(
            userPolicyDB["probabilities"])
        # the unfortunate case is where we have sum(probabilities) > 1 and some of the probabilites are 0 in this case this correction wont work and it would be better to devide the error by len([x for x in probabilities if x > o] ) but it will be too much slow and complicated for the code so for the moment i m ignoring it and i just raise an error
        assert 1-error <= sum(userPolicyDB["probabilities"]) <= 1+error


@ timeit
@ app.route('/<string:id>/products')
def products(id):
    if not (id in policyDB.keys()):
        # default configuration we know nothing about the suer
        logging.debug(f"adding a new user ({id}) to the policy base")
        policyDB[id] = deepcopy(policyDB["default"])
    # we pick some products and if the all the products in the list fits in one page we will print them all anyway
    shownProducts = np.random.choice(
        policyDB[id]["products"], size=min(PageSize, len(policyDB[id]["products"])), replace=False, p=policyDB[id]["probabilities"])
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
