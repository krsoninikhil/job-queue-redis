# Define all the tasks here as a seperate function, for now worker only
# looks here for task definitions.

def docker_task(args):
    '''
    args contains: name of docker image, list of commands, cpu and memory usage
    in dictionary and a dictionary of environment variables
    '''
    print(args)
    return 0
