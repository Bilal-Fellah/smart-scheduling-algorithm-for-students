# this file does: transform files to the format used in the fixed ga
#  {
#     "id": 21,
#     "title": "Morning Jog",
#     "priority": "medium",
#     "deadline": "2025-05-06T07:30:00",
#     "duration": 30,
#     "is_scheduled": false,
#     "category": "Health",
#     "to_reschedule": false,
#     "is_synched": true,
#     "status": "To Do",
#     "user": "test@gmail.com"
#   }

#  TO

    # {"id": "T1", "duration": 6, "category": 'School', "priority": 1},
    

from datetime import datetime 
import pandas as pd

sessions = pd.read_json('data/G7/db sample/db sample/sessions.json')



def format_to_schedule_tasks_and_save(input_path, output_path):
    tasks_to_schedule = pd.read_json(input_path)
    mapping = {
        "low": 1,
        "medium": 2,
        "high": 3
    }
    formatted_tasks = tasks_to_schedule
    formatted_tasks["priority"] = tasks_to_schedule["priority"].map(mapping)
    formatted_tasks["duration"] =( tasks_to_schedule["duration"]/5).astype(int)
    print(formatted_tasks["duration"].head())

    formatted_tasks.to_json(output_path, orient='records')
    
input_path = "data/G7/db sample/tasks_to_schedule.json"
output_path = 'data/G7/db sample/formatted_tasks_to_schedule.json'

format_to_schedule_tasks_and_save(input_path, output_path)



def format_fixed_tasks_and_save(input_path, output_path, sessions):
    tasks_to_schedule = pd.read_json(input_path)

    
    mapping = {"low": 1, "medium": 2, "high": 3}
    tasks_to_schedule["priority"] = tasks_to_schedule["priority"].map(mapping)
    tasks_to_schedule["duration"] = (tasks_to_schedule["duration"] / 5).astype(int)
    tasks_to_schedule["start"] = None

    # Iterate through tasks and compute start times
    for idx, row in tasks_to_schedule.iterrows():
        task_id = row["id"]

        # Get the start datetime from sessions
        session_row = sessions[sessions["task_id"] == task_id]
        if session_row.empty:
            continue  # skip if no session found for this task

        datetime_str = session_row.iloc[0]["start_time"]
        datetime_obj =datetime_str
        

        # Calculate minutes from 8:00 AM and convert to 5-minute blocks
        start_minutes = (datetime_obj.hour * 60 + datetime_obj.minute) - 8 * 60
        start_block = start_minutes // 5

        tasks_to_schedule.at[idx, "start"] = start_block

    # Save the formatted tasks to a new JSON file
    tasks_to_schedule.to_json(output_path, orient='records', indent=2)

# Example usage
input_path = "data/G7/db sample/fixed_tasks.json"
output_path = "data/G7/db sample/formatted_fixed_tasks.json"

# Assuming you have sessions already loaded:
# sessions = pd.read_json("data/G7/db sample/sessions.json")
format_fixed_tasks_and_save(input_path, output_path, sessions)