# Published Jan 2013
# Revised Jan 2014 (to add new modules data)
# Author : Philippe Larduinat, philippelt@users.sourceforge.net
# Public domain source code

# This API provides access to the Netatmo (Internet weather station) devices
# This package can be used with Python2 or Python3 applications and do not
# require anything else than standard libraries

# PythonAPI Netatmo REST data access
# coding=utf-8

import xbmcaddon

import simplejson as json
import time

# HTTP libraries depends upon Python 2 or 3
from urllib import urlencode
import urllib2

_ADDON_ = xbmcaddon.Addon()

######################## USER SPECIFIC INFORMATION ######################

# To be able to have a program accessing your netatmo data, you have to register your program as
# a Netatmo app in your Netatmo account. All you have to do is to give it a name (whatever) and you will be
# returned a client_id and secret that your app has to supply to access netatmo servers.

_CLIENT_ID = "5488e4901e775983b163f5e1"  # Your client ID from Netatmo app registration at http://dev.netatmo.com/dev/listapps
_CLIENT_SECRET = "oFMOHe3ajCdtB7k5H7QQ7lk8iiuIfI6zf"  # Your client app secret   '     '
_USERNAME = _ADDON_.getSetting("username")  # Your netatmo account username
_PASSWORD = _ADDON_.getSetting("password")  # Your netatmo account password

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

        print 'TOKEN JUST RETRIEVED'
        print self._accessToken
        print '_________c_______'
        print '__________c______'
        print '___________c_____'
        print '__________c______'

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
        self.stations = {}
        for d in self.rawData['devices']: self.stations[d['_id']] = d
        self.modules = {}
        for m in self.rawData['modules']: self.modules[m['_id']] = m
        self.default_module = list(self.modules.values())[0]['module_name']

    def stationByName(self, station=None):
        if self.logLevel > 1: indigo.server.log(u'Entered: DeviceList stationByName' ,  type=self.pluginDisplayName + ' Debug', isError=False)
        if not station: station = self.default_station
        for i, s in self.stations.items():
            if s['station_name'] == station: return self.stations[i]
        return None

    def stationById(self, sid):
        if self.logLevel > 1: indigo.server.log(u'Entered: DeviceList stationById' ,  type=self.pluginDisplayName + ' Debug', isError=False)
        return None if sid not in self.stations else self.stations[sid]

    def moduleByName(self, module, station=None):
        if self.logLevel > 1: indigo.server.log(u'Entered: DeviceList moduleByName' ,  type=self.pluginDisplayName + ' Debug', isError=False)
        s = None
        if station:
            s = self.stationByName(station)
            if not s: return None
        for m in self.modules:
            mod = self.modules[m]
            if mod['module_name'] == module:
                if not s or mod['main_device'] == s['_id']: return mod
        return None

    def moduleById(self, mid, sid=None):
        if self.logLevel > 1: indigo.server.log(u'Entered: DeviceList moduleById' ,  type=self.pluginDisplayName + ' Debug', isError=False)
        s = self.stationById(sid) if sid else None
        if mid in self.modules:
            return self.modules[mid] if not s or self.modules[mid]['main_device'] == s['_id'] else None

    def lastData(self, module=None, exclude=0):
        m = self.ThermoByName(module)
        if not m: return None
        lastD = dict()
        ds = m['dashboard_data']
        lastD[m['module_name']] = ds.copy()
        # lastD[m['module_name']]['When'] = lastD[m['module_name']].pop("time_utc")
        return lastD

    def checkNotUpdated(self, station=None, delay=3600):
        res = self.lastData(station)
        ret = []
        for mn, v in res.items():
            if time.time() - v['When'] > delay: ret.append(mn)
        return ret if ret else None

    def checkUpdated(self, station=None, delay=3600):
        res = self.lastData(station)
        ret = []
        for mn, v in res.items():
            if time.time() - v['When'] < delay: ret.append(mn)
        return ret if ret else None

    def getTemp(self, device_id, module_id):
        postParams = {"access_token": self.getAuthToken}
        postParams['device_id'] = device_id
        postParams['module_id'] = module_id
        resp = postRequest(_GETTHERMO_REQ, postParams)
        self.temperature = resp['body']['measured']['temperature']
        return self.temperature

    def getSetTemp(self, device_id, module_id):
        postParams = {"access_token": self.getAuthToken}
        postParams['device_id'] = device_id
        postParams['module_id'] = module_id
        resp = postRequest(_GETTHERMO_REQ, postParams)
        self.setpoint_temp = resp['body']['measured']['setpoint_temp']
        return self.setpoint_temp

    def getMode(self, device_id, module_id):
        postParams = {"access_token": self.getAuthToken}
        postParams['device_id'] = device_id
        postParams['module_id'] = module_id
        resp = postRequest(_GETTHERMO_REQ, postParams)
        self.setpoint_mode = resp['body']['setpoint']['setpoint_mode']
        return self.setpoint_mode

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


# auto-test when executed directly

if __name__ == "__main__":

    from sys import exit, stdout, stderr

    if not _CLIENT_ID or not _CLIENT_SECRET or not _USERNAME or not _PASSWORD:
        stderr.write("Library source missing identification arguments to check lnetatmo.py (user/password/etc...)")
        exit(1)

    authorization = ClientAuth()  # Test authentication method
    user = User(authorization)  # Test GETUSER
    devList = DeviceList(authorization)  # Test DEVICELIST

    # If we reach this line, all is OK

    # If launched interactively, display OK message
    print("lnetatmo.py : OK")

    exit(0)