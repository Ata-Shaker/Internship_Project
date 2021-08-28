import sys, os, re
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QMainWindow, QPlainTextEdit, QVBoxLayout, QFrame
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QGridLayout, QMessageBox
from PySide6.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont
from functools import partial
import numpy as np
from datetime import datetime, timedelta


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
    
       

class MainWinCtrl():
    def __init__(self, view):
        self._view = view
        self.SIZE = (1878, 636)  # May be Automated
        self.PIX_PER_SEC = 2.92  # Subject to Change. May need a funtion.
        self.COLORS = {"black": (0, 0, 0), "white": (255, 255, 255), "blue": (0, 0, 255), "red": (255, 0, 0), "green": (0, 255, 0),
                       "yellow": (255, 255, 0)}
        self.destAddress = None
        self.name = None
        self.strt_time = None
        self.end_time = None
        self.text = None
        self.color = None

        self._connectSignals()

    def _connectSignals(self):
        self._view.browseButton1.clicked.connect(partial(self.browse, 1))
        self._view.browseButton2.clicked.connect(partial(self.browse, 2))
        self._view.runButton1.clicked.connect(self.crop_and_merge)
        self._view.runButton2.clicked.connect(self.box_and_annotate)
        self._view.stdBtns.clicked.connect(self._view.close)

    def browse(self, numOfDisplay):
        self.folderName = QFileDialog.getExistingDirectory(self._view, 'Select a Directory', QtCore.QDir.rootPath())
        if numOfDisplay == 1:
            self._view.srcDisplay.setText(self.folderName)
        elif numOfDisplay == 2:
            self._view.destDisplay.setText(self.folderName)

    def crop_and_merge(self):
        # Error Handling
        if self._view.srcDisplay.text() == '':
            QMessageBox.critical( None, 'Source address missing', 'Please enter a directory.')
        elif self._view.destDisplay.text() == '': 
            QMessageBox.critical( None, 'Destination address missing', 'Please enter a directory.')
        elif self._view.fileName.text() == '':
            QMessageBox.critical(None, 'File Name missing', 'Please enter a Name.')
        elif self._view.yCoordinate.text() == '':
            QMessageBox.critical(None, 'Y-coordinate missing', 'Please enter a Name.')
        else:
        # Crop
            srcAddress = self._view.srcDisplay.displayText()
            destAddress = self._view.destDisplay.displayText()
            name = self._view.fileName.displayText()
            yCord = int(self._view.yCoordinate.displayText())

            recordStart = self._view.recordStartStime.text()
            recordStartDic = re.match(r'(?P<Hour>\d{1,2}):(?P<Minute>\d{1,2}):(?P<Second>\d{1,2})', recordStart).groupdict()
            #recordStart_datetime = 
            os.chdir(r'{}'.format(srcAddress))

            imageNameList = [re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg', imageName)[0] for imageName in os.listdir() if re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg', imageName) != []]
            images = [Image.open(image) for image in imageNameList]
            if images == []:
                QMessageBox.critical(None, 'Directory Empty', 'Please choose a folder containing images.')
                return None

            for image in images[0:-1]:
                images[images.index(image)] = image.crop(
                    (0, 0, yCord, self.SIZE[1]))
            #------------------------------------------------------------------------#
            # Merge
            widths, heights = zip(*(image.size for image in images))
            total_width = sum(widths)
            max_height = max(heights)
            self.canvas = Image.new("RGB", size=(
                total_width, max_height + 80), color=(255, 255, 255))
            x_offset = 0

            for image in images:
                self.canvas.paste(image, (x_offset, 30))
                x_offset += image.size[0]
                if x_offset % (self.PIX_PER_SEC * 1800) == 0:
                    pass

            os.chdir(r'{}'.format(destAddress))
            self.canvas.save(f"{name}.png")
            QMessageBox.information(None, 'Info', 'Done!')

    def box_and_annotate(self):
        #Error
        if self._view.fileName.text() == '':
            QMessageBox.critical( None, 'File Name missing', 'Please enter a Name.')
        elif self._view.startTime.text() == '':
            QMessageBox.critical(None, 'Start Time Missing ', 'Please enter a Start Time.')
        elif self._view.endTime.text() == '':
            QMessageBox.critical(None, 'Start Time Missing ', 'Please enter an End Time.')
        elif self.time_to_pix(self._view.startTime.text()) > self.time_to_pix(self._view.endTime.text()):
            QMessageBox.critical(None, 'Time Paradox', 'Start Time must be earlier than End Time.')
        else:
            self.destAddress = self._view.destDisplay.displayText()
            self.name = self._view.fileName.displayText()
            self.strt_time = self._view.startTime.displayText()
            self.end_time = self._view.endTime.displayText()
            self.text = self._view.plainText.toPlainText()
            self.color = str(self._view.colorCombo.currentText()).lower()
            try:
                self.image  = Image.open(r'{}'.format(self.destAddress + f'/{self.name}.png'))
            except:
                QMessageBox.critical(None, 'File Non-Existant', 'Make sure the File Name you provided is valid.')
            else:
                
                #Starting 
                strt_pix = self.time_to_pix(self.strt_time)
                end_pix =  self.time_to_pix(self.end_time)
                
                frame = (strt_pix, 30, end_pix, self.SIZE[1] + 30)
                # Box
                draw = ImageDraw.Draw(self.image)
                draw.rectangle(frame, outline = self.COLORS[self.color], width=3)
                #Annotate
                text_font = ImageFont.truetype(r'‪C:\Windows\Fonts\arial.ttf', size=11)
                draw.text((strt_pix, self.SIZE[1] + 10), self.text, self.color, text_font)
                self.image.save(f"{self.name}.png")
                self._view.startTime.clear()
                self._view.endTime.clear()
                self._view.plainText.clear()
                QMessageBox.information(None, 'Info', 'Done!')


    def time_to_pix(self, times):
        time = re.match(r'(?P<Hour>\d{1,2}):(?P<Minute>\d{1,2}):(?P<Second>\d{1,2})', times).groupdict()
        seconds = int(time['Hour']) * 3600 + int(time['Minute']) * 60 + int(time['Second'])
        return np.round(seconds * self.PIX_PER_SEC)  # May not need the round function

def main():
    app = QApplication(sys.argv)
    GUI = MainWin()
    Ctrl = MainWinCtrl(GUI)
    GUI.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()  
