from celery import Celery
from flask import Flask, jsonify
import json
import os
import timeit
import re

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

# -------- *1* Run Tweet Counter in Flask -------- #
@app.route('/task1')
def process():
    result = count_pronouns.delay()
    time.sleep(10)
    return result.get()

# -------- *1* Present result in Flask -------- #
@celery.task(name='make_celery.count_pronouns')
def count_pronouns():
    start = timeit.default_timer()

    def find_word(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    han_counter = 0
    hon_counter = 0
    den_counter = 0
    det_counter = 0
    denna_counter = 0
    denne_counter = 0
    hen_counter = 0
    unique_counter = 0

    for subdir, dirs, files in os.walk('data'):
        for file in files:
            filepath = subdir + os.sep + file
            file = open(filepath, 'r')

            lines = file.readlines()
            for index, line in enumerate(lines):
                if index % 2 == 0 and 'retweeted_status' not in json.loads(line.strip()):
                    if find_word('han')(json.loads(line.strip())['text']) is not None:
                        han_counter += 1
                    if find_word('hon')(json.loads(line.strip())['text']) is not None:
                        hon_counter += 1
                    if find_word('den')(json.loads(line.strip())['text']) is not None:
                        den_counter += 1
                    if find_word('det')(json.loads(line.strip())['text']) is not None:
                        det_counter += 1
                    if find_word('denna')(json.loads(line.strip())['text']) is not None:
                        denna_counter += 1
                    if find_word('denne')(json.loads(line.strip())['text']) is not None:
                        denne_counter += 1
                    if find_word('hen')(json.loads(line.strip())['text']) is not None:
                        hen_counter += 1
                    unique_counter += 1

    file.close()

    # print('Han appearing', han_counter, 'times.')
    # print('Hon appearing', hon_counter, 'times.')
    # print('Den appearing', den_counter, 'times.')
    # print('Det appearing', det_counter, 'times.')
    # print('Denna appearing', denna_counter, 'times.')
    # print('Denne appearing', denne_counter, 'times.')
    # print('Hen appearing', hen_counter, 'times.')
    # print('Number of unique tweets:', unique_counter, '.')
    #
    # objects = ('Han', 'Hon', 'Den', 'Det', 'Denna', 'Denne', 'Hen')
    # y_pos = np.arange(len(objects))
    # performance = [han_counter / unique_counter, hon_counter / unique_counter,
    #                den_counter / unique_counter, det_counter / unique_counter,
    #                denna_counter / unique_counter, denne_counter / unique_counter,
    #                hen_counter / unique_counter]
    #
    # plt.bar(y_pos, performance, align='center', alpha=1)
    # plt.xticks(y_pos, objects)
    # plt.title('Frequencies of pronouns normalized by total number of unique tweets')
    # plt.ylabel('Frequencies')
    # plt.title('Pronouns')
    # plt.grid(axis='y')
    # plt.show()

    stop = timeit.default_timer()
    timer = stop - start

    #print('Time: ', stop - start)

    pronouns = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen', 'Total unique tweets', 'Time for finding pronouns']
    counter = [han_counter, hon_counter, denne_counter, denna_counter, denna_counter, denne_counter, hen_counter,
               unique_counter, timer]
    result = dict(zip(pronouns, counter))

    return result

    # lift = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # drag = ['high', 'low', 'medium', 'small', 'high', 'low', 'medium', 'high', 'small', 'small']
    # result = dict(zip(lift, drag))
    # time.sleep(10)
    # return result



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
