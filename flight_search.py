from flight_data import FlightData
import requests
import os
from datetime import datetime, timedelta

TEQ_API_KEY = os.environ.get("TEQ_API_KEY")
TEQ_ENDPOINT = "https://tequila-api.kiwi.com"


class FlightSearch(FlightData):
    def __init__(self):
        super().__init__()

    def get_iata_code(self, city):
        header = {
            "apikey": TEQ_API_KEY
        }

        parameters = {
            "term": city,
            "limit": 1,
        }

        response = requests.get(url=f"{TEQ_ENDPOINT}/locations/query", params=parameters, headers=header)

        iata_code = response.json()["locations"][0]["code"]
        return iata_code

    def search_flight(self, iata_code, price):
        header = {
            "apikey": TEQ_API_KEY
        }

        today_date = datetime.today().date()
        tomorrow_date = str((today_date + timedelta(days=1)).strftime("%d/%m/%Y"))
        future_date = str((today_date + timedelta(days=182)).strftime("%d/%m/%Y"))

        parameters = {
            "fly_from": self.fly_from,
            "fly_to": iata_code,
            "date_from": tomorrow_date,
            "date_to": future_date,
            "nights_in_dst_from": self.nights_from,
            "nights_in_dst_to": self.nights_to,
            "flight_type": self.flight_type,
            "curr": self.currency,
            "price_to": price,
            "one_for_city": 1,
            "max_stopovers": 0
        }

        response = requests.get(url=f"{TEQ_ENDPOINT}/v2/search", params=parameters, headers=header)
        try:
            data = response.json()["data"][0]
        except IndexError:
            return None
        else:
            out_date = data["route"][0]["local_departure"].split("T")[0]
            total_tenure_date = str(
                (datetime.strptime(out_date, "%Y-%m-%d") + timedelta(days=data["nightsInDest"])).strftime("%Y-%m-%d"))

            self.price = data["price"]
            self.origin_city = data["route"][0]["cityFrom"]
            self.destination_city = data["route"][0]["cityTo"]
            self.destination_airport = data["route"][0]["flyTo"]
            self.out_date = out_date
            self.return_date = total_tenure_date
            self.link = f"https://www.google.ca/flights?hl=en#flt={self.fly_from}.{self.destination_airport}.{self.out_date}*{self.destination_airport}.{self.fly_from}.{self.return_date}"
            return True
