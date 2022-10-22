from codecs import getincrementaldecoder
from decimal import InvalidOperation
import string
import requests
from requests.auth import HTTPBasicAuth
import json
import os

class WattTime:
    token=""
    ba=""
    INDEX_URL = 'https://api2.watttime.org/index'
    LOGIN_URL = 'https://api2.watttime.org/v2/login'
    REGION_URL = 'https://api2.watttime.org/v2/ba-from-loc'
    def __init__(self, username="", password="", latt="", long="") -> None:
        if username=="":
            username=os.environ.get('WATTTIMEUSERNAME')
        if password=="": 
            password=os.environ.get('WATTTIMEPASSWORD')
        if latt=="":
            latt=os.environ.get('LATT')
        if long=="":
            long=os.environ.get('LONG')

        resp_plain = requests.get(self.LOGIN_URL, auth=HTTPBasicAuth(username, password))
        self.token=resp_plain.json()['token']
        
        ba_resp=self.get_BA(latt,long)
        self.ba=ba_resp['abbrev']


    def get_index(self, ba=""):
        if self.token=="":
            raise InvalidOperation("please login first.")
        if ba=="":
            ba=self.ba

        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'ba': '{}'.format(ba)}
        resp_text=requests.get(self.INDEX_URL, headers=headers, params=params)
        index=resp_text.json()
        return index

    def get_BA(self, latt, long)->string:
        if self.token=="":
            raise InvalidOperation("please login first.")
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'latitude': '{}'.format(latt), 'longitude': '{}'.format(long)}
        resp_plain=requests.get(self.REGION_URL, headers=headers, params=params)
        return resp_plain.json()
