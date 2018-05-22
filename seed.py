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
client_id = os.environ.get('YELP_CLIENT_ID')  


#############################################################################

# Functions associated with seeding database


def load_restaurants():
    """ Load restaurant and bakery data into database. """

    neighborhood_list = Neighborhood.query.all()

    for neighborhood in neighborhood_list:
        # Make a GET request to the API
        payload = {'location': neighborhood.neighborhood_name + ' san francisco', 'categories': 'gluten_free,bakeries'}

        # r1 returns <Response 200>
        r1 = requests.get('https://api.yelp.com/v3/businesses/search', headers={'Authorization': 'Bearer %s' % api_key}, params=payload)

        # results1.keys() is [u'region', u'total', u'businesses']
        results1 = r1.json()

        bakeries = results1['businesses']


        for bakery in bakeries:
            name = bakery['name']
            addresses = bakery['location']['display_address']  # location key has a dict value
            phone_number = bakery['display_phone']
            picture = bakery['image_url']
            website_url =bakery['url']
            avg_rating = bakery['rating']
            nh = neighborhood.neighborhood_id
            latitude = bakery['coordinates']['latitude']
            longitude =bakery['coordinates']['longitude']
            price = bakery['price']
            id_b = bakery['id']

            titles = bakery['categories']
            
            alias = []
            for title in titles:
                if title['title']:
                    alias.append(title['title'])


            types_of_food = ' '.join(alias)

            # Convert addresses (datatype is list) to a string for correct format to store in db
            address = ' '.join(addresses)
       
            bakery_info = Restaurant(name=name, address=address, phone_number=phone_number, picture=picture, website_url=website_url, avg_rating=avg_rating, neighborhood_id=nh, latitude=latitude, longitude=longitude, price=price, types_of_food=types_of_food)
            # Add bakery data to the database.
            db.session.add(bakery_info)
            
            db.session.flush()
            bakery_info_id = bakery_info.restaurant_id
            gf_type_bakery = Restaurant_type(gf_type_id=3, restaurant_id=bakery_info_id)

            db.session.add(gf_type_bakery)
    db.session.commit()


    for neighborhood in neighborhood_list:
        # Make a GET request to the API
        payload = {'location': neighborhood.neighborhood_name + 'san francisco', 'categories': 'gluten_free,restaurants'}

        # r2 returns <Response 200>
        r3 = requests.get('https://api.yelp.com/v3/businesses/search', headers={'Authorization': 'Bearer %s' % api_key}, params=payload)

        # results2.keys() is [u'region', u'total', u'businesses']
        results3 = r3.json()

        restaurants = results3['businesses']

        for restaurant in restaurants:
            name = restaurant['name']
            addresses = restaurant['location']['display_address']  # location key has a dict value
            phone_number = restaurant['display_phone']
            picture = restaurant['image_url']
            website_url =restaurant['url']
            avg_rating = restaurant['rating']
            nh = neighborhood.neighborhood_id
            latitude = restaurant['coordinates']['latitude']
            longitude =restaurant['coordinates']['longitude']
            price = restaurant['price']
            id_r = restaurant['id']

            titles = restaurant['categories']

            alias = []
            for title in titles:
                if title['title']:
                    alias.append(title['title'])

            types_of_food = ' '.join(alias)
          

            # Convert addresses (datatype is list) to a string for correct format to store in db
            address = ' '.join(addresses)

            restaurant_info = Restaurant(name=name, address=address, phone_number=phone_number, picture=picture, website_url=website_url, avg_rating=avg_rating, neighborhood_id=nh, latitude=latitude, longitude=longitude, price=price, types_of_food=types_of_food)

            # Add restaurant data to the database.
            db.session.add(restaurant_info)
            
            db.session.flush()
            restaurant_info_id = restaurant_info.restaurant_id
            gf_type_restaurant = Restaurant_type(gf_type_id=2, restaurant_id=restaurant_info_id)

            db.session.add(gf_type_restaurant)
    db.session.commit()


def set_val_gf_types_table():
    """ Set the values to the table gf_types. """

    completely_gf = GF_type(gf_type="Completely Gluten Free")
    gf_options = GF_type(gf_type="Gluten Free Options")
    gf_bakeries = GF_type(gf_type="Gluten Free Bakeries")

    db.session.add_all([completely_gf, gf_options, gf_bakeries])
    db.session.commit()



def set_val_neighborhoods_table():
    """ Set the values to the table neighborhoods. """

    n1 = Neighborhood(neighborhood_name="North Beach", lat=37.804711, lng=-122.408690)
    n2 = Neighborhood(neighborhood_name="Russian Hill", lat=37.800543, lng=-122.418776)
    n3 = Neighborhood(neighborhood_name="Fisherman's Wharf", lat=37.807292, lng=-122.417498)
    n4 = Neighborhood(neighborhood_name="Marina", lat=37.803054, lng=-122.437067)
    n5 = Neighborhood(neighborhood_name="Cow Hollow", lat=37.796986, lng=-122.437049)
    n6 = Neighborhood(neighborhood_name="Presidio Heights", lat=37.788082, lng=-122.453893)
    n7 = Neighborhood(neighborhood_name="Seacliff", lat=37.784760, lng=-122.490144)
    n8 = Neighborhood(neighborhood_name="Pacific Heights", lat=37.792122, lng=-122.436046)
    n9 = Neighborhood(neighborhood_name="Nob Hill", lat=37.792018, lng=-122.416133)
    n10 = Neighborhood(neighborhood_name="Financial District", lat=37.793790, lng=-122.400361)
    n11 = Neighborhood(neighborhood_name="China Town", lat=37.794527, lng=-122.407207)

    n12 = Neighborhood(neighborhood_name="South of Market", lat=37.777843, lng=-122.406263)
    n13 = Neighborhood(neighborhood_name="Mission", lat=37.757929, lng=-122.414524)
    n14 = Neighborhood(neighborhood_name="Potrero Hill", lat=37.759693, lng=-122.401177)
    n15 = Neighborhood(neighborhood_name="Castro", lat=37.760168, lng=-122.434051)
    n16 = Neighborhood(neighborhood_name="Noe Valley", lat=37.749107, lng=-122.433235)
    n17 = Neighborhood(neighborhood_name="Bernal Heights", lat=37.740487, lng=-122.416799)
    n18 = Neighborhood(neighborhood_name="Twin Peaks", lat=37.753618, lng=-122.447719)
    n19 = Neighborhood(neighborhood_name="Haight Ashbury", lat=37.764000, lng=-122.445745)
    
    n20 = Neighborhood(neighborhood_name="Richmond District", lat=37.778451, lng=-122.479047) # Inner/outer richmond
    n21 = Neighborhood(neighborhood_name="Sunset District", lat=37.758029, lng=-122.481450) # Inner/Outer sunset
    n22 = Neighborhood(neighborhood_name="Parkside", lat=37.740284, lng=-122.489240)
    n23 = Neighborhood(neighborhood_name="Lakeshore", lat=37.720691, lng=-122.482743)
    n24 = Neighborhood(neighborhood_name="Ocean View", lat=37.713333, lng=-122.456367)
    n25 = Neighborhood(neighborhood_name="Bayview", lat=37.729627, lng=-122.385299)

    db.session.add_all([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25])
    db.session.commit()



if __name__ == "__main__":

    connect_to_db(app)

    set_val_gf_types_table()
    set_val_neighborhoods_table()
    load_restaurants()
    
