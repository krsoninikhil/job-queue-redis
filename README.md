## Job-Queue

An application for queueing tasks for later execution, uses Redis as message broker.

## Requirements

- Install `redis`, on Arch Linux do:
```bash
sudo pacman install redis
```
- If you are running docker related tasks then install that too.
- It uses `redis` and `docker` python client. Install them with:
```bash
sudo pip install -r requirements.txt
```

## Instructions To Use

- Start a redis server and update configurations in `config.json` file.
- Define any other required tasks in `tasks.py`.
- Enqueue any task with:
```python
from task_queue import TaskQueue
q = TaskQueue(config_file='config.json')
q.push('task_function_name', arguments)
```
Here `arguments` is in dictionary like `{'image': 'alpine', 'cmd': ['ls', '-a'],
'env': {'FOO': 'bar'}, 'resources': {'cpu': '2', 'mem': '2'}}` where value of `cpu`
is the percentange of CPU allowed and `mem` is the memory (bytes) allowed for
this task.

- Start the worker with (you might want to run this as background process):
```bash
python worker.py <available_cpu> <available_memory>
```
Here `available_cpu` is in percentange and `available_memory` is in bytes. To run any docker related task, minimum memory limit is 4MB

- Almost all the functionality can be understood by reading examples in
`tests.py`. Execute tests by:
```bash
python tests.py
```
For a successful execution, this should not throw any exceptions.
- If you need help setting up, please [contact](http://nikhilsoni.me/contact/).

## Known Caveats

- It is assumed that if worker has started a task, it will be executed
successfully.
- Currently only single channel/queue called `tasks` is implemented, should
support multiples.
- Since worker is executing multiple tasks in parallel, depending on the
execution time, the order of execution of tasks might not remain same as they
were enqueued.
- Available CPU given to worker as well as to the jobs while queueing
them is in percentange i.e. multiple CPUs should be considered while queueing jobs
itself.
- When any task starts executing, it is assumed it is taking all the resources that
are allowed for it.

## License

[MIT License](https://nks.mit-license.org/)
