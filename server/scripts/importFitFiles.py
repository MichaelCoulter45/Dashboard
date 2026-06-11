import os
import glob
import fitdecode
import warnings
import json
from datetime import datetime


# Suppress UserWarnings specifically coming from the fitdecode reader
warnings.filterwarnings("ignore", category=UserWarning, module="fitdecode")



## Input
# Target path for all the .fit files
FIT_PATH = './Dashboard/data/fitness-data/fit'
# Find all the .fit files in the path
FIT_FILES = glob.glob(os.path.join(FIT_PATH, "*.fit"))


## Output
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# OUTPUT_JSON_PATH = f'./Dashboard/data/fitness-data/normalized_data/monster_list_{timestamp}.json'
# OUTPUT_JSON_SUMMARY_PATH = f'./Dashboard/data/fitness-data/normalized_data/summary_list_{timestamp}.json'
OUTPUT_JSON_PATH = f'./Dashboard/data/fitness-data/normalized_data/monster_list.json'
OUTPUT_JSON_SUMMARY_PATH = f'./Dashboard/data/fitness-data/normalized_data/summary_list.json'
all_activities_data = [] # Monster list to host all data
summaries_data = []


# Data we want to save:
FIT_DATA = [
    'activityID',
    'date',
    'activityType',
    'distance',
    'duration',
    'elevationGain',
    'elevationLoss',
    'trainingLoad',
    'calories',
    'totalTime',
    'verticalSpeed',
    'groundTime',
    'strideRatio',
    'strideHeight',
]
AVG_DATA = [
    'avgHeartRate',
    'avgCadence',
    'avgPower',
    'avgSpeed',
    'avgPace',
    'avgStrideLength',
]
MAX_DATA = [
    'maxHeartRate',
    'maxCadence',
    'maxPower',
    'maxSpeed',
    'maxPace',
]





def save_monster_list():
    # Ensure output directory exists before saving
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    # Save the monster list to a single JSON file
    print(f"\nSaving to Monster List..")
    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(all_activities_data, json_file, indent=4, default=str)
    print(f"Successfully saved all data to: '{OUTPUT_JSON_PATH}'")


def save_summaries_list():
    # Ensure output directory exists before saving
    os.makedirs(os.path.dirname(OUTPUT_JSON_SUMMARY_PATH), exist_ok=True)
    # Save the summaries list to a single JSON file
    print(f"\nSaving to Summary List..")
    with open(OUTPUT_JSON_SUMMARY_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(summaries_data, json_file, indent=4, default=str)
    print(f"Successfully saved all data to: '{OUTPUT_JSON_SUMMARY_PATH}'")






def main():
    print(f"Found {len(FIT_FILES)} .fit files to process.\n")
    
    for index, file_path in enumerate(FIT_FILES, start=1):
        file_name = os.path.basename(file_path)
        print(f"[{index}/{len(FIT_FILES)}] | Processing: '{file_name}'")
        
        # Initialize dictionaries to separate record daata from summary data
        activity_entry = {
            "file_name": file_name,
            "summaries": [],
            "trackpoints": [],
            "activity": [],
            "lap": []
        }
        
        # Open and stream the binary .fit file
        with fitdecode.FitReader(file_path) as fit:
            for frame in fit:
                # Filter frames to only get actual data messages
                if isinstance(frame, fitdecode.records.FitDataMessage):
                    
                    ## Extract everything in this frame
                    frame_data = {field.name: field.value for field in frame.fields}
                    
                    # Option 1: Capture moment-by-moment tracking metrics
                    if frame.name == 'record':
                        activity_entry["trackpoints"].append(frame_data)
                    
                    ## Option 2: Capture overarching totals, maxes, and averages
                    elif frame.name == 'session':
                        # Adds the message type name into the dictionary for clarity
                        frame_data["message_type"] = frame.name
                        # Save the summary data to the current active entry
                        activity_entry['summaries'].append(frame_data)
                    
            # Append this completed file's data to the monster list
            all_activities_data.append(activity_entry)
            # Create a seperate list with just the summaries
            summaries_data.append({
                "file_name": file_name,
                "summaries": activity_entry['summaries']
                })
            
    save_monster_list()
    save_summaries_list()





if __name__ == "__main__":
    main()


