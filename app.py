from flask import Flask, jsonify, render_template, request
from models import db, User, WeatherData
from config import DATABASE_URI
import requests
from datetime import datetime
from flask_caching import Cache

app = Flask(__name__)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Set up caching
app.config['CACHE_TYPE'] = 'simple'  # or another type like 'redis' for more complex caching
cache = Cache(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/details', methods=['GET'])
def weather_details():
    # API URL and key
    api_key = "q4eyjEHUZAaGTiiek5kE1g0pWvOm7Sa2"  # Replace with your actual API key
    location = "London"  # Change this to the desired location or make it dynamic
    
    # OpenWeatherMap API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    
    # Send GET request to the API
    response = requests.get(url)
    data = response.json()  # Parse the response as JSON
    
    if response.status_code == 200:
        # Extract weather data from the API response
        weather_data = {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "time_recorded": data["dt"]
        }
        return render_template('weather_details.html', weather_data=weather_data)
    else:
        # If API request fails, show an error
        error = "Unable to fetch weather data. Please try again later."
        return render_template('weather_details.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/weather', methods=['GET'])
@cache.cached(timeout=300)  # Cache the response for 5 minutes
def get_weather():
    # Fetch data from Tomorrow.io API (replace with your API key)
    api_key = "q4eyjEHUZAaGTiiek5kE1g0pWvOm7Sa2"
    location = request.args.get('location', 'New York')
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["data"]["values"]["temperature"],
            "humidity": data["data"]["values"]["humidity"],
            "wind_speed": data["data"]["values"]["windSpeed"],
            "location": location
        }

        # Save to database
        weather_data = WeatherData(
            temperature=weather['temperature'],
            humidity=weather['humidity'],
            wind_speed=weather['wind_speed'],
            time_recorded=datetime.now()
        )
        db.session.add(weather_data)
        db.session.commit()

        # Fetch recent weather alerts (if any)
        alerts_url = f"https://api.tomorrow.io/v4/alerts?location={location}&apikey={api_key}"
        alerts_response = requests.get(alerts_url)
        alerts = []
        if alerts_response.status_code == 200:
            alerts_data = alerts_response.json()
            alerts = alerts_data.get('data', [])

        # Fetch weather forecast (for example, for the next 5 days)
        forecast_url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}"
        forecast_response = requests.get(forecast_url)
        forecast = []
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            forecast = forecast_data.get('data', [])

        return jsonify({
            "weather": weather,
            "alerts": alerts,
            "forecast": forecast
        })
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
