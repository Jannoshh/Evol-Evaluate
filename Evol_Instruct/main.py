import json
import random

#TODO: delete this file when done since just for testing
from openai_access import call_chatgpt
from depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from breadth import createBreadthPrompt


fr = open('data/alpaca_data.json','r')

all_objs = json.load(fr)

evol_objs = []


for cur_obj in all_objs:
	
	instruction = cur_obj['instruction'].strip()
	if cur_obj['input'].strip():
		instruction += '\r\n. Here are some examples: ' + cur_obj['input'].strip()
		
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




