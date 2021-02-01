from flask import Flask, render_template, redirect, url_for, jsonify, request
import requests
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12)

@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('covid'))

@app.route("/covid", methods = ["POST", "GET"])
def covid():

    nigeria_data_url = "https://disease.sh/v2/countries/Nigeria?yesterday=true&strict=true"
    nigeria_content = requests.get(nigeria_data_url)
    nigeria_data = nigeria_content.json()

    countries_data = countries()
    countries_data_all = country_api()

    return render_template("index.html", data = nigeria_data, countries = countries_data, world = countries_data_all)

@app.route("/countries", methods = ["POST", "GET"])
def countries():

    countries_data_url = "https://coronavirus-tracker-api.herokuapp.com/v2/locations"
    countries_content = requests.get(countries_data_url)
    countries_data = countries_content.json()

    countries_dict = {}
    for item in countries_data['locations']:
        if item['country'] not in countries_dict:
            countries_dict.update({item['country']:{'Population':item['country_population'], 'Confirmed': item['latest']['confirmed'],'Deaths':item['latest']['deaths']}})
        else:
            countries_dict[item['country']]['Confirmed'] += item['latest']['confirmed']
            countries_dict[item['country']]['Deaths'] += item['latest']['deaths']

    return countries_dict

@app.route("/covid/world", methods = ["POST", "GET"])
def world():

    countries_data = countries()
    world_data = country_api()
    return render_template("world.html", countries = countries_data, world = world_data)

@app.route("/covid/nigeria", methods = ["POST", "GET"])
def nigeria():

    from data_render import daywise_data_nigeria
    nigeria_plot_daywise_data = daywise_data_nigeria()
    day = nigeria_plot_daywise_data[0]
    confirmed = nigeria_plot_daywise_data[1]
    deaths = nigeria_plot_daywise_data[2]


    nigeria_data_url = "https://disease.sh/v2/countries/Nigeria?yesterday=true&strict=true"
    nigeria_content = requests.get(nigeria_data_url)
    nigeria_data = nigeria_content.json()


    return render_template("nigeria.html", data = nigeria_data, day = day, confirmed = confirmed, deaths = deaths)

# @app.route("/covid/contribute")
# def contribute():
#     return render_template("contribute.html")

@app.route("/daywise_nigeria_data")
def daywise_nigeria_data():

    from data_render import daywise_data_nigeria
    nigeria_plot_daywise_data = daywise_data_nigeria()
    day = nigeria_plot_daywise_data[0]
    confirmed = nigeria_plot_daywise_data[1]
    deaths = nigeria_plot_daywise_data[2]
    
    return jsonify({'day':day, 'confirmed':confirmed, 'deaths':deaths})

def country_api():
    
    world_data = requests.get("https://corona.lmao.ninja/v2/all").json()
    return world_data

if __name__ == "__main__":
    app.run(debug=True)