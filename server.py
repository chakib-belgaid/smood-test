from queue import Queue
from threading import Thread
from time import sleep

import logging
import numpy as np
from flask import Flask, send_file, jsonify

# additional imports
from flask import request
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
user: User = None
usersDB: Dict[int, User] = {}


def process(element):
    raise NotImplementedError


@app.route('/<string:id>/products')
def products(id):
    raise NotImplementedError


# ***** End of your solution *****


@app.route('/', methods=['POST', 'GET'])
def index():
    userid = request.cookies.get('userID')

    response = send_file('index.html')
    if userid:
        user = usersDB[userid]
        logger.info(f"got the user {userid}")
    else:
        user = User()
        usersDB[user.id] = user
        logger.info(f"added  : {user.id}")
    return response


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
