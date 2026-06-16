import requests
API_KEY = "809d645cd50c43a4b0c101505240611"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(city_name):
    url = f"{BASE_URL}?key={API_KEY}&q={city_name}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        location = data['location']
        current = data['current']
        print(f"City: {location['name']}, {location['country']}")
        print(f"Temperature: {current['temp_c']}°C")
        print(f"Humidity: {current['humidity']}%")
        print(f"Condition: {current['condition']['text']}")
    else:
        print("Error: Could not retrieve data.check yout internet")

# city = input("Enter the city name: ")
# get_weather(city)