# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask is running!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)