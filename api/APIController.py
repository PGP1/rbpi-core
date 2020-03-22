import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
from Encryption import Encryption

env = load_dotenv(find_dotenv())
class APIController():
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    END_POINT = os.environ.get("END_POINT")

    def subscribe(self):
        req = Encryption.createRequest(self.ACCESS_KEY, self.SECRET_KEY)
        res = req.post(self.END_POINT)
        print(res)

APIController().subscribe();
