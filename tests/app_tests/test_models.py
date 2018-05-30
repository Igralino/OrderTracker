import unittest
from datetime import timedelta

from app import app, db
from app.models import Business, Client, BusinessCard, Comments


class BusinessTests(unittest.TestCase):

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.sqlite"
        app.config["CSRF_ENABLED"] = False
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_needed_fields_exist(self):
        self.assertTrue(hasattr(Business, 'name'))
        self.assertTrue(hasattr(Business, 'password'))
        self.assertTrue(hasattr(Business, 'email'))
        self.assertTrue(hasattr(Business, 'confirmed'))
        self.assertTrue(hasattr(Business, 'registered_on'))

    def test_func_save(self):
        business = Business(name='name',
                            password='password',
                            email='email',
                            confirmed=True)
        business.save()
        committed_business = Business.query.get(business.id)
        self.assertEqual(business, committed_business)

    def test_func_get_name(self):
        business = Business(name='name',
                            password='password',
                            email='email',
                            confirmed=True)
        db.session.add(business)
        db.session.commit()
        self.assertEqual(business.name, Business.get_name(business.id))

    def test_func_get_email(self):
        business = Business(name='name',
                            password='password',
                            email='email',
                            confirmed=True)
        db.session.add(business)
        db.session.commit()
        self.assertEqual(business.email, Business.get_email(business.id))

    def test_func_name_is_free(self):
        business = Business(name='name',
                            password='password',
                            email='email',
                            confirmed=True)
        business.registered_on -= timedelta(days=32)
        db.session.add(business)
        db.session.commit()
        self.assertTrue(Business.name_is_free('name1'))
        self.assertFalse(Business.name_is_free('name'))

    def test_func_email_is_free(self):
        business = Business(name='name',
                            password='password',
                            email='email',
                            confirmed=True)
        business.registered_on -= timedelta(days=32)
        db.session.add(business)
        db.session.commit()
        self.assertTrue(Business.email_is_free('email1'))
        self.assertFalse(Business.email_is_free('email'))

    def test_func_it_works(self):
        business1 = Business(name='name',
                             password='password',
                             email='email',
                             confirmed=True)
        business2 = Business(name='name',
                             password='password',
                             email='email',
                             confirmed=True)
        business2.registered_on -= timedelta(days=32)
        business3 = Business(name='name',
                             password='password',
                             email='email',
                             confirmed=False)
        business3.registered_on -= timedelta(days=32)
        business4 = Business(name='name',
                             password='password',
                             email='email',
                             confirmed=False)
        db.session.add(business1)
        db.session.add(business2)
        db.session.add(business3)
        db.session.add(business4)
        db.session.commit()
        self.assertTrue(Business.it_works(business1.id))
        self.assertTrue(Business.it_works(business2.id))
        self.assertFalse(Business.it_works(business3.id))
        self.assertTrue(Business.it_works(business4.id))

    def test_func_check_confirmed(self):
        business = Business(name='name',
                            password='password',
                            email='email',
                            confirmed=True)
        db.session.add(business)
        db.session.commit()
        self.assertTrue(Business.check_confirmed(business.id))
        next_business = Business(name='name',
                                 password='password',
                                 email='email',
                                 confirmed=False)
        db.session.add(next_business)
        db.session.commit()
        self.assertFalse(Business.check_confirmed(next_business.id))

    def test_func_account_is_old(self):
        business1 = Business(name='name',
                             password='password',
                             email='email',
                             confirmed=True)
        business2 = Business(name='name',
                             password='password',
                             email='email',
                             confirmed=True)
        business2.registered_on -= timedelta(days=32)
        db.session.add(business1)
        db.session.add(business2)
        db.session.commit()
        self.assertFalse(Business.account_is_old(business1.id))
        self.assertTrue(business2.id)

    def test_func_get_all(self):
        business1 = Business(name='name',
                             password='password',
                             email='email',
                             confirmed=True)
        business2 = Business(name='name2',
                             password='password2',
                             email='email2',
                             confirmed=False)
        db.session.add(business1)
        db.session.add(business2)
        db.session.commit()
        businesses = Business.get_all()
        self.assertEqual(businesses[0], business1)
        self.assertEqual(businesses[1], business2)


class ClientTests(unittest.TestCase):

    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.sqlite"
        app.config["CSRF_ENABLED"] = False
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_needed_fields_exist(self):
        self.assertTrue(hasattr(Client, 'id'))
        self.assertTrue(hasattr(Client, 'email'))

    def test_func_save(self):
        client = Client(email='email')
        client.save()
        committed_client = Client.query.get(client.id)
        self.assertEqual(committed_client, client)

    def test_func_get_email(self):
        client = Client(email='email')
        db.session.add(client)
        db.session.commit()
        self.assertEqual(client.email, Client.get_email(client.id))

    def test_func_get_id(self):
        client = Client(email='email')
        db.session.add(client)
        db.session.commit()
        self.assertEqual(client.id, Client.get_id(client.email))

    def test_func_email_is_free(self):
        client = Client(email='email')
        db.session.add(client)
        db.session.commit()
        self.assertFalse(Client.email_is_free('email'))
        self.assertTrue(Client.email_is_free('email1'))


class BusinessCardTests(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.sqlite"
        app.config["CSRF_ENABLED"] = False
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_needed_fields_exist(self):
        self.assertTrue(hasattr(BusinessCard, 'name'))
        self.assertTrue(hasattr(BusinessCard, 'description'))
        self.assertTrue(hasattr(BusinessCard, 'contact_information'))
        self.assertTrue(hasattr(BusinessCard, 'business_id'))
        self.assertTrue(hasattr(BusinessCard, 'rating'))
        self.assertTrue(hasattr(BusinessCard, 'picture'))

    def test_func_save(self):
        BC = BusinessCard(name='name',
                          description='description',
                          contact_information='contact_information',
                          business_id=1)
        BC.save()
        committed_BC = BusinessCard.query.get(BC.id)
        self.assertEqual(BC, committed_BC)

    def test_func_by_rating(self):
        BC = BusinessCard(name='name',
                          description='description',
                          contact_information='contact_information',
                          business_id=1)
        self.assertEqual(BC.rating, BusinessCard.by_rating(BC))

    def test_func_get_name(self):
        BC = BusinessCard(name='name',
                          description='description',
                          contact_information='contact_information',
                          business_id=1)
        db.session.add(BC)
        db.session.commit()
        self.assertEqual(BC.name, BusinessCard.get_name(BC.business_id))

    def test_func_how_much(self):
        BC1 = BusinessCard(name='name',
                           description='description',
                           contact_information='contact_information',
                           business_id=2)
        BC2 = BusinessCard(name='name',
                           description='description',
                           contact_information='contact_information',
                           business_id=1)
        db.session.add(BC1)
        db.session.add(BC2)
        db.session.commit()
        self.assertEqual(2, BusinessCard.how_much())

    def test_func_get_picture(self):
        BC = BusinessCard(name='name',
                          description='description',
                          contact_information='contact_information',
                          business_id=1)
        db.session.add(BC)
        db.session.commit()
        self.assertEqual(BC.picture, BusinessCard.get_picture(BC.business_id))

    def test_func_get_description(self):
        BC = BusinessCard(name='name',
                          description='description',
                          contact_information='contact_information',
                          business_id=1)
        db.session.add(BC)
        db.session.commit()
        self.assertEqual(BC.description, BusinessCard.get_description(BC.business_id))

    def test_func_get_contact_information(self):
        BC = BusinessCard(name='name',
                          description='description',
                          contact_information='contact_information',
                          business_id=1)
        db.session.add(BC)
        db.session.commit()
        self.assertEqual(BC.contact_information, BusinessCard.get_contact_information(BC.id))

    def test_func_is_real(self):
        BC1 = BusinessCard(name='name',
                           description='description',
                           contact_information='contact_information',
                           business_id=1)
        BC2 = BusinessCard(name='name',
                           description='description',
                           contact_information='contact_information',
                           business_id=2)
        db.session.add(BC1)
        db.session.commit()
        self.assertTrue(BusinessCard.is_real(BC1.id))
        self.assertFalse(BusinessCard.is_real(BC2.id))


class CommentsTests(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.sqlite"
        app.config["CSRF_ENABLED"] = False
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_needed_fields_exist(self):
        self.assertTrue(hasattr(Comments, 'text'))
        self.assertTrue(hasattr(Comments, 'client_id'))
        self.assertTrue(hasattr(Comments, 'business_id'))
        self.assertTrue(hasattr(Comments, 'client_name'))
        self.assertTrue(hasattr(Comments, 'star'))

    def test_func_save(self):
        comment = Comments(text='text',
                           client_id=1,
                           business_id=1,
                           client_name='client_name',
                           star=1)
        comment.save()
        self.assertEqual(comment, Comments.query.get(comment.id))

    def test_func_get_name(self):
        comment = Comments(text='text',
                           client_id=1,
                           business_id=1,
                           client_name='client_name',
                           star=1)
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(comment.client_name, Comments.get_name(comment.id))

    def test_func_get_star(self):
        comment = Comments(text='text',
                           client_id=1,
                           business_id=1,
                           client_name='client_name',
                           star=1)
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(comment.star, Comments.get_star(comment.id))
