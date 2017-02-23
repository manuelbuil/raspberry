import libs.sensor as sensor
import libs.openweather as ow
import logging
from stevedore import driver

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():

    plugin = 'mail'  

    mgr = driver.DriverManager(
        namespace='water.curier',
        name=plugin,
        invoke_on_load=True,
    )

    # Check the humidity
    hum = sensor.read_humidity()
    logger.info("This is the humidity: %s" %hum)

    if hum < 60:
        logger.info("Will it rain tomorrow? %s" %ow.rain_tomorrow())
        logger.info("Max. temperature tomorrow: %s" %ow.maxT_tomorrow())
#        if (not ow.rain_tomorrow() and ow.maxT_tomorrow() > 25):
        if ow.maxT_tomorrow() > 5:
            # We need to water the plant
            print("We must water the plants")
            logger.info("We choose the plug-in: %s" % mgr.driver.get_type())
            message = "Rains tomorrow: " + str(ow.rain_tomorrow()) + "\nMax temperature tomorrow: " + str(ow.maxT_tomorrow())
            worked = mgr.driver.send_message(message)
            if worked:
                return
            else:
                log.error("Something went wrong while watering")
           
    if hum < 35:
        if (not ow.rain_today()):
           print("Water the plants a bit")
           return

    logger.info("Nothing to do today")


if __name__ == "__main__":
    main()
