from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PySide6 import QtGui
from PySide6.QtCore import Qt


class myDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('More Information Needed!')
        self.dialog_Layout = QGridLayout(parent = self)
        
        self.cropCoordinate_Label = QLabel(parent = self, text = 'The Crop Coordinate: (Pixels)')
        self.dialog_Layout.addWidget(self.cropCoordinate_Label, 0, 0, 1, 1) # --> The First Label for Crop Coordinate

        self.cropCoordinateEdit = QLineEdit(parent = self)
        self.cropCoordinateEdit.setAlignment(Qt.AlignCenter)
        self.cropCoordinateEdit.setValidator(QtGui.QIntValidator(bottom = 0)) # top = self.SIZE[0]
        self.dialog_Layout.addWidget(self.cropCoordinateEdit, 1, 0, 1, 4) # --> The First Line Edit for Crop Coordinate

        self.imageLength_Label = QLabel(parent = self, text = 'The Length of each Image: (Seconds)')
        self.dialog_Layout.addWidget(self.imageLength_Label, 2, 0, 1, 1)# --> The Second Label for Time Length

        self.imageLengthEdit = QLineEdit(parent = self)
        self.imageLengthEdit.setAlignment(Qt.AlignCenter)
        self.imageLengthEdit.setValidator(QtGui.QIntValidator(bottom = 0))
        self.dialog_Layout.addWidget(self.imageLengthEdit, 3, 0, 1, 4) # --> The Second Line Edit for Time Length

        self.submitButton = QPushButton(parent = self, text = 'Submit')
        self.dialog_Layout.addWidget(self.submitButton, 4, 3, 1, 1, Qt.AlignRight) # --> Submit Button

        self.setLayout(self.dialog_Layout)

class myDialogCtrl():
    def __init__(self, dialogView):
        self._dialogView = dialogView
        self.cropCoordinate = None
        self.imageLength = None
        self.connectSignals()

    def connectSignals(self):
        self._dialogView.submitButton.clicked.connect(self.submitClicked)

    def submitClicked(self):
        if self._dialogView.cropCoordinateEdit.text() == '':
            QMessageBox.critical(None, 'The Y-Coordinate Missing!', 'Please Enter a Y-Coordinate.')
        elif self._dialogView.imageLengthEdit.text() == '':
            QMessageBox.critical(None, 'Image Length Missing!', 'Please Enter a Time Length in Seconds.' )
        else:
            self.cropCoordinate = float(self._dialogView.cropCoordinateEdit.text())
            self.imageLength = float(self._dialogView.imageLengthEdit.text())
            self._dialogView.close()