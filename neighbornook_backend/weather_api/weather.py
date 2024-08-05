import requests
from datetime import datetime
from django.conf import settings

def fetch_weather_data(location):
    base_url = settings.METEOMATICS_BASE_URL
    username = settings.METEOMATICS_USERNAME
    password = settings.METEOMATICS_PASSWORD

    parameters = 't_2m:C,weather_symbol_1h:idx' #if error check the idx
    time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    api_url = f'{base_url}/{time}/{parameters}/{location}/json'

    response = requests.get(api_url, auth=(username, password))

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_weather_icon(weather_data):
    try:
        temperature = weather_data['data'][0]['coordinates'][0]['dates'][0]['value']
        weather_symbol = weather_data['data'][1]['coordinates'][0]['dates'][0]['value']

        icon_mapping = {
            1: 'sunny.png',
            2: 'partly_cloudy.png',
            3: 'cloudy.png',
            4: 'rain.png',
            5: 'thunderstorm.png',
            6: 'snowy.png',
        }

        icon = icon_mapping.get(weather_symbol, 'default.png')
        return icon, temperature
    except (IndexError, KeyError) as e:
        print(f"Error processing weather data: {e}")
        return 'default.png', None
    
def get_weather_context(location):
    weather_data = fetch_weather_data(location)

    if weather_data:
        weather_icon, temperature = get_weather_icon(weather_data)
        context = {
            'temperature': temperature,
            'weather_icon': weather_icon,
            'location': 'London, UK',
            # 'date': datetime.now().strftime('%Y-%m-%d'),
        }
    else:
        context = {
            'temperature': None,
            'weather_icon': 'default.png',
            'location': 'Unknown',
            # 'date': datetime.now().strftime('%Y-%m-%d'),
        }
    
    return context