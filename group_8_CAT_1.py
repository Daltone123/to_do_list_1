# Task Management Component
#This component manages tasks by allowing you to add, update, view, and delete tasks.

class Task:
    def __init__(self, task_id, title, description, due_date, status ="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = "Pending"  # Default status

    def __repr__(self):
        return f"{self.task_id}: {self.title} | {self.status} | Due: {self.due_date}"

class TaskManager:
    def __init__(self):
        self.tasks = PersistenceManager.load_tasks()
        self.next_id = self._get_next_id()

    def _get_next_id(self):
        return max((task.task_id for task in self.tasks), default=0) + 1

    def add_task(self, title, description, due_date):
        task = Task(self.next_id, title, description, due_date)
        self.tasks.append(task)
        self.next_id += 1
        PersistenceManager.save_tasks(self.tasks)  # Save to JSON after adding
        print(f"Task '{title}' added successfully.")

    def update_task_status(self, task_id, new_status):
        task = self.find_task_by_id(task_id)
        if task:
            task.status = new_status
            PersistenceManager.save_tasks(self.tasks)  # Save to JSON after updating
            print(f"Task '{task.title}' status updated to {new_status}.")
        else:
            print("Task not found.")

    def delete_task(self, task_id):
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            PersistenceManager.save_tasks(self.tasks)  # Save to JSON after deleting
            print(f"Task '{task.title}' deleted.")
        else:
            print("Task not found.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            for task in self.tasks:
                print(task)

    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None


''' Initialize TaskManager
task_manager = TaskManager()

# Add a few tasks
task_manager.add_task("Finish assignment", "Complete the Component-Oriented Programming project", "2024-12-01")
task_manager.add_task("Grocery shopping", "Buy milk, eggs, and bread", "2024-11-10")

# List tasks
print("\nListing all tasks:")
task_manager.list_tasks()

# Update a task's status
print("\nUpdating the status of the first task:")
task_manager.update_task_status(1, "Completed")

# List tasks again to see the update
print("\nListing all tasks after status update:")
task_manager.list_tasks()

# Delete a task
print("\nDeleting the second task:")
task_manager.delete_task(2)

# List tasks again to see the deletion
print("\nListing all tasks after deletion:")
task_manager.list_tasks()'''


#User Interface Component

# provides a simple text-based interface for the user to interact with the application.

#It calls methods from TaskManager based on user input.

class ToDoApp:
    def __init__(self):
        self.task_manager = TaskManager()

    def display_menu(self):
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Update Task Status")
        print("3. Delete Task")
        print("4. List All Tasks")
        print("5. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.update_task_status()
            elif choice == "3":
                self.delete_task()
            elif choice == "4":
                self.list_tasks()
            elif choice == "5":
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_task(self):
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date (e.g., 2024-12-31): ")
        self.task_manager.add_task(title, description, due_date)

    def update_task_status(self):
        task_id = int(input("Enter task ID to update: "))
        new_status = input("Enter new status (Pending, Completed): ")
        self.task_manager.update_task_status(task_id, new_status)

    def delete_task(self):
        task_id = int(input("Enter task ID to delete: "))
        self.task_manager.delete_task(task_id)

    def list_tasks(self):
        self.task_manager.list_tasks()


# Saving component 

import json

class PersistenceManager:
    FILE_PATH = "tasks.json"

    @staticmethod
    def save_tasks(tasks):
        # Convert each Task object to a dictionary
        tasks_dict = [task.__dict__ for task in tasks]
        with open(PersistenceManager.FILE_PATH, 'w') as file:
            # Use indent and sort_keys for a readable, clean JSON format
            json.dump(tasks_dict, file, indent=4, sort_keys=True)
        print("Tasks saved to tasks.json")

    @staticmethod
    def load_tasks():
        try:
            with open(PersistenceManager.FILE_PATH, 'r') as file:
                tasks_data = json.load(file)
                # Convert each dictionary back to a Task object
                return [Task(**data) for data in tasks_data]
        except FileNotFoundError:
            return []


# Running the Application

if __name__ == "__main__":
    app = ToDoApp()
    app.run()

