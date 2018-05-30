import os
import unittest

from app import app, db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, 'test.sqlite')


class MainPageTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB_PATH
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_page_exist(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_main_page_exist(self):
        response = self.client.get("/business/main_page", follow_redirects=True)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_business_main_page_exist(self):
        response = self.client.get("/business/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB_PATH
        db.create_all()
        self.client = app.test_client()
        self.form = {
            "name": "Test_Name",
            "password": "1234567890",
            "check_password": "1234567890",
            "email": "test@mail.com"
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration_page_exist(self):
        response = self.client.get("/business/registration_business", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_registration_page_works(self):
        response = self.client.post("/business/registration_business", data=self.form, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
