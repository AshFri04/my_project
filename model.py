""" Models for Gluten-Free WebApp Project. """

from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()

#############################################################################
# Model definitions

class Users(db.Model):
    """ Users of our website; stored in a database. """

    __tablename__ = "users"

    user_id = db.Column(Integer, primary_key=True, autoincrement=True)
    fname = db.Column(String(25))
    lname = db.Column(String(25))
    email = db.Column(String(25))
    password = db.Column(String(25))
    favorites = db.Column(String(25))

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Users user_id={} fname={} lname={} email={} favorites={}>".format(self.user_id, self.fname, self.lname, self.email, self.favorites)


class Restaurants(db.Model):
    """ Restaurants used in our website; stored in a database. """

    __tablename__ = "restaurants"

    restaurant_id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50))
    phone_number = db.Column(Integer)
    picture = db.Column(String(75))
    menu_url= db.Column(String(50))
    website_url = db.Column(String(50))
    last_update = db.Column(Integer)
    avg_rating = db.Column(Integer)
    neighborhood_id = db.Column(Integer)
    GF_type_id = db.Column(Integer)

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Restaurants restaurant_id={} name={} phone_number={} picture={} menu_url={} website_url={} last_update={} avg_rating={} neighborhood_id={} GF_type_id={}>".format(self.restaurant_id, self.name, self.phone_number, self.picture, self.menu_url, self.website_url, self.last_update, self.avg_rating, self.neighborhood_id, self.GF_type_id)


class Favorite_restaurants(db.Model):
    """ Association Table: restaurant id and user id; stored in a database."""

    __tablename__ = "favorite_restaurants"

    user_id = db.Column(Integer)
    restaurant_id = db.Column(Integer)

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Favorite_restaurants user_id={} restaurant_id={}>".format(self.user_id, self.restaurant_id)



class GF_types(db.Model):
    """ 3 Types: Completely GF, GF options and GF bakeries; stored in a database."""

    __tablename__ = "GF_types"

    GF_type_id = db.Column(Integer, primary_key=True)
    GF_type = db.Column(String(50))


class Neighborhoods(db.Model):
    """ SF neighborhoods used in our website; stored in a database. """

    __tablename__ = "neighborhoods"

    neighborhood_id = db.Column(Integer, primary_key=True)
    neighborhood_name = db.Column(String(50))

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Neighborhoods neighborhood_id={} neighborhood_name={}>".format(self.neighborhood_id, self.neighborhood_name)



class Ratings(db.Model):
    """ 1-5 Star rating for each restaurant; stored in a database. """

    __tablename__ = "ratings"

    rating_id = db.Column(Integer, primary_key=True)
    restaurant_id = db.Column(Integer)

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Ratings rating_id={} restaurant_id={}>".format(self.rating_id, self.restaurant_id)



