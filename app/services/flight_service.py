from app.clients.datagov_client import search_flights


class FlightService:

    def search(self, origin, destination):
        return search_flights(origin, destination)