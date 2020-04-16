# Problem 1: Task Scheduler
# Philip Chow

import json
import database
import datetime as dt
import pytz

def read_config(filepath):
    # Parses a task scheduler config file. This assumes the config JSON file is structured
    # with one key value pair in the entire file called task_config. task_config is
    # a JSON array, where each element in the array consists of five fields. Any other
    # fields in the config are ignored.
    #
    # task_name - a string to name a task. This must be unique, though different task
    #   names can call the same task location
    # task_location - a string indicating where a program is located on the filesystem
    # task_interval - an int specifying time between runs in seconds. If 0, then the task
    #   is run only once. If this value is blank, it is assumed to be 0.
    # task_scheduled_time - a string indicating a time to run the first iteration of the
    #   task. If blank, the task runs immediately. If task_scheduled is false, this value
    #   is ignored
    # task_scheduled - bool (formatted as a str) indicating if a task is intended to be
    #   scheduled. If false, the value in task_scheduled_time is ignored and the task
    #   runs immediately.
    #
    # This function returns a dict containing all configs, where each config only has the
    # five fields listed above
    
    # Open the file and start parsing it
    with open(filepath) as f:
        data = json.load(f)
        
        # Check that task_config exists in the file, and stop if it doesn't
        if 'task_config' not in data.keys():
            raise Exception('The key ''task_config'' doesn''t exist in the JSON file')
        
        config_list_orig = data['task_config']
        
        # Check length of list. If zero, stop processing
        if len(config_list_orig) == 0:
            raise Exception('No configurations found in ''task_config''')
        
        # Initialize new variable for holding config data. This is the output of this
        # function.
        config_list = []
        
        # Counter variable to allow for easier debugging on config file
        count = 0
        
        # Extract just the config data that we want
        for obj in config_list_orig:
            # Reinitialize tmp on every iteration so it's obvious if it didn't work
            tmp = {}
            
            # Assign keys from original list to tmp object
            # Force variable types and also check for existence of value. If the key
            # doesn't exist, keep going and let user know in console
            try:
                tmp['task_name'] = str(obj['task_name'])
            except KeyError:
                print('Couldn''t find the key ''task_name'' at iteration ' + str(count))
            
            try:
                tmp['task_location'] = str(obj['task_location'])
            except KeyError:
                print('Couldn''t find the key ''task_location'' at iteration ' + str(count))
            
            try:
                # Check if task_interval is blank
                if obj['task_interval'] == '':
                    tmp['task_interval'] = 0
                else:
                    tmp['task_interval'] = int(obj['task_interval'])
            except KeyError:
                print('Couldn''t find the key ''task_interval'' at iteration ' + str(count))
            except ValueError:
                print('Couldn''t convert ''task_interval'' to an int at iteration ' + str(count))
            
            try:
                tmp['task_scheduled_time'] = str(obj['task_scheduled_time'])
            except KeyError:
                print('Couldn''t find the key ''task_scheduled_time'' at iteration ' + str(count))
            
            # If task_scheduled is a string, set it to lowercase and match it with true/false
            # If it's not a string or a bool, just error out
            try:
                if type(obj['task_scheduled']) == str:
                    if obj['task_scheduled'].lower() == 'true':
                        tmp['task_scheduled'] = True
                    elif obj['task_scheduled'].lower() == 'false':
                        tmp['task_scheduled'] = False
                    else:
                        raise ValueError()
                elif type(obj['task_scheduled']) == bool:
                    tmp['task_scheduled'] = (obj['task_scheduled'])
                else:
                    raise ValueError()
            except ValueError:
                print('Couldn''t find the key ''task_scheduled'' at iteration ' + str(count))
            
            # Assign data to final config_list if it has 5 fields (having an issue with
            # tmp being appended even though exceptions should remove it, specifically at
            # task_scheduled checkpoint)
            if len(tmp) == 5:
                config_list.append(tmp)
            
            # Increment counter
            count = count + 1
    
    return config_list

def get_jobs_to_run(config_list):
    # Given a list of job configurations, identify which ones need to be run based on the
    # scheduled time provided in the configuration. It is assumed that this scheduler runs
    # once a minute, so only jobs with expected start times within one minute of now are
    # kicked off.
    
    # Initialize variables
    utcTz = pytz.timezone("UTC") # Always use UTC
    now = utcTz.localize(dt.datetime.now())
    to_run_list = []
    
    # Loop through all objects in config_list
    for obj in config_list:
        try:
            # If task_scheduled is false, the job runs
            # Otherwise, need to do some time comparisons
            if obj['task_scheduled'] == False:
                to_run_list.append(obj)
            elif obj['task_scheduled'] == True:
                # If task_scheduled_time has values, parse it
                if obj['task_scheduled_time'] == '':
                    print('Couldn''t find any values for task_scheduled_time')
                    raise Exception()
                
                # The following line of code doesn't work even though %Z should handle EST, per
                # strptime documentation. Hard-coding EST for now.
                # This might be an issue between Python 3.6 and whatever the online documentation is for
                # runtime = dt.datetime.strptime(obj['task_scheduled_time'], '%m/%d/%Y %H:%M:%S %Z')
                
                runtimeEST = dt.datetime.strptime(obj['task_scheduled_time'], '%m/%d/%Y %H:%M:%S EST')
                runtimeUTC = utcTz.localize(runtimeEST + dt.timedelta(hours = 5)) # Force it to time aware in UTC
                
                # If the start time is before now, then we need to march the time forward
                while runtimeUTC < now:
                    runtimeUTC = runtimeUTC + dt.timedelta(seconds = obj['task_interval'])
                print(runtimeUTC)
            else:
                # This shouldn't happen, but put it here just in case
                print('Error: task_scheduled is neither true nor false')
                raise Exception()
        except Exception as error:
            print('Failed to identify jobs to run (get_jobs_to_run): ' + str(error))
    
    return to_run_list

def check_job_runtime(to_run_list, running_list):
    # Given a list of job configurations and jobs that are already running, make sure
    # that there are no collisions. i.e. if a job is already running, don't try to kick
    # it off again.
    
    final_run_list = []
    
    return final_run_list

def run_jobs(final_run_list):
    # Dummy function to run some jobs
    
    for obj in final_run_list:
        name = obj['task_name']
        program = obj['task_location']
        print('Task ' + task_name + ' at ' + task_location + ' kicked off')
        
        # For Windows, I choose to use os.system. Leaving this commented out because
        # the functions don't actually exist
        # os.system(program)

def scheduler(CONFIG_FILE = 'config.json'):
    # Given a config.json file (assumed to share the same directory as this file), then
    # do some scheduling tasks. The scheduler first parses the config file to identify
    # all tasks that need to be run, as well as associated parameters
    #
    # Assumes a default CONFIG_FILE name of 'config.json'. This can be modified by the
    # user when calling the function if so desired
    
    # Initialize database
    db = database.csvDB()
    
    # Get list of configurations
    config_list = read_config(CONFIG_FILE)
    
    # Check what needs to be run now based on config_list
    to_run_list = get_jobs_to_run(config_list)
    
    # Check what is already running (from database)
    running_list = db.get_running()
    
    # If there is a collision in task name between what is running now and what needs to
    # kick off, don't kick off the new task.
    final_run_list = check_job_runtime(to_run_list, running_list)
    
    # Otherwise, kick off the new task
    run_jobs(final_run_list)
    
    # Insert new jobs into the the database
    # db.add_task(SOME_DATA)
    
    # Check job status for all jobs previously identified as running. If the job is
    # done or errored out, update it accordingly in the database
    
    # Return variables for debugging purposes
    return config_list, running_list, to_run_list

if __name__ == "__main__":
    # Run the function. Also fetch output for debug purposes
    output = scheduler()