import os
import requests
import datetime
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from model import connect_to_db, db, User, Restaurant, Favorite_restaurant, GF_type, Restaurant_type, Neighborhood
from server import app

# Key to access data via YELP Fusion API
api_key = os.environ.get('YELP_ACCESS_KEY')
client_id = os.environ.get('YELP_CLIENT_ID')   # added .get() and deleted []


#############################################################################

url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'Bearer %s' % api_key}
payload = {'location': 'san francisco', 'categories': 'gluten_free'}

r = requests.get(url, headers=headers, params=payload)

# results type is a str
results = r.content

def load_restaurants(data):
    """ Load restaurant data into database. """

    # with open(filename, 'w') as my_file:
    #     my_file.write(results)
        
        # Turns into dictionary (type=dict)
        # Keys = [u'region', u'total', u'businesses']
    data = json.loads(data)    
    restaurants = data['businesses']   # type = list (List of dictionaries)
    # print restaurants

    for restaurant in restaurants:
        name = restaurant['name']
        address = restaurant['location']['display_address']  # location key has a dict value
        phone_number = restaurant['display_phone']
        picture = restaurant['image_url']
        website_url =restaurant['url']
        avg_rating = restaurant['rating']


        restaurant_info = Restaurant(name=name, address=address, phone_number=phone_number, picture=picture, website_url=website_url, avg_rating=avg_rating)

        db.session.add(restaurant_info)

    db.session.commit()

    
    # neighborhood_id


if __name__ == "__main__":

    connect_to_db(app)

    load_restaurants(results)


    