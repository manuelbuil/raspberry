import pyowm

owm = pyowm.OWM('252115bbe068ef499054670c9494249b')  # You MUST provide a valid API key

def _get_forecast_tomorrow():
    return owm.daily_forecast("Sabinanigo,es", limit=1)
    
def rain_tomorrow():
    forecast = _get_forecast_tomorrow()
    return forecast.will_have_rain()

def maxT_tomorrow():
    forecast = _get_forecast_tomorrow()
    f = forecast.get_forecast()
    weathers = f.get_weathers()
    temperature = weathers[0].get_temperature('celsius')    
    return temperature['max']

def humidity_tomorrow():
    forecast = _get_forecast_tomorrow()
    f = forecast.get_forecast()
    weathers = f.get_weathers()
    humidity = weathers[0].get_humidity()    
    return humidity

