import unittest

from fastapi.testclient import TestClient
from pydantic import json

from app.channel.router import router

client = TestClient(router)


class ChatTest(unittest.TestCase):

    @classmethod
    def setupClass(cls) -> None:
        pass

    @classmethod
    def teardownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    # def test_read_chat(self) -> json:
    #     response = client.get('/')
    #     assert response.status_code == 200
    #     assert response.json() == {'chat_content': 'chat_content_is_here'}
    #     return response
    #
    # def test_chat_id_not_found(self)->json:
    #     response = client.get('/')
    #     assert response.status_code == 404
    #     assert response.json() == {'chat_id': 'chat_id_not_found'}
    #     return response
    #
    # def test_invalid_chat_keyword_input(self) -> json:
    #     response = client.get('/')
    #     assert response.status_code == 401
    #     assert response.json() == {'chat': 'invalid_chat_keyword'}
    #     return response

