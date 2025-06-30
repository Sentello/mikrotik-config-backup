import paramiko
import json
import os
from datetime import datetime

# Configuration file for Mikrotik devices
DEVICES_FILE = 'mikrotik_devices.json'
# Directory to save backups
BACKUP_DIR = 'backups'

def create_backup_dir():
    """Creates the backup directory if it doesn't exist."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")

def load_devices(file_path):
    """Loads Mikrotik device credentials from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Devices file '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'. Check file format.")
        return []

def backup_mikrotik_config(device):
    """Connects to a Mikrotik device and downloads its configuration."""
    name = device.get('name', 'unknown_device')
    host = device.get('host')
    username = device.get('username')
    password = device.get('password')

    if not all([host, username, password]):
        print(f"Skipping device '{name}': Missing host, username, or password.")
        return

    print(f"Attempting to connect to {name} ({host})...")
    client = paramiko.SSHClient()
    try:
        client.load_system_host_keys()
    except Exception as e:
        print(f"Warning: Could not load system host keys: {e}")
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    try:
        client.connect(hostname=host, username=username, password=password, port=22, timeout=30, look_for_keys=False, allow_agent=False)
        print(f"Successfully connected to {name}.")

        # Execute the export command
        stdin, stdout, stderr = client.exec_command('/export')
        config_output = stdout.read().decode('utf-8')
        error_output = stderr.read().decode('utf-8')

        if error_output:
            print(f"""Error during export on {name}:
{error_output}""")
            return

        # Save the configuration to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = os.path.join(BACKUP_DIR, f"{name}_config_{timestamp}.rsc")

        with open(backup_filename, 'w') as f:
            f.write(config_output)
        print(f"Backup for {name} saved to {backup_filename}")

    except paramiko.AuthenticationException:
        print(f"Authentication failed for {name} ({host}). Check username and password.")
    except paramiko.SSHException as e:
        print(f"SSH error connecting to {name} ({host}): {e}")
    except Exception as e:
        print(f"An unexpected error occurred while connecting to {name} ({host}): {e}")
    finally:
        if client:
            client.close()

def main():
    create_backup_dir()
    devices = load_devices(DEVICES_FILE)
    if not devices:
        print("No devices to backup. Please populate mikrotik_devices.json.")
        return

    for device in devices:
        backup_mikrotik_config(device)

if __name__ == "__main__":
    main()
