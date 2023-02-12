import hashlib
import datetime
import random

class Hasher:
    def hash(string : str):
        """
        take string and return hash string
        """
        salt = str(datetime.datetime.now().timestamp()) + str(random.random())
        pre_hash = f'{salt}{string}'
        result = hashlib.md5(pre_hash.encode()).hexdigest()
        return result
