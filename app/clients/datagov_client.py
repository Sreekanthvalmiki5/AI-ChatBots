import requests
import logging
from app.core.config import DATA_GOV_API_KEY, DATA_GOV_API_URL

logger = logging.getLogger(__name__)

def search_flights(origin: str, destination: str, max_results: int = 30):

    params = {
        "api-key": DATA_GOV_API_KEY,
        "format": "json",
        "filters[origin]": origin,
        "filters[destination]": destination,
        "limit": max_results,
        "offset": 0
    }

    # Replicate a real browser / Postman handshake to avoid server-side dropping
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Connection": "keep-alive"
    }

    # print(f"[FlightClient] Searching: {origin} → {destination}")

    try:
        # Pass the headers and explicitly define a reasonable timeout
        response = requests.get(DATA_GOV_API_URL, params=params, headers=headers, timeout=15)
        
        # print(f"[FlightClient] Status: {response.status_code}")
        # print(f"[FlightClient] URL called: {response.url}")

        response.raise_for_status()
        data = response.json()

        records = data.get("records", [])
        # print(f"[FlightClient] Records returned: {len(records)}")
        
        # print(records)
        

        return records

    except requests.exceptions.RequestException as e:
        logger.error(f"[FlightClient] Request failed: {e}")
        # Return an empty array so your FastAPI app handles errors gracefully instead of 500 crashing
        return []