#!/usr/bin/python3
# encoding=utf-8

import xbmcaddon
import xbmcgui
import lnetatmo
import sys

authorization = lnetatmo.ClientAuth()
devList = lnetatmo.DeviceList(authorization)

__addon__ = xbmcaddon.Addon()
defaulttime = __addon__.getSetting("duration")
__CWD = __addon__.getAddonInfo('path').decode('utf-8')

class ThermoWindow(xbmcgui.WindowXML):

    def __init__(self,strXMLname, strFallbackPath):
        # Changing the three varibles passed won't change, anything
        # Doing strXMLname = "bah.xml" will not change anything.
        # don't put GUI sensitive stuff here (as the xml hasn't been read yet
        # Idea to initialize your variables here
        pass

    def onInit(self):
        battery = devList.battery
        self.getControl(200).setPercent(battery)
        pass

    # def onAction(self, action):
    #     # Same as normal python Windows.
    #     pass
    #
    # def onClick(self, controlID):
    #     """
    #         Notice: onClick not onControl
    #         Notice: it gives the ID of the control not the control object
    #     """
    #     pass
    #
    # def onFocus(self, controlID):
    #     pass

class thermopage:
    def __init__(self):
        self.parseargv()
        if self.SETTEMP:
            self.askfortemperature()
        elif self.AWAY:
            self.setaway()
        elif self.NOFREEZE:
            self.setnofreeze()
        elif self.TURNON:
            self.setmax()
        elif self.TURNOFF:
            self.setoff()
        elif self.PROGRAM:
            self.setprogram()
        else:
            ui = ThermoWindow('netatmo.xml', __addon__.getAddonInfo('path').decode('utf-8'))
            ui.doModal()


        # UPDATE VALUES

        temp = str(devList.temperature)
        xbmcgui.Window(10000).setProperty('netatmo_HomeTemperature', temp)
        settemp = str(float(devList.setpoint_temp))
        xbmcgui.Window(10000).setProperty('netatmo_HomeSetTemperature', settemp)
        setmode = str(devList.setpoint_mode)
        xbmcgui.Window(10000).setProperty('netatmo_HomeSetMode', setmode)
        relaycommand = unicode(devList.thermrelaycmd)
        xbmcgui.Window(10000).setProperty('netatmo_RelayCommand', relaycommand)
        module_name = str(devList.modulename)
        xbmcgui.Window(10000).setProperty('netatmo_ModuleName', module_name)
        device_name = str(devList.devicename)
        xbmcgui.Window(10000).setProperty('netatmo_LocationName', device_name)

        respdev = str(devList.respdev)
        xbmcgui.Window(10000).setProperty('dev', respdev)
        respter = str(devList.respthermo)
        xbmcgui.Window(10000).setProperty('ter', respter)

        if setmode == 'manual':
            manual_end = str(devList.manual_endpoint)
            manual_end = lnetatmo.toTimeString(manual_end)

            xbmcgui.Window(10000).setProperty('ManualEnd', manual_end)




    def askfortemperature(self):
        dialog = xbmcgui.Dialog()
        try:
            d = dialog.numeric(0, 'Enter Desired Temperature')
        except:
            d = devList.Temperature
        try:
            t = dialog.numeric(0, 'Enter Desired Duration in minutes')
            t = int(t) * 60
            t = str(t)
        except:
            t = defaulttime

        devList.setthermpoint('manual', d, t)


    def setaway(self):
        devList.setstatus('away')

    def setprogram(self):
        devList.setstatus('program')

    def setnofreeze(self):
        devList.setstatus('hg')

    def setmax(self):
        try:
            t = dialog.numeric(0, 'Enter Desired Duration in minutes')
            t = int(t) * 60
            t = str(t)
        except:
            t = defaulttime

        d = 45
        devList.setthermpoint('manual', d, t)

    def setoff(self):
        devList.setstatus('off')

    def parseargv(self):
        try:
            self.params = dict(arg.split("=") for arg in sys.argv[1].split("&"))
        except:
            self.params = {}

        xbmc.log("### params: %s" % self.params)

        self.SETTEMP = self.params.get("settemp", False)
        self.AWAY = self.params.get("away", False)
        self.NOFREEZE = self.params.get("hg", False)
        self.TURNON = self.params.get("max", False)
        self.TURNOFF = self.params.get("off", False)
        self.PROGRAM = self.params.get("program", False)


thermopage()