# Fake database library
# Ideally, this would interface with MySQL or MongoDB. For purposes of this problem, I
# will use CSV files

import csv

class csvDB:
    # Creating a class for handling a "database", which is really a CSV file meant to
    # represent MySQL. All of these are horribly inefficient because I have to keep
    # opening/closing the CSV file each time.
    
    # Columns:
    # 0 - id -- mimics MySQL setup. Not important to the other stuff
    # 1 - name -- task name
    # 2 - location -- filepath to program
    # 3 - runtime -- time at which program was run
    # 4 - status -- COMPLETE, RUNNING, or ERROR (in MySQL, this would be an enum)

    def __init__(self, DB_FILENAME = 'database\\tasks.csv'):
        self.dbFile = DB_FILENAME
        
        # Check the file and assign to self the last ID number
        self.maxId = 0
        with open(self.dbFile, mode='r') as csvFile:
            fileObj = csv.reader(csvFile, delimiter=',')
            for row in fileObj:
                # Ignore first row, which has column names
                if row[0] != 'id':
                    if int(row[0]) > self.maxId:
                        self.maxId = int(row[0])

    def get_running(self):
        # MySQL: SELECT * FROM tasks WHERE status == RUNNING
        # Return a list of tasks with the RUNNING status
        # Returns [] if none found
        
        # Initialize list of rows with runs
        running_tasks = []
        
        # Read the file
        with open(self.dbFile, mode='r') as csvFile:
            fileObj = csv.reader(csvFile, delimiter=',')
            for row in fileObj:
                if row[4] == 'RUNNING':
                    running_tasks.append(row)
        
        return running_tasks
    
    def add_task(self, newRow):
        # Adds a row into the "database" indicating a new run
        # newRow should be a comma-delimited string with values for name, location, and
        # runtime. Status is automatically added as RUNNING. ID is added automatically
        # and incremented from previous max value
        
        # Increment maxId number
        self.maxId = self.maxId + 1
        
        # Append to the file
        with open(self.dbFile, mode='a') as csvFile:
            insertRow = str(self.maxId) + ',' + newRow + ',RUNNING\r'
            csvFile.write(insertRow)
    
    def update_task(self, updateId = '', newStatus = ''):
        # Updates a row with a new status (i.e. goes from RUNNING to COMPLETE or ERROR)
        # User needs to provide an ID for the task and a status to update it to
        
        # Check if user supplied values properly
        try:
            int(updateId)
        except ValueError:
            print('Could not process updateId as an int')
        if newStatus != 'COMPLETE' and newStatus != 'ERROR':
            raise Exception('Invalid newStatus value provided')
        
        # Complete this later once I think through how to modify CSV without copy/pasting
        # the whole thing into memory

# __main__ function block put here for testing purposes
if __name__ == "__main__":
    testDB = csvDB()
    output = testDB.get_running()
    
    newRow = 'Test insert,C:\\file\\path,04/16/2020 06:00:00 EST'
    testDB.add_task(newRow)