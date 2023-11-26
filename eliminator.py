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
results_dir = 'results/Awareness of Being an AI' #TODO(user): change this to the path of the json file you want to use as input


#1) Go over all the questions created by evolv-instruct and check if they are okay and if not delete them. 
# Possible criteria to delete:
# - [ ] if #The Given Prompt# or #Rewritten Prompt# appears on the question
# - [ ] if the question does not include choices