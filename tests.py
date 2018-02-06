from task_queue import TaskQueue
from tasks import test_task, docker_task
from worker import start_worker

# define task arguments for testing
args = {'image': 'alpine:latest', 'cmd': ['ls', '-a'], 'env': {'FOO': 'bar'},
        'resources': {'cpu': '20', 'mem': '9000000'}}

# make a test queue object
q = TaskQueue(config_file='config.json')

# get current number of tasks enqueued
n = q.q_size()

# test if task executes with exit status 0
print('Testing docker_task explicitly...')
assert docker_task(args) == 0
print('Done')

# test if task gets enqueued to the queue
assert q.push('test_task', args) == 0
assert q.push('test_task', args) == 0
assert q.push('test_task', args) == 0
assert q.push('test_task', args) == 0

# test if task has enqueued
assert q.q_size() == n + 4

# test if worker executes 3 tasks with given resources and exit with status 0
# since the required cpu of the tasks is 20% and available is 50% only 2 tasks
# should be executed parallely and 3rd will be executed only when one of
# the earlier two is completed. This can be verified through log timestamp.
assert start_worker(max=3, resources=[50, 18000000]) == 0

# test if task has removed from queue
assert q.q_size() == n + 1

# test if pop and front works
assert not q.front() is None
assert not q.pop() is None

# test if pop reduced the size of queue
assert q.q_size() == n
