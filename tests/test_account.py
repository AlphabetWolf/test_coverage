"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db, app
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)
    
    """ Test the representation of an account """
    def test_repr(self):
        account = Account()
        account.name = "Foo"
        self.assertEqual(str(account), "<Account 'Foo'>")

    def test_to_dict(self):
        """ Test account to dict """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
        self.assertEqual(account.date_joined, result["date_joined"])

    def test_from_dict(self):
        """ Test setting account attributes from a dictionary """
        # Create a dictionary with account data
        data = {
            'name': 'GG',
            'email': 'GG@example.com',
            'phone_number': '123456',
            'disabled': False,
            'date_joined': '2024-02-01'
        }
        
        # Create an Account object and populate it using from_dict
        account = Account()
        account.from_dict(data)
        
        # Assert that the Account object's attributes match the dictionary
        self.assertEqual(account.name, data['name'])
        self.assertEqual(account.email, data['email'])
        self.assertEqual(account.phone_number, data['phone_number'])
        self.assertEqual(account.disabled, data['disabled'])
        self.assertEqual(account.date_joined, data['date_joined'])


    def test_update_account_success(self):
        """Test updating an account successfully."""
        # Assuming ACCOUNT_DATA has an 'id' and is valid for an update.
        data = ACCOUNT_DATA[self.rand]
        account = Account(**data)
        account.create()  # Add the account to the mock database
        # Change some attribute to simulate an update
        original_name = account.name
        updated_name = "Updated " + original_name
        account.name = updated_name
        # Call the update method
        account.update()
        # Assert the mock commit was called and the object was updated
        self.assertEqual(account.name, updated_name)

    def test_update_account_without_id(self):
        """Test updating an account with no ID raises DataValidationError."""
        # Create an account but do not set an ID to simulate a new or invalid object
        account = Account(name="Foo", email="foo@example.com")
        # Do not call create to simulate an account without an ID

        # Expect DataValidationError when update is called on an account without an ID
        with self.assertRaises(DataValidationError):
            account.update()

    def test_delete_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_find_account(self):
        """Test finding an account by ID."""
        # Assuming ACCOUNT_DATA has an 'id' field and is valid.
        data = ACCOUNT_DATA[self.rand]
        # Create and add the account to the database.
        account = Account(**data)
        account.create()  # Simulate saving the account in the database.

        # Attempt to find the account by its ID.
        found_account = Account.find(account.id)

        # Check that the found account matches the created one.
        self.assertIsNotNone(found_account, "Account should be found.")
        self.assertEqual(found_account.id, account.id, "ID should be the same.")
        self.assertEqual(found_account.name, account.name, "Name should be the same.")

