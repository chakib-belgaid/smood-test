
import logging
import time
import server
import re
import numpy as np
import pytest

LOGGER = logging.getLogger(__name__)

productsDB = ['beef', 'pizza', 'pasta', 'fondue']
policyDB = {}
policyDB["default"] = {"products": np.array(productsDB), "probabilities": np.full(
    len(productsDB), 1/len(productsDB))}
# just a test

policyDB["ko8w8kdmd"] = {"products": np.array(['beef', 'pizza', 'pasta', 'fondue']),
                         "probabilities": np.array([0.3, 0.3, 0.2, 0.1])}


@server.timeit
def sleeping():
    time.sleep(1)


def test_timeit(caplog):
    caplog.set_level(logging.INFO)
    sleeping()
    assert re.match(".*100\d+\.\d\d us", caplog.text)


def test_update_probabilities():
    probabilities = [0.1, 0.05, 0.2, 0.4, 0.25]
    results = server.update_probabilities(probabilities, 2, 0.05)
    expectedResults = [0.0875, 0.0375, 0.25, 0.3875, 0.2375]
    for i, j in zip(results, expectedResults):
        assert pytest.approx(i, 1e-6) == j


def test_add_newproduct1():
    server.policyDB = policyDB
    server.add_new_product("default", "potato")
    assert policyDB["default"]["probabilities"][-1] == 0.2
    assert policyDB["default"]["probabilities"][1] == 0.2


def test_add_newproduct2():
    server.policyDB = policyDB
    server.add_new_product("ko8w8kdmd", "potato")
    assert policyDB["ko8w8kdmd"]["probabilities"][-1] == 0.2
    assert policyDB["ko8w8kdmd"]["probabilities"][1] == 0.25


def test_update_policy1():
    server.policyDB = policyDB
    element = {"id": "default", "product": "beef"}
    server.process(element)
    assert pytest.approx(policyDB["default"]
                         ["probabilities"][0], 1e-6) == 0.205
    assert pytest.approx(policyDB["default"]
                         ["probabilities"][3], 1e-6) == 0.19875


def test_update_policy2():
    server.policyDB = policyDB
    element = {"id": "ko8w8kdmd", "product": "beef"}
    server.process(element)
    assert pytest.approx(policyDB["ko8w8kdmd"]
                         ["probabilities"][0], 1e-6) == 0.25625
    assert pytest.approx(policyDB["ko8w8kdmd"]
                         ["probabilities"][1], 1e-6) == 0.2484375
