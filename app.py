from flask import Flask, jsonify
import json
import os
import time
import re

app = Flask(__name__)


# -------- Flask Test -------- #
# Returns entered name
@app.route('/test/<name>')
def proc(name):
    return name


# -------- *1* Present result in Flask -------- #
@app.route('/task1')
def process():
    # for subdir, dirs, files in os.walk('data'):
    #     for file in files:
    #         filepath = subdir + os.sep + file
    #         file = open(filepath, 'r')
    #         lines = file.readlines()
    #         for index, line in enumerate(lines):
    #
    # file.close()
    result = "hej"
    time.sleep(10)
    return result.get()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
