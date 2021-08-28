import Internship_Project_Ctrl
import sys, os
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QMainWindow, QPlainTextEdit, QVBoxLayout, QFrame
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QGridLayout, QMessageBox
from PySide6.QtCore import Qt


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        # General Setup
        self.setWindowTitle("Photo Editor")
        self.setFixedSize(600, 550)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setAlignment(Qt.AlignTop)

        # -----Beginning of First Layout-----
        self.firstLayout = QGridLayout()

        self.srcPathLabel = QLabel('Source Path:')
        self.firstLayout.addWidget(self.srcPathLabel, 0, 0)

        self.srcDisplay = QLineEdit()
        self.srcDisplay.setAlignment(Qt.AlignCenter)
        self.srcDisplay.setReadOnly(True)
        self.browseButton1 = QPushButton('Browse')
        self.firstLayout.addWidget(self.srcDisplay, 1, 0, 1, 5)
        self.firstLayout.addWidget(self.browseButton1, 1, 5, 1, 1)

        self.destPathLabel = QLabel('Destination Path:')
        self.firstLayout.addWidget(self.destPathLabel, 2, 0)

        self.destDisplay = QLineEdit()
        self.destDisplay.setAlignment(Qt.AlignCenter)
        self.destDisplay.setReadOnly(True)
        self.browseButton2 = QPushButton('Browse')
        self.firstLayout.addWidget(self.destDisplay, 3, 0, 1, 5)
        self.firstLayout.addWidget(self.browseButton2, 3, 5, 1 ,1)

        self.fileNameLabel = QLabel('File Name:')
        self.firstLayout.addWidget(self.fileNameLabel, 4, 0, 1, 3)
        self.yCoordinateLabel = QLabel('Y Coordinate:')
        self.firstLayout.addWidget(self.yCoordinateLabel, 4, 3, 1, 3)
        
        self.fileName = QLineEdit()
        self.fileName.setPlaceholderText('Enter the Name')
        self.fileName.setAlignment(Qt.AlignCenter)
        self.firstLayout.addWidget(self.fileName, 5, 0, 1, 3)

        self.yCoordinate = QLineEdit() 
        self.yCoordinate.setPlaceholderText('Enter the Y Coordinate')
        self.yCoordinate.setAlignment(Qt.AlignCenter)
        self.yCoordinate.setValidator(QtGui.QIntValidator(bottom = 0))
        self.firstLayout.addWidget(self.yCoordinate, 5, 3, 1, 3 )

        self.recordStartTimeLabel = QLabel('Record Start Time:')
        self.firstLayout.addWidget(self.recordStartTimeLabel, 6, 0, 1, 3)
        self.singularTimeLengthLabel = QLabel('Duration of Each File: (Seconds)')
        self.firstLayout.addWidget(self.singularTimeLengthLabel, 6, 3, 1, 3)

        self.recordStartTime = QLineEdit()
        self.recordStartTime.setPlaceholderText('HH:MM:SS')
        self.recordStartTime.setAlignment(Qt.AlignCenter)
        self.recordStartTime.setValidator(QtGui.QRegularExpressionValidator(r"[0-1]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}|[2]{1}[0-4]{1}:[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}"))
        self.firstLayout.addWidget(self.recordStartTime, 7, 0, 1, 3)

        self.singularTimeLength = QLineEdit()
        self.singularTimeLength.setPlaceholderText('Enter the Duration of Each Image in Seconds')
        self.singularTimeLength.setAlignment(Qt.AlignCenter)
        self.singularTimeLength.setValidator(QtGui.QIntValidator(bottom = 0))
        self.firstLayout.addWidget(self.singularTimeLength, 7, 3, 1, 3)

        self.runButton1 = QPushButton('Merge')
        self.runButton1.setFixedHeight(25)
        self.firstLayout.addWidget(self.runButton1, 8, 0, 1, 6)

        self.generalLayout.addLayout(self.firstLayout)

        # -----End of First Layout-----

        self.generalLayout.addSpacing(6)
        self.horizontalLine = QFrame()
        self.horizontalLine.setFrameShape(QFrame.HLine)
        self.horizontalLine.setFrameShadow(QFrame.Sunken)
        self.generalLayout.addWidget(self.horizontalLine)     

        # -----Beginning of Second Layout-----
        self.secondLayout = QGridLayout()

        # Labels
        self.startTimeLabel = QLabel('Start Time:')
        self.endTimeLabel = QLabel('End Time:')
        self.colorComboLabel = QLabel('Color:')
        self.secondLayout.addWidget(self.startTimeLabel, 0, 0, 1, 2)
        self.secondLayout.addWidget(self.endTimeLabel, 0, 2, 1, 2)
        self.secondLayout.addWidget(self.colorComboLabel, 0, 4, 1, 1)

        # Buttons
        self.startTime = QLineEdit()
        self.startTime.setPlaceholderText('HH:MM:SS')
        self.startTime.setValidator(QtGui.QRegularExpressionValidator(r"[0-9]{1,2}:[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}"))
        self.startTime.setAlignment(Qt.AlignCenter)
        self.endTime = QLineEdit()
        self.endTime.setPlaceholderText('HH:MM:SS')
        self.endTime.setValidator(QtGui.QRegularExpressionValidator(r"[0-9]{1,2}:[0-5]{0,1}[0-9]{1}:[0-5]{0,1}[0-9]{1}"))
        self.endTime.setAlignment(Qt.AlignCenter)
        self.colorCombo = QComboBox()
        self.colorCombo.addItem('Black')
        self.colorCombo.addItem('White')
        self.colorCombo.addItem('Green')
        self.colorCombo.addItem('Red')
        self.colorCombo.addItem('Blue')
        self.colorCombo.addItem('Yellow')
        self.secondLayout.addWidget(self.startTime, 1, 0, 1, 2)
        self.secondLayout.addWidget(self.endTime, 1, 2, 1, 2)
        self.secondLayout.addWidget(self.colorCombo, 1, 4, 1, 1)


        self.plainTextLabel = QLabel('Comment:')
        self.secondLayout.addWidget(self.plainTextLabel, 2, 0)
        self.plainText = QPlainTextEdit()
        self.plainText.setPlaceholderText('Enter Comment')
        self.secondLayout.addWidget(self.plainText, 3, 0, 1, 5)

        self.runButton2 = QPushButton('Annotate')
        self.secondLayout.addWidget(self.runButton2, 4, 0, 1, 5)

        self.generalLayout.addLayout(self.secondLayout)
        #-----End of Second Layout


        self.stdBtns = QDialogButtonBox()
        self.stdBtns.setStandardButtons(QDialogButtonBox.Close)
        self.generalLayout.addWidget(self.stdBtns)

        
        self._centralWidget.setLayout(self.generalLayout)
    
       

def main():
    app = QApplication(sys.argv)
    GUI = MainWin()
    Ctrl = Internship_Project_Ctrl.MainWinCtrl(GUI)
    GUI.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()  
