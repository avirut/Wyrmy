import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

WIDTH = 1500
HEIGHT = 950

QtCore.QCoreApplication.addLibraryPath('//server/location/PyQt5/plugins')
app = QApplication(sys.argv)

screen_res = app.desktop().screenGeometry()
screen_width, screen_height = screen_res.width(), screen_res.height()

w = QWidget()
w.resize(WIDTH, HEIGHT)
w.move(int((screen_width/2)-(WIDTH/2)), int(((screen_height-100)/2)-(HEIGHT/2)))
w.setWindowTitle('Wyrmy')
w.setWindowIcon(QIcon('resources/wyrmytheworm.png'))
w.show()

sys.exit(app.exec_())
