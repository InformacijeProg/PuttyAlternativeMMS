import tkinter as tk
import subprocess
import json

# Load the JSON data
with open('connections.json', 'r') as json_file:
    data = json.load(json_file)

# Function to establish SSH connection
def connect_ssh(address, port):
    ssh_command = f'ssh -i openSSHkey.pem -p {port} tibcorun@{address}'
    subprocess.run(ssh_command, shell=True)

# Create the main window
root = tk.Tk()
root.title("Rockin' SSH Connection Manager")

# Create a listbox to display connection names
listbox = tk.Listbox(root, selectmode=tk.SINGLE)
listbox.pack()

# Populate the listbox with connection names
for connection in data['connection']:
    listbox.insert(tk.END, connection['name'])

# Function to handle the "Connect" button click
def connect_button():
    selected_index = listbox.curselection()
    if selected_index:
        selected_connection = data['connection'][selected_index[0]]
        connect_ssh(selected_connection['address'], selected_connection['port'])

# Create a "Connect" button
connect_button = tk.Button(root, text="Connect", command=connect_button)
connect_button.pack()

# Start the GUI main loop
root.mainloop()
