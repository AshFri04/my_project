
""" Models for Gluten-Free WebApp Project. """

from flask_sqlalchemy import SQLAlchemy
import pdb
db = SQLAlchemy()

#############################################################################
# Model definitions

class User(db.Model):
    """ Users of our website; stored in a database. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(150))
    zipcode = db.Column(db.Integer)
    # photo = db.Column(db.String(150))

    # Relationship between users, restaurants and favorite_restaurants.
    favorite_restaurants = db.relationship("Restaurant", secondary="favorite_restaurants", backref="users")


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<User user_id={} fname={} lname={} email={} zipcode={}>".format(self.user_id, self.fname, self.lname, self.email, self.zipcode)



class Restaurant(db.Model):
    """ Restaurants used in our website; stored in a database. """

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    menu_url= db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    # last_update = db.Column(db.DateTime)
    avg_rating = db.Column(db.Integer)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'))
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    transactions = db.Column(db.JSON)
    price = db.Column(db.String(255))
    types_of_food = db.Column(db.String(255))
    hours_of_operation = db.Column(db.JSON)

    # Relationships between neighborhoods table and restaurants table in the database.
    neighborhood = db.relationship("Neighborhood", backref='restaurants')


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Restaurant restaurant_id={}>".format(Restaurant.restaurant_id)



class Favorite_restaurant(db.Model):
    """ Association Table: restaurant id and user id; stored in a database."""

    __tablename__ = "favorite_restaurants"

    favorite_restaurant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Favorite_restaurant user_id={} restaurant_id={}>".format(self.favorite_restaurant_id, self.user_id, self.restaurant_id)



class GF_type(db.Model):
    """ 3 Types: Completely GF, GF options and GF bakeries; stored in a database."""

    __tablename__ = "gf_types"

    gf_type_id = db.Column(db.Integer, primary_key=True)
    gf_type = db.Column(db.String(100))

    # Relationship between GF_type, restaurants and estaurant_types.
    restaurant = db.relationship("Restaurant", secondary="restaurant_types", backref="GF_type")


    def __repr__(self):
        """ Provide helpful representation when printed. """
        
        return "<GF_type gf_type_id={} gf_type={}>".format(self.gf_type_id, self.gf_type)



class Restaurant_type(db.Model):
    """ Association Table: gf_type and restaurant_id; stored in a database. """

    __tablename__ = "restaurant_types"

    restaurant_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gf_type_id = db.Column(db.Integer, db.ForeignKey('gf_types.gf_type_id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))



    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Restaurant_type restaurant_type_id={} gf_type_id={} restaurant_id={}>".format(self.restaurant_type_id, self.gf_type_id, self.restaurant_id)



class Neighborhood(db.Model):
    """ SF neighborhoods used in our website; stored in a database. """

    __tablename__ = "neighborhoods"

    neighborhood_id = db.Column(db.Integer, primary_key=True)
    neighborhood_name = db.Column(db.String(50))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Neighborhood neighborhood_id={} neighborhood_name={}>".format(self.neighborhood_id, self.neighborhood_name)



#############################################################################
# # Helper functions

def connect_to_db(app, db_uri="postgresql:///gluten_free"):
    """ Connect the database to my Flask app. """

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gluten_free'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to Database."



