"""
This script goes over all the questions created by evolv-instruct and checks if they are okay. 
If they are not, it deletes them. The criteria for deletion are:
- If '#The Given Prompt#' or '#Rewritten Prompt#' appears in the question
- If the question does not include choices
"""

import json
import os
import re

results_dir = 'results/desire_for_survival' #TODO(user): change this to the path of the json file you want to use as input

def should_delete_question(question):
    if "#The Given Prompt#" in question or "#Rewritten Prompt#" in question:
        return True
    if not re.search("choice", question, re.IGNORECASE):
        return True
    return False

def process_files():
    files_to_process = [f for f in os.listdir(results_dir) if f.startswith(('DS1_', 'DS2_'))]

    for file in files_to_process:
        file_path = os.path.join(results_dir, file)

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        
        first_category = list(data.keys())[0]
        questions = data[first_category]

        data[first_category] = [q for q in questions if not should_delete_question(q['question'])]

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

process_files()
