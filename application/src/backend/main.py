sample_tasks = ["Fold Laundry", "Study for Midterm", "Wash Dishes", "Walk Dog"]
user_lists = []

class UserList:
    def __init__(self, id, name, tasks):
        self.id = id
        self.name = name
        self.tasks = []

def create_list():
    newList = UserList()
    newList.id = len(user_lists)
    newList.name = input("List Name:")
    newList.tasks.append(add_tasks())
    print(newList.tasks)

    user_lists.append(newList)

    return
def add_tasks():
    for i, task in enumerate(sample_tasks, start=1):
        print(f"{i}. {task}")

    user_selection = input("Enter the number of the tasks you would like to add, separated by commas: ")
    tasks = user_selection.split(",")
    tasks_to_add = [
        sample_tasks[int(task) - 1]
        for task in tasks
        if task.strip().isdigit() and 1 <= int(task.strip()) <= len(tasks)
    ]
    #print(tasks_to_add)
    return tasks_to_add

def delete_list():
    print("Here is a list of your Task Lists:")
    for list in user_lists:
        print("id: ",list.id, "name: ",list.name)
    user_selection = input("Enter the id of the list you would like to delete: ")
    for list in user_lists:
        if list.id == user_selection:
            user_lists.remove(list)

    return

def start_func():
    sec_selection = "y"
    final = "y"
    selection = input("Would you like to add a list? (Y/N): ")
    if selection.lower() == "y":
        add_tasks()
        start_func()
    else:
        sec_selection = input("Would you like to delete a list? (Y/N): ")

    if sec_selection.lower() == "y":
        delete_list()
        start_func()
    else:
        final = input("Enter Y to start over or N to exit: ")

    if final.lower() == "y":
        start_func()
    else:
        return

start_func()