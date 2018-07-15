# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.6
# author: chenwi
# data:2018/7/12

import sys
from ui import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from tcga_download import WorkThread


class MyWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)  # from Ui_Dialog parent

        self.directory, self.fileName = "", ""
        self.thread = QThread()

        self.pushButton_4.clicked.connect(self.getDirectory)
        self.pushButton_3.clicked.connect(self.getFile)
        self.pushButton.clicked.connect(self.download_start)
        self.pushButton_2.clicked.connect(self.stopButton)

    def stopButton(self):
        if self.thread.isRunning():
            reply = QMessageBox.question(self, 'Message', "Are you sure to stop?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes and self.thread:
                self.thread.terminate()

                self.pushButton.setEnabled(True)
            else:
                pass

    def getFile(self):
        # simple file
        self.fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "C:/", "Text Files (*.txt)")
        self.lineEdit.setText(self.fileName)
        self.pushButton.setEnabled(True)  # repeat open file can also download
        self.label_5.setText("Have a nice day!")
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(0)

    def getDirectory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "选择文件夹", "")  # ""起始路径,空路径会记忆
        self.lineEdit_2.setText(self.directory)
        self.pushButton.setEnabled(True)
        self.label_5.setText("Have a nice day!")
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(0)

    def download_start(self):

        if self.directory and self.fileName:
            self.pushButton.setEnabled(False)
            self.label_5.setText("Have a nice day!")

            self.thread = WorkThread(self.fileName, self.directory)  # thread must be private self

            self.thread.signal1.connect(self.set_value1)
            self.thread.signal2.connect(self.set_value2)
            self.thread.signal3.connect(self.set_value3)
            self.thread.signal4.connect(self.set_value4)
            self.thread.start()


        else:
            box = QMessageBox()
            box.warning(self, "Warning", "File or directory is null !")

    def set_value1(self, l):

        if (l >= 0) and (l <= 100):
            self.progressBar_2.setValue(l)
            if l == 100:
                self.label_5.setText("<font color=#FF0000>Download completed. </font>")


        elif l == -1:
            box = QMessageBox()
            box.warning(self, "Warning", "File or directory error !")
            self.pushButton.setEnabled(True)
        else:
            box = QMessageBox()
            box.warning(self, "Warning", "Unknown error !")
            self.pushButton.setEnabled(True)

    def set_value2(self, l):
        if (l >= 0) and (l <= 100):
            self.progressBar.setValue(l)
            self.label_5.setText("Have a nice day! ")  # network is ok
            self.pushButton.setEnabled(False)  # when network is ok, the button is false
        elif l == 404:

            self.label_5.setText("<font color=#FF0000>Warning! Request failed. </font>")
            self.pushButton.setEnabled(True)
        else:
            # l==-1 other error
            box = QMessageBox()
            box.warning(self, "Warning", "Unknown error !")
            self.pushButton.setEnabled(True)

    def set_value3(self, l):
        tem = l[0]
        length = l[1]
        self.label_6.setText(f"Files: {tem} / {length}")

    def set_value4(self, l):
        if l == -1:
            self.label_5.setText(f"<font color=#FF0000>Manifest file error. </font>")
            self.thread.terminate()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to close?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    QApplication.addLibraryPath("./plugins")
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("TCGAD")
    window.setWindowIcon(QIcon('./down.PNG'))
    window.show()
    sys.exit(app.exec_())
