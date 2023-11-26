import os
from openai import OpenAI
import time
import requests

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")



def get_oai_completion(prompt):

    try: 
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                
                ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.6,
            presence_penalty=0.6,
            stop=None
            )
        res = response.choices[0].message.content
        gpt_output = res
        return gpt_output
    except Exception as e: #TODO: all these exceptions have not been tested so they should be tested
        error_message = str(e)

        if "Invalid request error" in error_message:
            print(f"The OpenAI API request was invalid: {e}")
            return None

        elif "API connection error" in error_message:
            print(f"Network error connecting to the OpenAI API: {e}")
            return None

        elif "The operation was timeout" in error_message:
            print("The OpenAI API request timed out. Please try again later.")
            return get_oai_completion(prompt)            

        elif "Rate limit error" in error_message:
            print(f"Rate limit exceeded: {e}")
            return get_oai_completion(prompt)

        elif "Authentication error" in error_message:
            print(f"Authentication with OpenAI API failed: {e}")
            return None

        else:
            print(f"An error occurred with the OpenAI API: {e}")
            return None

def call_chatgpt(ins):
    success = False
    re_try_count = 15
    ans = ''
    while not success and re_try_count >= 0:
        re_try_count -= 1
        try:
            ans = get_oai_completion(ins)
            success = True
        except:
            time.sleep(5)
            print('retry for sample:', ins)
    return ans