import Adafruit_BBIO.PWM as PWM
import time

# Setup Pins:
# Enable PWM
# config-pin P1_33 pwm
# Enable 12V Rail:
# config-pin P1_31 hi
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


speed = 30
SpeedSendVal = map(speed, 0, 250, 0, 1680)
SpeedSendVal = 15000

pin = "P1_33"
PWM.stop(pin)
PWM.cleanup()
# PWM.start(channel, duty, freq=2000, polarity=0)
# duty values are valid 0 (off) to 100 (on)
PWM.start(pin, 50, SpeedSendVal, 0)
# PWM.set_duty_cycle(pin, 25.5)

time.sleep(60)
PWM.stop(pin)
PWM.cleanup()
