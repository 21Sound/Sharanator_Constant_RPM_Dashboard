import can
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
import math
import os

os.system("sudo ip link set can0 down")
os.system("sudo ip link set can0 up type can bitrate 500000")

bus = can.interface.Bus(channel='can0', bustype='socketcan')

#app = QtWidgets.QApplication([])
#win = pg.GraphicsLayoutWidget(show=True, title="CAN Gauge")
#plot = win.addPlot()
#plot.hideAxis('bottom')
#plot.hideAxis('left')

#needle = pg.PlotDataItem(pen=pg.mkPen('r', width=4))
#plot.addItem(needle)

while(True):
    msg = bus.recv(timeout=0.01)
    if msg and msg.arbitration_id == 0x280:

        pedalPercent = msg.data[5] * 100.0 / 0xFA
        print(pedalPercent)

        RPM = ( (msg.data[3]<<8) + msg.data[2] ) * 0.25
        print(RPM)