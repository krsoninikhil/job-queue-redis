## Instructions

- Start a redis server and update configurations in `config.json` file.
- Define any other required tasks in `tasks.py`.
- Enqueue any task with:
```python
q = TaskQueue(config_file='config.json')
q.push('task_function_name', arguments)
```
- Start the worker with (you might want to run this as background process):
```bash
python worker.py
```
- Run tests with:
```bash
python tests.py
```
This should not throw any exceptions.

## Known Caveats

- It is assumed that if worker has started a task, it will be executed
successfully.
- Currently only single channel/queue called `tasks` is implemented, should
support multiples.
