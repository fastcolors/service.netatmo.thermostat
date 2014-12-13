service.netatmo.thermostat
==========================

Connects to NETATMO thermostats and retireves infos in order to display them in your KODI instance.

so far sets these properties:

Window(Home).Property(HomeTemperature) > Temperature percieved by thermostat
Window(Home).Property(HomeSetTemperature) > Wanted Temperature set by program or manually
Window(Home).Property(HomeSetMode) > Shows how the temperature is set, manually or by program
Window(Home).Property(RelayCommand) > Shows the value of the Relay
      (can be easily used this way to return if the boiler is on or off : 0 = off / not0 = on)
      

this is still in it's early stages.
and based on lnetatmo by Philippe Larduinat
https://github.com/philippelt/netatmo-api-python/blob/master/lnetatmo.py

