import logging
from datetime import datetime, timedelta, timezone

from fastapi import Header, HTTPException
from jwt import InvalidAlgorithmError, ImmatureSignatureError, InvalidIssuedAtError, \
    InvalidIssuerError, InvalidAudienceError, ExpiredSignatureError, InvalidSignatureError
from jwt import encode, decode

from app.errors.jwt_error import AccessTokenExpired, RefreshTokenExpired


def issue_token(user_info: dict, delta: timedelta):
    """
    This function doesn't take care of errors!

    :param user_info:
    :param delta:
    :return:
    """
    logging.debug('in issue_token (jwt.py)')
    payload = user_info.copy()

    payload.update({'iat': datetime.now(tz=timezone.utc), 'exp': datetime.now(tz=timezone.utc) + delta})

    jwt = encode(payload=payload, key='secret_key', algorithm='HS256')
    logging.debug(f'jwt: {jwt}')

    return jwt


def extract_payload_from_token(token: str):
    """
    This function doesn't take care of errors!

    :param token:
    :return:
    """
    logging.debug('in issue_token (jwt.py)')
    payload = decode(jwt=token, key='secret_key', algorithms=['HS256'])
    logging.debug(f'payload: {payload}')

    return payload


# TODO: Refactoring.
# Dependency
def check_auth_using_token(access_token: str = Header(...), refresh_token: str = Header(...)):
    logging.debug('in issue_token (jwt.py)')
    # Check `refresh_token` first.
    try:
        payload = extract_payload_from_token(refresh_token)
        logging.debug(f'refresh_token payload: {payload}')

        # Check `access_token` second.
        try:
            payload = extract_payload_from_token(access_token)
            logging.debug(f'access_token payload: {payload}')
            return payload
        # Unacceptable error.
        except InvalidAlgorithmError as e:
            raise HTTPException(detail=f'JWT Error (InvalidAlgorithmError/{e.__repr__()})', status_code=401)
        except ImmatureSignatureError as e:
            raise HTTPException(detail=f'JWT Error (ImmatureSignatureError/{e.__repr__()})', status_code=401)
        except InvalidIssuerError as e:
            raise HTTPException(detail=f'JWT Error (InvalidIssuerError/{e.__repr__()})', status_code=401)
        except InvalidAudienceError as e:
            raise HTTPException(detail=f'JWT Error (InvalidAudienceError/{e.__repr__()})', status_code=401)
        except InvalidSignatureError as e:
            raise HTTPException(detail=f'JWT Error (InvalidSignatureError/{e.__repr__()})', status_code=401)
        except InvalidIssuedAtError as e:  # When `iat` is future.
            raise HTTPException(detail=f'JWT Error (InvalidIssuedAtError/{e.__repr__()})', status_code=401)

        # Acceptable error. Should re-issue token.
        except ExpiredSignatureError:
            return AccessTokenExpired()

    # Unacceptable error.
    except InvalidAlgorithmError as e:
        raise HTTPException(detail=f'JWT Error (InvalidAlgorithmError/{e.__repr__()})', status_code=401)
    except ImmatureSignatureError as e:
        raise HTTPException(detail=f'JWT Error (ImmatureSignatureError/{e.__repr__()})', status_code=401)
    except InvalidIssuerError as e:
        raise HTTPException(detail=f'JWT Error (InvalidIssuerError/{e.__repr__()})', status_code=401)
    except InvalidAudienceError as e:
        raise HTTPException(detail=f'JWT Error (InvalidAudienceError/{e.__repr__()})', status_code=401)
    except InvalidSignatureError as e:
        raise HTTPException(detail=f'JWT Error (InvalidSignatureError/{e.__repr__()})', status_code=401)
    except InvalidIssuedAtError as e:  # When `iat` is future.
        raise HTTPException(detail=f'JWT Error (InvalidIssuedAtError/{e.__repr__()})', status_code=401)

    # Acceptable error. Should re-issue token.
    except ExpiredSignatureError:
        return RefreshTokenExpired()
    except AccessTokenExpired:
        return AccessTokenExpired()
