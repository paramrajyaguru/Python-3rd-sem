import json
import os

# --- METHOD 3 MAGIC: Automatically find the folder this script is in ---
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "logs.json")
# ----------------------------------------------------------------------

try:
    # We use the dynamic file_path here instead of just "logs.json"
    with open(file_path, "r") as file:
        data = json.load(file)
        
    if not isinstance(data, list):
        raise ValueError("Invalid JSON data: Expected a list of logs.")
        
    info_count = 0
    warning_count = 0
    error_count = 0
    
    print("\n----- ALL LOG RECORDS -----")
    
    for log in data:
        if not isinstance(log, dict):
            print("Invalid log record:", log)
            continue
            
        timestamp = log.get("timestamp", "N/A")
        level = log.get("level", "N/A")
        message = log.get("message", "N/A")
        
        print("Timestamp:", timestamp)
        print("Level:", level)
        print("Message:", message)
        print("--------------------------")
        
        level = str(level).upper()
        
        if level == "INFO":
            info_count += 1
        elif level == "WARNING":
            warning_count += 1
        elif level == "ERROR":
            error_count += 1
            
    print("\n----- LOG SUMMARY -----")
    print("Total INFO messages:", info_count)
    print("Total WARNING messages:", warning_count)
    print("Total ERROR messages:", error_count)
    print("Total log records:", len(data))
    
except FileNotFoundError:
    print(f"Error: The file was not found at {file_path}")
except json.JSONDecodeError:
    print("Error: Invalid JSON data in logs.json.")
except ValueError as e:
    print(e)