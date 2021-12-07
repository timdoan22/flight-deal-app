from flight_search import FlightSearch
import requests

SHEETY_AUTH = ")XmXvxJKyAFlaJzxdhjasd*&2312e48fasASDda"
FLIGHT_INFO_ENDPOINT = "https://api.sheety.co/446cb60337921dfccf06f0b764a2bd28/flightDatabase/flights"
USER_INFO_ENDPOINT = "https://api.sheety.co/446cb60337921dfccf06f0b764a2bd28/flightDatabase/users"

SHEETY_HEADERS = {
    "Authorization": f"Bearer {SHEETY_AUTH}"
}


class DataManager(FlightSearch):
    def __init__(self):
        super().__init__()

    def read_flight_sheet(self):
        response = requests.get(url=FLIGHT_INFO_ENDPOINT, headers=SHEETY_HEADERS)
        data = response.json()["flights"]
        return data

    def read_user_sheet(self):
        response = requests.get(url=USER_INFO_ENDPOINT, headers=SHEETY_HEADERS)
        data = response.json()["users"]
        return data

    def populate_iata_code(self):
        doc_data = self.read_flight_sheet()

        for row in doc_data:
            if row["iataCode"] == "":
                city = row["city"]
                iata_code = self.get_iata_code(city)
                self.edit_row(iata_code=iata_code, row_num=row["id"])

    def edit_row(self, iata_code, row_num):
        edit_param = {
            "flight": {
                "iataCode": iata_code
            }
        }
        self.response = requests.put(url=f"{FLIGHT_INFO_ENDPOINT}/{row_num}", json=edit_param,
                                     headers=SHEETY_HEADERS)
