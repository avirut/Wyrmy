import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QGroupBox, QGridLayout
from PyQt5.QtGui import QIcon, QImageReader


class Wyrmy(QWidget):

    def __init__(self, outside):
        super(Wyrmy, self).__init__()

        # get/set basic information
        screen_res = outside.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_res.width(), screen_res.height()
        self.setWindowIcon(QIcon('resources/wyrmytheworm.png'))

        # get images to use
        self.file_names = []
        self.load_images()
        self.index = 0

        # create first image, determine all dimensions
        self.img, self.label, self.panel_height, self.width, self.height = None, None, 0, 0, 0
        self.layout, self.panel, self.alive, self.dead = None, None, None, None
        self.percent, self.previous, self.next = None, None, None
        self.refresh()

        self.show()

    def load_images(self):
        file_names_import = QFileDialog.getOpenFileNames(self, "Open Image", "/",
                                                         "Image Files (*.png *.jpg *.bmp *.tiff *.tif)")
        self.file_names = file_names_import[0]

    def refresh(self):
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        orig = QtGui.QPixmap(self.file_names[self.index])
        scale_by = self.screen_height*0.75/orig.height()
        self.img = orig.scaled(orig.width()*scale_by, orig.height()*scale_by, QtCore.Qt.KeepAspectRatio)
        self.panel_height = self.screen_height*0.1
        self.width, self.height = self.img.width(), self.img.height()+self.panel_height

        curr_img_name = self.file_names[self.index]
        last_index = curr_img_name.rfind('/')
        self.panel = QGroupBox(self.file_names[self.index][last_index+1:last_index+4])
        self.panel.move(0, self.img.height())
        self.panel.setFixedWidth(self.width)
        self.panel.setFixedHeight(self.panel_height)
        self.layout.addWidget(self.panel, 1, 0)

        self.resize(self.width, self.height)
        self.move(int((self.screen_width/2)-(self.width/2)),
                  int(((self.screen_height-100)/2)-(self.height / 2)))
        self.label = QLabel(self)
        self.label.setPixmap(self.img)
        self.layout.addWidget(self.label, 0, 0)
        self.setWindowTitle('Wyrmy - ' + curr_img_name)


if __name__ == '__main__':
    # QtCore.QCoreApplication.addLibraryPath('//server/location/PyQt5/plugins')
    app = QApplication(sys.argv)
    window = Wyrmy(app)
    sys.exit(app.exec_())
