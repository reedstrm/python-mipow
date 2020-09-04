# Python module for control of Shy (ELK-BLEDOM) bluetooth LED controller

# Copyright 2020 Ross Reedstrom <ross@reedstrom.org>
#
# This code is released under the terms of the MIT license. See the LICENSE
# file for more details.

import time

from bluepy import btle, BTLEInternalError


class shy:
    def __init__(self, mac):
        self.mac = mac

    def connect(self):
        self.device = btle.Peripheral(self.mac, addrType=btle.ADDR_TYPE_PUBLIC)
        self.writehandle = None
        handles = self.device.getCharacteristics()
        for handle in handles:
            if handle.uuid == "fff3":
                self.writehandle = handle

    def send_packet(self, data):
        initial = time.time()
        while True:
            if time.time() - initial >= 10:
                return False
            try:
                return self.writehandle.write(bytes(data))
            except BTLEInternalError:
                self.connect()

    def on(self):
        self.power = True
        self.send_packet(bytearray.fromhex("7e 00 04 01 00 00 00 00 ef"))

    def off(self):
        self.power = True
        self.send_packet(bytearray.fromhex("7e 00 04 00 00 00 00 00 ef"))

    def set_brightness(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self.brightness = value
        bytes = bytearray.fromhex(f"7e 00 01 {value:x} 00 00 00 00 ef")
        self.send_packet(bytes)

    def get_on(self):
        return self.power

    def get_brightness(self):
        return self.brightness
