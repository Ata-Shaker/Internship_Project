import sys, os
import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog
from PySide6.QtCore import Qt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from functools import partial




class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.LAST_INNER_LAYOUT_POSITION = 7

        # General Setup
        self.setWindowTitle("Photo Editor")
        self.setFixedSize(400, 400)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setAlignment(Qt.AlignTop)
        
        self.pathLabel = QLabel('Source Path:')
        self.generalLayout.insertWidget(0, self.pathLabel) 

        #General Layout
        self.srclayout = QHBoxLayout() 
        self.srcDisplay = QLineEdit()
        self.srcDisplay.setReadOnly(True)
        self.browseButton1 = QPushButton('Browse')
        self.srclayout.addWidget(self.srcDisplay)
        self.srclayout.addWidget(self.browseButton1)
        self.generalLayout.insertLayout(1, self.srclayout)

        self.pathLabel = QLabel('Destination Path:')
        self.generalLayout.insertWidget(2, self.pathLabel)

        self.destLayout = QHBoxLayout()
        self.destDisplay = QLineEdit()
        self.destDisplay.setReadOnly(True)
        self.browseButton2 = QPushButton('Browse')
        self.destLayout.addWidget(self.destDisplay)
        self.destLayout.addWidget(self.browseButton2)
        self.generalLayout.insertLayout(3, self.destLayout)

        self.generalLayout.insertSpacing(4, 5)

        self.runButton1 = QPushButton('Run')
        self.runButton1.setFixedHeight(25)
        self.generalLayout.addWidget(self.runButton1)

        self.generalLayout.insertSpacing(6, 5)


        self.insertLayout()

        self.stdBtns = QDialogButtonBox()
        self.stdBtns.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        self.generalLayout.addWidget(self.stdBtns)
        
        self._centralWidget.setLayout(self.generalLayout)
    

    def insertLayout(self):        
        innerLayout = QVBoxLayout()


        # Labels
        labelLayout = QHBoxLayout()
        startTimeLabel = QLabel('Start Time:')
        endTimeLabel = QLabel('End Time:')
        colorComboLabel = QLabel('Color:')
        labelLayout.addWidget(startTimeLabel)
        labelLayout.addWidget(endTimeLabel)
        labelLayout.addWidget(colorComboLabel)
        labelLayout.insertSpacing(1,95)
        labelLayout.insertSpacing(3,94)
        innerLayout.addLayout(labelLayout)

        # Buttons
        btnLayout = QHBoxLayout()
        startTime = QLineEdit()
        startTime.setInputMask('99:99:99')
        endTime = QLineEdit()
        endTime.setInputMask('99:99:99')
        colorCombo = QComboBox()
        colorCombo.addItem('Black')
        colorCombo.addItem('White')
        colorCombo.addItem('Green')
        colorCombo.addItem('Red')
        colorCombo.addItem('Blue' )
        colorCombo.addItem('Yellow')
        btnLayout.addWidget(startTime)
        btnLayout.addWidget(endTime)
        btnLayout.addWidget(colorCombo)

        innerLayout.addLayout(btnLayout)

        plainTextLabel = QLabel('Comment:')
        innerLayout.addWidget(plainTextLabel)
        plainText = QPlainTextEdit()
        innerLayout.addWidget(plainText)

        
        self.generalLayout.insertLayout(self.LAST_INNER_LAYOUT_POSITION, innerLayout)
        

class MainWinCtrl():
    def __init__(self, view):
        self._view = view
        self._connectSignals()

        self.SIZE = (1878, 636)  # May be Automated
        self.PIX_PER_SEC = 2.92  # Subject to Change. May need a funtion.
        self.COLORS = {"black": (0, 0, 0), "white": (255, 255, 255), "blue": (0, 0, 255), "red": (255, 0, 0), "green": (0, 255, 0),
          "yellow": (255, 255, 0)}
        

    def _connectSignals(self):
        self._view.browseButton1.clicked.connect(partial(self.browse, 1))
        self._view.browseButton2.clicked.connect(partial(self.browse, 2))
        self._view.runButton1.clicked.connect(self.crop_and_merge)


    def browse(self, numOfDisplay):
        self.folderName = QFileDialog.getExistingDirectory(self._view, 'Select a Directory', QtCore.QDir.rootPath())
        if numOfDisplay == 1:
            self._view.srcDisplay.setText(self.folderName)
        elif numOfDisplay == 2:
            self._view.destDisplay.setText(self.folderName)

    def crop_and_merge(self):
    # Crop
        srcAddress = self._view.srcDisplay.displayText()
        destAddress = self._view.destDisplay.displayText()
        y_cord = 1752
        os.chdir(r'{}'.format(srcAddress))
        images = [Image.open(image) for image in os.listdir()]
        for image in images[0:-1]:
            images[images.index(image)] = image.crop((0, 0, y_cord, self.SIZE[1]))
        #------------------------------------------------------------------------#
        # Merge
        widths, heights = zip(*(image.size for image in images))
        total_width = sum(widths)
        max_height = max(heights)
        self.canvas = Image.new("RGB", size=(
            total_width, max_height + 50), color=(255, 255, 255))
        x_offset = 0

        for image in images:
            self.canvas.paste(image, (x_offset, 0))
            x_offset += image.size[0]

        os.chdir(r'{}'.format(destAddress))
        self.canvas.save("Result.png")



def main():
    app  = QApplication(sys.argv)
    GUI = MainWin()
    Ctrl = MainWinCtrl(GUI)
    GUI.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()