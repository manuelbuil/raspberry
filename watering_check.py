import sensor
import openweather as ow

def main():

    # Check the humidity
    hum = sensor.read_humidity()

    if hum < 60:
        if (not ow.rain_tomorrow() and ow.maxT_tomorrow() > 25):
            # We need to water the plant
            print("We must water the plants")
            return
            
    print("Nothing to do")


if __name__ == "__main__":
    main()
