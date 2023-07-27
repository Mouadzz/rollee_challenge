import json
import unittest
from rollee.models import AccountRecord
from .account import Account
from .solution import get_accounts_for_user
from django.test import RequestFactory
from .views import accounts_list


class TestSolution(unittest.TestCase):
    """Test the module rollee"""

    @classmethod
    def setUpClass(cls):
        """Extract accounts for valid user id"""
        cls.accounts = get_accounts_for_user(
            "test_candidate",
            "test_candidate123",
            "de344889-428a-4be0-93d4-d286d02a7252",
        )

    def test_total_accounts(self):
        """
        Should return 2 accounts for user id
        """
        self.assertEqual(len(self.accounts), 2)

    def test_accounts_details(self):
        """
        Should have these exact account details
        """
        self.assertEqual(
            self.accounts,
            [
                Account(
                    account_id="ac70a627-561a-4fa9-a86b-c8a8f7d73c2e",
                    name="Anne Herrmann",
                    email="AnneHerrmann@teleworm.us",
                    platform_name="Bolt",
                    country="ar",
                    currency="",
                    gross_earnings=0.0,
                ),
                Account(
                    account_id="ea8eab61-84cf-438c-a385-8f93a693c087",
                    name="Taylor Lloyd",
                    email="TaylorLloyd@teleworm.us",
                    platform_name="Deel",
                    country="ar",
                    currency="",
                    gross_earnings=0.0,
                ),
            ],
        )

    def test_invalid_credentials(self):
        """
        Should raise exception for invalid credentials with message 'Invalid credentials'
        """
        self.assertRaisesRegex(
            Exception,
            "Invalid credentials",
            get_accounts_for_user,
            "invalid_username",
            "whatever123",
            "de344889-428a-4be0-93d4-d286d02a7252",
        )

    def test_invalid_user_id(self):
        """
        Should raise exception if user id doesn't exist with message 'User not found'
        """
        self.assertRaisesRegex(
            Exception,
            "User not found",
            get_accounts_for_user,
            "test_candidate",
            "test_candidate123",
            "aaaaaaaa-1111-2222-3333-bbbbbbcccccc",
        )

    def test_data_saved_to_database(self):
        """
        The data is saved and the count is as expected
        """
        saved_accounts = AccountRecord.objects.filter(
            user_id="de344889-428a-4be0-93d4-d286d02a7252")

        self.assertEqual(saved_accounts.count(), 2)


    def post_request(self, data):
        request = RequestFactory().post("http://127.0.0.1:8000/dashboard/login_and_get_accounts",
                                        data=data)
        response = accounts_list(request)
        return response

    def test_missing_username(self):
        """
        Should return 400 with error message 'Username is missing'
        """
        data = {
            "password": "test_candidate123",
            "user_id": "de344889-428a-4be0-93d4-d286d02a7252"
        }
        response = self.post_request(data)

        self.assertEqual(response.status_code, 400)

        expected_content = {"error": "Username is missing"}
        response_content = json.loads(response.content)

        self.assertEqual(response_content, expected_content)

    def test_missing_password(self):
        """
        Should return 400 with error message 'Password is missing'
        """
        data = {
            "username": "test",
            "user_id": "de344889-428a-4be0-93d4-d286d02a7252"
        }

        response = self.post_request(data)

        self.assertEqual(response.status_code, 400)

        expected_content = {"error": "Password is missing"}
        response_content = json.loads(response.content)

        self.assertEqual(response_content, expected_content)

    def test_missing_user_id(self):
        """
        Should return 400 with error message 'User ID is missing'
        """
        data = {
            "username": "test",
            "password": "test_candidate123"
        }
        response = self.post_request(data)

        self.assertEqual(response.status_code, 400)

        expected_content = {"error": "User ID is missing"}
        response_content = json.loads(response.content)

        self.assertEqual(response_content, expected_content)
