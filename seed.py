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


# Dont hard code a list of neighborhoods // create a query to my db for neighborhood names
# save it to a variable and loop through it

neighborhood_list = Neighborhood.query.all()

for neighborhood in neighborhood_list:
    # make request
    payload = {'location': neighborhood.neighborhood_name + ' san francisco', 'categories': 'gluten_free,bakeries'}
    r1 = requests.get(url, headers=headers, params=payload)

for neighborhood in neighborhood_list:
    payload = {'location': neighborhood + 'san francisco', 'categories': 'gluten_free,restaurants'}
    r2 = requests.get(url, headers=headers, params=payload)

# r = requests.get(url, headers=headers, params=payload)

# results1 and results2 type is a str
results1 = r1.content
results2 = r2.content



# def load_restaurants(data):
#     """ Load restaurant data into database. """

#     # with open(filename, 'w') as my_file:
#     #     my_file.write(results)
        
#         # Turns into dictionary (type=dict)
#         # Keys = [u'region', u'total', u'businesses']
#     data = json.loads(data)    
#     restaurants = data['businesses']   # type = list (List of dictionaries)
#     # print restaurants

#     for restaurant in restaurants:
#         name = restaurant['name']
#         address = restaurant['location']['display_address']  # location key has a dict value
#         phone_number = restaurant['display_phone']
#         picture = restaurant['image_url']
#         website_url =restaurant['url']
#         avg_rating = restaurant['rating']


#         restaurant_info = Restaurant(name=name, address=address, phone_number=phone_number, picture=picture, website_url=website_url, avg_rating=avg_rating)

#         db.session.add(restaurant_info)

#     db.session.commit()

    
    # neighborhood_id

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
    n3 = Neighborhood(neighborhood_name="Fisherman's Wharf")
    n4 = Neighborhood(neighborhood_name="Marina")
    n5 = Neighborhood(neighborhood_name="Cow Hollow")
    n6 = Neighborhood(neighborhood_name="Presidio Heights")
    n7 = Neighborhood(neighborhood_name="Seacliff")
    n8 = Neighborhood(neighborhood_name="Pacific Heights")
    n9 = Neighborhood(neighborhood_name="Nob Hill")
    n10 = Neighborhood(neighborhood_name="Financial District")
    n11 = Neighborhood(neighborhood_name="China Town")

    n12 = Neighborhood(neighborhood_name="South of Market")
    n13 = Neighborhood(neighborhood_name="Mission")
    n14 = Neighborhood(neighborhood_name="Potrero Hill")
    n15 = Neighborhood(neighborhood_name="Castro")
    n16 = Neighborhood(neighborhood_name="Noe Valley")
    n17 = Neighborhood(neighborhood_name="Bernal Heights")
    n18 = Neighborhood(neighborhood_name="Twin Peaks")
    n19 = Neighborhood(neighborhood_name="Haight Ashbury")
    
    n20 = Neighborhood(neighborhood_name="Richmond District") # Inner/outer richmond
    n21 = Neighborhood(neighborhood_name="Sunset District") # Inner/Outer sunset
    n22 = Neighborhood(neighborhood_name="Parkside")
    n23 = Neighborhood(neighborhood_name="Lakeshore")
    n24 = Neighborhood(neighborhood_name="Ocean View")
    n25 = Neighborhood(neighborhood_name="Bayview")

    db.session.add_all([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25])
    db.session.commit()
    



if __name__ == "__main__":

    connect_to_db(app)

    # load_restaurants(results)
    # set_val_gf_types_table()
    # set_val_neighborhoods_table()


