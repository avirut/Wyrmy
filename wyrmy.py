import sys
import pickle
import resources

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QGridLayout, QBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


# stores coordinate points
class Pair:

    def __init__(self, x, y):
        self.x = x
        self.y = y


# stores data for each worm picture
class WormPic:

    def __init__(self, filename=''):
        self.filename = filename
        self.dead = []
        self.alive = []


# main application object
class Wyrmy(QWidget):

    def __init__(self, outside):
        super(Wyrmy, self).__init__()

        # get/set basic information
        self.app_control = outside
        screen_res = self.app_control.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_res.width(), screen_res.height()
        self.setWindowIcon(QIcon(':/resources/wyrmytheworm.png'))

        # get images to use
        self.worms = {}
        self.index = 0
        self.file_names = []
        self.images = {}
        self.load_images()

        # create first image, determine all dimensions
        self.label, self.panel_height, self.width, self.height = QLabel(self), 0, 0, 0
        self.alive, self.dead = QLabel(), QLabel()
        self.percent = QLabel()
        self.open, self.save, self.export = QPushButton(), QPushButton(), QPushButton()
        self.curr_img_disp = QLabel()
        self.alive.setText('Alive: 0')
        self.dead.setText('Dead: 0')
        self.percent.setText('Percent: 0%')
        self.open.setText('Open')
        self.open.setToolTip('Load a data file')
        self.save.setText('Save')
        self.save.setToolTip('Save a data file')
        self.export.setText('Export')
        self.export.setToolTip('Export data as CSV')
        self.open.setMaximumWidth(100)
        self.save.setMaximumWidth(100)
        self.export.setMaximumWidth(100)
        self.open.clicked.connect(self.open_file)
        self.save.clicked.connect(self.save_file)
        self.export.clicked.connect(self.export_data)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.panel_layout = QGridLayout(self.layout.widget())
        self.panel_layout.setContentsMargins(15, 0, 15, 0)

        self.orig = QtGui.QPixmap(self.file_names[self.index])
        scale_by = self.screen_height * 0.75 / self.orig.height()
        self.img = self.orig.scaled(self.orig.width() * scale_by, self.orig.height() * scale_by, QtCore.Qt.KeepAspectRatio)
        self.panel_height = self.screen_height * 0.1
        self.width, self.height = self.img.width(), self.img.height() + self.panel_height

        # self.panel = QGroupBox()
        # self.layout.addWidget(self.panel)
        # self.panel.move(0, self.img.height())
        # self.panel.setFixedWidth(self.width)
        # self.panel.setFixedHeight(self.panel_height)

        self.layout.addLayout(self.panel_layout, 1, 0)

        self.panel_layout.addWidget(self.alive, 0, 0)
        self.panel_layout.addWidget(self.dead, 1, 0)
        self.panel_layout.addWidget(self.percent, 2, 0)
        self.panel_layout.addWidget(self.curr_img_disp, 1, 1)
        self.panel_layout.addWidget(self.open, 0, 2)
        self.panel_layout.addWidget(self.save, 1, 2)
        self.panel_layout.addWidget(self.export, 2, 2)

        startX = int((self.screen_width / 2) - (self.width / 2))
        startY = int(((self.screen_height - 100) / 2) - (self.height / 2))
        self.move(startX, startY)

        self.label.mousePressEvent = self.image_clicked
        self.dead_pic = QtGui.QPixmap(':/resources/red_target_scaled.png')
        self.alive_pic = QtGui.QPixmap(':/resources/green_target_scaled.png')

        self.layout.addWidget(self.label, 0, 0)

        self.markers = QBoxLayout(QBoxLayout.LeftToRight)
        self.layout.addChildLayout(self.markers)

        self.refresh()

        self.show()

    def load_images(self):
        file_names_import = QFileDialog.getOpenFileNames(self, "Open Image", "/",
                                                         "Image Files (*.png *.jpg *.bmp *.tiff *.tif)")
        self.file_names = file_names_import[0]
        for name in self.file_names:
            self.worms[Wyrmy.pic_name(name)] = WormPic(filename=Wyrmy.pic_name(name))

    def refresh(self):
        # take care of index wraparounds
        if len(self.file_names) == 0:
            self.app_control.quit()
        if self.index > len(self.file_names)-1:
            self.index = 0
        if self.index < 0:
            self.index = len(self.file_names)-1

        curr_img_name = self.file_names[self.index]
        # self.panel.setTitle(Wyrmy.pic_name(self.file_names[self.index]))

        orig = QtGui.QPixmap(self.file_names[self.index])
        scale_by = self.screen_height * 0.75 / orig.height()
        self.img = orig.scaled(orig.width() * scale_by, orig.height() * scale_by, QtCore.Qt.KeepAspectRatio)

        self.label.setPixmap(self.img)
        self.setWindowTitle('Wyrmy - ' + curr_img_name)

        curr_pic = self.worms[Wyrmy.pic_name(self.file_names[self.index])]

        self.curr_img_disp.setText(Wyrmy.pic_name(curr_img_name))

        num_dead = len(curr_pic.dead)
        num_alive = len(curr_pic.alive)
        alive_text = 'Alive: ' + str(num_alive)
        self.alive.setText(alive_text)
        dead_text = 'Dead: ' + str(num_dead)
        self.dead.setText(dead_text)
        if num_dead + num_alive > 0:
            percent_text = '% Dead: ' + str(100 * num_dead / (num_dead + num_alive))
        else:
            percent_text = '% Dead: 0'
        self.percent.setText(percent_text)

        for ind in reversed(range(self.markers.count())):
            widget = self.markers.takeAt(ind).widget()
            if widget is not None:
                widget.deleteLater()

        for coords in curr_pic.dead:
            curr_dead = QLabel(self)
            curr_dead.setPixmap(self.dead_pic)
            self.markers.addWidget(curr_dead)
            curr_dead.move(coords.x*self.img.width()-25, coords.y*self.img.height()-12.5)
            # print(coords.x, ', ', coords.y)
        for coords in curr_pic.alive:
            curr_alive = QLabel(self)
            curr_alive.setPixmap(self.alive_pic)
            self.markers.addWidget(curr_alive)
            curr_alive.move(coords.x * self.img.width()-25, coords.y * self.img.height()-12.5)
            # print(coords.x, ', ', coords.y)

    def safe_index(self, index):
        if index < 0:
            new_ind = len(self.file_names) + index
        elif index > len(self.file_names) - 1:
            new_ind = index - len(self.file_names)
        else:
            new_ind = index
        if new_ind < 0:
            new_ind = 0
        elif new_ind > len(self.file_names) - 1:
            new_ind = len(self.file_names) - 1
        return new_ind

    @staticmethod
    def pic_name(file_name):
        last_index = file_name.rfind('/')
        return file_name[last_index + 1:last_index + 4]

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_W:
            self.index -= 1
        if event.key() == QtCore.Qt.Key_S:
            self.index += 1
        if event.key() == QtCore.Qt.Key_A:
            start = QWidget.mapToGlobal(self.label, self.label.pos())
            click_x = (QtGui.QCursor.pos().x() - start.x()) / self.img.width()
            click_y = (QtGui.QCursor.pos().y() - start.y()) / self.img.height()
            click = Pair(click_x, click_y)
            self.worms[Wyrmy.pic_name(self.file_names[self.index])].alive.append(click)
        if event.key() == QtCore.Qt.Key_D:
            start = QWidget.mapToGlobal(self.label, self.label.pos())
            click_x = (QtGui.QCursor.pos().x() - start.x()) / self.img.width()
            click_y = (QtGui.QCursor.pos().y() - start.y()) / self.img.height()
            click = Pair(click_x, click_y)
            self.worms[Wyrmy.pic_name(self.file_names[self.index])].dead.append(click)
        if event.key() == QtCore.Qt.Key_X:
            curr_pic = self.worms[Wyrmy.pic_name(self.file_names[self.index])]
            curr_pic.alive = []
            curr_pic.dead = []
        self.refresh()
        event.accept()

    def image_clicked(self, event):
        click = Pair(event.x()/self.img.width(), event.y()/self.img.height())
        if event.button() == QtCore.Qt.LeftButton:
            self.worms[Wyrmy.pic_name(self.file_names[self.index])].alive.append(click)
        if event.button() == QtCore.Qt.RightButton:
            self.worms[Wyrmy.pic_name(self.file_names[self.index])].dead.append(click)
        # if event.button() == QtCore.Qt.MidButton:
        #     curr_pic = self.worms[Wyrmy.pic_name(self.file_names[self.index])]
        #     max_diff_x = 25/self.img.width()
        #     max_diff_y = 25/self.img.height()
        #     for ind, coords in enumerate(curr_pic.alive):
        #         if abs(coords.x-click.x) < max_diff_x and abs(coords.y-click.y) < max_diff_y:
        #             del curr_pic.alive[ind]
        #             break
        #     for ind, coords in enumerate(curr_pic.dead):
        #         if abs(coords.x-click.x) < max_diff_x and abs(coords.y-click.y) < max_diff_y:
        #             del curr_pic.dead[ind]
        #             break
        self.refresh()
        event.accept()

    @pyqtSlot()
    def open_file(self):
        input_from = QFileDialog.getOpenFileName(self, caption='Open File', filter='Wyrmy Data (*.wyrm)')
        if len(input_from[0]) > 0:
            with open(input_from[0], 'rb') as reading:
                self.worms = pickle.load(reading)
                reading.close()
        self.refresh()

    @pyqtSlot()
    def save_file(self):
        output_at = QFileDialog.getSaveFileName(self, caption='Save File', filter='Wyrmy Data (*.wyrm)')
        if len(output_at[0]) > 0:
            with open(output_at[0], 'wb') as out:
                pickle.dump(self.worms, out)
                out.close()

    @pyqtSlot()
    def export_data(self):
        output_at = QFileDialog.getSaveFileName(self, caption='Save File', filter='CSV (Comma delimited) (*.csv)')
        if len(output_at[0]) > 0:
            out = open(output_at[0], 'a')
            out.write('Name,Alive,Dead\n')
            for name in self.file_names:
                curr = self.worms[Wyrmy.pic_name(name)]
                this_pic = str(curr.filename) + ',' + str(len(curr.alive)) + ',' + str(len(curr.dead)) + '\n'
                out.write(this_pic)
            out.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Wyrmy(app)
    sys.exit(app.exec_())
