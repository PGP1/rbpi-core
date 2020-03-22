import sys, os, base64, datetime, hashlib, hmac 
from requests_sigv4 import Sigv4Request


class Encryption:

    def createRequest(access_key, secret_key):
        print('access_key', access_key, secret_key)
        return Sigv4Request(region='us-east-1', access_key=access_key,secret_key=secret_key, \
            session_expires=3600,role_session_name='awsrequest',service='execute-api')