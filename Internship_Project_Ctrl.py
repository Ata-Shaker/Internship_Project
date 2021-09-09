import os, re, PySide6
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import  QFileDialog, QGridLayout, QLabel, QLineEdit, QMessageBox, QDialog, QPushButton, QPlainTextEdit
from PySide6.QtCore import SIGNAL, QTime, Qt, Signal
from PIL import Image, ImageDraw, ImageFont
from functools import partial
from datetime import datetime, timedelta
from numpy import round

class myPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
    def keyPressEvent(self, e):
        if len(self.toPlainText()) < 100 and str(self.toPlainText()).count('\n') < 2 :
            print(str(self.toPlainText()).count('\n'))
            return super().keyPressEvent(e)
        else:
            if e.key() in [Qt.Key_Delete, Qt.Key_Backspace, Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right, 
                           Qt.Key_PageDown, Qt.Key_PageDown, Qt.Key_Home, Qt.Key_End]:
                return super().keyPressEvent(e)

class MainWinCtrl():
    def __init__(self, view):
        self._view = view
        self.blackBoxYCoordinate = None
        self.imageLength = None
        self.SIZE = None
        self.COLORS = {"black": (0, 0, 0), "white": (255, 255, 255), "blue": (0, 0, 255), 
                    "red": (255, 0, 0), "green": (0, 255, 0), "yellow": (255, 255, 0)}
        self.text_font = ImageFont.truetype(r'‪C:\Windows\Fonts\arial.ttf', size=11) # --> May able to use QFonts. 
        self.connectSignals()

    def connectSignals(self):
        self._view.sourceBrowseButton.clicked.connect(partial(self.browse, 'source'))
        self._view.destinationBrowseButton.clicked.connect(partial(self.browse, 'display'))
        self._view.mergeButton.clicked.connect(self.cropAndMerge)
        
        #self._view.endTimeRadio.toggled.connect(self.radioEnableAndDisable)
        #self._view.timeLengthRadio.toggled.connect(self.radioEnableAndDisable)
        self._view.endTimeOrTimeLengthCheck.toggled.connect(self.checkMarkEnableAndDisable)
        #self._view.comment.textChanged.connect(self.commentKeyPressEvent)
        self._view.annotateButton.clicked.connect(self.boxAndAnnotate)
        self._view.closeButton.clicked.connect(self._view.close)

    def browse(self, Display):
        self.folderName = QFileDialog.getExistingDirectory(self._view, 'Select a Directory', QtCore.QDir.rootPath())
        if Display == 'source':
            self._view.sourceDisplay.setText(self.folderName)
        elif Display == 'display':
            self._view.destinationDisplay.setText(self.folderName)

    def cropAndMerge(self):
        #--------------------------------------CROP Start-----------------------------------------#

        #---------------------------Error Handling Start-------------------------#
        if self._view.sourceDisplay.text() == '':
            QMessageBox.critical( None, 'Source address missing', 'Please enter a directory.')
            return None
        elif self._view.destinationDisplay.text() == '': 
            QMessageBox.critical( None, 'Destination address missing', 'Please enter a directory.')
            return None
        elif self._view.fileName.text() == '':
            QMessageBox.critical(None, 'File Name missing', 'Please enter a Name.')
            return None
        #---------------------------Error Handling End---------------------------#

        #-----------------------Initializing Attributes Start--------------------#
        sourceAddress = self._view.sourceDisplay.text()
        destinationAddress = self._view.destinationDisplay.text()
        fileName = self._view.fileName.text()
        fileType = str(self._view.fileType.currentText()).lower()
        recordStartTime = self._view.recordStartTime.text()
        recordStart_datetime = datetime.strptime(recordStartTime,  r'%Y/%m/%d %H:%M')
        intervalLength = timedelta(minutes = self.getIntervalLength())
        #-----------------------Initializing Attributes End----------------------#
        
        #---------------------------Oppening Files Start-------------------------#
        os.chdir(r'{}'.format(sourceAddress))
        imageNameList = [re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg', imageName)[0] for imageName in os.listdir() if re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg', imageName) != []]
        self.images = [Image.open(image) for image in imageNameList]
        #----------------------------Oppening Files End--------------------------#
        
        #--------"What if the Program couldn't open any files" Error Start-------#
        if self.images == []:
            QMessageBox.critical(None, 'Directory Empty', 'Please choose a folder containing images.')
            return None
        #---------"What if the Program couldn't open any files" Error End--------#
     
        #--------"What if the images didn't have equal lengths" Error Start------#
        for index in range(len(self.images) - 1):
            if self.images[index].size[0] != self.images[index + 1].size[0]:
                QMessageBox.critical(None, 'Width Inconsistency', 'All images must have equal lengths.')
                return None
        #--------"What if the images didn't have equal lengths" Error End--------#

        #------------------------Getting PixPerSec Start-------------------------#
        self.SIZE = (self.getImageDimensions()[0]/len(self.images), self.getImageDimensions()[1]) 
        if self.blackBoxYCoordinate == None and self.imageLength == None:
            self.dialog()
        #------------------------Getting PixPerSec End---------------------------#

        for image in self.images[0:-1]:
            self.images[self.images.index(image)] = image.crop(
                (0, 0, self.blackBoxYCoordinate, self.SIZE[1]))
        #---------------------------------------CROP END------------------------------------------#

        #-------------------------------------Merge Start-----------------------------------------#
        self.total_width = self.getImageDimensions()[0]
        self.max_height = self.getImageDimensions()[1]
        self.canvas = Image.new("RGB", size=(
            self.total_width, self.max_height + 80), color=(255, 255, 255))
        
        xOffset = 0
        for image in self.images:
            self.canvas.paste(image, (xOffset, 30))
            xOffset += image.size[0]
        #-------------------------------------Merge End-------------------------------------------#

        #------------------------Closing Pictures Start--------------------------#
        for image in self.images:
            image.close()
        #------------------------Closing Pictures End----------------------------#

        #---------------------------Printing Time Start--------------------------#
        xOffset = 0
        canvasDraw = ImageDraw.Draw(self.canvas)
        while xOffset < self.total_width:
            canvasDraw.text((xOffset, 15), recordStart_datetime.strftime(r'%Y/%m/%d %H:%M:%S'), self.COLORS['blue'], self.text_font )
            xOffset += (self.getIntervalLength() * 60) * self.getPixPerSec()
            recordStart_datetime += intervalLength
        #---------------------------Printing Time End----------------------------#

        os.chdir(r'{}'.format(destinationAddress))
        self.canvas.save(f"{fileName}.{fileType}")
        QMessageBox.information(None, 'Info', 'Done!')

    def boxAndAnnotate(self):
        #Error
        if self.blackBoxYCoordinate == None and self.imageLength == None:
            self.dialog()

        if self._view.destinationDisplay.text() == '':
            QMessageBox.critical( None, 'Destination Path Missing', 'Please enter a Destination Path.')
        elif self._view.fileName.text() == '':
            QMessageBox.critical( None, 'File Name Missing', 'Please enter a Name.')
        elif self._view.endTimeOrTimeLength.text() == '00:00:00':
            QMessageBox.critical(None, 'Finish Time/Time Length cannot be 0', 'Please enter an Finish Time/Time Length.')
        elif not(self._view.endTimeOrTimeLengthCheck.isChecked()) and self.convertTimeToPix(self._view.startTime.text()) > self.convertTimeToPix(self._view.endTimeOrTimeLength.text()):
            QMessageBox.critical(None, 'Time Paradox', 'Start Time must be earlier than Finish Time.')
        else:
            destinationAddress = self._view.destinationDisplay.displayText()
            fileName = self._view.fileName.displayText()
            fileType = str(self._view.fileType.currentText()).lower()
            startTime = self._view.startTime.text()
            endTimeOrTimeLength = self._view.endTimeOrTimeLength.text()
            comment = self._view.comment.toPlainText()
            color = str(self._view.color.currentText()).lower()
            os.chdir(r'{}'.format(destinationAddress))
            try:
                self.image  = Image.open(f'{fileName}.{fileType}')
            except:
                QMessageBox.critical(None, 'File Non-Existant', 'Make sure the File Name and File Type you provided are valid.')
            else:
                #Starting 
                startPix = self.convertTimeToPix(startTime) 
                if not(self._view.endTimeOrTimeLengthCheck.isChecked()):
                    endPix =  self.convertTimeToPix(endTimeOrTimeLength)
                else:
                    timeLengthPix = self.convertTimeToPix(endTimeOrTimeLength)
                    endPix = startPix + timeLengthPix

                if startPix > self.image.size[0] or endPix > self.image.size[0]:
                    QMessageBox.critical(None, 'Time Paradox', 'Start Time and End Time must be within the limits.')
                else:
                    frame = (startPix, 30, endPix, self.image.size[1] - 50)
                    # Box
                    draw = ImageDraw.Draw(self.image)
                    draw.rectangle(frame, outline = self.COLORS[color], width=3)
                    #Annotate
                    if comment != '':
                        draw.text((startPix, self.image.size[1] - 40), comment, color, self.text_font)
                        
                    self.image.save(f"{fileName}.{fileType}")
                    self._view.startTime.setTime(QTime(0, 0, 0))
                    self._view.endTimeOrTimeLength.setTime(QTime(0, 0, 0))
                    self._view.comment.clear()
                    QMessageBox.information(None, 'Info', 'Done!')
                    
    def dialog(self):
        self.dialog = QDialog(parent = self._view)
        self.dialog.setWindowTitle('More Information Needed!')
        self.dialog_Layout = QGridLayout(parent = self.dialog)
        
        self.blackBoxYCoordinate_Label = QLabel(parent = self.dialog, text = 'The Y-Coordinate of Black Box: (Pixels)')
        self.dialog_Layout.addWidget(self.blackBoxYCoordinate_Label, 0, 0, 1, 1)

        self.blackBoxYCoordinateEdit = QLineEdit(parent = self.dialog)
        self.blackBoxYCoordinateEdit.setAlignment(Qt.AlignCenter)
        self.blackBoxYCoordinateEdit.setValidator(QtGui.QIntValidator(bottom = 0)) # top = self.SIZE[0]
        self.dialog_Layout.addWidget(self.blackBoxYCoordinateEdit, 1, 0, 1, 4)

        self.imageLength_Label = QLabel(parent = self.dialog, text = 'The Length of each Image: (Seconds)')
        self.dialog_Layout.addWidget(self.imageLength_Label, 2, 0, 1, 1)

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
        if self.blackBoxYCoordinateEdit.text() == '':
            QMessageBox.critical(None, 'The Y-Coordinate Missing!', 'Please Enter a Y-Coordinate.')
        elif self.imageLengthEdit.text() == '':
            QMessageBox.critical(None, 'Image Length Missing!', 'Please Enter a Time Length in Seconds.' )
        else:
            self.blackBoxYCoordinate = float(self.blackBoxYCoordinateEdit.text())
            self.imageLength = float(self.imageLengthEdit.text())
            self.dialog.close()

    def radioEnableAndDisable(self):
        readOnlyPalette = QtGui.QPalette()
        readOnlyPalette.setColor(QtGui.QPalette.Text, Qt.darkGray)

        normalPalette = QtGui.QPalette()
        normalPalette.setColor(QtGui.QPalette.Base, Qt.white)
        normalPalette.setColor(QtGui.QPalette.Text, Qt.black)

        if self._view.endTimeRadio.isChecked():
            self._view.endTime.setReadOnly(False)
            self._view.endTime.setPalette(normalPalette)

            self._view.timeLength.setTime(QTime(0,0,0))
            self._view.timeLength.setReadOnly(True)
            self._view.timeLength.setPalette(readOnlyPalette)
        else:
            self._view.timeLength.setReadOnly(False)
            self._view.timeLength.setPalette(normalPalette)


            self._view.endTime.setReadOnly(True)
            self._view.endTime.setPalette(readOnlyPalette)   
            self._view.endTime.setTime(QTime(0,0,0))
        
    def checkMarkEnableAndDisable(self):
        if self._view.endTimeOrTimeLengthCheck.isChecked():
            self._view.endTimeOrTimeLength_Label.setText('Time Length:')
            self._view.endTimeOrTimeLength.setTime(QTime(0,0,0))
        else:
            self._view.endTimeOrTimeLength_Label.setText('Finish Time:  ')
            self._view.endTimeOrTimeLength.setTime(QTime(0,0,0))            

    def convertTimeToPix(self, times):
        time = re.match(r'(?P<Hour>\d{1,2}):(?P<Minute>\d{1,2}):(?P<Second>\d{1,2})', times).groupdict()
        seconds = int(time['Hour']) * 3600 + int(time['Minute']) * 60 + int(time['Second'])
        return round(seconds * self.getPixPerSec())  # May not need the round function

    def getPixPerSec(self):
        return self.blackBoxYCoordinate/self.imageLength

    def getIntervalLength(self):
        if self._view.thirtyMin.isChecked():
            return 30
        elif self._view.oneHour.isChecked():
            return 60
        elif self._view.ninetyMin.isChecked():
            return 90
        elif self._view.twoHours.isChecked():
            return 120

    def getImageDimensions(self):
        widths, heights = zip(*(image.size for image in self.images))
        total_width = sum(widths)
        max_height = max(heights)
        return (total_width, max_height)
