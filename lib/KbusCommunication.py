#!/usr/bin/env python

"""
Class for driving the Instrument Cluster over the K-Bus
"""

from . import IBUSService as ibus_

import threading


class KbusCommunication:
    debug = 0
    ibus = 0

    def onIBUSready(self):
        pass

    def onIBUSpacket(packet):
        print(packet)

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
                                  length="06",
                                  destination_id="bf",
                                  data="5b00760a3c00")
        self.ibus.send(packet.raw)
