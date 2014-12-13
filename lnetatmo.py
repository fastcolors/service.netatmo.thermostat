# Published Dec 2014
# Author : fastcolors, HEAVILY BASED ON THE WORK OF Philippe Larduinat, philippelt@users.sourceforge.net
# Public domain source code

# This API provides access to the Netatmo Thermostat devices

# PythonAPI Netatmo REST data access
# coding=utf-8

import xbmcaddon
import simplejson as json
import time
from urllib import urlencode
import urllib2

_ADDON_ = xbmcaddon.Addon()

# NETATMO KODI THERMOSTAT API INFOS

_CLIENT_ID = "5488e4901e775983b163f5e1"  # Your client ID from Netatmo app registration at http://dev.netatmo.com/dev/listapps
_CLIENT_SECRET = "oFMOHe3ajCdtB7k5H7QQ7lk8iiuIfI6zf"  # Your client app secret   '     '
_USERNAME = _ADDON_.getSetting("username")
_PASSWORD = _ADDON_.getSetting("password")
_REFRESH = _ADDON_.getSetting("refresh")

if not _REFRESH:
    _REFRESH = 60

_REFRESH = float(_REFRESH)

print _REFRESH

#########################################################################

# Common definitions

_BASE_URL = "https://api.netatmo.net/"
_AUTH_REQ = _BASE_URL + "oauth2/token"
_GETUSER_REQ = _BASE_URL + "api/getuser"
_DEVICELIST_REQ = _BASE_URL + "api/devicelist"
_GETMEASURE_REQ = _BASE_URL + "api/getmeasure"
_GETTHERMO_REQ = _BASE_URL + "api/getthermstate"


class ClientAuth:
    "Request authentication and keep access token available through token method. Renew it automatically if necessary"

    def __init__(self, clientId=_CLIENT_ID,
                 clientSecret=_CLIENT_SECRET,
                 username=_USERNAME,
                 password=_PASSWORD):
        postParams = {
            "grant_type": "password",
            "client_id": clientId,
            "client_secret": clientSecret,
            "username": username,
            "password": password,
            "scope": "read_station read_thermostat write_thermostat"
        }
        resp = postRequest(_AUTH_REQ, postParams)

        self._clientId = clientId
        self._clientSecret = clientSecret
        self._accessToken = resp['access_token']
        self.refreshToken = resp['refresh_token']
        self._scope = resp['scope']
        self.expiration = int(resp['expire_in'] + time.time())

    @property
    def accessToken(self):
        if self.expiration < time.time():  # Token should be renewed

            postParams = {
                "grant_type": "refresh_token",
                "refresh_token": self.refreshToken,
                "client_id": self._clientId,
                "client_secret": self._clientSecret
            }
            resp = postRequest(_AUTH_REQ, postParams)

            self._accessToken = resp['access_token']
            self.refreshToken = resp['refresh_token']
            self.expiration = int(resp['expire_in'] + time.time())

        return self._accessToken


class User:
    def __init__(self, authData):
        postParams = {
            "access_token": authData.accessToken
        }
        resp = postRequest(_GETUSER_REQ, postParams)
        self.rawData = resp['body']
        self.id = self.rawData['_id']
        self.devList = self.rawData['devices']
        self.ownerMail = self.rawData['mail']


class DeviceList:
    def __init__(self, authData):
        self.getAuthToken = authData.accessToken
        postParams = {
            "access_token": self.getAuthToken,
            "app_type": "app_thermostat"
        }
        resp = postRequest(_DEVICELIST_REQ, postParams)
        self.rawData = resp['body']

        self.devices = {}
        for d in self.rawData['devices']: self.devices[d['_id']] = d
        self.modules = {}
        for m in self.rawData['modules']: self.modules[m['_id']] = m

        self.default_device_id = list(self.devices.values())[0]['_id']
        self.default_module_id = list(self.modules.values())[0]['_id']
        self.thermrelaycmd = list(self.modules.values())[0]['therm_relay_cmd']

        self.getthermoinfo(self.default_device_id,self.default_module_id)

    def modulesNamesList(self, station=None):
        res = [m['module_name'] for m in self.modules.values()]
        res.append(self.stationByName(station)['module_name'])
        return res

    def getthermoinfo(self, device_id, module_id):
        postParams = {"access_token": self.getAuthToken}
        postParams['device_id'] = device_id
        postParams['module_id'] = module_id
        resp = postRequest(_GETTHERMO_REQ, postParams)

        self.temperature = resp['body']['measured']['temperature']
        self.setpoint_temp = resp['body']['measured']['setpoint_temp']
        self.setpoint_mode = resp['body']['setpoint']['setpoint_mode']


# Utilities routines

def postRequest(url, params):
    params = urlencode(params)
    # print params
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    req = urllib2.Request(url=url, data=params, headers=headers)
    try:
        resp = urllib2.urlopen(req).read()
        return json.loads(resp)
    except:
        return "oh darn!"
    return json.loads(resp)


def toTimeString(value):
    return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(int(value)))


def toEpoch(value):
    return int(time.mktime(time.strptime(value, "%Y-%m-%d_%H:%M:%S")))


def todayStamps():
    today = time.strftime("%Y-%m-%d")
    today = int(time.mktime(time.strptime(today, "%Y-%m-%d")))
    return today, today + 3600 * 24
