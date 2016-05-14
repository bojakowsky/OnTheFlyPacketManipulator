import sys

from threading import Thread
from subprocess import call
from GUI.mainWindow import *


def main():
    try:
        call("iptables-save > iptables-backup", shell=True)
        call("iptables -t filter --flush", shell=True)
        call("iptables -t nat --flush", shell=True)
        call("iptables -t raw --flush", shell=True)
        call("iptables -t mangle --flush", shell=True)

        app = QtGui.QApplication(sys.argv)
        mainWindowRun()
        sys.exit(app.exec_())

    finally:
        print("closing..")
        call("iptables-restore < iptables-backup", shell=True)

if __name__ == '__main__':
    main()

