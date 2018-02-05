from task_queue import TaskQueue
from tasks import docker_task
from worker import start_worker

# define task arguments for testing
args = {'image': 'test', 'cmds': ['cmd'], 'resources': {}, 'env': {}}

# make a test queue object
q = TaskQueue(config_file='config.json')

# get current number of tasks enqueued
n = q.q_size()

# test if task executes with exit status 0
#assert docker_task(args) == 0

# test if task gets enqueued to the queue
assert q.push('docker_task', args) == 0
assert q.push('docker_task', args) == 0
assert q.push('docker_task', args) == 0

# test if task has enqueued
assert q.q_size() == n + 3

# test if worker executes the one task and exit with status 0
assert start_worker(max=2) == 0

# test if task has removed from queue
assert q.q_size() == n + 1

# test if pop and front works
assert not q.front() is None
assert not q.pop() is None

# test if pop reduced the size of queue
assert q.q_size() == n
