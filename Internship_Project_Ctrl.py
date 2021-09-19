from Internship_Project_Dialog import myDialog, myDialogCtrl
import os, re
import pandas as pd
from PySide6 import QtCore, QtGui 
from PySide6.QtWidgets import  QFileDialog, QMessageBox
from PySide6.QtCore import QTime, Qt
from PIL import Image, ImageDraw, ImageFont, ImageColor
from functools import partial
from datetime import datetime, timedelta
from numpy import round


class MainWinCtrl():
    def __init__(self, view):
        self._view = view
        self.dialog = myDialog(self._view)
        self.dialogCtrl = myDialogCtrl(self.dialog)
        self.cropCoordinate = None
        self.imageLength = None
        self.SIZE = (None, None)
        self.COLORS = ImageColor.colormap
        # {"black": (0, 0, 0), "white": (255, 255, 255), "blue": (0, 0, 255), 
        # "red": (255, 0, 0), "green": (0, 255, 0), "yellow": (255, 255, 0)}
        self.text_font = ImageFont.truetype(r'‪C:\Windows\Fonts\arial.ttf', size = 12) # --> May able to use QFonts. 
        self.connectSignals()

    def connectSignals(self):
        self._view.sourceBrowseButton.clicked.connect(partial(self.browse, 'source'))
        self._view.destinationBrowseButton.clicked.connect(partial(self.browse, 'display'))
        self._view.mergeButton.clicked.connect(self.cropAndMerge)
        self._view.endTimeOrTimeLengthCheck.toggled.connect(self.checkMarkEnableAndDisable)
        self._view.comment.textChanged.connect(self.countCharacter)
        self._view.addButton.clicked.connect(self.handleCSVFile)
        self._view.annotateButton.clicked.connect(self.boxAndAnnotate)
        self._view.closeButton.clicked.connect(self._view.close)
        # self._view.endTimeRadio.toggled.connect(self.radioEnableAndDisable) --> Connection to an unused functions 
        # self._view.timeLengthRadio.toggled.connect(self.radioEnableAndDisable) --> Connection to an unused functions 

    def browse(self, browseType):
        self.folderName = QFileDialog.getExistingDirectory(self._view, 'Select a Directory', QtCore.QDir.rootPath())
        if browseType == 'source':
            self._view.sourceDisplay.setText(self.folderName) # --> The First Browse Button
        elif browseType == 'display':
            self._view.destinationDisplay.setText(self.folderName) # --> The Second Button 

    def cropAndMerge(self):
        #--------------------------------------CROP Start-----------------------------------------#

        #---------------------------Error Handling Start---------------------------#
        if self._view.sourceDisplay.text() == '': # --> No Source Address Error
            QMessageBox.critical( None, 'Source address missing', 'Please enter a directory.')
            return None
        elif self._view.destinationDisplay.text() == '': # --> No Destination Adress Error
            QMessageBox.critical( None, 'Destination address missing', 'Please enter a directory.')
            return None
        elif self._view.fileName.text() == '': # --> No File Name Error
            QMessageBox.critical(None, 'File Name missing', 'Please enter a Name.')
            return None

        #-----------------------Initializing Attributes Start----------------------#
        sourceAddress = self._view.sourceDisplay.text()
        destinationAddress = self._view.destinationDisplay.text()
        fileName = self._view.fileName.text()
        fileType = str(self._view.fileType.currentText()).lower()
        recordStartTime = self._view.recordStartTime.text()
        recordStart_datetime = datetime.strptime(recordStartTime,  r'%Y/%m/%d %H:%M')
        intervalLength = timedelta(minutes = self.getIntervalLength())
        
        #---------------------------Oppening Files Start---------------------------#
        os.chdir(r'{}'.format(sourceAddress))
        imageNameList = [re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg|^.+\.BMP', imageName)[0] for imageName in os.listdir() if re.findall(r'^.+\.png|^.+\.jpg|^.+\.jpeg', imageName) != []]
        self.images = [Image.open(image) for image in imageNameList] # --> Removing Files with Extensions other than PNG, JPEG, BMP
        
        #--------"What if the Program couldn't open any files" Error Start---------#
        if self.images == []:
            QMessageBox.critical(None, 'Directory Empty', 'Please choose a folder containing images.')
            return None
     
        #--------"What if the images didn't have equal lengths" Error Start--------#
        for index in range(len(self.images) - 1):
            if self.images[index].size[0] != self.images[index + 1].size[0]:
                QMessageBox.critical(None, 'Width Inconsistency', 'All images must have equal lengths.')
                return None

        #------------------------Getting PixPerSec Start---------------------------#
        self.SIZE = (self.getImageDimensions()[0]/len(self.images), self.getImageDimensions()[1]) 
        if self.cropCoordinate == None and self.imageLength == None:
            self.dialog.exec()
            #---------Checking Whether the Crop Coordinate in in Range Start-------#
            if self.dialogCtrl.cropCoordinate <= self.SIZE[0]:
                self.cropCoordinate = self.dialogCtrl.cropCoordinate
                self.imageLength = self.dialogCtrl.imageLength
            else:
                QMessageBox.critical(None, 'Crop Coordinate Out of Range!', f'Crop Coordinate must be less than {self.SIZE[0]}.')
                return None


        for image in self.images[0:-1]:
            self.images[self.images.index(image)] = image.crop(
                (0, 0, self.cropCoordinate, self.SIZE[1]))

        #-------------------------------------Merge Start-----------------------------------------#
        self.total_width = self.getImageDimensions()[0]
        self.max_height = self.getImageDimensions()[1]
        self.canvas = Image.new("RGB", size=(
            self.total_width, self.max_height + 90), color=(255, 255, 255))
        
        xOffset = 0
        for image in self.images:
            self.canvas.paste(image, (xOffset, 30))
            xOffset += image.size[0]

        #------------------------Closing Pictures Start----------------------------#
        for image in self.images:
            image.close()

        #---------------------------Printing Start Time Start----------------------------#
        xOffset = 0
        canvasDraw = ImageDraw.Draw(self.canvas)
        while xOffset < self.total_width:
            canvasDraw.text((xOffset, 15), recordStart_datetime.strftime(r'%Y/%m/%d %H:%M:%S'), self.COLORS['blue'], self.text_font )
            xOffset += (self.getIntervalLength() * 60) * self.getPixPerSec()
            recordStart_datetime += intervalLength

        #---------------------------Saving File Start------------------------------#
        os.chdir(r'{}'.format(destinationAddress))
        self.canvas.save(f"{fileName}.{fileType}")
        self.showDoneMessage()

    def boxAndAnnotate(self):
        #------------------------Getting PixPerSec Start---------------------------#
        if self.cropCoordinate == None and self.imageLength == None:
            self.dialog.exec()
            self.cropCoordinate = self.dialogCtrl.cropCoordinate
            self.imageLength = self.dialogCtrl.imageLength

        #---------------------------Error Handling Start---------------------------#
        if self._view.destinationDisplay.text() == '': # --> No Destination Address Error
            QMessageBox.critical( None, 'Destination Path Missing', 'Please enter a Destination Path.')
            return None
        elif self._view.fileName.text() == '': # --> No File Name Error
            QMessageBox.critical( None, 'File Name Missing', 'Please enter a Name.')
            return None
        elif self._view.endTimeOrTimeLength.text() == '00:00:00': # --> Invalid Time Error
            QMessageBox.critical(None, 'Finish Time/Time Length cannot be 00:00:00', 'Please enter an Finish Time/Time Length.')
            return None
        elif not(self._view.endTimeOrTimeLengthCheck.isChecked()) and self.convertTimeToPix(self._view.startTime.text()) > self.convertTimeToPix(self._view.endTimeOrTimeLength.text()):
            QMessageBox.critical(None, 'Time Paradox', 'Start Time must be earlier than Finish Time.') # --> Time Paradox Error
            return None
        
        #-----------------------Initializing Attributes Start----------------------#
        destinationAddress = self._view.destinationDisplay.displayText()
        fileName = self._view.fileName.displayText()
        fileType = str(self._view.fileType.currentText()).lower()
        startTime = self._view.startTime.text()
        endTimeOrTimeLength = self._view.endTimeOrTimeLength.text()
        comment = self._view.comment.toPlainText()
        color = str(self._view.color.currentText()).lower()
        
        os.chdir(r'{}'.format(destinationAddress))
        #--------"What if the Program couldn't open any files" Error Start---------#
        try:
            self.image  = Image.open(f'{fileName}.{fileType}')
        except:
            QMessageBox.critical(None, 'File Non-Existant', 'Make sure the File Name and File Type you provided are valid.')
        else:
            #----------------The Initialization of Time Stamps Start---------------#
            startPix = self.convertTimeToPix(startTime) 
            endPixOrPixLength = self.convertTimeToPix(endTimeOrTimeLength)
            endPix = self.getEndPix(startPix, endPixOrPixLength, not(self._view.endTimeOrTimeLengthCheck.isChecked()))
            
            #--------"What if the time input was out of limits." Error Start-------#
            if startPix > self.image.size[0] or endPix > self.image.size[0]:
                QMessageBox.critical(None, 'Time Out of Limit', 'Start Time and End Time must be within the limits.')
                return None
            
            #-----------------------------Boxing Start-----------------------------#
            draw = ImageDraw.Draw(self.image)
            frame = (startPix, 30, endPix, self.image.size[1] - 60)
            draw.rectangle(frame, outline = color, width=2)

            #-----------------------------Commenting Start-------------------------#
            if comment != '':
                draw.text((startPix, self.image.size[1] - 50), comment, color, self.text_font)

            #---------------------------Saving File Start--------------------------#
            self.image.save(f"{fileName}.{fileType}")

            #---------------------------Resetting Fields Start---------------------#
            self._view.startTime.setTime(QTime(0, 0, 0))
            self._view.endTimeOrTimeLength.setTime(QTime(0, 0, 0))
            self._view.comment.clear()

            self.showDoneMessage()

    def checkMarkEnableAndDisable(self):
        if self._view.endTimeOrTimeLengthCheck.isChecked(): # If the cechkbox is CHECKED the QlineEdit will accept Length
            self._view.endTimeOrTimeLength_Label.setText('Time Length:')
            self._view.endTimeOrTimeLength.setTime(QTime(0, 0, 0))
        else: # If the cechkbox is UNCHECKED the QlineEdit will accept Length
            self._view.endTimeOrTimeLength_Label.setText('Finish Time:  ')
            self._view.endTimeOrTimeLength.setTime(QTime(0, 0, 0))            

    #----------------------------------CSV Functions Start---------------------------------#
    def handleCSVFile(self):
        if self._view.destinationDisplay.text() == '':
            QMessageBox.critical( None, 'Destination Path Missing', 'Please enter a Destination Path.')
            return None

        if self.cropCoordinate == None and self.imageLength == None:
            self.dialog.exec()
            self.cropCoordinate = self.dialogCtrl.cropCoordinate
            self.imageLength = self.dialogCtrl.imageLength

        self.CSVFileAddress = QFileDialog.getOpenFileName(self._view, 'Open CSV File', QtCore.QDir.rootPath(), 'CSV Files (*.csv *.txt)')
        try:
            self.dataframe = pd.read_csv(r'{}'.format(self.CSVFileAddress[0]))
            self.dataframe['Validity'] = True # Adds another column named Validity 
        except:
            QMessageBox.critical( None, 'Unable to Open the File!', 'Please verify the selected file meets the specified criteria.')
            return None

        #-----"What if the dataframe's columns are uncorresponding" Error Start----#
        if (set(self.dataframe.columns) != {'Row', 'Start Time', 'End Time(True)/Time Length(False)', 'Bool', 'Comment', 'Color', 'Validity'}
        and set(self.dataframe.columns) != {'Row', 'Start Time', 'End Time(1)/Time Length(0)', 'Bool', 'Comment', 'Color', 'Validity'}):
            text = 'The file must contain the following column labels:\n1) Row\n2) Start Time\n3) End Time(True)/Time Length(False)\n4) Bool\n5) Comment\n6) Color'
            criticalMessage = QMessageBox(QMessageBox.Critical, 'Uncorresponding Column Labels!', text)
            criticalMessage.exec()
            return None
        
        #------------------------Opening the Image Start---------------------------#
        self.fileName = self._view.fileName.displayText()
        self.fileType = str(self._view.fileType.currentText()).lower()
        destinationAddress = self._view.destinationDisplay.text()
        os.chdir(r'{}'.format(destinationAddress))
        try:
            self.image  = Image.open(f'{self.fileName}.{self.fileType}')
        except:
            QMessageBox.critical(None, 'File Non-Existant', 'Make sure the File Name and File Type you provided are valid.')
            return None
        
        #-------------------------Calling Validate Function------------------------#
        self.validatedDataframe = self.dataframe.apply(lambda x: self.validateCSVFile(x), axis = 1)
        # The validateCSVFile function is not called independently rather it is applied to the dataframe
        
        self.annotateWithCSV()

    def validateCSVFile(self, row):
        #-----------------------------Time Format Invalidity-----------------------#
        try:
            datetime.strptime(row['Start Time'], '%H:%M:%S')
            datetime.strptime(row['End Time(True)/Time Length(False)'], '%H:%M:%S')
        except:
            row['Validity'] = False
    
        #---------------------Keyword Uncorrespondence Invalidity------------------#
        if ((type(row['Bool']) == str and row['Bool'].lower() not in ['true', 'false' 't', 'f', '1', '0' 'yes' 'no'])
            or (type(row['Bool']) == int and row['Bool'] not in [0, 1])):
               row['Validity'] = False

        #--------------------------Time Paradox Invalidity-------------------------#
        if row['Validity'] and self.convertToBool(row['Bool']):
            if (datetime.strptime(row['Start Time'], '%H:%M:%S') > datetime.strptime(row['End Time(True)/Time Length(False)'], '%H:%M:%S')):
                row['Validity'] = False 

        #------------------------Time Out of Range Invalidity----------------------#
        if row['Validity']:
            if self.convertTimeToPix(row['Start Time']) > self.image.size[0]:
                row['Validity'] = False
            if self.convertTimeToPix(row['End Time(True)/Time Length(False)']) > self.image.size[0]:
                row['Validity'] = False

        return row

    def annotateWithCSV(self):
        draw = ImageDraw.Draw(self.image)
        invalidRowsList = []

        #-------------------------Pixel Data Initialization------------------------#
        for index , row in self.validatedDataframe.iterrows():
            if row['Validity']:
                startPix = self.convertTimeToPix(row['Start Time'])
                endPixOrPixLength = self.convertTimeToPix(row['End Time(True)/Time Length(False)'])                
                endPix = self.getEndPix(startPix, endPixOrPixLength, self.convertToBool(row['Bool']))
                
                frame = (startPix, 30, endPix, self.image.size[1] - 60)
                color = str(row['Color']).lower()

                #----Setting an alternative way in case the Color is not valid-----#
                if color in list(self.COLORS.keys()):
                    draw.rectangle(frame, outline = color, width=2)
                    if row['Comment'] != '' and not(pd.isna(row['Comment'])):
                        draw.text((startPix, self.image.size[1] - 50), row['Comment'], color, self.text_font)
                else:
                    draw.rectangle(frame, outline = 'blue', width=2)
                    if row['Comment'] != '' and not(pd.isna(row['Comment'])):
                        draw.text((startPix, self.image.size[1] - 50), row['Comment'], 'blue', self.text_font)
            else:
                invalidRowsList.append(row['Row'])
        
        #-----------Saving the Image and Displaying the Warning message------------#
        self.getWarningText(invalidRowsList)   
        self.image.save(f"{self.fileName}.{self.fileType}")
        self.showDoneMessage()

    #----------------------------------Peripheral Functions Start---------------------------------#
    def getEndPix(self, startPix, endPixOrPixLength, boolVal):
        if boolVal:
            return endPixOrPixLength
        else:
            return startPix + endPixOrPixLength
    
    def getWarningText(self, invalidRowsList): 
        if invalidRowsList != []:
            invalidRowsText = '{'
            for rowIndex in invalidRowsList:
                if rowIndex != invalidRowsList[-1]:
                    invalidRowsText += f'{rowIndex}, '
                else:
                    invalidRowsText += f'{rowIndex}' 
                    invalidRowsText += '}'
            warningText_1 = 'The following rows could not be added because of an error:\n'
            warningText_2 = '\nPlease check the inputs of these rows and try again.\n'
            warningText_3 = 'Be wary of SPACES! There should NOT be any space after or before the CSV File entries.'
            warningText_Final = warningText_1 + invalidRowsText + warningText_2 + warningText_3 
            QMessageBox.warning(None, 'Oops!', warningText_Final)

    def convertTimeToPix(self, times):
        time = re.match(r'(?P<Hour>\d{1,2}):(?P<Minute>\d{1,2}):(?P<Second>\d{1,2})', times).groupdict()
        seconds = int(time['Hour']) * 3600 + int(time['Minute']) * 60 + int(time['Second'])
        return round(seconds * self.getPixPerSec())  # May not need the round function

    def getPixPerSec(self):
        return self.cropCoordinate/self.imageLength

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

    def countCharacter(self):
        length = len(self._view.comment.toPlainText())
        self._view.characterCount_Label.setText(f'{length}/100')

    def showDoneMessage(self):
        messageBox = QMessageBox(QMessageBox.Information, 'Info', 'Mission Accomplished!')
        messageBox.exec()
    
    def convertToBool(self, expression):
        if type(expression) == int:
            if expression == 1:
                return True
            elif expression == 0:
                return False
        else:
            if str(expression).lower() in ('true', 'yes', 't', '1'):
                return True
            elif str(expression).lower() in ('false', 'no', 'f', '0'):
                return False

    #----------------------------Unused Function Start-----------------------------# 
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