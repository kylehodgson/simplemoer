from codecs import getincrementaldecoder
from decimal import InvalidOperation
import string
import requests
from requests.auth import HTTPBasicAuth
import json
import os


class WattTime:
    token = ""
    ba = ""
    INDEX_URL = 'https://api2.watttime.org/index'
    LOGIN_URL = 'https://api2.watttime.org/v2/login'
    REGION_URL = 'https://api2.watttime.org/v2/ba-from-loc'
    REGISTER_URL = 'https://api2.watttime.org/v2/register'

    def __init__(self, username="", password="", latt="", long="") -> None:
        if not username:
            username = os.environ.get('WATTTIMEUSERNAME')
        if not password:
            password = os.environ.get('WATTTIMEPASSWORD')
        if not latt:
            latt = os.environ.get('LATT')
        if not long:
            long = os.environ.get('LONG')

        if not username or not password or not latt or not long:
            raise Exception(
                "Did not find watttime credentials or GPS coordinates. "
                "Either provide them while enstantiating WattTime, or "
                "make sure the WATTTIMEUSERNAME, WATTTIMEPASSWORD, LATT "
                "and LONG environment variables are set.")

        resp_plain = requests.get(
            self.LOGIN_URL, auth=HTTPBasicAuth(username, password))
        self.token = resp_plain.json()['token']

        ba_resp = self.get_BA(latt, long)
        self.ba = ba_resp['abbrev']
        return

    def get_index(self, ba=""):
        if self.token == "":
            raise InvalidOperation("please login first.")
        if ba == "":
            ba = self.ba

        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'ba': '{}'.format(ba)}
        resp_text = requests.get(
            self.INDEX_URL, headers=headers, params=params)
        index = resp_text.json()
        return index

    def get_BA(self, latt, long) -> string:
        if self.token == "":
            raise InvalidOperation("please login first.")
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'latitude': '{}'.format(
            latt), 'longitude': '{}'.format(long)}
        resp_plain = requests.get(
            self.REGION_URL, headers=headers, params=params)
        return resp_plain.json()

    @classmethod
    def register(cls, username, password, email, org=""):
        params = {
            'username': username,
            'password': password,
            'email': email}
        if org:
            params.org = org
        resp_plain = requests.post(WattTime.REGISTER_URL, json=params)
        response = resp_plain.json()
        if 'error' in response:
            raise Exception(
                f"WattTime registration returned an error: {response['error']}")
        return response
