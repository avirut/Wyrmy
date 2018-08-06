import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QImageReader


class Wyrmy(QWidget):

    def __init__(self, app):
        super(Wyrmy, self).__init__()

        # get basic information
        screen_res = app.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_res.width(), screen_res.height()

        # get images to use
        file_names_import = QFileDialog.getOpenFileNames(self, "Open Image", "/",
                                                         "Image Files (*.png *.jpg *.bmp *.tiff *.tif)")
        self.file_names = file_names_import[0]

        # create first image
        orig = QtGui.QPixmap(self.file_names[0])
        scale_by = self.screen_height*0.75/orig.height()
        self.img = orig.scaled(orig.width()*scale_by, orig.height()*scale_by, QtCore.Qt.KeepAspectRatio)

        panel_height = self.screen_height*0.1

        self.width, self.height = self.img.width(), self.img.height()+panel_height

        self.init_win()

        self.show()

    def init_win(self):
        self.resize(self.width, self.height)
        self.move(int((self.screen_width / 2) - (self.width / 2)),
                  int(((self.screen_height - 100) / 2) - (self.height / 2)))
        self.setWindowIcon(QIcon('resources/wyrmytheworm.png'))
        label = QLabel(self)
        label.setPixmap(self.img)
        self.setWindowTitle('Wyrmy - ' + self.file_names[0])


if __name__ == '__main__':
    # QtCore.QCoreApplication.addLibraryPath('//server/location/PyQt5/plugins')
    app = QApplication(sys.argv)
    window = Wyrmy(app)
    sys.exit(app.exec_())
