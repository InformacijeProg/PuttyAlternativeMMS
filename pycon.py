import paramiko
import json
import tkinter as tk

hostname = ""
port = 22
username = ""
key_filename = "openSSHkey.pem"
command =""
data =""
listbox = None
#windowSize =(128,720)
# Load the JSON data
with open('connections.json', 'r') as json_file:
    data = json.load(json_file)

# Function to handle the "Connect" button click
def connect_button():
    selected_index = listbox.curselection()
    if selected_index:
        hostname = data['connection'][selected_index[0]]['name']
        selected_connection = data['connection'][selected_index[0]]['address']
        username = "tibcorun"
    else:
        hostname = ""
        selected_connection = ""    
# Create the main window
root = tk.Tk()
root.title("Putty alternative (SSH)")
#root.size = windowSize
# Create a listbox to display connection names
listbox = tk.Listbox(root, selectmode=tk.SINGLE)
listbox.pack()
# Populate the listbox with connection names
for connection in data['connection']:
    listbox.insert(tk.END, connection['name'])
    
# Create a "Connect" button
connect_button = tk.Button(root, text="Connect", command=connect_button)
connect_button.pack()
# Start the GUI main loop
root.mainloop()

def ssh_client(hostname, port, username, key_filename, command):
    # Create an SSH client
    client = paramiko.SSHClient()
    
    # Automatically add the server's host key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server using key-based authentication
        client.connect(hostname, port=port, username=username, key_filename=key_filename)

        # Execute the command to open the terminal (replace with the appropriate command for your server)
        open_terminal_command = 'gnome-terminal'  # Change this based on your server's terminal emulator
        stdin, stdout, stderr = client.exec_command(f'{open_terminal_command} -e "{command}"')

        # Print the command output
        print("Command Output:")
        print(stdout.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SSH connection
        client.close()


# Call the function
ssh_client(hostname, port, username, key_filename, command)
