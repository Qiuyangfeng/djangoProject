from django.conf import settings
import hashlib

def md5(data_string):
    """md5加密"""
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()

from django.contrib.auth.hashers import make_password

def pbkdf2(data_string):
    """pbkdf2加密"""
    return make_password(data_string, None, 'pbkdf2_sha256')