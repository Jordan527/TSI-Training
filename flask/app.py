from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, FloatField, validators
import requests
import json

class SearchCityForm(Form):
    city = StringField('City', [validators.Length(min=1, max=25)], render_kw={'class': 'form-control', 'placeholder': 'City'})
    
class SearchCoordsForm(Form):
    lon = FloatField('Longitude', render_kw={'class': 'form-control', 'placeholder': 'Longitude'})
    lat = FloatField('Latitude', render_kw={'class': 'form-control', 'placeholder': 'Latitude'})

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
            cityWeather = get_city_weather(city)
            coords = cityWeather['coord']
            print(coords)
            weather = get_coord_weather(coords['lon'], coords['lat'])
            return render_template('index.html', form=form, action='/city', weather=weather)
        else:
            return render_template('index.html', form=form, action='/city', error='City is required')
    else:
        return render_template('index.html', form=form, action='/city')

@app.route('/coords', methods=['GET', 'POST'])
def coords():
    form = SearchCoordsForm(request.form)
    if request.method == 'POST':
        if form.validate():
            lat = request.form['lat']
            lon = request.form['lon']
            weather = get_coord_weather(lon, lat)
            print(weather)
            return render_template('index.html', form=form, action='/coords', weather=weather)
        else:
            return render_template('index.html', form=form, action='/coords')
    else:
        return render_template('index.html', form=form, action='/coords')

def get_city_weather(city):
    appid = 'c37f69fc7204e9c21807e36cd7b0ab94'
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}')
    return response.json()

def get_coord_weather(lon, lat):
    appid = 'c37f69fc7204e9c21807e36cd7b0ab94'
    response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lon={lon}&lat={lat}&exclude=minutely,daily&appid={appid}')
    return response.json()
    