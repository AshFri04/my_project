""" Models for Gluten-Free WebApp Project. """

from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()

#############################################################################
# Model definitions

class User(db.Model):
    """ Users of our website; stored in a database. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    email = db.Column(db.String(75))
    password = db.Column(db.String(25))

    # Relationship between users, restaurants and favorite_restaurants.
    favorite_restaurants = db.relationship("Restaurant", secondary="favorite_restaurants",                                  backref="users")


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<User user_id={} fname={} lname={} email={}>".format(self.user_id, self.fname, self.lname, self.email)



class Restaurant(db.Model):
    """ Restaurants used in our website; stored in a database. """

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone_number = db.Column(db.Integer)
    picture = db.Column(db.String(75))
    menu_url= db.Column(db.String(50))
    website_url = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)
    avg_rating = db.Column(db.Integer)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'))
    gf_type_id = db.Column(db.Integer, db.ForeignKey('gf_types.gf_type_id'))

    # Relationships between neighborhoods table and restaurants table in the database.
    neighborhood = db.relationship("Neighborhood", backref='restaurants')


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Restaurant restaurant_id={} name={} phone_number={} picture={} menu_url={} website_url={} last_update={} avg_rating={} neighborhood_id={} gf_type_id={}>".format(self.restaurant_id, self.name, self.phone_number, self.picture, self.menu_url, self.website_url, self.last_update, self.avg_rating, self.neighborhood_id, self.gf_type_id)



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
    gf_type = db.Column(db.String(50))

    # Relationship between GF_type, restaurants and estaurant_types.
    restaurant_type = db.relationship("Restaurant", secondary="restaurant_types",                                  backref="GF_type")


    def __repr__(self):
        """ Provide helpful representation when printed. """
        
        return "<GF_type gf_type_id={} gf_type={}>".format(self.gf_type_id, self.gf_type)



class Restaurant_type(db.Model):
    """ Association Table: gf_type and restaurant_id; stored in a database. """

    __tablename__ = "restaurant_types"

    restaurant_type_id = db.Column(db.Integer, primary_key=True)
    gf_type_id = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer)


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Restaurant_type restaurant_type_id={} gf_type_id={} restaurant_id={}>".format(self.restaurant_type_id, self.gf_type_id, self.restaurant_id)



class Neighborhood(db.Model):
    """ SF neighborhoods used in our website; stored in a database. """

    __tablename__ = "neighborhoods"

    neighborhood_id = db.Column(db.Integer, primary_key=True)
    neighborhood_name = db.Column(db.String(50))


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Neighborhood neighborhood_id={} neighborhood_name={}>".format(self.neighborhood_id, self.neighborhood_name)






