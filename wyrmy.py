import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QImageReader

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

fileName = QFileDialog.getOpenFileName(w, "Open Image", "/", "Image Files (*.png *.jpg *.bmp *.tiff *.tif)")
img = QtGui.QPixmap(fileName[0])

label = QLabel(w)
label.setPixmap(img)
w.resize(img.width(), img.height())
w.setWindowTitle('Wyrmy - ' + fileName[0])

w.show()

sys.exit(app.exec_())
