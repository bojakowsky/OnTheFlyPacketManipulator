import sys

import multiprocessing
from subprocess import call
from GUI.mainWindow import *




def runApp(queue):
    app = QtGui.QApplication(sys.argv)
    mv = MainView(queue)
    sys.exit(app.exec_())

def runPacketManager(queue):
    pm = PacketManager(queue)
    pm.run_manager()


def main():
    try:
        call("iptables-save > iptables-backup", shell=True)
        call("iptables -t filter --flush", shell=True)
        call("iptables -t nat --flush", shell=True)
        call("iptables -t raw --flush", shell=True)
        call("iptables -t mangle --flush", shell=True)


        queue = multiprocessing.Manager().list()

        packetManagerProcess = multiprocessing.Process(target=runPacketManager, args=(queue,))
        packetManagerProcess.start()

        appProcess = multiprocessing.Process(target=runApp, args=(queue,))
        appProcess.start()

    finally:
        packetManagerProcess.join()
        appProcess.join

        print("retoring...")
        call("iptables-restore < iptables-backup", shell=True)
        print("resotred.")

if __name__ == '__main__':
    main()

