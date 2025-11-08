import requests
import json


def getWeatherdata():
    api_url = "https://weather.tsukumijima.net/api/forecast/city/140010"
    response = requests.get(api_url)
    data = response.json()
    # print(data["forecasts"][0]["telop"])
    forecast = {
        'date': data["forecasts"][0]["date"].replace('-','/'),
        'telop' : data["forecasts"][0]["telop"],
        'image':data["forecasts"][0]["image"]["url"],
        'max' : data["forecasts"][0]["temperature"]["max"]["celsius"],
        'min' : data["forecasts"][0]["temperature"]["min"]["celsius"],
    }
    return forecast