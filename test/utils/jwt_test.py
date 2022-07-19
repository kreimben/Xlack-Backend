import unittest
from unittest import TestCase

from fastapi import HTTPException
from jwt import InvalidIssuedAtError, ExpiredSignatureError, PyJWTError

import app.utils.jwt as jwt
from app.errors.jwt_error import AccessTokenExpired, RefreshTokenExpired


class TestJWT(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.fake_at = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0IjoxNjU3MjAwODk1LCJleHAiOjE2NTcyMDQ0OTV9.XZiynM4equufSiNL7Cz68wng387ErgElmypGadk536A'
        cls.fake_rt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0IjoxNjU3MjAwODk1LCJleHAiOjE2NTg0MTA0OTV9.urBEo0G9TzjO_i9G_ftQaTJZQy__YCi5nwD3Be4G1VE'

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_wrong_token_InvalidIssuedAtError(self):
        fake_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0Ijo5OTk5OTk5OTk5LCJleHAiOjE2OTg0MTA0OTV9.faW17kV6XjWE20nBJmPfqKAngdUeQYjG4MfDboSwoI4'
        with self.assertRaises((InvalidIssuedAtError, HTTPException)):
            payload = jwt.check_auth_using_token(fake_token, fake_token)

    def test_wrong_token_ExpiredSignatureError(self):
        # Change signature (just random value)
        fake_at = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0IjoxNjU3MjAwODk1LCJleHAiOjE2OTg0MTA0OTV9.ne7uD9qtVnJFNtlUECFybsV53TuFIrAbWvqTAZRqH9k'
        with self.assertRaises((ExpiredSignatureError, HTTPException)):
            payload = jwt.check_auth_using_token(fake_at, fake_at)

    @unittest.skip('No possibility to execute this.')
    def test_wrong_token_HTTPException(self):
        with self.assertRaises(HTTPException):
            payload = jwt.check_auth_using_token(self.fake_at, self.fake_rt)

    @unittest.skip('Meaningless test function.')
    def test_wrong_token_PyJWTError(self):
        with self.assertRaises(PyJWTError):
            payload = jwt.check_auth_using_token(self.fake_at, self.fake_rt)

    @unittest.skip('Meaningless test function.')
    def test_wrong_refresh_token_Exception(self):
        fake_at = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0IjoxNjU3MjAwODk1LCJleHAiOjE2OTg0MTA0OTV9.ne7uD9qtVnJFNtlUECFybsV53TuFIrAbWvqTAZRqH9k'
        fake_rt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0IjoxNjU3MjAwODk1LCJleHAiOjEwMDAwMDAwMDB9.ZNuz4FuHywz3Y9pMJ-nl5BoW-GuhgGTKjy1u_KKt_7o'
        with self.assertRaises(Exception):
            payload = jwt.check_auth_using_token(fake_rt, fake_rt)

    def test_wrong_token_AccessTokenExpired(self):
        with self.assertRaises(AccessTokenExpired):
            payload = jwt.check_auth_using_token(self.fake_at, self.fake_rt)

    def test_wrong_token_RefreshTokenExpired(self):
        # exp 2022 jul 21
        fake_at = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0IjoxNjU3MjAwODk1LCJleHAiOjE2NTg0MTA0OTV9.urBEo0G9TzjO_i9G_ftQaTJZQy__YCi5nwD3Be4G1VE'
        # exp 2022 jul 7 (already expired.)
        fake_rt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InN0cmluZyIsIm5hbWUiOiJzdHJpbmciLCJ0aHVtYm5haWxfdXJsIjoic3RyaW5nIiwiZ2l0aHViX2lkIjowLCJhdXRob3JpemF0aW9uIjoibWVtYmVyIiwiaWF0IjoxNjU3MjAwODk1LCJleHAiOjE2NTcyMDEwMDB9.p2NSl4yBZEAUUjXncgDV3zfbg5yz4Cry_qGn10MSeY4'
        with self.assertRaises(RefreshTokenExpired):
            payload = jwt.check_auth_using_token(fake_at, fake_rt)

    def test_token_not_none(self):
        payload = jwt.check_auth_using_token(self.fake_rt, self.fake_rt)
        self.assertIsNot(payload, None)

    def test_token_true(self):
        payload = jwt.check_auth_using_token(self.fake_rt, self.fake_rt)
        self.assertTrue(payload)

    def test_token_isinstance(self):
        payload = jwt.check_auth_using_token(self.fake_rt, self.fake_rt)
        self.assertIsInstance(payload, dict)


if __name__ == '__main__':
    unittest.main()
