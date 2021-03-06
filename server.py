import os

from flask import Flask, render_template, request, redirect, session, flash, jsonify, url_for
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Restaurant, Favorite_restaurant, GF_type, Restaurant_type, Neighborhood

from passlib.hash import pbkdf2_sha256

from datetime import datetime

from random import choice


app = Flask(__name__)
bcrypt = Bcrypt(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ["FLASK_SECRET_KEY"]


api_key = os.environ['YELP_ACCESS_KEY']
client_id = os.environ['YELP_CLIENT_ID']
google_maps_key = os.environ['GOOGLE_MAPS_API_KEY']


################################################################################

# Landing Page

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
    """ Process registration/add to db and thank the user for signing up. """

    first_name = request.form.get("firstname")
    lname = request.form.get("lastname")
    email = request.form.get("email")
    confirm_email = request.form.get("confirm_email")
    zipcode = request.form.get("zipcode")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    terms = request.form.get("terms")

    fname = first_name.capitalize()

    # bcrypt password encryption with a work factor of 10
    # (Work factor value determines how slow the hash function will be)
    pw_hash = bcrypt.generate_password_hash(password, 10)

    if email == confirm_email:
        if password == confirm_password:
            if User.query.filter_by(email=email).first():
                flash("This email address is already registered.")
                return redirect('/signup')
            else:
                user_info = User(fname=fname, lname=lname, email=email, zipcode=zipcode, password=pw_hash)

                # Add user information to the database.
                db.session.add(user_info)
                db.session.commit()

                # Add user information to the session
                session["user_id"] = user_info.user_id
                session["email"] = user_info.email
                session["fname"] = user_info.fname

                return redirect('/profile')
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
    candidate = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    pw_hash = user.password

    if user:
        # Helps to prevent timing attacks
        if bcrypt.check_password_hash(pw_hash, candidate):  # returns True
            session['user_id'] = user.user_id
            session['email'] = user.email
            session['fname'] =user.fname

            return redirect("/profile")

    flash("The email or password you've entered does not match any of our accounts. \n Please try again.")
    return redirect('/login')



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


@app.route('/favorite', methods=["POST"])
def add_favorite_restaurant():
    """Adds a restaurant to user's favorites in db when user clicks favorites button."""

    user_id = session["user_id"]

    rest_id = request.form.get("restaurant_id")
    restaurant_name = request.form.get("restaurant_name")
    restaurant_id = int(rest_id)

    fav_restaurant_db = Favorite_restaurant.query.filter(Favorite_restaurant.restaurant_id == restaurant_id).first()

    if fav_restaurant_db:

        # AJAX call: confirms that restaurant was already added to favorites.
        return "{} is already one of your favorites!".format(restaurant_name)


    else:

        new_fav_restaurant = Favorite_restaurant(restaurant_id=restaurant_id, user_id=user_id)

        db.session.add(new_fav_restaurant)
        db.session.commit()

        # AJAX call: confirms that restaurant was added to favorites.
        return "{} is now in your favorites!".format(restaurant_name)


################################################################################

# Routes initiated with User clicks on option 1 & 2 on Homepage


@app.route("/is-glutie")
def display_if_glutie():
    """ Display restaurant that user typed in - checking to see if its a Glutie or not. """


    rest_objects = Restaurant.query.all()
    user_choice = request.args.get("place").title()
  
    restaurant = None

    for r in rest_objects:
        if user_choice in r.name:
            restaurant = r

    if restaurant:
        return render_template("found-glutie.html", restaurant=restaurant, restaurants=rest_objects)
    else:
        return render_template("googlemaptest.html", restaurant=rest_objects)



@app.route("/restaurants")
def search_by_neighborhood():
    """ Display all restaurants and bakeries that are in the neighborhood the user choose."""


    user_choice = request.args.get("neighborhood") # (dropdown bar) name=neighborhood on html side

    restaurants = Restaurant.query.filter(Restaurant.neighborhood_id==user_choice).all()

    neighborhood = Neighborhood.query.filter(Neighborhood.neighborhood_id==user_choice).first()
  
    return render_template("restaurants.html", key=google_maps_key, restaurants=restaurants, neighborhood=neighborhood)


################################################################################

# Routes used when User is using the 'Filter By Search' option in NavBar

@app.route("/search")
def display_options():
    """ Displays features for the user to filter out their search. """

    return render_template("filter-search.html")


@app.route("/search-results")
def display_search_results():
    """ Display search results from user input in Filter By Search Page. """

    restaurant = request.args.get("restaurants")
    bakery = request.args.get("bakeries")
    bar = request.args.get("bars")
    coffee_shop = request.args.get("coffee-shops")

    open_now = request.args.get("open")
    price = request.args.get("price")
    neighborhood = request.args.get("neighborhoods")

    if neighborhood == 'False':
        rest_objects = Restaurant.query.all()
    else:
        rest_objects = Restaurant.query.filter(Restaurant.neighborhood_id==neighborhood).all() 

    results = []
    open_restaurants = []

    if open_now:
        for restaurant in results:
            rest_hours = restaurant.hours_of_operation
            for hours in rest_hours[0:]:
                if hours["day"] == 0 and datetime.date.today().strftime("%w") == '0':
                    time = str(datetime.datetime.now()).split(" ")
                    time1 = time[1][0:5].split(":")
                    time2 = "".join(time1)
                    if int(time2) in range(int(hours['start']), int(hours['end']) + 1):
                        open_restaurants.append(restaurant)
                elif hours["day"] == 1 and datetime.date.today().strftime("%w") == '1':
                    time = str(datetime.datetime.now()).split(" ")
                    time1 = time[1][0:5].split(":")
                    time2 = "".join(time1)
                    if int(time2) in range(int(hours['start']), int(hours['end']) + 1):
                        open_restaurants.append(restaurant)
                elif hours["day"] == 2 and datetime.date.today().strftime("%w") == '2':
                    time = str(datetime.datetime.now()).split(" ")
                    time1 = time[1][0:5].split(":")
                    time2 = "".join(time1)
                    if int(time2) in range(int(hours['start']), int(hours['end']) + 1):
                        open_restaurants.append(restaurant)
                elif hours["day"] == 3 and datetime.date.today().strftime("%w") == '3':
                    time = str(datetime.datetime.now()).split(" ")
                    time1 = time[1][0:5].split(":")
                    time2 = "".join(time1)
                    if int(time2) in range(int(hours['start']), int(hours['end']) + 1):
                        open_restaurants.append(restaurant)
                elif hours["day"] == 4 and datetime.date.today().strftime("%w") == '4':
                    time = str(datetime.datetime.now()).split(" ")
                    time1 = time[1][0:5].split(":")
                    time2 = "".join(time1)
                    if int(time2) in range(int(hours['start']), int(hours['end']) + 1):
                        open_restaurants.append(restaurant)
                elif hours["day"] == 5 and datetime.date.today().strftime("%w") == '5':
                    time = str(datetime.datetime.now()).split(" ")
                    time1 = time[1][0:5].split(":")
                    time2 = "".join(time1)
                    if int(time2) in range(int(hours['start']), int(hours['end']) + 1):
                        open_restaurants.append(restaurant)
                elif hours["day"] == 6 and datetime.date.today().strftime("%w") == 6:
                    time = str(datetime.datetime.now()).split(" ")
                    time1 = time[1][0:5].split(":")
                    time2 = "".join(time1)
                    if int(time2) in range(int(hours['start']), int(hours['end']) + 1):
                        open_restaurants.append(restaurant)


    
    restaurants = []
    if restaurant:
        # If user chooses restaurants
        food_types = ('Southern', 'Seafood', 'American', 'Tapas/Small Plates', 'French', 'Pizza', 'Breakfast', 'Wings', 'Moroccan', 'Burgers', 'Sandwiches', 'Mexican')
        for restaurant in rest_objects:
            food1 = restaurant.types_of_food
            foods = food1.split()
            if 'Bakeries' not in foods and "Cafe" not in foods and "Coffee" not in foods: 
                for food in foods:
                    if food in food_types:
                        restaurants.append(restaurant)
       
        if price:
            rest_prices = Restaurant.query.filter(Restaurant.price==price).all()
            for rest in rest_prices:
                if rest in restaurants and rest not in results:
                    results.append(rest)


    bakeries = []
    if bakery:
        # If user chooses bakeries
        bakery_names = ['Bakeries', 'Bakery']
        for bakery in rest_objects:
            bakery1 = bakery.types_of_food
            treats = bakery1.split()
            # print treats
            for treat in treats:
                if treat in bakery_names:
                    bakeries.append(bakery)
            
        if price:
            bakery_prices = Restaurant.query.filter(Restaurant.price==price).all()
            for b in bakery_prices:
                if b in bakeries and b not in results:
                    print b
                    results.append(b)


    bars = []
    if bar:
        # If user chooses bars
        bar_names = ['Bars', 'Bar', 'Wine', 'Cocktail']
        for bar in rest_objects:
            bar1 = bar.types_of_food
            drinks = bar1.split()
            for drink in drinks:
                if drink in bar_names:
                    bars.append(bar)
                    
        if price:
            bar_prices = Restaurant.query.filter(Restaurant.price==price).all()
            for bar in bar_prices:
                if bar in bars and bar not in results:
                    results.append(bar)

    coffee_shops = []
    if coffee_shop:
        # If user chooses coffee shops
        shops_names = ('coffee', 'tea', 'Coffee', 'Tea', 'Sandwiches')
        for shop in rest_objects:
            coffee1 = shop.types_of_food
            shops = coffee1.split()
            for shop in shops:
                if shop in shops_names:
                    coffee_shops.append(shop)
                    
        if price:
            print price
            coffee_prices = Restaurant.query.filter(Restaurant.price==price).all()
            for coffee in coffee_prices:
                if coffee in coffee_shops and coffee not in results:
                    results.append(coffee)

                   
    return render_template("search-categories.html", key=google_maps_key, results=results, open_restaurants=results, neighborhood=neighborhood)


################################################################################



# def convert_military_to_pretty_time(start_time, end_time):

#      datetime.datetime.strptime(x,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(x,'%H:%M').strftime('%I:%M %p')


@app.route('/rest_info', methods=["POST"])
def display_transactions():
    """ Display restaurant information."""

  
    rest_id = request.form.get("rest_id")

    restaurant = Restaurant.query.filter_by(restaurant_id=rest_id).first()
    rest_hours = restaurant.hours_of_operation

    # day_mappings = { 0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday" }

    # # Ex: [ 0, 3, 4 ]
    # days_that_have_schedules = map(lambda x: day_mappings[x], rest_hours)
    # # Ex: [ 1, 2, 5, 6 ]
    # days_missing_schedules = set(day_mappings.keys()) - set(days_that_have_schedules)

    # # Ex: [ { "start": 0800, "end": 2000, "day": "Monday"}, { "start": 0700, "end": 2200, "day": "Tuesday"} ]
    # open_hours = map(lambda x: { "hours": convert_military_to_pretty_time(x["start"], x["end"]), "day": day_mappings[x]}, day_mappings)

    # # Ex: [ { "start": 0000, "end": 0000, "day": "Wednesday"} ]
    # closed_hours = map(lambda x: { "hours": "closed", "day": day_mappings[x]}, days_missing_schedules)
    # hours_of_op = open_hours + closed_hours
    # hours_of_op_map = {}
    # map(lambda x: { hours_of_op_map[x["day"]] = x }, hours_of_op)

    # today = day_mappings[datetime.date.today().strftime("%w")]
    # if today in open_hours and ():
    #     then its open now

    # { "Monday": { "start": 0800, "end": 2000, "day": "Monday"}, "Tuesday": { "start": 0000, "end": 0000, "day"}}
  
    # for hours in rest_hours[0:]:
    #     if hours["day"] == 0 and datetime.date.today().strftime("%w") == '0':
    #         su_start = hours['start'][:-2] + ":" + hours['start'][-2:]
    #         su_end = hours['end'][:-2] + ":" + hours['end'][-2:]
    #         su_hours = datetime.datetime.strptime(su_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(su_end,'%H:%M').strftime('%I:%M %p')
    #     elif hours["day"] == 1 and datetime.date.today().strftime("%w") == '1':
    #         m_start = hours['start'][:-2] + ":" + hours['start'][-2:]
          
    #         m_end = hours['end'][:-2] + ":" + hours['end'][-2:]
            
    #         m_hours = datetime.datetime.strptime(m_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(m_end,'%H:%M').strftime('%I:%M %p')
          
    #     elif hours["day"] == 2 and datetime.date.today().strftime("%w") == '2':
    #         t_start = hours['start'][:-2] + ":" + hours['start'][-2:]
    #         t_end = hours['end'][:-2] + ":" + hours['end'][-2:]
    #         t_hours = datetime.datetime.strptime(t_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(t_end,'%H:%M').strftime('%I:%M %p')
    #     elif hours["day"] == 3 and datetime.date.today().strftime("%w") == '3':
    #         w_start = hours['start'][:-2] + ":" + hours['start'][-2:]
    #         w_end = hours['end'][:-2] + ":" + hours['end'][-2:]
    #         w_hours = datetime.datetime.strptime(w_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(w_end,'%H:%M').strftime('%I:%M %p')
    #     elif hours["day"] == 4 and datetime.date.today().strftime("%w") == '4':
    #         th_start = hours['start'][:-2] + ":" + hours['start'][-2:]
    #         th_end = hours['end'][:-2] + ":" + hours['end'][-2:]
    #         th_hours = datetime.datetime.strptime(th_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(th_end,'%H:%M').strftime('%I:%M %p')
    #     elif hours["day"] == 5 and datetime.date.today().strftime("%w") == '5':
    #         f_start = hours['start'][:-2] + ":" + hours['start'][-2:]
    #         f_end = hours['end'][:-2] + ":" + hours['end'][-2:]
    #         f_hours = datetime.datetime.strptime(f_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(f_end,'%H:%M').strftime('%I:%M %p')
    #     elif hours["day"] == 6 and datetime.date.today().strftime("%w") == '6':
    #         sa_start = hours['start'][:-2] + ":" + hours['start'][-2:]
    #         sa_end = hours['end'][:-2] + ":" + hours['end'][-2:]
    #         sa_hours = datetime.datetime.strptime(sa_start,'%H:%M').strftime('%I:%M %p') + " - " + datetime.datetime.strptime(sa_end,'%H:%M').strftime('%I:%M %p')
    #     else:
    #         su_hours = "Closed"
    #         m_hours = "Closed"
    #         t_hours = "Closed"
    #         w_hours = "Closed"
    #         th_hours = "Closed"
    #         f_hours = "Closed"
    #         sa_hours = "Closed"


  
        
    
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



################################################################################

if __name__ == "__main__": 

    app.debug = True
    connect_to_db(app)


    app.run(port=5000, host="0.0.0.0")

