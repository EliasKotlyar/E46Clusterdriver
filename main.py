from cmd import Cmd
from time import sleep

from lib import CanCommunication
from lib import KbusCommunication
from lib import DbusCommunication
import configparser


class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome to E46 Cluster. Type ? to list commands"

    canComm = CanCommunication.CanCommunication()
    kbusComm = KbusCommunication.KbusCommunication()
    dbusComm = DbusCommunication.DbusCommunication()

    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.canComm.setup(config)
        self.kbusComm.setup(config)
        self.dbusComm.setup(config)

    def do_blink(self, inp):
        self.canComm.blink()
        pass

    def do_backlight(self, inp):
        self.kbusComm.setBacklight(inp)
        pass

    def do_setrpm(self, inp):
        inp = int(inp)
        if(inp == 0):
            inp = 255
        self.dbusComm.setLamps(inp)
        #for x in range(0, 1000):
        #    self.kbusComm.sendMessage("80","0c09ff010203040506")
        pass


    def do_test(self, inp):
        self.dbusComm.acticateTest()
        sleep(10)
        self.dbusComm.deactivateTest()
        pass

    def do_setrpm(self, rpm):
        rpm = int(rpm)
        self.dbusComm.setRpm(rpm)

    def do_lamps(self, rpm):
        #for x in range(0, 5):
        self.dbusComm.setLamps(255)
        #    sleep(1)
        #    self.dbusComm.setLamps(0)
        #    sleep(1)


    def do_demo(self, demo):
        for x in range(0, 7000, 500):
            self.dbusComm.setRpm(x)
            sleep(0.2)
            if (x % 1000 == 0):
                self.canComm.setValue(int(x / 1000)+1)
        self.canComm.blink()
        self.dbusComm.setRpm(2000)


    def do_exit(self, inp):
        print("Bye")
        return True

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    blink_EOF = do_blink
    backlight_EOF = do_backlight
    setrpm_EOF = do_setrpm
    do_demoEOF = do_demo
    do_lampsEOF = do_lamps
    do_testEOF = do_test


if __name__ == '__main__':
    MyPrompt().cmdloop()
