import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 11 (GPIO 17) auf Output setzen
GPIO.setup(11, GPIO.OUT)

# Dauersschleife
while 1:

  print("Going DOWN")
  # LED immer ausmachen
  GPIO.output(11, GPIO.LOW)

  # Warte 5s
  time.sleep(5)

  print("Going UP")

  # LED an
  GPIO.output(11, GPIO.HIGH)

  # Warte 5s
  time.sleep(5)

