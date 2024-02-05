import json
import subprocess
import os
# Global variables
privateKeyPath = "openSSHkey.pem"
User = "tibcorun"

def read_json_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {filename} contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def get_connection_data():
    connections = read_json_file("connections.json")
    if connections is None or 'connection' not in connections or not connections['connection']:
        return None
    
    return connections['connection']

def select_connection(connections):
    for i, connection in enumerate(connections, start=1):
        print(f"{i}.) {connection.get('name', 'Unknown')}")
    
    while True:
        selection = input("Choose connection number or 'q' to quit: ").strip()
        if selection.lower() == 'q':
            quit()
        if selection.isdigit() and 1 <= int(selection) <= len(connections):
            return connections[int(selection) - 1]
        else:
            print("Invalid selection, please try again.")

def main():
    connections = get_connection_data()
    if not connections:
        print("No connection data available. Please check the JSON file.")
        return

    selected_connection = select_connection(connections)
    host = selected_connection.get("address")
    port = selected_connection.get("port")
    user = selected_connection.get("user", "tibcorun")  # Use the provided default username if not specified in JSON
    sshKeypass = selected_connection.get("sshKeypass", "")  # Assuming your JSON has the sshKeypass field

    # Construct the SSH command
    ssh_command = f"putty -ssh {user}@{host} -P {port}"

    # Open a new Putty window and execute the SSH command
    try:
        os.system(ssh_command)
    except FileNotFoundError:
        print("It seems like there is a problem with Putty or SSH is not installed.")

if __name__ == "__main__":
    main()