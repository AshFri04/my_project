import os

from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Restaurant, Favorite_restaurant, GF_type, Restaurant_type, Neighborhood

from passlib.hash import pbkdf2_sha256

from datetime import datetime

from random import choice

from werkzeug.utils import secure_filename


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'ABC'

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

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

    first_name = request.form.get("firstname")
    lname = request.form.get("lastname")
    email = request.form.get("email")
    confirm_email = request.form.get("confirm_email")
    zipcode = request.form.get("zipcode")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    terms = request.form.get("terms")

# FIX BUG WITH ZIPCODE!!
    fname = first_name.capitalize()

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
        return redirect('/profile')
    
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
# CREATE AJAX!!
            flash("Great to have you back, {}!".format(user.fname))
            return redirect("/profile")
# CREATE AJAX!
# Why doesn't the else work here
    flash("The email or password you've entered does not match any of our accounts. \n Please try again.")
    return redirect('/login')



# @app.route('/display_mainpage')
# def display_login_mainpage():
#     """ Display the main page after user logs in. """

#     return render_template("login_mainpage.html")

@app.route('/sign_out')
def sign_out():
    """ Sign out of user's account. """
    
    session.clear()
        
    return render_template("sign_out.html")


################################################################################

# User Profile Routes

@app.route('/profile')
def display_profile():
    """ Display user profile. """

    user_id = session['user_id']

    user_object = User.query.filter_by(user_id=user_id).first()
    fav_restaurants = user_object.favorite_restaurants

    restaurants = Restaurant.query.all()

    random_restaurant = choice(restaurants)

    return render_template('user_profile.html', restaurants=fav_restaurants, user=user_object, random=random_restaurant)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """ """
    user_id = session.get('user_id')
    path = str(user_id) + '.jpg'
    if request.method == 'POST' and 'photo' in request.files:
       request.files['photo'].filename = path
       filename = photos.save(request.files['photo'])
       user = User.query.get(user_id)
       user.photo = '/' + app.config['UPLOADED_PHOTOS_DEST'] + '/' + path
       db.session.commit()

    flash("You've successfully loaded your photo to your profile!")
    return redirect('/profile')



        # file = request.files['file']
        # (if user does not select file, browser also)
        # (submit an empty part without filename)
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file',
        #                             filename=filename))




@app.route('/rest_info', methods=["POST"])
def display_transactions():
    """ Display restaurant information."""

    user_id = session["user_id"]
    rest_id = request.form.get("rest_id")

    restaurant = Restaurant.query.filter_by(restaurant_id=rest_id).first()
    
    try:
        # Start time
        mon_start = restaurant.hours_of_operation[0]["start"]
        m_start_hour = mon_start[:-2]
        m_start_minute = mon_start[-2:]
        m_start = m_start_hour + ':' + m_start_minute
        # End time
        mon_end = restaurant.hours_of_operation[0]["end"]
        m_end_hour = mon_end[:-2]
        m_end_minute = mon_end[-2:]
        m_end = m_end_hour + ':' + m_end_minute
        # Hours of Operation
        m_hours = datetime.strptime(m_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.strptime(m_end,'%H:%M').strftime('%I:%M %p')
    except:
        m_hours = "Closed"


    try:
        # Start time
        tues_start = restaurant.hours_of_operation[1]["start"]
        t_start_hour = tues_start[:-2]
        t_start_minute = tues_start[-2:]
        t_start = t_start_hour + ':' + t_start_minute
        # End time
        tues_end = restaurant.hours_of_operation[1]["end"]
        t_end_hour = tues_end[:-2]
        t_end_minute = tues_end[-2:]
        t_end = t_end_hour + ':' + t_end_minute
        # Hours of Operation
        t_hours = datetime.strptime(t_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.strptime(t_end,'%H:%M').strftime('%I:%M %p')
    except:
        t_hours = 'Closed'


    try:
        # Start time
        wedn_start = restaurant.hours_of_operation[2]["start"]
        w_start_hour = wedn_start[:-2]
        w_start_minute = wedn_start[-2:]
        w_start = w_start_hour + ':' + w_start_minute
        # End time
        wedn_end = restaurant.hours_of_operation[2]["end"]
        w_end_hour = wedn_end[:-2]
        w_end_minute = wedn_end[-2:]
        w_end = w_end_hour + ':' + w_end_minute
        # Hours of Operation
        w_hours = datetime.strptime(w_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.strptime(w_end,'%H:%M').strftime('%I:%M %p')
    except:
        w_hours = 'Closed'


    try:
        # Start time
        thurs_start = restaurant.hours_of_operation[3]["start"]
        th_start_hour = thurs_start[:-2]
        th_start_minute = thurs_start[-2:]
        th_start = th_start_hour + ':' + th_start_minute
        # End time
        thurs_end = restaurant.hours_of_operation[3]["end"]
        th_end_hour = thurs_end[:-2]
        th_end_minute = thurs_end[-2:]
        th_end = th_end_hour + ':' + th_end_minute
        # Hours of Operation
        th_hours = datetime.strptime(th_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.strptime(th_end,'%H:%M').strftime('%I:%M %p')
    except:
        th_hours = 'Closed'


    try:
        # Start time
        fri_start = restaurant.hours_of_operation[4]["start"]
        f_start_hour = fri_start[:-2]
        f_start_minute = fri_start[-2:]
        f_start = f_start_hour + ':' + f_start_minute
        # End time
        fri_end = restaurant.hours_of_operation[4]["end"]
        f_end_hour = fri_end[:-2]
        f_end_minute = fri_end[-2:]
        f_end = f_end_hour + ':' + f_end_minute
        # Hours of Operation
        f_hours = datetime.strptime(f_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.strptime(f_end,'%H:%M').strftime('%I:%M %p')
    except:
        f_hours = 'Closed'

    try:    
        # Start time
        sat_start = restaurant.hours_of_operation[5]["start"]
        sa_start_hour = sat_start[:-2]
        sa_start_minute = sat_start[-2:]
        sa_start = sa_start_hour + ':' + sa_start_minute
        # End time
        sat_end = restaurant.hours_of_operation[5]["end"]
        sa_end_hour = sat_end[:-2]
        sa_end_minute = sat_end[-2:]
        sa_end = sa_end_hour + ':' + sa_end_minute
        # Hours of Operation
        sa_hours = datetime.strptime(sa_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.strptime(sa_end,'%H:%M').strftime('%I:%M %p')
    except:
        sa_hours = 'Closed'


    try:
        # Start time
        sun_start = restaurant.hours_of_operation[6]["start"]
        s_start_hour = sun_start[:-2]
        s_start_minute = sun_start[-2:]
        su_start = s_start_hour + ':' + s_start_minute
        # End time
        sun_end = restaurant.hours_of_operation[6]["end"]
        s_end_hour = sun_end[:-2]
        s_end_minute = sun_end[-2:]
        su_end = s_end_hour + ':' + s_end_minute
        # Hours of Operation
        su_hours = datetime.strptime(su_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.strptime(su_end,'%H:%M').strftime('%I:%M %p')
    except:
        su_hours = 'Closed'


    return render_template("restaurant_info.html", restaurant=restaurant, m_hours=m_hours, t_hours=t_hours, w_hours=w_hours, th_hours=th_hours, f_hours=f_hours, sa_hours=sa_hours, su_hours=su_hours)

   

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

@app.route('/favorite', methods=["POST"])
def add_favorite_restaurant():
    """Adds a restaurant to user's favorites in db when user clicks favorites button."""

    user_id = session["user_id"]

    rest_id = request.form.get("restaurant_id")
    restaurant_name = request.form.get("restaurant_name")
    restaurant_id = int(rest_id)

    fav_restaurant_db = Favorite_restaurant.query.filter(Favorite_restaurant.restaurant_id == restaurant_id).first()

    if fav_restaurant_db:

        # Way to confirm on the front end that this AJAX request/response was successful
        return "{} is already one of your favorites!".format(restaurant_name)


    else:
       
        new_fav_restaurant = Favorite_restaurant(restaurant_id=restaurant_id, user_id=user_id)

        db.session.add(new_fav_restaurant)
        db.session.commit()

        # Way to confirm on the front end that this AJAX request/response was successful
        return "{} is now in your favorites!".format(restaurant_name)




# ################################################################################

# Neighborhoods and their associated restaurants/bakeries routes




@app.route("/restaurants")
def search_by_neighborhood():
    """ Display all restaurants and bakeries that are in the neighborhood the user choose."""

    user_choice = request.args.get("neighborhood") # (dropdown bar) name=neighborhood on html side

    restaurants = Restaurant.query.filter(Restaurant.neighborhood_id==user_choice).all()

    neighborhood = Neighborhood.query.filter(Neighborhood.neighborhood_id==user_choice).first()
    # bakeries = db.session.query(Restaurant).join(Restaurant_type).filter(Restaurant.neighborhood_id==user_choice, Restaurant_type.gf_type_id==3).all()

    return render_template("restaurants.html", restaurants=restaurants, neighborhood=neighborhood)



@app.route("/is-glutie")
def display_if_glutie():
    """ Display glutie restaurant that user typed in. """


    rest_objects = Restaurant.query.all()
  

    user_choice = request.args.get("place").title()
  
    restaurant = None

    for r in rest_objects:
        # rest = restaurant.name
        # restaurants.append(rest)
        if user_choice in r.name:
            restaurant = r

    if restaurant:
        return render_template("found-glutie.html", restaurant=restaurant)
    else:
        return render_template("googlemaps.html")



@app.route("/restaurants-all")
def display_all_restaurants():
    """ Display all restaurants in San Francisco;

        Sort by neighborhood, open now, delivery, pickup, reservation & price. """

    food_types = ('Southern', 'Seafood', 'American', 'Tapas/Small Plates', 'French', 'Pizza', 'Breakfast', 'Wings', 'Moroccan', 'Burgers', 'Sandwiches', 'Mexican')

    restaurants = []

    rest_objects = Restaurant.query.all()

    for restaurant in rest_objects:
        food1 = restaurant.types_of_food
        foods = food1.split()
        print foods
        print
        for food in foods:
            if food in food_types:
                restaurants.append(restaurant)
                break

    return render_template("restaurants-all.html", restaurants=restaurants)



@app.route("/bakeries-all")
def display_all_bakeries():
    """ Display all bakeries in San Francisco;

        Sort by neighborhood, open now, delivery, pickup, reservation & price. """


    restaurants = Restaurant.query.filter(Restaurant.types_of_food.in_(['bakery', 'bakeries', 'Bakeries', 'Bakery'])).all()

    neighborhood = Neighborhood.query.filter(Neighborhood.neighborhood_id).all()

    return render_template("restaurants.html", restaurants=restaurants, neighborhood=neighborhood)



@app.route("/bars-all")
def display_all_bars():
    """ Display all bakeries in San Francisco;

        Sort by neighborhood, open now, delivery, pickup, reservation & price. """


    restaurants = Restaurant.query.filter(Restaurant.types_of_food.in_(['bar', 'Bar'])).all()

    neighborhood = Neighborhood.query.filter(Neighborhood.neighborhood_id).all()

    return render_template("restaurants.html", restaurants=restaurants, neighborhood=neighborhood)



@app.route("/coffee-shops-all")
def display_all_coffee_shops():
    """ Display all coffee shops in San Francisco;

        Sort by neighborhood, open now, delivery, pickup, reservation & price. """


    restaurants = Restaurant.query.filter(Restaurant.types_of_food.in_(['coffee', 'tea', 'Coffee', 'Tea', 'Sandwiches'])).all()
    # (or if cafe in name) Sandwiches?
    neighborhood = Neighborhood.query.filter(Neighborhood.neighborhood_id).all()

    return render_template("restaurants.html", restaurants=restaurants, neighborhood=neighborhood)

# @app.route('/restaurant.json')
# def restaurant_info():
#     """ JSON information about restaurants. """

#     neighborhood = request.form.get("neighborhood_id")
    
#     restaurants = Restaurant.query.filter(Restaurant.neighborhood_id==neighborhood).all()

#     all_rest_info = {}

#     for restaurant in restaurants:
#         rest_info = {
#         "name": restaurant.name,
#         "type_of_food": restaurant.type_of_food
#         }
    
#         all_rest_info[restaurant.restaurant_id] = rest_info

#     return jsonify(all_rest_info)

@app.route("/googlemaps")
def display_map():
    """ """

    return render_template("googlemaptest.html")








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