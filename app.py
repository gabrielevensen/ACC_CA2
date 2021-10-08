from celery import Celery
from flask import Flask, jsonify
import json
import os
import time


def make_celery(app):
    celery = Celery(app.import_name, backend='rpc://',
                    broker='pyamqp://guest@localhost//')
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
celery = make_celery(app)


# -------- Flask Test -------- #
# Returns entered name
@app.route('/test/<name>')
def proc(name):
    return name


# -------- *1* Run celery task in Flask -------- #
@app.route('/<name>')
def process1(name):
    print_str.delay(name)
    return 'OK request!'


# -------- *1* Run Tweet Counter in Flask -------- #
@app.route('/task1')
def process():
    fp = './subset'
    result = count_pronouns.delay(fp)
    time.sleep(10)
    return result.get()


# -------- *2* Tweet Counter Function TASK -------- #
@celery.task(name='celery1.count_pronouns')
def count_pronouns(filepath):
    pronouns = ["han", "hon", "den", "det", "denna", "denne", "hen"]
    count = [0, 0, 0, 0, 0, 0, 0]
    files = os.listdir(filepath)
    for file in files:
        path = filepath + '/' + file
        data = []
        with open(path, "r") as file:
            for line in file:
                if not line.strip():
                    continue
                tweet = json.loads(line)
                if 'retweeted_status' not in tweet:
                    data.append(tweet['text'])
        for tweet in data:
            if 'han' in tweet:
                count[0] += 1
            elif 'hon' in tweet:
                count[1] += 1
            elif 'den' in tweet:
                count[2] += 1
            elif 'det' in tweet:
                count[3] += 1
            # elif 'denna' in tweet:
            #   count[4] += 1
            # elif 'denne' in tweet:
            #   count[5] += 1
            elif 'hen' in tweet:
                count[6] += 1

            if 'denna' in tweet:
                count[4] += 1
            if 'denne' in tweet:
                count[5] += 1

    res = dict(zip(pronouns, count))
    with open('output.txt', 'w') as output:
        json.dump(res, output)

    return res


# -------- *2* A celery task -------- #
@celery.task(name='celery_test.print_str')
def print_str(a_string):
    return a_string


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
