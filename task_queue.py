import redis
import json
import time
import random


class TaskQueue:
    """
    Definition of the task queue.
    """
    def __init__(self, config_file='config.json'):
        self.broker = self.connect(config_file)

    def connect(self, config_file):
        """Connect to broker service, redis in this case"""
        try:
            with open(config_file) as f:
                conf = json.load(f)['broker']
            conn = redis.StrictRedis(host=conf['host'], port=conf['port'])
            return conn
        except FileNotFoundError:
            print('Configuration file not found!')
            exit(1)

    def push(self, task, args):
        """Push a task in queue"""
        key = '{}_{}_{}'.format(task, time.time(), random.uniform(0, 1))
        task_args = json.dumps({'task': task, 'args': args})
        self.broker.rpush('tasks', key)
        self.broker.set(key, task_args)
        return 0

    def pop(self):
        """Deletes the top element and return its value"""
        key = self.broker.lpop('tasks')
        value = self.broker.get(key)
        self.broker.delete(key)
        return value

    def q_size(self):
        """Returns the number of tasks that are enqueued"""
        return self.broker.llen('tasks')

    def front(self):
        """Returns the front element"""
        key = self.broker.lindex('tasks', 0)
        return self.broker.get(key)
