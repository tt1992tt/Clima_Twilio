#!/usr/bin/env python
# coding: utf-8

# <img src=https://i.ytimg.com/vi/knxlmCVFAZI/maxresdefault.jpg>

# In[1]:


#!pip3 install twilio#


# In[15]:


#!pip install tqdm#


# In[17]:


#!pip install extract_usd#


# In[7]:


import os
from twilio.rest import Client 
from twilio_config import * # el template que cree
import time

from requests import Request, Session 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects 
import json


import pandas as pd
import requests
from bs4 import BeautifulSoup 
from tqdm import tqdm  # barra de progreso %

from datetime import datetime 


# # Armado de la URL

# In[8]:


query = 'Buenos Aires'
api_key = API_KEY_WAPI

url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

url_clima


# In[9]:


response = requests.get(url_clima).json()


# In[10]:


response


# In[11]:


response.keys()


# In[12]:


response['forecast'].keys()


# In[13]:


response['forecast']['forecastday'][0].keys() # solo tiene 1 elemento forecastday 


# In[14]:


len(response['forecast']['forecastday'][0]['hour'])


# In[15]:


response['forecast']['forecastday'][0]['hour'][0]  # puede ir del 0 al 23 (las 24 horas)


# In[16]:


response['forecast']['forecastday'][0]['hour'][0]['time'].split()[0]


# In[17]:


response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1].split(':')[0]


# In[18]:


response['forecast']['forecastday'][0]['hour'][0]['will_it_rain']


# In[19]:


response['forecast']['forecastday'][0]['hour'][2]['chance_of_rain']


# # Dataframe

# In[20]:


def get_forecast(response,i):
    
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return fecha,hora,condicion,tempe,rain,prob_rain


# In[21]:


datos = []

# es una barra de progreso del loop
for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])), colour = 'green'):
    
    datos.append(get_forecast(response, i))


# In[22]:


listado = []  # si solo quisiera loopear

for i in range(len(response['forecast']['forecastday'][0]['hour'])):
    
    listado.append(get_forecast(response, i))
    print(listado[i])


# In[23]:


datos[0]


# In[24]:


col = ['Fecha','Hora','Condicion','Temperatura','Lluvia','prob_lluvia']
df = pd.DataFrame(datos, columns=col)
df = df.sort_values('Hora', ascending = True)
df


# In[25]:


df[df['Lluvia']==1]


# In[ ]:





# In[26]:


df_rain = df[df['Hora'].between(18, 22, inclusive='both')] 
df_rain = df_rain[['Hora','Condicion']]
df_rain.set_index('Hora',inplace = True) 


# In[27]:


df_rain


# In[28]:


print('\nHola! \n\n\n El pronostico del tiempo hoy '+ df['Fecha'][0] +' en ' + query +' es : \n\n\n ' + str(df_rain))


# In[29]:


PHONE_NUMBER


# In[30]:


TWILIO_AUTH_TOKEN


# # Mensaje SMS desde Twilio

# In[31]:


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


# # Challenge 
# 
# * Extrae el valor del dolar en tu país y el top 10 de criptomonedas con su respectiva valoración
# * Ahora envia un mensaje diarío a tu Whatsapp usando Twilio
# 
# **hint 💡** Investiga que API's gratuitas existen para consultar estos datos
# 
# 
# 
# <img src="WhatsApp Image 2022-09-13 at 9.12.18 AM.jpeg" width="200" height="200" />

# In[ ]:





# In[ ]:



