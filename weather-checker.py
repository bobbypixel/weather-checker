import pathlib
import requests

def read_email() -> str:
    email_file = pathlib.Path(__file__).parent / "email.txt"

    with open(email_file) as f:
        email = f.read().strip()
    
    return email

def get_weather(latitude: float, longitude: float, email: str):
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact"
    response = requests.get(
        url,
        params={"lat": latitude, "lon": longitude},
        headers={"User-agent": "weather-checker {email}"},
    )
    if response.status_code == 200:
        next_12_hours_forecast = response.json()["properties"]["timeseries"][0]["data"]["next_12_hours"]["summary"]["symbol_code"]

        print(
            f"\nYour weather forecast in the next 12 hours is: {next_12_hours_forecast}\n"
        )
    elif response.status_code == 403:
        print(
            "\nStatus 403 Forbidden: Please use a unique, identifying User-Agent header.\n"
        )
    else:
        print(f"\n{response}\nError in retrieving the weather.\n")


def get_float_input(prompt) -> str:
    result = input(prompt)
    while not result.replace(".", "", 1).isdigit():
        result = input(prompt)
    return result


def start():
    print("🌻 A SIMPLE WEATHER CHECKER 🍃")
    print("Warning: To prevent the risk of being blocked by the MET Weather API service, include your email in email.txt.")
    print("More information can be found here: https://api.met.no/doc/TermsOfService\n")

    latitude_prompt = "What is your latitude? "
    longitude_prompt = "What is your longitude? "

    latitude = get_float_input(latitude_prompt)
    longitude = get_float_input(longitude_prompt)
    email = read_email()

    get_weather(latitude, longitude, email)


if __name__ == "__main__":
    start()
