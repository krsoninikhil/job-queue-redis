# Define all the tasks here as a seperate function, for now worker only
# looks here for task definitions.
import time

def docker_task(args):
    '''
    args contains: name of docker image, list of commands, cpu and memory usage
    in dictionary and a dictionary of environment variables
    '''
    print(args)
    time.sleep(3)
    print('done')
    return 0

def test_task(args):
    print('Testing task is executing!')
    time.sleep(3)
    print('done')
    return 0
