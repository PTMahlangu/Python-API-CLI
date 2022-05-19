import unittest
import sys
import os
from unittest.mock import patch, Mock
sys.path.insert(0, os.getcwd())
from app import getData,formatData

class ApiTests(unittest.TestCase):

    def test_mock_whole_function(self):
        """Mocking a whole function"""
        mock_get_patcher = patch('app.requests.get')
        users = [{
                "01-01-2022": 300,
                "02-01-2022": 500,
                "03-01-2022": 700,
                "04-01-2022": 1300,
                "05-01-2022": 2000,
                "06-01-2022": 3000,
                "07-01-2022": 3500,
                "08-01-2022": 4000,
                "09-01-2022": 4500,
                "10-01-2022": 5000,
                "11-01-2022": 20000,
                "12-01-2022": 35000,
                "13-01-2022": 46000,
                "14-01-2022": 70000,
                "15-01-2022": 90000
                }]

        # Start patching 'requests.get'.
        mock_get = mock_get_patcher.start()

        # Configure the mock to return a response with status code 200 and a list of users.
        mock_get.return_value = Mock(status_code = 200)
        mock_get.return_value.json.return_value = users

        # Call the service, which will send a request to the server.
        response = getData()

        # Stop patching 'requests'.
        mock_get_patcher.stop()

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), users)



    @patch('app.getData')
    def test_get_one_user(self, mock_get_users):
        """
        Test for getting one user using their dataID
        Demonstrates mocking third party functions
        """
        users = [{
                "01-01-2022": 300,
                "02-01-2022": 500,
                "03-01-2022": 700,
                "04-01-2022": 1300,
                "05-01-2022": 2000,
                "06-01-2022": 3000,
                "07-01-2022": 3500,
                "08-01-2022": 4000,
                "09-01-2022": 4500,
                "10-01-2022": 5000,
                "11-01-2022": 20000,
                "12-01-2022": 35000,
                "13-01-2022": 46000,
                "14-01-2022": 70000,
                "15-01-2022": 90000
                }]
        mock_get_users.return_value = Mock()
        mock_get_users.return_value.json.return_value = users
        dates,user = formatData(getData())
        users = list( [x] for x in users[0])
        self.assertEqual(user[2], user[2])

if __name__ == "__main__":
    unittest.main()
