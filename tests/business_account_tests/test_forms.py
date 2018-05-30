import unittest

from business_account.forms import RegistrationBusinessForm, LoginBusinessForm, ChangeBusinessNameForm


class RegistrationBusinessFormTests(unittest.TestCase):

    def test_needed_fields_exist(self):
        self.assertTrue(hasattr(RegistrationBusinessForm, 'name'))
        self.assertTrue(hasattr(RegistrationBusinessForm, 'password'))
        self.assertTrue(hasattr(RegistrationBusinessForm, 'check_password'))
        self.assertTrue(hasattr(RegistrationBusinessForm, 'email'))


class LoginBusinessFormTests(unittest.TestCase):

    def test_needed_fields_exist(self):
        self.assertTrue(hasattr(LoginBusinessForm, 'email'))
        self.assertTrue(hasattr(LoginBusinessForm, 'password'))


class ChangeBusinessNameFormTests(unittest.TestCase):

    def test_needed_fields_exist(self):
        self.assertTrue(hasattr(ChangeBusinessNameForm, 'new_name'))
        self.assertTrue(hasattr(ChangeBusinessNameForm, 'password'))
        self.assertTrue(hasattr(ChangeBusinessNameForm, 'submit1'))
