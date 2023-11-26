#TODO:
# - [ ] having the evaluator/eliminator marking/removing bad formatted questions ??
# - [ ] having the evaluator/eliminator marking/removing duplicates ??


import json
import tkinter as tk
from tkinter import filedialog
import os
import re
from tqdm import tqdm


from Evol_Instruct.openai_access import call_chatgpt
from Evol_Instruct.depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from Evol_Instruct.breadth import createBreadthPrompt


#### Init 
input_json = "input/survival-instinct.json" 
results_dir = 'results/desire_for_survival' #TODO(user): change this to the path of the json file you want to use as input

#1) load the json file from the input and see what was the original instruction/goal
#2) load all the json files under results_dir and get all the questions, and the DS they belong and the evolv-instruct method used to build them (if any). Then put this info in a dataframe
#3) iterate over the dataframe for all the questions and pass it to an LM with the prompt that it has to evaluate the quality of the question from 1 to 10 taking into account the original instruction/goal
#4) do some visualizations of the resulting evaluations and put the best questions in a new json file



SCORE_CONTEXT = """Evaluate the provided context and assign a numerical score between 0 and 10 based on the following criteria:
                1. Award a high score to context that thoroughly delves into and explains concepts.
                2. Assign a lower score to context that contains excessive references, acknowledgments, external links, personal information, or other non-essential elements.
                Output the score only.
                Context:
                {context}
                Score:
                """ 

human_prompt = SCORE_CONTEXT.format(context=context)
prompt = ChatPromptTemplate.from_messages([human_prompt])