from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import platform

from Ui_haverhill import Ui_Form

from gis import GIS


class Haverhill(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Haverhill, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle('Haverhill Constituent Services')

        # set style
        palette = QtGui.QPalette()
        palette.setColor(self.backgroundRole(), QColor('#FFFFFF'))
        self.setPalette(palette)

        with open('resource/style/blue.css', 'r', encoding='UTF-8') as f:
            self.setStyleSheet(f.read())
        self.label.setPixmap(QPixmap('resource/img/haverhill.png'))
        self.label.setScaledContents(True)

        self.label_5.setStyleSheet("color:red")
        self.label_6.setStyleSheet("color:red")

        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)

        # affair
        self.gis = GIS()
        self.requests_file_path = None
        self.refuse_routes_file_path = None
        self.directory_path = self.gis.get_directory_path()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if self.requests_file_path is None:
            q_message_box = QMessageBox.warning(self, 'warning', 'Please select one file!')
        elif not self.requests_file_path.endswith('.csv'):
            q_message_box = QMessageBox.warning(self, 'warning', 'The selected file should be csv format!')
        else:
            self.pushButton.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.label_5.setText("Working...")
            # start a thread
            requests_processing = RequestsProcessing(self.gis, self.requests_file_path)
            requests_processing.signal.connect(self.handle_requests_processing)
            requests_processing.start()
            requests_processing.exec()

    @pyqtSlot(int)
    def handle_requests_processing(self, val: int):
        if val == 1:
            q_message_box = QMessageBox.information(self, 'success', 'The QAlert requests file has been successfully '
                                                                     'processed!')
        else:
            q_message_box = QMessageBox.warning(self, 'warning', "The file doesn't have the right format!")
        self.pushButton.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.label_5.clear()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        if (self.refuse_routes_file_path is not None) and (not self.refuse_routes_file_path.endswith('.json')):
            q_message_box = QMessageBox.warning(self, 'warning', 'The selected file should be json format!')
        else:
            self.pushButton_2.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.label_6.setText("Working...")
            # start a thread
            refuse_routes_drawing = RefuseRoutesDrawing(self.gis, self.refuse_routes_file_path)
            refuse_routes_drawing.signal.connect(self.handle_refuse_routes_drawing)
            refuse_routes_drawing.start()
            refuse_routes_drawing.exec()

    @pyqtSlot(int)
    def handle_refuse_routes_drawing(self, val: int):
        if val == 1:
            q_message_box = QMessageBox.information(self, 'success', 'The refuse refuses file has been successfully '
                                                                     'processed!')
        else:
            q_message_box = QMessageBox.warning(self, 'warning', "The file doesn't have the right format!")
        self.pushButton_2.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.label_6.clear()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        system_name = platform.system()
        if system_name == 'Windows':
            os.system('start ' + self.directory_path)
        else:
            os.system('open ' + self.directory_path)

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        self.lineEdit.clear()

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        self.lineEdit_2.clear()

    @pyqtSlot()
    def on_toolButton_clicked(self):
        res = QFileDialog.getOpenFileName(self, 'open file', '/')
        if res[0]:
            file_path = res[0]
            self.lineEdit.setText(file_path)
            self.requests_file_path = file_path

    @pyqtSlot()
    def on_toolButton_2_clicked(self):
        res = QFileDialog.getOpenFileName(self, 'open file', '/')
        if res[0]:
            file_path = res[0]
            self.lineEdit_2.setText(file_path)
            self.refuse_routes_file_path = file_path


class RequestsProcessing(QtCore.QThread):
    signal = pyqtSignal(int)

    def __init__(self, gis, requests_file_path):
        QThread.__init__(self)
        self.gis = gis
        self.requests_file_path = requests_file_path

    def run(self):
        try:
            self.gis.process_requests(self.requests_file_path)
            self.signal.emit(1)
        except Exception as e:
            print(e)
            self.signal.emit(0)


class RefuseRoutesDrawing(QtCore.QThread):
    signal = pyqtSignal(int)

    def __init__(self, gis, refuse_routes_file_path):
        QThread.__init__(self)
        self.gis = gis
        self.refuse_routes_file_path = refuse_routes_file_path

    def run(self):
        try:
            if self.refuse_routes_file_path is None:
                self.gis.draw_refuse_routes_map()
            else:
                self.gis.draw_refuse_routes_map(self.refuse_routes_file_path)
            self.signal.emit(1)
        except Exception as e:
            print(e)
            self.signal.emit(2)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Haverhill()
    ui.show()
    sys.exit(app.exec_())
