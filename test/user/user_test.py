import logging
import string
import random

from fastapi.testclient import TestClient
from unittest import TestCase

from pydantic import BaseModel
from starlette import status

from main import app


class User(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


class UserCase(TestCase):
    client = TestClient(app)

    member_users = []
    guest_users = []

    def generate_random_string(self):
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(10))

    def test_user_as_guest(self):
        # Create
        res = self.client.post('/user/', json={
            "email": self.generate_random_string(),
            "name": self.generate_random_string(),
            "thumbnail_url": None,
            "github_id": int(random.random() * 1000),
            "authorization": "guest"
        })

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.guest_users.append(User(user_id=res.json()['user']['user_id'],
                                     access_token=res.json()['access_token'],
                                     refresh_token=res.json()['refresh_token']))

        # Read
        user_id = self.guest_users[0].user_id
        logging.debug(f'user_id: {user_id}')

        res = self.client.get(f'/user/{user_id}', headers={
            'access-token': self.guest_users[0].access_token,
            'refresh-token': self.guest_users[0].refresh_token
        })

        logging.debug(f'res: {res.json()}')

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Read other
        user_id = 1  # self.guest_users[0].user_id
        logging.debug(f'user_id: {user_id}')

        res = self.client.get(f'/user/{user_id}', headers={
            'access-token': self.guest_users[0].access_token,
            'refresh-token': self.guest_users[0].refresh_token
        })

        logging.debug(f'res: {res.json()}')

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Read all
        user_id = self.guest_users[0].user_id
        logging.debug(f'user_id: {user_id}')

        res = self.client.get(f'/user/all', headers={
            'access-token': self.guest_users[0].access_token,
            'refresh-token': self.guest_users[0].refresh_token
        })

        logging.debug(f'res: {res.json()}')

        self.assertEqual(res.json()['success'], False)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # Update
        user_id = self.guest_users[0].user_id
        logging.debug(f'user_id: {user_id}')

        res = self.client.put(f'/user/{user_id}',
                                headers={
                                    'access-token': self.guest_users[0].access_token,
                                    'refresh-token': self.guest_users[0].refresh_token
                                },
                                json={
                                    "email": "update_guest",
                                    "name": "string",
                                    "authorization": "guest"
                                })

        logging.debug(f'res: {res.json()}')

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Delete
        user_id = self.guest_users[0].user_id
        logging.debug(f'user_id: {user_id}')

        res = self.client.delete(f'/user/{user_id}', headers={
            'access-token': self.guest_users[0].access_token,
            'refresh-token': self.guest_users[0].refresh_token
        })

        logging.debug(f'res: {res.json()}')

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.guest_users.clear()

    def test_user_as_member(self):
        # Create
        res = self.client.post('/user/', json={
            'email': self.generate_random_string(),
            'name': self.generate_random_string(),
            'thumbnail_url': None,
            'github_id': int(random.random() * 1000),
            'authorization': 'member'
        })

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.member_users.append(User(user_id=res.json()['user']['user_id'],
                                      access_token=res.json()['access_token'],
                                      refresh_token=res.json()['refresh_token']))

        # Read
        user_id = self.member_users[0].user_id
        res = self.client.get(f'/user/{user_id}', headers={
            'access-token': self.member_users[0].access_token,
            'refresh-token': self.member_users[0].refresh_token
        })

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Read other
        res = self.client.get(f'/user/1', headers={
            'access-token': self.member_users[0].access_token,
            'refresh-token': self.member_users[0].refresh_token
        })

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Read all
        res = self.client.get(f'/user/all', headers={
            'access-token': self.member_users[0].access_token,
            'refresh-token': self.member_users[0].refresh_token
        })

        self.assertEqual(res.json()['success'], False)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        # Delete
        user_id = self.member_users[0].user_id
        logging.debug(f'user_id: {user_id}')

        res = self.client.delete(f'/user/{user_id}', headers={
            'access-token': self.member_users[0].access_token,
            'refresh-token': self.member_users[0].refresh_token
        })

        logging.debug(f'res: {res.json()}')

        self.assertEqual(res.json()['success'], True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
