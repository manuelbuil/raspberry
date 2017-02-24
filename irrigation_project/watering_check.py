import libs.sensor as sensor
import libs.openweather as ow
import logging
import syslog
from stevedore import driver

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def water_plants()

    syslog.syslog("We choose the plug-in: %s" % mgr.driver.get_type())
    message = "Rains tomorrow: " + str(ow.rain_tomorrow()) + "\nMax temperature tomorrow: " + str(ow.maxT_tomorrow())
    worked = mgr.driver.send_message(message)
    if worked:
        return
    else:
        syslog.syslog(syslog.LOG_ERR,"Something went wrong while watering")
     

def main():

    plugin = 'mail'  

    mgr = driver.DriverManager(
        namespace='water.curier',
        name=plugin,
        invoke_on_load=True,
    )

    # Check the humidity
    hum = sensor.read_humidity()
    syslog.syslog("This is the humidity: %s" %hum)

    if hum < 60:
        syslog.syslog("Will it rain tomorrow? %s" %ow.rain_tomorrow())
        syslog.syslog("Max. temperature tomorrow: %s" %ow.maxT_tomorrow())
        if (not ow.rain_tomorrow() and ow.maxT_tomorrow() > 25):
            # We need to water the plant
            water_plants()
            return

    if hum < 40:
        if (not ow.rain_today()):
           water_plants()
           return

    syslog.syslog("Nothing to do today")


if __name__ == "__main__":
    syslog.syslog("Starting watering_check")
    main()
