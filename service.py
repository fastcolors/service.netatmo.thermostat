#!/usr/bin/python3
# encoding=utf-8

import xbmc
import xbmcgui
import lnetatmo

WINDOW = xbmcgui.Window(10000)

monitor = xbmc.Monitor()
authorization = lnetatmo.ClientAuth()
devList = lnetatmo.DeviceList(authorization)

relaycommand = str(devList.thermrelaycmd)
temp = str(devList.temperature)
settemp = str(devList.setpoint_temp)
setmode = str(devList.setpoint_mode)

WINDOW.setProperty('HomeTemperature', temp)
WINDOW.setProperty('HomeSetTemperature', settemp)
WINDOW.setProperty('HomeSetMode', setmode)
WINDOW.setProperty('RelayCommand', relaycommand)

while not monitor.waitForAbort(lnetatmo._REFRESH):

    print 'REFRESHED NETATMO REFRESHED NETATMO REFRESHED NETATMO REFRESHED NETATMO REFRESHED NETATMO'

    devList = lnetatmo.DeviceList(authorization)

    relaycommand = str(devList.thermrelaycmd)
    temp = str(devList.temperature)
    settemp = str(devList.setpoint_temp)
    setmode = str(devList.setpoint_mode)

    WINDOW.setProperty('HomeTemperature', temp)
    WINDOW.setProperty('HomeSetTemperature', settemp)
    WINDOW.setProperty('HomeSetMode', setmode)
    WINDOW.setProperty('RelayCommand', relaycommand)