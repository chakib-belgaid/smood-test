from dataclasses import dataclass

# for the moment we generate a unique ID using random but i will change it later
import random
random.seed(1234)
#############


@dataclass
class User:
    id: str

    def __init__(self):
        self.id = random.randint(1, 1e9)
