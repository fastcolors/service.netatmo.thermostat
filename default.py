#!/usr/bin/python3
# encoding=utf-8

import xbmc
import xbmcgui
import xbmcplugin
import inetatmo

WINDOW = xbmcgui.Window(10000)

monitor = xbmc.Monitor()
#
# while not monitor.waitForAbort(350):
#     # todo find station /module by id and call
authorization = inetatmo.ClientAuth()
devList = inetatmo.DeviceList(authorization)

temp = devList.getTemp('70:ee:50:06:30:00', module_id='04:00:00:06:3c:4c')
settemp = devList.getSetTemp('70:ee:50:06:30:00', module_id='04:00:00:06:3c:4c')
setmode = devList.getMode('70:ee:50:06:30:00', module_id='04:00:00:06:3c:4c')
temp = str(temp)
settemp = str(settemp)

WINDOW.setProperty('HomeTemperature', temp)
WINDOW.setProperty('HomeSetTemperature', settemp)
WINDOW.setProperty('HomeSetMode', setmode)
