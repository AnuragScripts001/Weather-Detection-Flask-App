from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import datetime

import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'your_secret_key')

def get_weather(city):
    weather_data = {
        'Bangalore': {'temp': '25', 'description': 'Sunny'},
        'Delhi': {'temp': '32', 'description': 'Cloudy'},
        'Mumbai': {'temp': '29', 'description': 'Rainy'},
    }
    return weather_data.get(city.title(), {'temp': 'N/A', 'description': 'No data available'})

def get_city_image(city):
    # Read API keys from environment variables
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY')
    SEARCH_ENGINE_ID = os.environ.get('SEARCH_ENGINE_ID', 'YOUR_SEARCH_ENGINE_ID')
    query = f"{city} famous landmark tourist attraction"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&searchType=image&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}&imgSize=large"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        print('Google Custom Search API response for', city, ':', data)  # Debug print
        items = data.get('items')
        if items and len(items) > 0:
            image_url = items[0].get('link')
            return image_url
        else:
            # Fallback to a default image if Google returns no result
            return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"
    except Exception as e:
        print('Error fetching Google image:', e)
        return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"

@app.route('/', methods=['GET', 'POST'])
def index():
    city = "Bangalore"
    if request.method == 'POST':
        city = request.form.get('city', 'Bangalore')
    weather = get_weather(city)
    temp = weather['temp']
    description = weather['description']
    day = datetime.datetime.now().strftime("%A")
    return render_template('index.html', city=city, temp=temp, description=description, day=day)

@app.route('/pred', methods=['POST', 'GET'])
def pred():
    city = request.form['city'] if request.method == 'POST' else "Bangalore"
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', None)
    if not OPENWEATHER_API_KEY:
        flash('OpenWeather API key not configured. Set OPENWEATHER_API_KEY environment variable.', 'error')
        return redirect(url_for('index'))
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    PARAMS = {'units': 'metric'}
    try:
        data = requests.get(url, params=PARAMS).json()
        print(data)
        if 'main' not in data:
            flash('Weather data not available for the specified city.', 'error')
            return redirect(url_for('index'))
        temp = data['main']['temp']
        description = data['weather'][0]['description'].title()
        day = datetime.datetime.now().strftime("%A")
        icon = data['weather'][0]['icon'] if 'icon' in data['weather'][0] else None
        humidity = data['main'].get('humidity', 'N/A')
        wind_speed = data.get('wind', {}).get('speed', 'N/A')
        max_temp = data['main'].get('temp_max', 'N/A')
        min_temp = data['main'].get('temp_min', 'N/A')
        pressure = data['main'].get('pressure', 'N/A')
        cloudiness = data.get('clouds', {}).get('all', 'N/A')
        visibility = data.get('visibility', 'N/A')
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S') if 'sys' in data and 'sunrise' in data['sys'] else 'N/A'
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S') if 'sys' in data and 'sunset' in data['sys'] else 'N/A'
        city_image_url = get_city_image(city)
        return render_template('index.html', city=city, temp=temp, description=description, day=day,
                               icon=icon, humidity=humidity, wind_speed=wind_speed, max_temp=max_temp,
                               min_temp=min_temp, pressure=pressure, cloudiness=cloudiness,
                               visibility=visibility, sunrise=sunrise, sunset=sunset,
                               city_image_url=city_image_url)
    except Exception:
        flash('Error retrieving weather data. Please try again.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
