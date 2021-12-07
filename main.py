from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_mngr = DataManager()
flight_search = FlightSearch()
notify_deal = NotificationManager()


def check_flights():
    doc_data = data_mngr.read_flight_sheet()
    for row in doc_data:
        iata_code = row["iataCode"]
        price_to_compare = row["pricePoint"]
        travel_city = row["city"]
        flight = flight_search.search_flight(iata_code=iata_code, price=price_to_compare)

        if flight == None:
            print(f"No deals currently for {travel_city}, check again later.")
        else:
            booking_link = flight_search.link.encode('utf-8')
            body = f"Low price alert! Only ${flight_search.price} to fly from {flight_search.origin_city}-{flight_search.fly_from} to {flight_search.destination_city}-{flight_search.destination_airport}, from {flight_search.out_date} to {flight_search.return_date}. \nLink to book: {booking_link.decode('utf-8')}"
            # notify_deal.send_sms(body)

            # send_sms_blast(body)
            send_email_blast(body)


def send_email_blast(email_body):
    doc_data = data_mngr.read_user_sheet()
    for row in doc_data:
        first_name = row["firstName"]
        user_email = row["email"]
        notify_deal.send_email(first_name, user_email, email_body)

def send_sms_blast(message):
    doc_data = data_mngr.read_user_sheet()
    for row in doc_data:
        user_phone = row["phoneNumber"]
        notify_deal.send_email(user_phone, message)


data_mngr.populate_iata_code()
check_flights()
