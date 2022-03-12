# pip install requests
# used Python 3.8.5
# run as:
# pytest api_test.py -s

from random import randint
import requests
import json
from time import sleep
try:
    import unittest2 as unittest
except ImportError:
    import unittest

newUser = {'name':'Johnny Bravo', 'gender':'male', 'email':'johnny.bravo@aol.com', 'status':'active'}
randomNumber = randint(1000,10000)      # necessary for a unique email
newUser.update({'email': 'johnny.bravo'+str(randomNumber)+'@aol.com'})
print("newUser:\n", newUser)
my_headers = {'Authorization' : 'Bearer c0852f3b5c51022db6485473effd1d4bc31551b21e9a3e3b9fafe0fbb0cd4216'}
BASE_PATH = 'https://gorest.co.in/public/v2/users/'

class SimpleTest(unittest.TestCase):

    # Auxiliary methods
    def extractId(self, tmpDict):
        userId = tmpDict.get('id')
        print("Extracted userId: ",userId)
        return userId

    def modifyEmail(self, tmpDict):
        userEmail = tmpDict.get('email')
        newEmail = {'email':userEmail.split('@')[0] + '@yahoo.com'}
        print("newEmail: ", newEmail)
        return newEmail

    def printResponseNicely(self, resp):
        print(json.dumps(resp.json(), indent=4))

    # Test Case
    # the goal is to:
    # - create a new user
    # - check if this user was created
    # - update user's email
    # - delete this user
    # - check if the user was deleted
    
    def test_simpleAPI(self):
        # Create a new user
        print("\n\nCREATE USER:")
        response = requests.post(BASE_PATH, headers=my_headers, data=newUser)
        print(response)
        self.assertEqual(201, response.status_code)
        self.printResponseNicely(response)
        createdUser=response.json()
        userId = self.extractId(createdUser)      # EXTRACT ID of the newly created user
        sleep(1)      

        # Get newly created user
        print("\n\nGET USER:")
        response = requests.get(BASE_PATH + str(userId)+'', headers=my_headers)
        print(response)
        self.assertEqual(200, response.status_code)
        self.printResponseNicely(response)
        newEmail = self.modifyEmail(createdUser)
        sleep(1)

        # Update existing user
        print("\n\nUPDATE USER:")
        response = requests.put(BASE_PATH + str(userId)+'', headers=my_headers, data=newEmail)
        print(response)
        self.assertEqual(200, response.status_code)
        self.printResponseNicely(response)
        sleep(1)

        # Get updated user
        print("\n\nGET USER:")
        response = requests.get(BASE_PATH + str(userId)+'', headers=my_headers)
        print(response)
        self.assertEqual(200, response.status_code)
        self.printResponseNicely(response)
        sleep(1)

        # Delete user
        print("\n\nDELETE USER:")
        response = requests.delete(BASE_PATH + str(userId)+'', headers=my_headers)
        print(response)
        self.assertEqual(204, response.status_code)
        sleep(1)

        # Check if the user was really deleted
        print("\n\nGET USER:")
        response = requests.get(BASE_PATH + str(userId)+'', headers=my_headers)
        print(response)
        self.assertEqual(404, response.status_code)
        self.printResponseNicely(response)
