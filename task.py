# Submitted by: Chandrashekhar Tripathi (NIT Arunachal Pradesh, B.Tech. 2nd year)

import sys
import csv
import os

# header for csv database file
csv_header = ['Name', 'Priority', 'Done']

class Tasks:
    pending = []
    completed = []
    # Initialize the list of tasks
    def __init__(self, data_file: str):
        self.data_file = data_file


    # Load data from csv file into memory
    def load(self):
        # writing header data to file
        if not os.path.isfile(self.data_file):
            with open(self.data_file, 'a') as file:
                to_file = csv.DictWriter(file, csv_header)
                to_file.writeheader()

        # Load data from file in tasks
        with open (self.data_file, 'r') as file:
            reader = csv.DictReader(file)

            for task in reader:
                for key in task:
                    if not key == 'Name':
                        task[key] = int(task[key])
                if task['Done'] == 0:
                    self.pending.append(task)
                else:
                    self.completed.append(task)
            
            # sorting the tasks list
            self.pending = sorted(self.pending, key= lambda task: task['Priority'])
            
    
    # Add a task to the list of Tasks
    def add_task(self, name: str, priority: int, done: int):
        new_task = {'Name': name, 'Priority': priority, 'Done': done}

        if new_task not in self.pending:
            for i,task in zip(range(len(self.pending)), self.pending):
                if task['Name'] == new_task['Name']:
                    self.pending.pop(i)
            
            for i,task in zip(range(len(self.completed)), self.completed):
                if task['Name'] == new_task['Name']:
                    self.completed.pop(i)

            self.pending.append(new_task)

            # writing to data file
            with open(self.data_file, "w") as file:
                to_file = csv.DictWriter(file, csv_header)
                to_file.writeheader()
                for task in self.pending:
                    to_file.writerow(task)
                for task in self.completed:
                    to_file.writerow(task)

        print('Added task: "{}" with priority {}'.format(new_task['Name'], new_task['Priority']))
    

    # List the pending tasks from the list of tasks
    def ls(self):
        if len(self.pending) == 0:
            print('There are no pending tasks!')

        for i,task in zip(range(len(self.pending)), sorted(self.pending, key=lambda task: task['Priority'])):
            print(f"{i + 1}. {task['Name']} [{task['Priority']}]")
    

    # Print a report of pending and completed tasks
    def report(self):
        n_pending = len(self.pending)
        n_completed = len(self.completed)

        print(f'Pending : {n_pending}')
        for i,task in zip(range(len(self.pending)), sorted(self.pending, key=lambda task: task['Priority'])):
            print(f"{i + 1}. {task['Name']} [{task['Priority']}]")
        print()

        print(f'Completed : {n_completed}')
        for i,task in zip(range(len(self.completed)), sorted(self.completed, key=lambda task: task['Priority'])):
            print(f"{i + 1}. {task['Name']}")


    # Mark a task as done
    def task_done(self, index: int):
        if index-1 in range(len(self.pending)) and index > 0:
            done_task = self.pending[index - 1]
            done_task['Done'] = 1

            if done_task not in self.completed:
                for i,task in zip(range(len(self.completed)), self.completed):
                    if done_task['Name'] == task['Name']:
                        self.completed.pop(i)
                self.completed.append(self.pending.pop(index - 1))
            else:
                self.pending.pop(index - 1)

            # writing updated tasks to csv file after task is done
            with open(self.data_file, "w") as file:
                to_file = csv.DictWriter(file, csv_header)
                to_file.writeheader()
                for task in self.pending:
                    to_file.writerow(task)
                for task in self.completed:
                    to_file.writerow(task)
            
            print('Marked item as done.')
            
        else:
            print(f'Error: no incomplete item with index #{index} exists.')
    

    # Delete task from task list
    def task_del(self, index: int):
        if index-1 in range(len(self.pending)):
            self.pending.pop(index - 1)

            # writing updated tasks to csv file after task is done
            with open(self.data_file, "w") as file:
                to_file = csv.DictWriter(file, csv_header)
                to_file.writeheader()
                for task in self.pending:
                    to_file.writerow(task)
                for task in self.completed:
                    to_file.writerow(task)

            print(f'Deleted task #{index}')
        else:
            print(f'Error: task with index #{index} does not exist. Nothing deleted.')
    

    # Clear the database file
    def clear(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        else:
            print('Error: Database file does not exist')



def main():
    # display help
    help_str = """Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics"""

    if len(sys.argv) == 1 or sys.argv[1] == 'help':
        print(help_str)
        return
        
    # Create a Tasks object
    myTasks = Tasks(data_file='./task_database.csv')

    # load tasks from file
    myTasks.load()

    # reading options from command line
    if (len(sys.argv) >= 2):
        if sys.argv[1] == 'add':
            if len(sys.argv) == 4:
                myTasks.add_task(priority=int(sys.argv[2]), name=sys.argv[3], done=0)
            else:
                print('Error: Missing tasks string. Nothing added!')
        elif sys.argv[1] == 'ls':
            myTasks.ls()
        elif sys.argv[1] == 'report':
            myTasks.report()
        elif sys.argv[1] == 'done':
            if len(sys.argv) == 3:
                myTasks.task_done(index= int(sys.argv[2]))
            else:
                print('Error: Missing NUMBER for marking tasks as done.')
        elif sys.argv[1] == 'del':
            if len(sys.argv) == 3:
                myTasks.task_del(index= int(sys.argv[2]))
            else:
                print('Error: Missing NUMBER for deleting tasks.')
        elif sys.argv[1] == 'clear':
            if len(sys.argv) == 2:
                myTasks.clear()
            else:
                print('Error: Invalid syntax for clearing database file. Nothing cleared!')


main()