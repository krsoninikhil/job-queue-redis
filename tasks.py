# Define all the tasks here as a seperate function, for now worker only
# looks here for task definitions.
import time
import docker

def docker_task(args):
    '''
    args contains: name of docker image, list of commands, cpu and memory usage
    in dictionary and a dictionary of environment variables
    '''
    dc = docker.from_env()  # docker client
    logs = dc.containers.run(args['image'], args['cmd'],
        mem_limit=args['resources']['mem'], cpu_percent=args['resources']['cpu'],
        environment=args['env'])
    print(logs)
    return 0

def test_task(args):
    print('Testing task is executing!')
    time.sleep(3)
    print('done')
    return 0
