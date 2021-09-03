import os, re
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import  QFileDialog, QGridLayout, QLabel, QLineEdit, QMessageBox, QDialog, QPushButton
from PySide6.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont
from functools import partial
from datetime import datetime, timedelta
from numpy import round



class MainWinCtrl():
    def __init__(self, view):
        self._view = view
        self.blackBoxYCoordinate = None
        self.imagePixelLength = None

        self.SIZE = (1878, 636)  # May be Automated
        self.COLORS = {"black": (0, 0, 0), "white": (255, 255, 255), "blue": (0, 0, 255), "red": (255, 0, 0), "green": (0, 255, 0),
                       "yellow": (255, 255, 0)}
        self.text_font = ImageFont.truetype(r'‪C:\Windows\Fonts\arial.ttf', size=11) #--
        self._connectSignals()

    def _connectSignals(self):
        self._view.sourceBrowseButton.clicked.connect(partial(self.browse, 'source'))
        self._view.destinationBrowseButton.clicked.connect(partial(self.browse, 'display'))
        self._view.mergeButton.clicked.connect(self.crop_and_merge)
        self._view.annotateButton.clicked.connect(self.box_and_annotate)
        self._view.closeButton.clicked.connect(self._view.close)

    def browse(self, Display):
        self.folderName = QFileDialog.getExistingDirectory(self._view, 'Select a Directory', QtCore.QDir.rootPath())
        if Display == 'source':
            self._view.sourceDisplay.setText(self.folderName)
        elif Display == 'display':
            self._view.destinationDisplay.setText(self.folderName)

    def crop_and_merge(self):
        # Error Handling
        if self._view.sourceDisplay.text() == '':
            QMessageBox.critical( None, 'Source address missing', 'Please enter a directory.')
        elif self._view.destinationDisplay.text() == '': 
            QMessageBox.critical( None, 'Destination address missing', 'Please enter a directory.')
        elif self._view.fileName.text() == '':
            QMessageBox.critical(None, 'File Name missing', 'Please enter a Name.')
        else:
        # Crop
            sourceAddress = self._view.sourceDisplay.displayText()
            destinationAddress = self._view.destinationDisplay.displayText()
            fileName = self._view.fileName.displayText()
            
            self.dialog()         

            recordStartTime = self._view.recordStartTime.text()
            # recordStartDic = re.match(r'(?P<Hour>\d{1,2}):(?P<Minute>\d{1,2}):(?P<Second>\d{1,2})', recordStart).groupdict()
            # recordStart_datetime = datetime(1,1,1,int(recordStartDic['Hour']),int(recordStartDic['Minute']),int(recordStartDic['Second']))
            recordStart_datetime = datetime.strptime(recordStartTime,  r'%Y/%m/%d %H:%M')

            thirtyMinutes = timedelta(minutes=30)
            os.chdir(r'{}'.format(sourceAddress))

            imageNameList = [re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg', imageName)[0] for imageName in os.listdir() if re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg', imageName) != []]
            images = [Image.open(image) for image in imageNameList]
            if images == []:
                QMessageBox.critical(None, 'Directory Empty', 'Please choose a folder containing images.')
                return None

            for image in images[0:-1]:
                images[images.index(image)] = image.crop(
                    (0, 0, self.blackBoxYCoordinate, self.SIZE[1]))
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
                    


            os.chdir(r'{}'.format(destinationAddress))
            self.canvas.save(f"{fileName}.jpeg")
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
        return round(seconds * self.pix_per_sec())  # May not need the round function

    def pix_per_sec(self):
        return float(self._view.yCoordinate.text())/float(self._view.singularTimeLength.text())

    def dialog(self):
        if self.blackBoxYCoordinate == None and self.imagePixelLength == None:
            self.dialog = QDialog(parent = self._view)
            self.dialog.setWindowTitle('More Information Needed!')
            self.dialog_Layout = QGridLayout(parent = self.dialog)
            
            self.blackBoxYCoordinate_Label = QLabel(parent = self.dialog, text = 'The Y-Coordinate of Black Box: (Pixels)')
            self.dialog_Layout.addWidget(self.blackBoxYCoordinate_Label, 0, 0, 1, 1)

            self.blackBoxYCoordinateEdit = QLineEdit(parent = self.dialog)
            self.blackBoxYCoordinateEdit.setAlignment(Qt.AlignCenter)
            self.blackBoxYCoordinateEdit.setValidator(QtGui.QIntValidator(bottom = 0, top = self.SIZE[0]))
            self.dialog_Layout.addWidget(self.blackBoxYCoordinateEdit, 1, 0, 1, 4)

            self.imagePixelLength_Label = QLabel(parent = self.dialog, text = 'The Length of each Image: (Seconds)')
            self.dialog_Layout.addWidget(self.imagePixelLength_Label, 2, 0, 1, 1)

            self.imageLengthEdit = QLineEdit(parent = self.dialog)
            self.imageLengthEdit.setAlignment(Qt.AlignCenter)
            self.imageLengthEdit.setValidator(QtGui.QIntValidator(bottom = 0))
            self.dialog_Layout.addWidget(self.imageLengthEdit, 3, 0, 1, 4)

            self.dialogButton = QPushButton(parent = self.dialog, text = 'Submit')
            self.dialog_Layout.addWidget(self.dialogButton, 4, 3, 1, 1, Qt.AlignRight)

            self.dialog.setLayout(self.dialog_Layout)
            self.dialogButton.clicked.connect(self.dialogButtonClicked)

            self.dialog.exec()
    
    def dialogButtonClicked(self):
        if self.blackBoxYCoordinateEdit == '':
            QMessageBox.critical(None, title = 'The Y-Coordinate Missing!', text = 'Please Enter a Y-Coordinate.')
        elif self.imagePixelLengthEdit == '':
            QMessageBox.critical(None, title ='Image Length Missing!', text = 'Please Enter a Time Length in Seconds.' )
        else:
            self.blackBoxYCoordinate = int(self.blackBoxYCoordinateEdit.text())
            self.imageLength = int(self.imageLengthEdit.text())
            self.dialog.close()
