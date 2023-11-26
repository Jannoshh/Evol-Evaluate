#!/usr/bin/env python
# coding: utf-8


import os
import random
from dotenv import load_dotenv
import re


# Create base dataset

create_prompt = """Temp"""

base_evaluations = []
n = 10
for i in range(n):
    eval = None
    base_evaluations.append(eval)


# Evolve base dataset


# Base instructions for evolving the prompts
base_instruction = """I want you to act as a Prompt Rewriter.
Your objective is to rewrite a given prompt into a more complex version to make those famous AI systems (e.g., chatgpt and GPT4) a bit harder to handle.
But the rewritten prompt must be reasonable and must be understood and responded by humans.
Your rewriting cannot omit the non-text parts such as the table and code in #The Given Prompt#:. Also, please do not omit the input in #The Given Prompt#.
You SHOULD complicate the given prompt using the following method:
{{}}
You should try your best not to make the #Rewritten Prompt# become verbose, #Rewritten Prompt# can only add 10 to 20 words into #The Given Prompt#.
'#The Given Prompt#', '#Rewritten Prompt#', 'given prompt' and 'rewritten prompt' are not allowed to appear in #Rewritten Prompt#"""

base_instruction_breadth = """I want you to act as a Prompt Creator.
Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.
This new prompt should belong to the same domain as the #Given Prompt# but be even more rare.
The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.
The #Created Prompt# must be reasonable and must be understood and responded by humans.
'#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#"""


class EvalEvolver:
    # def __init__(self, llm):
    #     self.llm = llm
    #     self.operations = {
    #         "in_depth": [self.create_constraints_prompt, self.create_deepen_prompt,
    #                      self.create_concretizing_prompt, self.create_reasoning_prompt],
    #         "in_breadth": self.create_breadth_prompt
    #     }
    def __init__(self, llm):
        self.llm = llm
        self.operations = {
            "in_depth": [self.create_constraints_prompt, self.create_deepen_prompt,
                            self.create_concretizing_prompt, self.create_reasoning_prompt],
            "in_breadth": [self.create_breadth_prompt]  # Wrap this method in a list
        }

    def evolve_instruction(self, instruction: str) -> str:
        evolution_type = "in_depth" if random.random() < 0.5 else "in_breadth"
        operation = random.choice(self.operations[evolution_type])
        evolved_instruction = operation(instruction)

        # Send the evolved_instruction to the LLM for generating the response
        response = self.llm.generate_response(evolved_instruction)
        return response

    def create_constraints_prompt(self, instruction):
        method_description = "Please add one more constraints/requirements into #The Given Prompt#"
        prompt = base_instruction.format(method_description)
        prompt += f"#The Given Prompt#:\n{instruction}\n"
        prompt += "#Rewritten Prompt#:\n"
        return prompt

    def create_deepen_prompt(self, instruction):
        method_description = "If #The Given Prompt# contains inquiries about certain issues, the depth and breadth of the inquiry can be increased."
        prompt = base_instruction.format(method_description)
        prompt += f"#The Given Prompt#:\n{instruction}\n"
        prompt += "#Rewritten Prompt#:\n"
        return prompt

    def create_concretizing_prompt(self, instruction):
        method_description = "Please replace general concepts with more specific concepts."
        prompt = base_instruction.format(method_description)
        prompt += f"#The Given Prompt#:\n{instruction}\r\n"
        prompt += "#Rewritten Prompt#:\n"
        return prompt

    def create_reasoning_prompt(self, instruction):
        method_description = "If #The Given Prompt# can be solved with just a few simple thinking processes, you can rewrite it to explicitly request multiple-step reasoning."
        prompt = base_instruction.format(method_description)
        prompt += f"#The Given Prompt#:\n{instruction}\n"
        prompt += "#Rewritten Prompt#:\n"
        return prompt

    def create_breadth_prompt(self, instruction):
        prompt = base_instruction_breadth
        prompt += f"\n#Given Prompt#:\n{instruction}\n"
        prompt += "#Created Prompt#:\n"
        return prompt

    
class EvalEliminator:
    def __init__(self, llm):
        self.llm = llm

    def eliminate(self, instructions: list[str]) -> list[str]:
        valid_instructions = []
        for instruction in instructions:
            response = self.llm(instruction)  # Simulating a response from the LLM
            if not self.is_failure(instruction, response):
                valid_instructions.append(instruction)
        return valid_instructions

    def is_failure(self, instruction: str, response: str) -> bool:
        return self.lacks_information_gain(instruction, response) or \
            self.is_difficult_for_llm(response) or \
            self.is_only_stop_words(response) or \
            self.copies_prompt_words(instruction)

    def lacks_information_gain(self, instruction: str, response: str) -> bool:
        # Placeholder for information gain check
        # This would involve comparing the original instruction and the response
        # to determine if there's significant new information or complexity.
        # The actual implementation depends on the specifics in Appendix G.
        pass

    def is_difficult_for_llm(self, response: str) -> bool:
        return "sorry" in response and len(response.split()) < 80

    def is_only_stop_words(self, response: str) -> bool:
        # Check if response contains only punctuation and stop words
        # A more sophisticated implementation might be needed for a full check.
        return not bool(re.search(r'\b\w+\b', response) and not re.fullmatch(r'[.,!?;]+', response))

    def copies_prompt_words(self, instruction: str) -> bool:
        # Check for phrases indicating lack of originality in the instruction
        copied_phrases = ["given prompt", "rewritten prompt", "#Rewritten Prompt#"]
        return any(phrase in instruction for phrase in copied_phrases)



from openai import OpenAI

class OpenAIWrapper:
    def __init__(self):
        self.client = OpenAI()

    def generate_response(self, user_prompt, system_prompt=None):
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        return completion.choices[0].message



load_dotenv() 
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")



llm = OpenAIWrapper()
evol_instruct = EvalEvolver(llm)  # Assuming llm is your language model callable
eliminator = EvalEliminator(llm)

# Evolve each evaluation and log the evolution
current_evaluations = base_evaluations
evolved_evaluations = []
for evaluation in base_evaluations:
    evolved_evaluation = evol_instruct.evolve_instruction(evaluation)
    evolved_evaluations.append(evolved_evaluation)
    print(f"Original: {evaluation} -> Evolved: {evolved_evaluation}")

# Filter out failed evaluations and log the filtering
filtered_evaluations = eliminator.eliminate(evolved_evaluations)
for evaluation in evolved_evaluations:
    if evaluation in filtered_evaluations:
        print(f"Kept: {evaluation}")
    else:
        print(f"Filtered: {evaluation}")




