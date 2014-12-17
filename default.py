#!/usr/bin/python3
# encoding=utf-8

import xbmcaddon
import xbmcgui
import lnetatmo

authorization = lnetatmo.ClientAuth()

__addon__ = xbmcaddon.Addon()
defaulttime = __addon__.getSetting("duration")

class ThermoWindow(xbmcgui.WindowXML):
    def __init__(self, strXMLname, strFallbackPath):
        # Changing the three varibles passed won't change, anything
        # Doing strXMLname = "bah.xml" will not change anything.
        # don't put GUI sensitive stuff here (as the xml hasn't been read yet
        # Idea to initialize your variables here
        pass

    def onInit(self):
        self.getControl(304).setVisible(False)
        self.updatevalues()
        pass

    # def onAction(self, action):
    # # Same as normal python Windows.
    #     pass
    #
    def onClick(self, controlID):

        if controlID == 201:
            self.askfortemperature()
            self.updatevalues()

        elif controlID == 202:
            self.setmax()
            self.updatevalues()

        elif controlID == 203:
            self.setoff()
            self.updatevalues()

        elif controlID == 204:
            self.setaway()
            self.updatevalues()

        elif controlID == 205:
            self.sethg()
            self.updatevalues()
        pass

    #
    # def onFocus(self, controlID):
    #     pass

    def askfortemperature(self):
        dialog = xbmcgui.Dialog()
        try:
            d = dialog.numeric(0, 'Enter Desired Temperature')
        except:
            d = self.devList.Temperature
        try:
            t = dialog.numeric(0, 'Enter Desired Duration in minutes')
            t = int(t) * 60
            t = str(t)
        except:
            t = defaulttime

        self.devList.setthermpoint('manual', d, t)


    def setaway(self):
        self.devList.setstatus('away')

    def setprogram(self):
        self.devList.setstatus('program')

    def sethg(self):
        self.devList.setstatus('hg')

    def setmax(self):
        self.devList.setthermpoint('max', None, '3600')

    def setoff(self):
        self.devList.setstatus('off')

    def updatevalues(self):
        self.devList = lnetatmo.DeviceList(authorization)

        battery = self.devList.battery
        self.getControl(200).setPercent(battery)
        self.getControl(300).setLabel(str(self.devList.devicename))
        self.getControl(301).setLabel(str(self.devList.modulename))
        self.getControl(302).setLabel(str(self.devList.setpoint_temp))
        self.getControl(303).setLabel(str(self.devList.temperature))
        relaycommand = self.devList.thermrelaycmd
        if relaycommand == 0:
            self.getControl(304).setVisible(False)
        else:
            self.getControl(304).setVisible(True)


        setmode = str(self.devList.setpoint_mode)
        xbmcgui.Window(10000).setProperty('netatmo_HomeSetMode', setmode)
        if setmode == 'manual':
            manual_end = str(self.devList.manual_endpoint)
            manual_end = lnetatmo.toTimeString(manual_end)
            xbmcgui.Window(10000).setProperty('ManualEnd', manual_end)

        respdev = str(self.devList.respdev)
        xbmcgui.Window(10000).setProperty('dev', respdev)
        respter = str(self.devList.respthermo)
        xbmcgui.Window(10000).setProperty('ter', respter)


class thermopage:
    def __init__(self):
        ui = ThermoWindow('netatmo.xml', __addon__.getAddonInfo('path').decode('utf-8'))
        ui.doModal()
        del ui

thermopage()