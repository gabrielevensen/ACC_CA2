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
    lift = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    drag = ['high', 'low', 'medium', 'small', 'high', 'low', 'medium', 'high', 'small', 'small']
    result = dict(zip(lift, drag))
    time.sleep(10)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
