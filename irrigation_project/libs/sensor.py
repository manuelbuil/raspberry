import Adafruit_DHT

def _doRead():
    return Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
    
def read_humidity():
    read = _doRead()
    return read[0]

def read_temperature():
    read = _doRead
    return read[1]
