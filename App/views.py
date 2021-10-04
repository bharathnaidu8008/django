from django.shortcuts import render, redirect
from django.http import HttpResponse
from App.models import Indias, States
import requests

# Create your views here.
def index(request):
    print(request.method)
    return render(request, 'index.html')

def home(request):
    print(request.method)
    return render(request, 'index.html')

def store_data(request):
    data = requests.get("https://api.covid19api.com/dayone/country/india")
    if data.status_code == 200:
        Indias.objects.all().delete()
        covid_data = data.json()
        for data in covid_data:
            row = Indias(Active=data["Active"], Confirmed=data["Confirmed"], Deaths=data["Deaths"], Date=data["Date"][:10], Recovered=data["Recovered"])
            row.save()
    data = requests.get("https://covid-india-cases.herokuapp.com/states")
    if data.status_code == 200:
        States.objects.all().delete()
        covid_data = data.json()
        for data in covid_data:
            row = States(Active=data["noOfCases"]-data["cured"], Confirmed=data["noOfCases"], Deaths=data["deaths"], State=data["state"], Recovered=data["cured"])
            row.save()
    return HttpResponse("<h1>Data restored successfully")

def india(request):
    url = dashboard_url(1)
    return render(request, 'index.html', {"dashboard_url": url})

def state(request):
    url = dashboard_url(2)
    return render(request, 'index.html', {"dashboard_url": url})

def dashboard_url(dashboard_id):
    # You'll need to install PyJWT via pip 'pip install PyJWT' or your project packages file

    import jwt
    import time
    
    METABASE_SITE_URL = "https://covidmetabase.herokuapp.com"
    METABASE_SECRET_KEY = "424f722c9713a7d44deea297d6daf3745675aeeb0843593adc20770c4cd6ca8c"
    
    payload = {
      "resource": {"dashboard": dashboard_id},
      "params": {
        
      },
      "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    
    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token.decode("utf8") + "#bordered=true&titled=true"
    return iframeUrl