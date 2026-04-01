# Mikrotik Config Backup Tool

A simple Python script that connects to Mikrotik routers via SSH and backs up their configurations using the `/export` command. Useful for network admins who want to automate configuration backups from multiple Mikrotik devices.

## 🔧 Features

- Connects via SSH using `paramiko`
- Automatically detects RouterOS version (v6 or v7) to ensure sensitive data (passwords, keys) are included in the export
- Automatically creates a `backups/` directory
- Timestamps each backup file
- Reads devices from a JSON config
- Handles errors and connection issues gracefully

## 📦 Requirements

- Python 3.x
- `paramiko` library (`pip install paramiko`)

## 📁 File Structure

- `backup_mikrotik.py` - Main script to run the backup
- `mikrotik_devices.json` - List of Mikrotik devices with credentials
- `backups/` - Destination folder for all backup `.rsc` files

## 📝 Device Configuration Example

Create a file named `mikrotik_devices.json` in the same directory with the following content:

```json
[
    {
        "name": "OfficeRouter",
        "host": "192.168.88.1",
        "username": "admin",
        "password": "yourpassword"
    },
    {
        "name": "BackupRouter",
        "host": "192.168.88.2",
        "username": "admin",
        "password": "yourpassword"
    }
]
