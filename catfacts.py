from flask import Flask
from os import path
import random
import json
app = Flask(__name__)

class CatFacts:
    def __init__(self, filename=None):
        self.facts = []
        if filename:
            self.load(filename)

    def load(self, filename):
        with open(filename) as f:
            self.facts = json.load(f)

    def random(self):
        return random.choice(self.facts)

THEFACTS = CatFacts()

@app.route('/')
def hello_world():
    return THEFACTS.random()

if __name__ == '__main__':
    factfile = path.join(path.dirname(__file__), 'catfacts.json')
    THEFACTS.load(factfile)
    app.run(debug=True,host='0.0.0.0', port=80)
