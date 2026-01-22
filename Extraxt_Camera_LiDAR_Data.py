import json
import os
import pandas as pd

# Define the path of the JSON file
json_file_path = r"D:\3. Code\Sumo Network\1.My_Code\dddd\joined_sensor.json"

# Ensure the file exists
if not os.path.exists(json_file_path):
    print(f"Error: The file {json_file_path} does not exist.")
else:
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            print("Successfully loaded JSON file.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            data = None
    
    # Function to extract camera sensor transformation data recursively
    def extract_sensor_transformation(json_data):
        extracted_data = []
        
        def recursive_extract(obj):
            if isinstance(obj, dict):
                if "recording_timestamp_nsec" in obj and "frame_id" in obj and "translation" in obj and "rotation" in obj and "child_frame_id" in obj:
                    extracted_data.append({
                        "Timestamp (nsec)": obj.get("recording_timestamp_nsec"),
                        "Frame ID": obj.get("frame_id"),
                        "Translation X": obj.get("translation", {}).get("x", "N/A"),
                        "Translation Y": obj.get("translation", {}).get("y", "N/A"),
                        "Translation Z": obj.get("translation", {}).get("z", "N/A"),
                        "Rotation X": obj.get("rotation", {}).get("x", "N/A"),
                        "Rotation Y": obj.get("rotation", {}).get("y", "N/A"),
                        "Rotation Z": obj.get("rotation", {}).get("z", "N/A"),
                        "Rotation W": obj.get("rotation", {}).get("w", "N/A"),
                        "Child Frame ID": obj.get("child_frame_id")
                    })
                for key, value in obj.items():
                    recursive_extract(value)
            elif isinstance(obj, list):
                for item in obj:
                    recursive_extract(item)
        
        recursive_extract(json_data)
        return extracted_data
    
    if data:
        extracted_sensor_data = extract_sensor_transformation(data)
        
        if extracted_sensor_data:
            # Convert extracted data into a Pandas DataFrame for structured use
            df = pd.DataFrame(extracted_sensor_data)
            
            # Save extracted data to CSV for easy future integration with V2X messages
            extracted_data_path = r"D:\3. Code\Sumo Network\1.My_Code\dddd\extracted_sensor_data.csv"
            df.to_csv(extracted_data_path, index=False)
            
            print(f"Extracted sensor transformation data saved at: {extracted_data_path}")
        else:
            print("No sensor transformation data found in the JSON file.")
    else:
        print("No valid data extracted from JSON file.")
