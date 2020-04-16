# Problem 1: Task Scheduler
# Philip Chow

import json

def read_config(filename):
    # Parses a task scheduler config file. This assumes the config JSON file is structured
    # with one key value pair in the entire file called task_config. task_config is
    # a JSON array, where each element in the array consists of five fields:
    #
    # task_name - a string to name a task. This must be unique, though different task
    #   names can call the same task location
    # task_location - a string indicating where a program is located on the filesystem
    # task_interval - an int specifying time between runs in seconds. If 0, then the task
    #   is run only once
    # task_scheduled_time - a string indicating a time to run the first iteration of the
    #   task. If blank, the task runs immediately. If task_scheduled is false, this value
    #   is ignored
    # task_scheduled - bool (formatted as a str) indicating if a task is intended to be
    #   scheduled. If false, the value in task_scheduled_time is ignored and the task
    #   runs immediately.
    
    json = 'blargle'
    
    return json

def scheduler(CONFIG_FILE = 'config.json'):
    # Given a config.json file (assumed to share the same directory as this file), then
    # do some scheduling tasks. The scheduler first parses the config file to identify
    # all tasks that need to be run, as well as associated parameters
    #
    # Assumes a default CONFIG_FILE name of 'config.json'. This can be modified by the
    # user when calling the function if so desired
    
    print('Done')
    
    return 0

if __name__ == "__main__":
    scheduler()