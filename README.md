# Recommendations

The goal of this toy project is to introduce user-specific consumption-based recommendations.
The instructions are purposely vague and open so that there are multiple possible solutions.
However please do not modify the existing code base (outside the bounds) and make sure you use everything that is provided (you can add anything you need except new libraries).

Even if you are not acquainted with Javascript and/or HTML, the completion of those parts should be quickly feasible with the help of internet (and not representative of our daily challenges).
However copy-pasting entire function or algorithm is not an acceptable solution.

## Guidelines

1. Read carefully these instructions until the end
2. Complete both the frontend (`index.html`) and the backend (`server.py`) according to the specs below
3. Answer the questions at the end (max 1-2 sentences per question)
4. Keep it simple, a basic working solution is better than a cumbersome solution that is hard to maintain and understand

## Specs

- a user visits the website multiple times: he should get a unique identifier, persisted across browser/computer restarts
- each user should see a list of products ordered in a tailored way: he is more likely to pick products in the first rows than latter ones (think about thousands of products, the list could not fit into a single page)
- each time a user buys a product: his user policy (probability of buying for each product) should be updated accordingly and improve the likelihood of this product to be in the first rows (only this user should be affected by this change)
- good recommendations do not mean "always the same product first": the user should also be tempted to explore news products (which might be the ones he likes the most)
- use logs to keep track of the correctness on the server side

## Questions


- how would you implement batching of tracked events on the client side (mouse movements or clicks)?
    - answer
- why is there a worker processing the events from a waiting queue rather than processing elements directly?
    - answer
- how did you incorporate fairness among the products in your strategy?
    - answer
- how does the learning parameter affect the sorting?
    - answer

## Getting statred

You should use the latest Chrome available with python >3.8 (with numpy and flask).
```shell
export FLASK_APP=server.py
export FLASK_ENV=development
flask run
```

And browse [localhost:5000](http://localhost:5000).

Good luck!
