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
    msg = can.Message(
        arbitration_id=0x545, data=[0, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False
    )

    def setup(self,config):
        debug = int(config['DEFAULT']['DEBUG'])
        if debug == 1:
            self.bus = can.interface.Bus(interface="virtual")
        else:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")

        self.task = self.bus.send_periodic(self.msg, 0.03)

    def setValue(self, x):
        self.msg.data[3] = int("0x" + str(x) + "0",16)
        self.task.modify_data(self.msg)
        print(self.msg)

    def blink(self):
        for x in range(3):
            self.setValue(0)
            time.sleep(0.3)
            self.setValue(7)
            time.sleep(0.3)
        self.setValue(0)


