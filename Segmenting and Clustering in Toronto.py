#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
from pandas.io.json import json_normalize  # tranform JSON file into a pandas dataframe

import folium

from sklearn.cluster import KMeans

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors


# In[2]:


wiki_link = ('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')
raw_wikipedia_page= requests.get(wiki_link).text


# In[3]:


soup = BeautifulSoup(raw_wikipedia_page,'xml')


# In[4]:


from IPython.display import display_html
tab = str(soup.table)
display_html(tab,raw=True)


# In[5]:


geog_coordinates = pd.read_csv('https://cocl.us/Geospatial_data')
geog_coordinates.info()


# In[6]:


geog_coordinates


# In[7]:


df = pd.read_html(tab)

df = df[0]
df.info()


# In[8]:


df = pd.read_html(tab)

df = df[0]
df.info()


# In[9]:


df1 = df[df.Borough != 'Not assigned']


# In[10]:


df2 = df1.groupby(['Postal Code','Borough'], sort=False).agg(', '.join)
df2.reset_index(inplace=True)

df2['Neighbourhood'] = np.where(df2['Neighbourhood'] == 'Not assigned',df2['Borough'], df2['Neighbourhood'])

df2


# In[11]:


df3 = pd.merge(df2,geog_coordinates,on ='Postal Code')
df3.head()


# In[12]:


address = 'Toronto, Ontario Canada'

geolocator = Nominatim(user_agent="toronto_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto Canada are {}, {}.'.format(latitude, longitude))


# In[13]:


map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)


for lat, long, borough, neighborhood in zip(
        df3['Latitude'], 
        df3['Longitude'], 
        df3['Borough'], 
        df3['Neighbourhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, long],
        radius=5,
        popup=label,
        color='red',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  


# In[14]:


map_toronto


# In[15]:


df_toronto = df3[df3['Borough'].str.contains("Toronto")].reset_index(drop=True)
df_toronto.head()


# In[ ]:




