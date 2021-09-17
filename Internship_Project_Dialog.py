from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PySide6 import QtGui
from PySide6.QtCore import Qt


class myDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('More Information Needed!')
        self.dialog_Layout = QGridLayout(parent = self)
        
        self.blackBoxYCoordinate_Label = QLabel(parent = self, text = 'The Crop Coordinate: (Pixels)')
        self.dialog_Layout.addWidget(self.blackBoxYCoordinate_Label, 0, 0, 1, 1) # --> 

        self.blackBoxYCoordinateEdit = QLineEdit(parent = self)
        self.blackBoxYCoordinateEdit.setAlignment(Qt.AlignCenter)
        self.blackBoxYCoordinateEdit.setValidator(QtGui.QIntValidator(bottom = 0)) # top = self.SIZE[0]
        self.dialog_Layout.addWidget(self.blackBoxYCoordinateEdit, 1, 0, 1, 4)

        self.imageLength_Label = QLabel(parent = self, text = 'The Length of each Image: (Seconds)')
        self.dialog_Layout.addWidget(self.imageLength_Label, 2, 0, 1, 1)

        self.imageLengthEdit = QLineEdit(parent = self)
        self.imageLengthEdit.setAlignment(Qt.AlignCenter)
        self.imageLengthEdit.setValidator(QtGui.QIntValidator(bottom = 0))
        self.dialog_Layout.addWidget(self.imageLengthEdit, 3, 0, 1, 4)

        self.submitButton = QPushButton(parent = self, text = 'Submit')
        self.dialog_Layout.addWidget(self.submitButton, 4, 3, 1, 1, Qt.AlignRight)

        self.setLayout(self.dialog_Layout)

class myDialogCtrl():
    def __init__(self, dialogView):
        self._dialogView = dialogView
        self.blackBoxYCoordinate = None
        self.imageLength = None
        self.connectSignals()

    def connectSignals(self):
        self._dialogView.submitButton.clicked.connect(self.submitClicked)

    def submitClicked(self):
        if self._dialogView.blackBoxYCoordinateEdit.text() == '':
            QMessageBox.critical(None, 'The Y-Coordinate Missing!', 'Please Enter a Y-Coordinate.')
        elif self._dialogView.imageLengthEdit.text() == '':
            QMessageBox.critical(None, 'Image Length Missing!', 'Please Enter a Time Length in Seconds.' )
        else:
            self.blackBoxYCoordinate = float(self._dialogView.blackBoxYCoordinateEdit.text())
            self.imageLength = float(self._dialogView.imageLengthEdit.text())
            self._dialogView.close()