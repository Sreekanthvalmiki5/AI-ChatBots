tool = {
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "Search flights between two cities",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string"
                },
                "destination": {
                    "type": "string"
                }
            },
            "required": [
                "origin",
                "destination"
            ]
        }
    }
}