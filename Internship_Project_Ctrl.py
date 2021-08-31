import os, re
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import  QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont
from functools import partial
from datetime import datetime, timedelta
import numpy as np



class MainWinCtrl():
    def __init__(self, view):
        self._view = view
        self.SIZE = (1878, 636)  # May be Automated
        self.COLORS = {"black": (0, 0, 0), "white": (255, 255, 255), "blue": (0, 0, 255), "red": (255, 0, 0), "green": (0, 255, 0),
                       "yellow": (255, 255, 0)}
        self.text_font = ImageFont.truetype(r'‪C:\Windows\Fonts\arial.ttf', size=11)
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

            recordStart = self._view.recordStartTime.text()
            recordStartDic = re.match(r'(?P<Hour>\d{1,2}):(?P<Minute>\d{1,2}):(?P<Second>\d{1,2})', recordStart).groupdict()
            recordStart_datetime = datetime(1,1,1,int(recordStartDic['Hour']),int(recordStartDic['Minute']),int(recordStartDic['Second']))
            thirtyMinutes = timedelta(minutes=30)
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
            self.total_width = sum(widths)
            max_height = max(heights)
            self.canvas = Image.new("RGB", size=(
                self.total_width, max_height + 80), color=(255, 255, 255))
            
            x_offset = 0
            for image in images:
                self.canvas.paste(image, (x_offset, 30))
                x_offset += image.size[0]
            #------------------------------------------------------------------------#

            x_offset = 0
            canvasDraw = ImageDraw.Draw(self.canvas)
            while x_offset < self.total_width:
                canvasDraw.text((x_offset, 15), recordStart_datetime.strftime('%H:%M:%S'), self.COLORS['black'], self.text_font )
                x_offset += 1800 * self.pix_per_sec()
                recordStart_datetime += thirtyMinutes
                    


            os.chdir(r'{}'.format(destAddress))
            self.canvas.save(f"{name}.jpeg")
            QMessageBox.information(None, 'Info', 'Done!')

    def box_and_annotate(self):
        #Error
        if self._view.destDisplay.text() == '':
            QMessageBox.critical( None, 'Destination Path Missing', 'Please enter a Destination Path.')
        elif self._view.fileName.text() == '':
            QMessageBox.critical( None, 'File Name Missing', 'Please enter a Name.')
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
                self.image  = Image.open(r'{}'.format(self.destAddress + f'/{self.name}.jpeg'))
            except:
                QMessageBox.critical(None, 'File Non-Existant', 'Make sure the File Name you provided is valid.')
            else:
                
                #Starting 
                strt_pix = self.time_to_pix(self.strt_time)
                end_pix =  self.time_to_pix(self.end_time)

                if strt_pix > self.image.size[0] or end_pix > self.image.size[0]:
                    QMessageBox.critical(None, 'Time Paradox', 'Start Time and End Time must be within the limits.')
                else:
                    frame = (strt_pix, 30, end_pix, self.SIZE[1] + 30)
                    # Box
                    draw = ImageDraw.Draw(self.image)
                    draw.rectangle(frame, outline = self.COLORS[self.color], width=3)
                    #Annotate
                    draw.text((strt_pix, self.SIZE[1] + 10), self.text, self.color, self.text_font)
                    self.image.save(f"{self.name}.jpeg")
                    self._view.startTime.clear()
                    self._view.endTime.clear()
                    self._view.plainText.clear()
                    QMessageBox.information(None, 'Info', 'Done!')


    def time_to_pix(self, times):
        time = re.match(r'(?P<Hour>\d{1,2}):(?P<Minute>\d{1,2}):(?P<Second>\d{1,2})', times).groupdict()
        seconds = int(time['Hour']) * 3600 + int(time['Minute']) * 60 + int(time['Second'])
        return np.round(seconds * self.pix_per_sec())  # May not need the round function

    def pix_per_sec(self):
        return float(self._view.yCoordinate.text())/float(self._view.singularTimeLength.text())