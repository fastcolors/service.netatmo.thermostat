import xbmc
import xbmcgui
import lnetatmo

authorization = lnetatmo.ClientAuth()
monitor = xbmc.Monitor()

WINDOW = xbmcgui.Window(10000)


def retrieve():

    xbmc.log('SERVICE')
    # devList = lnetatmo.DeviceList(authorization)
    #
    # temp = str(devList.temperature)
    # xbmcgui.Window(10000).setProperty('netatmo_HomeTemperature', temp)
    # settemp = str(devList.setpoint_temp)
    # xbmcgui.Window(10000).setProperty('netatmo_HomeSetTemperature', settemp)
    # setmode = str(devList.setpoint_mode)
    # xbmcgui.Window(10000).setProperty('netatmo_HomeSetMode', setmode)
    # relaycommand = unicode(devList.thermrelaycmd)
    # xbmcgui.Window(10000).setProperty('netatmo_RelayCommand', relaycommand)
    # module_name = str(devList.modulename)
    # xbmcgui.Window(10000).setProperty('netatmo_ModuleName', module_name)
    # device_name = str(devList.devicename)
    # xbmcgui.Window(10000).setProperty('netatmo_LocationName', device_name)
    #
    # respdev = str(devList.respdev)
    # xbmcgui.Window(10000).setProperty('dev', respdev)
    # respter = str(devList.respthermo)
    # xbmcgui.Window(10000).setProperty('ter', respter)
    #
    # if setmode == 'manual':
    #     manual_end = str(devList.manual_endpoint)
    #     manual_end = lnetatmo.toTimeString(manual_end)
    #
    #     xbmcgui.Window(10000).setProperty('ManualEnd', manual_end)

retrieve()

while not monitor.waitForAbort(60):

    retrieve()
