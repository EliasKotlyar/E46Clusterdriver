import serial
import time

MOTRONIC = 0x12
AUTOMATIC_TRANSMISSION = 0x32
IKE = 0x80
LCM = 0xD0


class DbusCommunication(object):

    def setup(self, config):
        self.debug = int(config['DEFAULT']['DEBUG'])
        if self.debug == 0:
            self._device = serial.Serial("/dev/ttyS4", 9600, parity=serial.PARITY_EVEN)

    def run(self):
        for address in [MOTRONIC, AUTOMATIC_TRANSMISSION, IKE, LCM]:
            print("Querying " + hex(address))
            data = self._execute(address, bytes([0x00]))
            print("Got:")
            # print(hex(data))
            # Delay to work around unknown issue (perhaps a bug in MultiCom?)
            time.sleep(0.03)

    def _execute(self, address, payload_str):
        payload = bytes.fromhex(payload_str)

        self._write(address, payload)
        echo = self._read()
        self._device.timeout = 5
        reply = self._read()
        if reply is None:
            raise InvalidAddress("invalid address")
        sender, payload = reply
        self._device.timeout = None
        if sender != address:
            raise ProtocolError("unexpected sender")
        status = payload[0]
        if status == 0xa0:
            return payload[1:]
        elif status == 0xa1:
            raise ComputerBusy("computer busy")
        elif status == 0xa2:
            raise InvalidCommand("invalid parameter")
        elif status == 0xff:
            raise InvalidCommand("invalid command")
        else:
            raise ProtocolError("unknown status")

    def _write(self, address, payload):
        size = 2 + len(payload) + 1
        message = bytes([address, size]) + payload
        buf = message + bytes([self._checksum(message)])
        # hexdump(buf)
        self._device.write(buf)

    def _read(self):
        try:
            address = self._device.read(1)[0]
        except IndexError:
            return None
        size = self._device.read(1)[0]
        remaining = size - 3
        if remaining > 0:
            payload = self._device.read(remaining)
        else:
            payload = bytes([])
        expected_checksum = self._checksum(bytes([address, size]) + payload)
        actual_checksum = self._device.read(1)[0]
        if actual_checksum != expected_checksum:
            raise ProtocolError("invalid checksum")
        return (address, payload)

    def _checksum(self, message):
        result = 0
        for b in message:
            result ^= b
        return result

    def setAnalog(self, input, value):
        hexStr = "0c"
        hexStr += "0" + input
        hexStr += format(value, '04x')
        print(hexStr)
        self._execute(IKE, hexStr)
        pass

    def setKilometer(self, kmh):
        self.setAnalog("a", kmh)

    def setRpm(self, rpm):
        rpm = rpm / 1000
        rpm = rpm * 316
        rpm = int(round(rpm, 0))
        self.setAnalog("b", rpm)

    def setFuel(self, fuel):
        self.setAnalog("c", fuel)

    def setCoolant(self, temperature):
        self.setAnalog("d", temperature)

    def setOil(self, temperature):
        self.setAnalog("e", temperature)

    def setLamps(self,value):
        hexStr = "0c"
        hexStr += "09"
        hexStr += format(value, '02x')
        #for x in range(6):
        #    hexStr += "00"
        self._execute(IKE, hexStr)

    def acticateTest(self):
        hexStr = "30"
        hexStr += "b4"
        self._execute(IKE, hexStr)

    def deactivateTest(self):
        hexStr = "9f"
        hexStr += "1b"
        self._execute(IKE, hexStr)




class ProtocolError(Exception):
    pass


class ComputerBusy(Exception):
    pass


class InvalidAddress(Exception):
    pass


class InvalidCommand(Exception):
    pass
