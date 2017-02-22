import sensor
import openweather as ow
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():

    ow.rain_today()


    # Check the humidity
    hum = sensor.read_humidity()
    logger.info("This is the humidity: %s" %hum)

    if hum < 60:
        logger.info("Will it rain tomorrow? %s" %ow.rain_tomorrow())
        logger.info("Max. temperature tomorrow: %s" %ow.maxT_tomorrow())
        if (not ow.rain_tomorrow() and ow.maxT_tomorrow() > 25):
            # We need to water the plant
            print("We must water the plants")
            return
           
    if hum < 35:
        if (not ow.rain_today()):
           print("Water the plants a bit")
           return

    logger.info("Nothing to do today")


if __name__ == "__main__":
    main()
