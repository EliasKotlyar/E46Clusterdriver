#!/usr/bin/env python

"""
Class for driving the Instrument Cluster over the CAN-Bus
"""

import logging
import time
import can


logging.basicConfig(level=logging.INFO)


class CanCommunication:

    """A simple example class"""
    led_message = can.Message(
        arbitration_id=0x545, data=[0, 0, 0, 0, 0xF0, 0, 0, 0], is_extended_id=False
    )

    rpm_message = can.Message(
        arbitration_id=0x316, data=[0x05, 0x62, 0, 0, 0x65, 0x12, 0x0, 0x62], is_extended_id=False
    )

    def setup(self,config):
        debug = int(config['DEFAULT']['DEBUG'])
        if debug == 1:
            self.bus = can.interface.Bus(interface="virtual")
        else:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")

        self.task_rpm = self.bus.send_periodic(self.rpm_message, 0.03)
        self.task_led = self.bus.send_periodic(self.led_message, 0.03)


    def setValue(self, x):
        self.led_message.data[3] = int("0x" + str(x) + "0", 16)
        #self.led_message.data[4]
        self.task_led.modify_data(self.led_message)
        print(self.led_message)

    def blink(self):
        self.task = self.bus.send_periodic(self.led_message, 0.03)
        for x in range(3):
            self.setValue(0)
            time.sleep(0.3)
            self.setValue(7)
            time.sleep(0.3)
        self.setValue(0)
        self.task.stop()


    def fuelconsumption(self,fuel):
        fuel = self.toUint16(fuel)
        self.led_message.data[1] = fuel[0]
        self.led_message.data[2] = fuel[1]
        self.task_led.modify_data(self.led_message)

    def toUint16(self,rpm):
        rpm_uint16 = int(rpm)
        rpm_msb = rpm_uint16 & 0xff
        rpm_lsb = rpm_uint16 >> 8
        return rpm_lsb,rpm_msb


    def setRpm(self,rpm):
        rpm = rpm * 6.4
        rpm = self.toUint16(rpm)
        self.rpm_message.data[3] = rpm[0]
        self.rpm_message.data[4] = rpm[1]
        self.task_rpm.modify_data(self.rpm_message)


    def stoptask(self):
        self.task.stop()






