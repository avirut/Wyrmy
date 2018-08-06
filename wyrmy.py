import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QGroupBox, QGridLayout, QProgressBar
from PyQt5.QtGui import QIcon


class Wyrmy(QWidget):

    def __init__(self, outside):
        super(Wyrmy, self).__init__()

        # get/set basic information
        self.app_control = outside
        screen_res = self.app_control.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_res.width(), screen_res.height()
        self.setWindowIcon(QIcon('resources/wyrmytheworm.png'))

        # get images to use
        self.index = 0
        self.file_names = []
        self.images = {}
        self.load_images()

        # create first image, determine all dimensions
        self.label, self.panel_height, self.width, self.height = QLabel(self), 0, 0, 0
        self.alive, self.dead = None, None
        self.percent, self.previous, self.next = None, None, None

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        orig = QtGui.QPixmap(self.file_names[self.index])
        scale_by = self.screen_height * 0.75 / orig.height()
        self.img = orig.scaled(orig.width() * scale_by, orig.height() * scale_by, QtCore.Qt.KeepAspectRatio)
        self.panel_height = self.screen_height * 0.1
        self.width, self.height = self.img.width(), self.img.height() + self.panel_height

        self.panel = QGroupBox()
        self.panel.move(0, self.img.height())
        self.panel.setFixedWidth(self.width)
        self.panel.setFixedHeight(self.panel_height)
        self.layout.addWidget(self.panel, 1, 0)

        self.move(int((self.screen_width / 2) - (self.width / 2)),
                  int(((self.screen_height - 100) / 2) - (self.height / 2)))

        self.layout.addWidget(self.label, 0, 0)

        self.refresh()

        self.show()

    def load_images(self):
        file_names_import = QFileDialog.getOpenFileNames(self, "Open Image", "/",
                                                         "Image Files (*.png *.jpg *.bmp *.tiff *.tif)")
        self.file_names = file_names_import[0]

    def refresh(self):
        # take care of index wraparounds
        if len(self.file_names) == 0:
            self.app_control.quit()
        if self.index > len(self.file_names)-1:
            self.index = 0
        if self.index < 0:
            self.index = len(self.file_names)-1

        curr_img_name = self.file_names[self.index]
        last_index = curr_img_name.rfind('/')
        self.panel.setTitle(self.file_names[self.index][last_index + 1:last_index + 4])

        orig = QtGui.QPixmap(self.file_names[self.index])
        scale_by = self.screen_height * 0.75 / orig.height()
        self.img = orig.scaled(orig.width() * scale_by, orig.height() * scale_by, QtCore.Qt.KeepAspectRatio)

        self.label.setPixmap(self.img)
        self.setWindowTitle('Wyrmy - ' + curr_img_name)

    def safe_index(self, index):
        if index < 0:
            new_ind = len(self.file_names) + index
        elif index > len(self.file_names) - 1:
            new_ind = index - len(self.file_names) - 1
        else:
            new_ind = index
        if new_ind < 0:
            new_ind = 0
        elif new_ind > len(self.file_names) - 1:
            new_ind = len(self.file_names) -1
        return new_ind

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_A:
            self.index -= 1
        if event.key() == QtCore.Qt.Key_D:
            self.index += 1
        self.refresh()
        event.accept()

    # def reload_images(self):
    #     for i in range(self.index-24, self.index+24):
    #         if i < 0:
    #             new_ind = len(self.file_names)+i
    #         elif i > len(self.file_names)-1:
    #             new_ind = i-len(self.file_names)-1
    #         else:
    #             new_ind = i
    #
    #         if new_ind < 0 or new_ind > len(self.file_names):
    #             new_ind = self.index
    #
    #         if self.file_names[new_ind] not in self.images:
    #             orig = QtGui.QPixmap(self.file_names[new_ind])
    #             scale_by = self.screen_height * 0.75 / orig.height()
    #             self.images[self.file_names[new_ind]] = (orig.scaled(orig.width() * scale_by, orig.height() *
    #                                                   scale_by, QtCore.Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Wyrmy(app)
    sys.exit(app.exec_())
