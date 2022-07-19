import unittest

from fastapi.testclient import TestClient
from pydantic import json

from app.channel.router import router

client = TestClient(router)


class ChannelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_channel_read_by_name(self) -> json:
        response = client.get('/channel')
        assert response.status_code == 200
        assert response.json() == {'channel_name': 'test_channel_name'}
        return response

    def test_channel_name_not_found(self) -> json:
        response = client.get('/')
        assert response.status_code == 404
        assert response.json() == {"detail": "channel_name not found"}
        return response

    def test_invalid_keyword_error(self) -> json:
        response = client.get('/')
        assert response.status_code == 401
        assert response.json() == {'detail': "invalid channel name requested"}
        return response

    def test_db_connection_error(self) -> json:
        response = client.get('/')
        assert response.status_code == 401
        assert response.json() == {'detail': 'db connection error'}
        return response
