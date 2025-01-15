import os
from tkinter import *

root = Tk()
root.title("To Do List")
root.geometry("400x650+400+100")
root.resizable(False, False)

task_list = []

def openTaskFile():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to tasklist.txt
    tasklist_path = os.path.join(script_dir, "tasklist.txt")
    
    try:
        # Try to open the file for reading
        with open(tasklist_path, "r") as taskfile:
            tasks = taskfile.readlines()
            for task in tasks:
                if task.strip():  # Ignore empty lines
                    listbox.insert(END, task.strip())  # Add to the Listbox
    except FileNotFoundError:
        # Handle file not found: create an empty file
        print("tasklist.txt not found. Creating a new one...")
        with open(tasklist_path, "w") as taskfile:
            pass  # Creates an empty file

# Dynamically resolve image paths
script_dir = os.path.dirname(__file__)
icon_path = os.path.join(script_dir, 'images', 'icon.png')
topBar_path = os.path.join(script_dir, 'images', 'topbar.png')
dock_path = os.path.join(script_dir, 'images', 'dock.png')
delete_path = os.path.join(script_dir, 'images', 'delete.png')

# Set the application icon
try:
    icon = PhotoImage(file=icon_path)
    root.iconphoto(False, icon)
except Exception as e:
    print(f"Error loading icon: {e}")

# Setting the Top Bar
try:
    topBar = PhotoImage(file=topBar_path)
    Label(root, image=topBar).pack()
except Exception as e:
    print(f"Error loading top bar")

# Adding the dock
try:
    dock = PhotoImage(file=dock_path)
    Label(root, image=dock, bg="#77a1f2").place(x=30, y=25)
except Exception as e:
    print(f"Error loading dock")

heading = Label(root, text="To-Do", font="arial 20 bold", fg="white", bg="#77a1f2")
heading.place(x=150, y=20)

# Making the "Add" section
frame = Frame(root, width=400, height=50, bg="white")
frame.place(x=0, y=180)

task = StringVar()
task_entry = Entry(frame, width=18, font="arial 20", bd=0, textvariable=task)
task_entry.place(x=10, y=7)
task_entry.focus()

def addTask():
    new_task = task_entry.get().strip()
    if new_task:
        listbox.insert(END, new_task)  # Add the task to the Listbox
        task_list.append(new_task)  # Add to task_list
        saveTaskFile()  # Save tasks to file
        task_entry.delete(0, END)

button = Button(frame, text="Add", font="arial 20 bold", width=6, bg="#5a95ff", fg="#fff", bd=0, command=addTask)
button.place(x=300, y=0)

# Adding the list
frame1 = Frame(root, bd=3, width=700, height=280, bg="#77a1f2")
frame1.pack(pady=(160, 0))

listbox = Listbox(frame1, font=("arial", 12), width=40, height=16, bg="#77a1f2", fg="white", cursor="hand2", selectbackground="#5a95ff")
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

def saveTaskFile():
    # Save tasks to tasklist.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tasklist_path = os.path.join(script_dir, "tasklist.txt")
    with open(tasklist_path, "w") as taskfile:
        for task in listbox.get(0, END):  # Get all tasks from Listbox
            taskfile.write(task + "\n")

openTaskFile()  # Load tasks into the Listbox at startup

# Adding the delete option
def deleteTask():
    try:
        selected_task_index = listbox.curselection()[0]  # Get the index of the selected task
        listbox.delete(selected_task_index)  # Remove it from the Listbox
        saveTaskFile()  # Save updated task list to file
    except IndexError:
        pass  # No task selected, do nothing

try:
    delete = PhotoImage(file=delete_path)
    Button(root, image=delete, bd=0, command=deleteTask).pack(side=BOTTOM, pady=13)
except Exception as e:
    print(f"Error loading delete")

root.mainloop()
