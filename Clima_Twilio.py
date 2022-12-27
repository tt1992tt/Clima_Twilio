import os
from twilio.rest import Client 
from twilio_env import * # el template que cree
import time

from requests import Request, Session 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects 
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup 
from tqdm import tqdm  # barra de progreso %
from datetime import datetime 

query = 'Buenos Aires'
api_key = API_KEY_WAPI

url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

response = requests.get(url_clima).json()

def get_forecast(response,i):
    
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    return fecha,hora,condicion,tempe,rain,prob_rain

datos = []

# es una barra de progreso del loop
for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])), colour = 'green'):
    
    datos.append(get_forecast(response, i))

listado = []  # si solo quisiera loopear

for i in range(len(response['forecast']['forecastday'][0]['hour'])):
    
    listado.append(get_forecast(response, i))
    print(listado[i])

col = ['Fecha','Hora','Condicion','Temperatura','Lluvia','prob_lluvia']
df = pd.DataFrame(datos, columns=col)
df = df.sort_values('Hora', ascending = True)

df_rain = df[df['Hora'].between(18, 22, inclusive='both')] 
df_rain = df_rain[['Hora','Condicion']]
df_rain.set_index('Hora',inplace = True) 

print('\nHola! \n\n\n El pronostico del tiempo hoy '+ df['Fecha'][0] +' en ' + query +' es : \n\n\n ' + str(df_rain))

time.sleep(2)
account_sid = TWILIO_ACCOUNT_SID 
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body='\nHola! \n\n\n El pronostico de lluvia hoy '+ df['Fecha'][0] +' en ' + query +' es : \n\n\n ' + str(df_rain),
                     from_=PHONE_NUMBER,
                     to='+5491161050317'
                 )

print('Mensaje Enviado ' + message.sid)
