from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, FloatField, validators
from wtforms.validators import DataRequired, InputRequired
import requests
import json
from keys import WEATHER_API_KEY as appid
import datetime

class SearchCityForm(Form):
    city = StringField('City', [DataRequired(message="Must be filled")], render_kw={'class': 'form-control', 'placeholder': 'City'})
    
class SearchCoordsForm(Form):
    lon = StringField('Longitude', [DataRequired(message="Must be filled"), ], render_kw={'class': 'form-control', 'placeholder': 'Longitude'})
    lat = StringField('Latitude', [DataRequired(message="Must be filled")], render_kw={'class': 'form-control', 'placeholder': 'Latitude'})

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('city'))

@app.route('/city', methods=['GET', 'POST'])
def city():
    form = SearchCityForm(request.form)
    if request.method == 'POST':
        if form.validate():
            city = request.form['city']
            weather = get_weather_from_city(city)
            if not weather:
                return render_template('index.html', form=form, action='/city', weather=get_weather_from_file(), error='City not found')
            weather = format_weather(weather)
            with open('weather.json', 'w') as file:
                json.dump(weather, file)
            return render_template('index.html', form=form, action='/city', weather=weather)
        return render_template('index.html', form=form, action='/city', weather=get_weather_from_file())
    else:
        weather = get_weather_from_file()
    return render_template('index.html', form=form, action='/city', weather=weather)

@app.route('/coords', methods=['GET', 'POST'])
def coords():
    form = SearchCoordsForm(request.form)
    if request.method == 'POST':
        if form.validate():
            lat = request.form['lat']
            lon = request.form['lon']
            weather = get_weather_from_coords(lon, lat)
            if not weather:
                return render_template('index.html', form=form, action='/coords', weather=get_weather_from_file(), error='Coordinates not found')
            weather = format_weather(weather)
            with open('weather.json', 'w') as file:
                json.dump(weather, file)
            return render_template('index.html', form=form, action='/coords', weather=weather)
        return render_template('index.html', form=form, action='/coords', weather=get_weather_from_file())
    else:
        weather = get_weather_from_file()
    return render_template('index.html', form=form, action='/coords', weather=weather)

# Get the weather from the city
def get_weather_from_city(city):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}').json()
    if response['cod'] == '404':
        return None
    city = response['name']
    lon = response['coord']['lon']
    lat = response['coord']['lat']
    response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lon={lon}&lat={lat}&exclude=minutely,hourly&units=metric&appid={appid}').json()
    response['name'] = city
    return response

# Get the weather from the coordinates
def get_weather_from_coords(lon, lat):
    response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lon={lon}&lat={lat}&exclude=minutely,hourly&units=metric&appid={appid}').json()
    if 'cod' in response.keys() and response['cod'] == '400':
        return None
    city = get_city_name(lon, lat)
    response['name'] = city    
    return response

# Get the weather from the file if the stored data is from today, otherwise get new data
def get_weather_from_file():
    weather = json.load(open('weather.json'))
    
    first_day = weather['daily'][0]
    first_day_date = datetime.datetime.strptime(first_day['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    if first_day_date != today:
        lon = weather['longitude']
        lat = weather['latitude']
        weather = get_weather_from_coords(lon, lat)
        formattedWeather = format_weather(weather)
        with open('weather.json', 'w') as file:
            json.dump(formattedWeather, file)
        return formattedWeather
    return weather
    
# Format the weather data
def format_weather(weather):
    formatted = {
        'longitude': weather['lon'],
        'latitude': weather['lat'],
        'name': weather['name'],
        'daily': format_days(weather['daily'])
    }
    return formatted
    
# Get the city name from the coordinates
def get_city_name(lon, lat):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lon={lon}&lat={lat}&appid={appid}').json()
    return response['name']

# Format the days
def format_days(days):
    output = []
    for day in days:
        output.append({
            'date': datetime.datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d'),
            'lows': day['temp']['min'],
            'highs': day['temp']['max'],
            'description': day['weather'][0]['description'],
            'icon': day['weather'][0]['icon']
        })
    return output
    