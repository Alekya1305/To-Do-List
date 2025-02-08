import tkinter as tk
from tkinter import messagebox
import json
import os
import time

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from file (if exists)
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Display all pending tasks in the listbox
def show_pending_tasks():
    task_listbox.delete(0, tk.END)
    tasks = load_tasks()
    pending_tasks = [task for task in tasks if not task['done']]  # Filter out done tasks
    if pending_tasks:
        for idx, task in enumerate(pending_tasks, 1):
            task_listbox.insert(tk.END, f"{idx}. {task['task']} - Pending")
    else:
        task_listbox.insert(tk.END, "No pending tasks.")

# Add a new task
def add_task():
    task_name = task_entry.get()
    if task_name:
        tasks = load_tasks()
        task = {"task": task_name, "done": False}
        tasks.append(task)
        save_tasks(tasks)
        task_entry.delete(0, tk.END)
        show_pending_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Mark a task as done
def mark_done():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_num = selected_task[0]
        tasks = load_tasks()
        tasks[task_num]["done"] = True
        save_tasks(tasks)
        show_pending_tasks()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

# Update a task
def update_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_num = selected_task[0]
        new_task = task_entry.get()
        if new_task:
            tasks = load_tasks()
            tasks[task_num]["task"] = new_task
            save_tasks(tasks)
            task_entry.delete(0, tk.END)
            show_pending_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a new task description.")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to update.")

# Delete a task
def delete_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_num = selected_task[0]
        tasks = load_tasks()
        deleted_task = tasks.pop(task_num)
        save_tasks(tasks)
        show_pending_tasks()
        messagebox.showinfo("Success", f"Task '{deleted_task['task']}' deleted.")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Exit the application
def exit_app():
    root.quit()

# Function to update the clock
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)  # Update the clock every 1 second

# Set up the main application window
root = tk.Tk()
root.title("To-Do List Application")

# Set the background color and title font
root.configure(bg="#F1F1F1")

# Customizing font
font = ("Helvetica", 12)
heading_font = ("Helvetica", 16, "bold")

# Create a frame for the title
title_frame = tk.Frame(root, bg="#F1F1F1")
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="To-Do List", font=heading_font, bg="#F1F1F1", fg="#333")
title_label.pack()

# Create a frame for the task entry and buttons
frame = tk.Frame(root, bg="#F1F1F1")
frame.pack(pady=10)

# Task input entry field with padding and rounded edges
task_entry_frame = tk.Frame(frame, bg="#F1F1F1")
task_entry_frame.grid(row=0, column=0, padx=10, pady=5)  # Add padding to the frame

task_entry = tk.Entry(task_entry_frame, width=40, font=font, bd=2, relief="groove")
task_entry.pack(padx=10, pady=5)  # Add padding inside the entry

# Add task button with custom color
add_button = tk.Button(frame, text="Add Task", width=15, font=font, bg="#4CAF50", fg="white", relief="raised", command=add_task)
add_button.grid(row=0, column=1, padx=5, pady=5)

# Create the listbox to display tasks
task_listbox = tk.Listbox(root, width=50, height=10, font=font, selectmode=tk.SINGLE, bg="#E8F5E9", bd=2, relief="sunken")
task_listbox.pack(pady=10)

# Buttons to manage tasks
buttons_frame = tk.Frame(root, bg="#F1F1F1")
buttons_frame.pack(pady=5)

mark_done_button = tk.Button(buttons_frame, text="Mark as Done", width=15, font=font, bg="#8BC34A", fg="white", relief="raised", command=mark_done)
mark_done_button.grid(row=0, column=0, padx=5, pady=5)

update_button = tk.Button(buttons_frame, text="Update Task", width=15, font=font, bg="#FFC107", fg="white", relief="raised", command=update_task)
update_button.grid(row=0, column=1, padx=5, pady=5)

delete_button = tk.Button(buttons_frame, text="Delete Task", width=15, font=font, bg="#FF5722", fg="white", relief="raised", command=delete_task)
delete_button.grid(row=0, column=2, padx=5, pady=5)

# View Pending Tasks button with custom color
view_tasks_button = tk.Button(root, text="View Pending Tasks", width=20, font=font, bg="#2196F3", fg="white", relief="raised", command=show_pending_tasks)
view_tasks_button.pack(pady=5)

# Exit button with a distinct color
exit_button = tk.Button(root, text="Exit", width=15, font=font, bg="#F44336", fg="white", relief="raised", command=exit_app)
exit_button.pack(pady=10)

# Create and display the clock label
clock_label = tk.Label(root, font=("Helvetica", 20), fg="black", bg="#F1F1F1")
clock_label.pack(pady=10)

# Start updating the clock
update_clock()

# Show the current list of tasks (pending)
show_pending_tasks()

# Run the Tkinter event loop
root.mainloop()