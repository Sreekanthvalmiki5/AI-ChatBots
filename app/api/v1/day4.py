from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv(override=True)
import gradio as gr
from models import get_openrouter_model
import json
import sqlite3

class Day4:
    def __init__(self):
        self.name="Day 3"
        self.router=get_openrouter_model()
        self.ticket_prices={"india":"$500","paris":"$900","russia":"$1200","isrel":"$1799"}
        self.price_function={
            "name":"get_ticket_price",
            "description":"Get the Price of the Return ticket to destionation city",
            "parameters":{
                "type":"object",
                "properties":{
                    "destination_city":{
                        "type":"string",
                        "description":"the city of customer want to travel to"
                    }
                }
                ,
                "required":"destination_city",
                "additional_properties":False
            }
        }
        self.tools=[{"type":"function","function":self.price_function}]
        self.DB="prices.db"
        self.get_db()
        self.insert_prices()
    
    def chat(self,message,history):
        history=[{"role":h["role"],"content":h["content"]} for h in history]
        system_message = """"
        You are a helpful assistant for an Airline called FlightAI.
        Give short, courteous answers, no more than 1 sentence.
        Always be accurate. If you don't know the answer, say so.
        """
        messages=[{"role":"system","content":system_message}] +history +[{"role":"user","content":message}]
        response=self.router.chat.completions.create(model="gpt-oss-20b",messages=messages,tools=self.tools)
        print(response.choices[0])
        if response.choices[0].finish_reason=="tool_calls":
            message=response.choices[0].message
            response=self.handle_tool_call(message)
            messages.append(message)
            messages.append(response)
            responses=self.router.chat.completions.create(model="gpt-oss-20b",messages=messages)
            return responses.choices[0].message.content
        return response.choices[0].message.content
    def handle_tool_call(self,message):
        tool_call=message.tool_calls[0]
        if tool_call.function.name=="get_ticket_price":
            arguments=json.loads(tool_call.function.arguments)
            city=arguments.get('destination_city')
            price_details=self.get_ticket_price(city)
            response={
                "role":"tool",
                "content":price_details,
                "tool_call_id":tool_call.id
            }
            return response
        
            
    def chat_interface(self):
        gr.ChatInterface(fn=self.chat).launch()
    def get_ticket_price(self,destination_city):
        with sqlite3.connect(self.DB) as conn:
            cursor=conn.cursor()
            cursor.execute('SELECT price from prices WHERE city =?',(destination_city.lower(),))
            result=cursor.fetchone()
            return f"Ticket Price to {destination_city}is ${result[0]}" if result else "No prices data available for this city"
        # print(f"tool called from the city{destination_city}")
        # price=self.ticket_prices.get(destination_city.lower(),"Unkown ticket price")
        # return f"The price of the ticket to {destination_city} is {price}"
    
    
    
    def get_db(self):
        with sqlite3.connect(self.DB) as conn:
            cursor= conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS prices(city Text PRIMARY KEY,price REAL)")
            conn.commit()
    def set_ticket_prices(self,city,price):
        with sqlite3.connect(self.DB) as conn:
            cursor=conn.cursor()
            cursor.execute('INSERT INTO prices(city,price) VALUES(?,?) ON CONFLICT(city) DO UPDATE SET price=?',(city.lower(),price,price))
            conn.commit()
    def insert_prices(self):
        for city,price in self.ticket_prices.items():
            self.set_ticket_prices(city,price)
         
             
        
    
        
        
if __name__=="__main__":
    app = Day4()

    app.get_db()
    app.insert_prices()

    app.chat_interface()


