import multiprocessing
from GUI.mainWindow import *
from LOGIC.PacketManager import *


app = QtGui.QApplication(sys.argv)

def runApp(queue, queueRaw):
    mv = MainView(queue, queueRaw)
    sys.exit(app.exec_())

def runPacketManager(queue, queueRaw):
    pm = PacketManager(queue, queueRaw)
    pm.run_manager()


def main():
    try:
        call("iptables-save > iptables-backup", shell=True)
        call("iptables -t filter --flush", shell=True)
        call("iptables -t nat --flush", shell=True)
        call("iptables -t raw --flush", shell=True)
        call("iptables -t mangle --flush", shell=True)


        queue = multiprocessing.Manager().list()
        queueRaw = multiprocessing.Manager().list()
        packetManagerProcess = multiprocessing.Process(target=runPacketManager, args=(queue, queueRaw, ))
        packetManagerProcess.daemon = True
        packetManagerProcess.start()

        appProcess = multiprocessing.Process(target=runApp, args=(queue, queueRaw))
        appProcess.daemon = False
        appProcess.start()

        appProcess.join()
        packetManagerProcess.terminate()
    finally:
        print("Retoring ip tables...")
        call("iptables-restore < iptables-backup", shell=True)
        print("Resotred.")

        print("Cleaning up.")
        call("pkill -f ApplicationMain.py", shell=True) #making sure scapy nfqueue has been closed
        print("Bye!")

if __name__ == '__main__':
    main()

