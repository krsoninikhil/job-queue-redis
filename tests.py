# define task arguments for testing
args = {'image': 'test', 'cmds': ['cmd'], 'resources': {}, 'env': {}}

# make a test queue object
q = Queue()

# get current number of tasks enqueued
n = q.q_size

# test if task executes with exit status 0
assert docker_task(args) == 0

# test if task gets enqueued to the queue
assert q.enqueue(docker_task, args) == 0

# test if task has enqueued
assert q.q_size == n + 1

# test if worker executes the task and exit with status 0
assert worker() == 0

# test if task has removed from queue
assert q.q_size == n
