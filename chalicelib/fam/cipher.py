import hashlib
import binascii
import os
import jwt

from chalicelib.fam import config


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def get_current_username(req):
    token = req.headers['Authorization'].split(' ')
    if token[0] != 'Bearer':
        raise ValueError('Authorization method invalid')

    token = jwt.decode(token[1], config.SECRET, algorithm='HS256')

    return token['username']
