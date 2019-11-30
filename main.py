from cmd import Cmd

from lib import CanCommunication
import configparser


class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome to E46 Cluster. Type ? to list commands"

    canComm = CanCommunication.CanCommunication()

    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.canComm.setup(config)

    def do_blink(self, inp):
        self.canComm.blink()
        pass

    def do_exit(self, inp):
        print("Bye")
        return True

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    blink_EOF = do_blink


if __name__ == '__main__':
    MyPrompt().cmdloop()
