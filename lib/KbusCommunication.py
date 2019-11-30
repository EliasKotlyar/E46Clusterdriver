#!/usr/bin/env python

"""
Class for driving the Instrument Cluster over the K-Bus
"""
from time import sleep

from . import IBUSService as ibus_

import threading


class KbusCommunication:
    debug = 0
    ibus = 0

    def onIBUSready(self):
        pass

    def onIBUSpacket(self, packet):
        pass
        # print(packet)

    def setup(self, config):
        self.debug = int(config['DEFAULT']['DEBUG'])
        if self.debug == 0:
            self.ibus = ibus_.IBUSService(self.onIBUSready, self.onIBUSpacket)
            self.ibus.cmd = ibus_.IBUSCommands(self.ibus)
            self.ibus.main_thread = threading.Thread(target=self.ibus.start)
            self.ibus.main_thread.daemon = True
            self.ibus.main_thread.start()

    def setBacklight(self, value):
        print('Setting backlight to ' + str(value))

        packet = ibus_.IBUSPacket(source_id="d0",
                                  length="08",
                                  destination_id="bf",
                                  data="5b01740a3c00")
        self.ibus.send(packet.raw)
        sleep(0.1)
        packet = ibus_.IBUSPacket(source_id="d0",
                                  length="07",
                                  destination_id="bf",
                                  data="5ce037ff00")

        self.ibus.send(packet.raw)
        sleep(0.1)
        packet = ibus_.IBUSPacket(source_id="d0",
                                  length="08",
                                  destination_id="bf",
                                  data="5b 01 74 0a 3c 00")
        self.ibus.send(packet.raw)

    def sendMessage(self, toAdr, dataHex):
        length = int(len(dataHex) / 2) + 2
        length = format(length, '02x')
        packet = ibus_.IBUSPacket(source_id="3f",
                                  length=length,
                                  destination_id=toAdr,
                                  data=dataHex)
        print(packet.raw)
        self.ibus.send(packet.raw)
