import json
import random
import tkinter as tk
from tkinter import filedialog
import os

from Evol_Instruct.openai_access import call_chatgpt
from Evol_Instruct.depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from Evol_Instruct.breadth import createBreadthPrompt

input_json = "input/awareness.json" #TODO(user): change this to the path of the json file you want to use as input

def select_json_file():
	root = tk.Tk()
	root.withdraw()  # Hide the main window
	file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), 'input'), filetypes=[("Json files", "*.json")])
	return file_path

if not input_json:
	input_json = select_json_file()

with open(input_json, 'r') as file:
    data = json.load(file)

# Assign data to variables
title = data['title']
desired_size_dataset = data['desired_size_dataset']
instruction = data['instruction']
few_shots = data['few_shots']


if not few_shots:
    raise ValueError("Error: There should be at least 1 example shot to know the exact format that the output should have.")

# Creating datasets DS1 and DS2
DS1 = []
DS2 = []

test_extra_instruction = " Please be very creative with your answer."
instruction += test_extra_instruction

instruction_prompt_DS1 = instruction + "\nUse the same format as in this example:\n" + str(few_shots[0]) 
examples_few_shots = "\n".join(str(shot) for shot in few_shots)
instruction_prompt_DS2 = instruction_prompt_DS1 +  ".\n\n Please see these examples here to get an idea of what we are looking for:\n" + examples_few_shots

for _ in range(desired_size_dataset):
    # Dataset DS1: using only the instruction
    new_entry_DS1 = call_chatgpt(instruction_prompt_DS1)
    DS1.append(new_entry_DS1)

    # Dataset DS2: using the instruction and the examples for few shot prompting
    new_entry_DS2 = call_chatgpt(instruction_prompt_DS2)
    DS2.append(new_entry_DS2)


# Ensure 'results' directory exists
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)

# Ensure directory for 'title' exists
title_dir = os.path.join(results_dir, title)
os.makedirs(title_dir, exist_ok=True)

# Dump DS1 and DS2 as JSON files
with open(os.path.join(title_dir, 'DS1.json'), 'w') as f:
	json.dump(DS1, f)

with open(os.path.join(title_dir, 'DS2.json'), 'w') as f:
	json.dump(DS2, f)
evol_objs = []


for cur_obj in all_objs:
	
	instruction = cur_obj['instruction'].strip() + '\r\n'+ cur_obj['input'].strip()

	evol_prompts = []
	evol_prompts.append(createConstraintsPrompt(instruction))
	evol_prompts.append(createDeepenPrompt(instruction))
	evol_prompts.append(createConcretizingPrompt(instruction))
	evol_prompts.append(createReasoningPrompt(instruction))
	evol_prompts.append(createBreadthPrompt(instruction))

	selected_evol_prompt = random.choice(evol_prompts)


	evol_instruction = call_chatgpt(selected_evol_prompt)
	answer = call_chatgpt(evol_instruction)

	evol_objs.append({"instruction":evol_instruction,"output":answer})



with open('TEST_alpaca_data_evol.json', 'w') as f:	
	json.dump(evol_objs, f, indent=4)




