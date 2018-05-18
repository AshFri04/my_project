import os

from flask import Flask, render_template, request, redirect, session, flash

from model import connect_to_db, db, User, Restaurant, Favorite_restaurant, GF_type, Restaurant_type, Neighborhood
from flask_debugtoolbar import DebugToolbarExtension

from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'ABC'

api_key = os.environ['YELP_ACCESS_KEY']
client_id = os.environ['YELP_CLIENT_ID']

################################################################################


@app.route('/')
def homepage():
    """ Display homepage. """

    return render_template("homepage.html")


################################################################################

# Account related routes


@app.route('/signup')
def register():
    """ Display sign up form. """

    return render_template("signup.html")



@app.route('/thankyou', methods=["POST"])
def register_process():
    """ Process registration and thank the user for signing up. """

    fname = request.form.get("firstname")
    lname = request.form.get("lastname")
    email = request.form.get("email")
    confirm_email = request.form.get("confirm_email")
    zipcode = request.form.get("zipcode")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    terms = request.form.get("terms")

    password_hash = pbkdf2_sha256.hash(password)

    if email == confirm_email:
        if password == confirm_password:
            if User.query.filter_by(email=email).first():
                flash("This email address is already registered.")
                return redirect('/signup')
            else:
                user_info = User(fname=fname, lname=lname, email=email, zipcode=zipcode, password=password_hash)

                # Add user information to the database.
                db.session.add(user_info)
                db.session.commit()

                # Add user information to the session
                session["user_id"] = user_info.user_id
                session["email"] = user_info.email
                session["fname"] = user_info.fname

                return render_template("thankyou.html", name=fname)
        else:
            flash("Passwords do not match. Please try again.")
            return redirect('/signup')
    else:
        flash("Emails do not match. Please try again.")
        return redirect('/signup')



@app.route('/login', methods=["GET"])
def login():
    """ Display login form. """

    if session.get('user_id'):
        return redirect('/login_mainpage1')
    
    return render_template("login.html")



@app.route('/login_mainpage', methods=["POST"])
def login_process():
    """ Process login information; log a user into their account. """


    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        if pbkdf2_sha256.verify(password, user.password):
            session['user_id'] = user.user_id
            session['email'] = user.email
            session['fname'] =user.fname
            flash("Great to have you back, {}!".format(user.fname))
            return render_template("login_mainpage.html")

# Why doesn't the else work here
    flash("The email or password you've entered does not match any of our accounts. \n Please try again.")
    return redirect('/login')



@app.route('/login_mainpage1')
def display_login_mainpage():
    """ Display the main page after user logs in. """

    return render_template("login_mainpage.html")

@app.route('/sign_out')
def sign_out():
    """ Sign out of user's account. """
    
    session.clear()
        
    return render_template("sign_out.html")

# @app.route()
# def delete_account():
#     """ User deletes their account. """

#     pass

# @app.route()
# def change_password():
#     """ User changes their password. """

#     pass

# @app.route()
# def change_email():
#     """ User changes their email. """

#     pass

# @app.route()
# def update_account():
#     """ User updates their account. """

#     pass

# ################################################################################

# Neighborhoods and their associated restaurants/bakeries routes

# @app.route("/restaurants")
# def display_restaurants_northbeach():
#     """ Display all restaurants that are in North Beach."""


#     restaurants = db.session.query(Restaurant).join(Restaurant_type).filter(Restaurant.neighborhood_id==1, Restaurant_type.gf_type_id==2).all()

#     return render_template("restaurants.html", restaurants=restaurants)


# @app.route("/restaurants_and_bakeries")
# def display_all_northbeach():
#     """ Display all restaurants and bakeriesthat are in North Beach."""

#     # if user clicks on north beach in search
#     # return all restaurants and bakeries for that neighborhood
#     # dict of neighborhood ids and their associated values



#     restaurants = Restaurant.query.filter_by(neighborhood_id=1).all()

#     return render_template("restaurants.html", restaurants=restaurants)

@app.route("/restaurants")
def display_restaurants_northbeach():
    """ Display all restaurants that are in North Beach."""

    user_choice = request.args.get("neighborhood") # (dropdown bar) name=neighborhood on html side

    restaurants = db.session.query(Restaurant).join(Restaurant_type).filter(Restaurant.neighborhood_id==user_choice, Restaurant_type.gf_type_id==2).all()

    bakeries = db.session.query(Restaurant).join(Restaurant_type).filter(Restaurant.neighborhood_id==user_choice, Restaurant_type.gf_type_id==3).all()


    return render_template("restaurants.html", restaurants=restaurants, bakeries=bakeries)








# ################################################################################
# @app.route("/only_gf")
# def only_gf():
#     """ Display restaurants that are Completely Gluten Free."""

#     pass


# app.route("/restaurants_gf_options")
# def only_gf():
#     """ Display restaurants that have Gluten Free Options on their menu."""

#     pass


# app.route("/bakery_gf_options")
# def only_gf():
#     """ Display bakeries that have Gluten Free Options on their menu."""

#     pass


# # query restaurants table from there pass neigh id/ gf type










################################################################################

if __name__ == "__main__": 

    app.debug = True
    connect_to_db(app)


    app.run(port=5000, host="0.0.0.0")