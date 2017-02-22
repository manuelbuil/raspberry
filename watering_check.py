import sensor
import openweather as ow
import logging
from stevedore import driver

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():

    plugin = 'mail'  

    mgr = driver.DriverManager(
        namespace='watering.curier',
        name=plugin,
        invoke_on_load=True,
    )

    # Check the humidity
    hum = sensor.read_humidity()
    logger.info("This is the humidity: %s" %hum)

    if hum < 60:
        logger.info("Will it rain tomorrow? %s" %ow.rain_tomorrow())
        logger.info("Max. temperature tomorrow: %s" %ow.maxT_tomorrow())
        if (not ow.rain_tomorrow() and ow.maxT_tomorrow() > 25):
            # We need to water the plant
            print("We must water the plants")
            worked = mgr.driver.send_message()
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
