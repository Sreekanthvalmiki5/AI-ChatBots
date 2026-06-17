from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv(override=True)
import gradio as gr
from models import get_openrouter_model

class Day3:
    def __init__(self):
        self.name="Day 3"
        self.router=get_openrouter_model()
    
    def chat(self,message,history):
        history=[{"role":h["role"],"content":h["content"]} for h in history]
        system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage \
the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. \
For example, if the customer says 'I'm looking to buy a hat', \
you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.'\
Encourage the customer to buy hats if they are unsure what to get"
        messages=[{"role":"system","content":system_message}] +history +[{"role":"user","content":message}]
        response=self.router.chat.completions.create(model="gpt-oss-20b",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content
        yield result
    def chat_interface(self):
        gr.ChatInterface(fn=self.chat).launch()
        
        
if __name__=="__main__":
    day3=Day3()
    day3.chat_interface()
        


