from http.client import HTTPException


class TokenExpired(HTTPException):
    def __init__(self, status_code: int = 401, detail: str = 'Token Expired.'):
        self.status_code = status_code
        self.detail = detail

    def __repr__(self):
        return f'{self.__class__.__name__}'


class AccessTokenExpired(TokenExpired):
    def __init__(self, status_code: int = 401, detail: str = 'Access Token Expired.'):
        self.status_code = status_code
        self.detail = detail


class RefreshTokenExpired(TokenExpired):
    def __init__(self, status_code: int = 401, detail: str = 'Refresh Token Expired.'):
        self.status_code = status_code
        self.detail = detail
