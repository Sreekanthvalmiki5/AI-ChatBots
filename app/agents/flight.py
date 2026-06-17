from app.services.flight_service import FlightService
from app.api.v1.models import get_openrouter_model
from app.tools.flight_tool import tool

import os
import json

class Flight:
    def __init__(self):
        self.name = "Flight Assistant"
        self.router = get_openrouter_model()
        self.tools = [tool]

    def chat(self, message, history):
        history = [{"role": h["role"], "content": h["content"]} for h in history]
        
        system_message = """You are a friendly, helpful flight assistant for FlightAI.
            When the user asks for flights, you will call the search_flights tool to get real data.

            CRITICAL RULES FOR CONVERSATION AND FORMATTING:
            1. Respond to the user with a natural, brief, friendly introductory sentence acknowledging their route (e.g., "Sure, I found these flight options from Hyderabad to Bengaluru for you:" or "Here is the current flight schedule for your trip:").
            2. Immediately after your friendly introduction, append the flight details strictly inside the [FLIGHT_LIST] tag block.
            3. The content inside [FLIGHT_LIST] must be a clean, valid JSON array of flight objects. Never insert markdown text or descriptions inside or around the JSON block itself.

            Example Expected Output:
            Sure! I managed to look up the schedules. Here are the available flights from Hyderabad to Bengaluru:

            [FLIGHT_LIST]
            [
            {"airline": "Air India", "flightNumber": "515", "origin": "Hyderabad", "destination": "Bengaluru", "daysOfWeek": "Wednesday", "scheduledDepartureTime": "NA", "scheduledArrivalTime": "11:15"}
            ]
            [/FLIGHT_LIST]

            If the tool returns an empty list or no flights are found, say something empathetic and return an empty block, like this:
            "I checked our database but couldn't find any direct flight schedules for that route. [FLIGHT_LIST][]"
            """
                    
        messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}] 
        
        # 1. First completion call
        response = self.router.chat.completions.create(model="gpt-oss-20b", messages=messages, tools=self.tools) 
        assistant_message = response.choices[0].message
        
        if response.choices[0].finish_reason == "tool_calls" or assistant_message.tool_calls:
            # FIX: Format the assistant's tool call intent into a standard serializable dictionary
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in assistant_message.tool_calls
                ]
            })
            
            # FIX: Re-route tool result assignment away from overwriting the variable name
            tool_msg = self.handle_tool_call(assistant_message)
            messages.append(tool_msg) 
            
            # 2. Second model call to process payload structures inside instructions
            responses = self.router.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=messages
            ) 
            return responses.choices[0].message.content 
            
        return assistant_message.content

    def handle_tool_call(self, message):
        tool_call = message.tool_calls[0]

        if tool_call.function.name == "search_flights":
            arguments = json.loads(tool_call.function.arguments)

            origin_city = arguments.get('origin')
            destination_city = arguments.get('destination') 
            
            service = FlightService()
            flight_details = service.search(origin_city, destination_city)

            return {
                "role": "tool",
                "content": json.dumps(flight_details),
                "tool_call_id": tool_call.id
            }