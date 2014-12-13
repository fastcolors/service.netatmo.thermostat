
import xbmc
import xbmcgui
import lnetatmo

xbmc.log("### run_backend started")

authorization = lnetatmo.ClientAuth()
monitor = xbmc.Monitor()

WINDOW = xbmcgui.Window(10000)

for prop in ("HomeTemperature", "HomeSetTemperature", "HomeSetMode", "RelayCommand"):
    WINDOW.clearProperty(prop)
    
def retrieve():
    devList = lnetatmo.DeviceList(authorization)

    relaycommand = unicode(devList.thermrelaycmd)
    temp = str(devList.temperature)
    settemp = str(devList.setpoint_temp)
    setmode = str(devList.setpoint_mode)

    WINDOW.setProperty('HomeTemperature', temp)
    WINDOW.setProperty('HomeSetTemperature', settemp)
    WINDOW.setProperty('HomeSetMode', setmode)
    WINDOW.setProperty('RelayCommand', relaycommand)

retrieve()

while not monitor.waitForAbort(30):

    retrieve()
