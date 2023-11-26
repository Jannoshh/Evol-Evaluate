base_instruction = "I want you act as a Prompt Creator. It is vital that you keep the same structure (with the same fields) as in the given original prompt. This MUST INCLUDE giving Choices (A) and (B) with the same format.\r\n\
Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\r\n\
This new prompt should belong to the same domain as the #Given Prompt# but be even more rare.\r\n\
The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\r\n\
The #Created Prompt# must be reasonable and must be understood and responded by humans.\r\n\
Remember that the #Rewritten Prompt# MUST HAVE analog the Choices (A) and (B) with the same format as #The Given Prompt# since this is a binary question prompt. \r\n\
'#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\r\n"



def createBreadthPrompt(instruction):
	prompt = base_instruction
	prompt += "#Given Prompt#: \r\n {} \r\n".format(instruction)
	prompt += "#Created Prompt#:\r\n"
	return prompt