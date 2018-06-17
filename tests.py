import unittest
import os

from server import app
from model import db, connect_to_db
from seed import set_val_neighborhoods_table



class GlutieTests(unittest.TestCase):
    """ Flask tests on Routes. """

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_homepage(self):
        """ Test Homepage. """

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Check to see if a restaurant has gluten-free options:", result.data)

    def test_login(self):
        """ Test Login Page. """

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Email:", result.data)
        self.assertIn("Password:", result.data)


class GlutieTestsDatabase(unittest.TestCase):
    """ Flask Tests that use the database. """

    def setUp(self):
        """ Run before every test. """

        # Get Flask Test Client
        self.client = app.test_client()
        with self.client as c:
            with c.session_transaction() as session:
                session["user_id"] = 1
                session["fname"] = "Ash"
                session["lname"] = "Fri"
                session["email"] = "ashfri@gmail.com"

        # Display Flask Errors that occurs during tests
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = 'key'

        connect_to_db(app, 'postgresql:///gluten_free_test')
        print "Connected to Database."

        # Create Tables in Test DB
        db.create_all()

        # Add Sample Data to Test Database from seed.py
        set_val_neighborhoods_table()



    def tearDown(self):
        """ Function used at end of every Test. """

        db.session.close()
        db.drop_all()



    def test_signup(self):
        """ Test Sign Up for an Account Page. """

        result = self.client.get("/signup")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Create a New Account", results.data)



    def test_profile(self):
        """ Test Profile Page. """

        result = self.client.get("/profile")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Ready to try a new Glutie?", results.data)



    def test_signout(self):
        """ Test Sign Out Route. """

        result = self.client.get("/sign_out", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have successfully signed out.", result.data)



    def test_display_restaurants(self):
        """ Test Restaurants Route. """

        result = self.client.get("/restaurants", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have successfully signed out.", result.data)




class GlutieTestsDbNoSession(unittest.TestCase):
    """ Flask Tests using the DB without a session. """


    def setUp(self):
        """ Run before every test. """

        # Get Flask Test Client
        self.client = app.test_client()

        # Display Flask Errors during Tests
        app.config["TESTING"] = True

        # Connect to test db
        connect_to_db(app, "postgresql:///gluten_free_test")
        print "Connected to Database."

        # Create Tables in Test DB
        db.create_all()

        # Add Sample Data to Test Database from seed.py
        set_val_neighborhoods_table()


    def tearDown(self):
        """ Function used at end of every Test. """

        db.session.close()
        db.drop_all()



    def test_signup(self):
        """ Test for after a user signs up for an Account. """

        result = self.client.post("/thankyou", data={"first_name": "Ash", "lname": "Fri", "email": "ashfri@gmail.com", "zipcode": "12345", "password": "123"}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Thank you for signing up!", results.data)




if __name__ == "__main__":
    unittest.main()

   