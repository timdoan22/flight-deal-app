import requests

POST_SHEETY_ENDPOINT = "https://api.sheety.co/446cb60337921dfccf06f0b764a2bd28/flightDatabase/users"

SHEETY_HEADER = {
    "Authorization": BEARER_KEY
}

print("Welcome to the Flight Club where we find the best flight deals for you. \n")


def get_info():
    first_name = input("Enter your first name:\n")
    last_name = input("Enter your last name:\n")
    email = input("Enter your email:\n")
    email_verify = input("Enter your email again:\n")

    while email != email_verify:
        print("The email does not match.  Please enter the same matching email again.")
        email = input("Enter your email:\n")
        email_verify = input("Enter your email again: \n")

    add_record(first_name, last_name, email)


def add_record(first_name, last_name, email):
    parameters = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        }
    }

    response = requests.post(url=POST_SHEETY_ENDPOINT, json=parameters, headers=SHEETY_HEADER)

    print("You're now in the Flight Club! Be sure to check your email for exclusive new deals.")


get_info()
