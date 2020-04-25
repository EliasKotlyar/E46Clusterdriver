import board
import pulseio
import time


def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


speed = 30
SpeedSendVal = map(speed, 0, 250, 0, 1680)
SpeedSendVal = 1000

pin = board.P1_33
print("TEST pin {0}".format(pin))
pwm = pulseio.PWMOut( pin, duty_cycle=(2 ** 15), frequency=SpeedSendVal, variable_frequency=False)
time.sleep(1000)