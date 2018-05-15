import os

from flask import Flask, render_template, request, redirect, session

from model import connect_to_db, db, User, Restaurant, Favorite_restaurant, GF_type, Restaurant_type, Neighborhood
from flask_debugtoolbar import DebugToolbarExtension

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



@app.route('/signup')
def register():
    """ Display sign up form. """

    return render_template("signup.html")



@app.route('/thankyou', methods=["POST"])
def thank_user():
    """ Thank the user & store their information in the database. """

    fname = request.form.get("firstname")
    lname = request.form.get("lastname")
    email = request.form.get("email")
    confirm_email = request.form.get("confirm_email")
    zipcode = request.form.get("zipcode")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    terms = request.form.get("terms")

    user_info = User(fname=fname, lname=lname, email=email, zipcode=zipcode, password=password)

    # Add user information to the database.
    db.session.add(user_info)
    db.session.commit()


    return render_template("thankyou.html", name=fname)










################################################################################

if __name__ == "__main__": 

    app.debug = True
    connect_to_db(app)


    app.run(port=5000, host="0.0.0.0")