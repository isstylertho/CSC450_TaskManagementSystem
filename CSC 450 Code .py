sample_tasks = ["Fold Laundry", "Study for Midterm", "Wash Dishes", "Walk Dog"]
user_lists = []

class UserList:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.comments = []

def create_list():
    list_name = input("Enter the name for the new list: ")
    new_list = UserList(list_name)
    new_list.tasks.extend(add_tasks())
    user_lists.append(new_list)
    print(f"List '{new_list.name}' created with tasks: {new_list.tasks}")

def add_tasks():
    for i, task in enumerate(sample_tasks, start=1):
        print(f"{i}. {task}")

    user_selection = input("Enter the name of tasks you would like to add, separated by commas: ")
    tasks = user_selection.split(",")
    tasks_to_add = [
        sample_tasks[int(task) - 1]
        for task in tasks
        if task.strip().isdigit() and 1 <= int(task.strip()) <= len(sample_tasks)
    ]
    return tasks_to_add

def delete_list():
    print("Here is a list of your Task Lists:")
    for i, lst in enumerate(user_lists, start=1):
        print(f"{i}. {lst.name}")
    user_selection = input("Enter the number of the list you would like to delete: ")
    if user_selection.isdigit() and 1 <= int(user_selection) <= len(user_lists):
        deleted_list = user_lists.pop(int(user_selection) - 1)
        print(f"List '{deleted_list.name}' deleted.")
    else:
        print("Invalid selection.")

def add_comment():
    if not user_lists:
        print("No lists available. Please create a list first.")
        return
    
    print("Select a list to add a comment:")
    for i, lst in enumerate(user_lists, start=1):
        print(f"{i}. {lst.name}")
    
    list_selection = input("Enter the number of the list: ")
    if list_selection.isdigit() and 1 <= int(list_selection) <= len(user_lists):
        selected_list = user_lists[int(list_selection) - 1]
        comment = input("Enter your comment: ")
        selected_list.comments.append(comment)
        print(f"Comment added to list '{selected_list.name}': {comment}")
    else:
        print("Invalid selection.")

def delete_comment():
    if not user_lists:
        print("No lists available. Please create a list first.")
        return
    
    print("Select a list to delete a comment from:")
    for i, lst in enumerate(user_lists, start=1):
        print(f"{i}. {lst.name}")
    
    list_selection = input("Enter the number of the list: ")
    if list_selection.isdigit() and 1 <= int(list_selection) <= len(user_lists):
        selected_list = user_lists[int(list_selection) - 1]
        
        if not selected_list.comments:
            print("No comments to delete.")
            return
        
        print("Comments:")
        for i, comment in enumerate(selected_list.comments, start=1):
            print(f"{i}. {comment}")
        
        comment_selection = input("Enter the number of the comment to delete: ")
        if comment_selection.isdigit() and 1 <= int(comment_selection) <= len(selected_list.comments):
            deleted_comment = selected_list.comments.pop(int(comment_selection) - 1)
            print(f"Deleted comment: {deleted_comment}")
        else:
            print("Invalid comment number.")
    else:
        print("Invalid selection.")

def start_func():
    while True:
        print("\nMenu:")
        print("1. Add a List")
        print("2. Delete a List")
        print("3. Add a Comment")
        print("4. Delete a Comment")
        print("5. Exit")

        selection = input("Please select an option (1-5): ")

        if selection == "1":
            create_list()
        elif selection == "2":
            delete_list()
        elif selection == "3":
            add_comment()
        elif selection == "4":
            delete_comment()
        elif selection == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please try again.")

# Start the program
start_func()
