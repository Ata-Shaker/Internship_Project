import sys
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QComboBox, QDateTimeEdit, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QMainWindow, QPlainTextEdit, QRadioButton, QTimeEdit
from PySide6.QtWidgets import QGridLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget, QLineEdit
from PySide6.QtCore import QDate, QDateTime, QTime, Qt 

class MainWin(QMainWindow): 
    def __init__(self): 
        super().__init__() 
 
        self.setWindowTitle('New Photo Editor') 
        self.setFixedSize(350, 445) 
        self.centralWidget = QWidget(self) 
        self.setCentralWidget(self.centralWidget) 
 
        self.general_Layout = QVBoxLayout(parent = self.centralWidget) 
        self.innerlayout_1 = QGridLayout() 
        self.innerlayout_1.setAlignment(Qt.AlignTop) 
        
        #----------------------------Mutual Setup Start------------------------#
        self.addSourceWidgets() 
        self.addDestinationWidgets() 
        self.addFileWidgets() 
        self.general_Layout.addLayout(self.innerlayout_1)
        #-----------------------------Mutual Setup End-------------------------#

        self.createTabsWidgets() #-----> Creating Tabs

        #----------------------------Merge Tab Start---------------------------#
        self.mergeTabMain_Layout = QVBoxLayout(parent=self.mergeTab)
        self.addMergeCalendar()
        self.addMergeIntervalOptions()
        self.mergeTab.setLayout(self.mergeTabMain_Layout)
        #-----------------------------Merge Tab End----------------------------#

        #----------------------------Annotate Tab Start------------------------#
        self.annotateTabMain_Layout = QVBoxLayout(self.annotateTab)
        self.addAnnotateWidgets()
        self.annotateTab.setLayout(self.annotateTabMain_Layout)

        self.closeButton = QDialogButtonBox(QDialogButtonBox.Close, parent = self)
        self.general_Layout.addWidget(self.closeButton)

        self.centralWidget.setLayout(self.general_Layout)

    def addSourceWidgets(self): 
        self.sourceDisplay_Label = QLabel(parent = self.centralWidget, text = 'Source Path:') 
        self.innerlayout_1.addWidget(self.sourceDisplay_Label, 0, 0) # --> Label 
 
        self.sourceDisplay = QLineEdit(parent = self.centralWidget) 
        self.sourceDisplay.setAlignment(Qt.AlignCenter) 
        self.sourceDisplay.setReadOnly(True)    
        self.innerlayout_1.addWidget(self.sourceDisplay, 1, 0, 1, 5) # --> Display 
 
        self.sourceBrowseButton = QPushButton(parent = self.centralWidget, text= 'Browse') 
        self.innerlayout_1.addWidget(self.sourceBrowseButton, 1, 5, 1, 1) # --> Button 
 
    def addDestinationWidgets(self): 
        self.destinationDisplay_Label = QLabel(parent = self.centralWidget, text = 'Destination Path:') 
        self.innerlayout_1.addWidget(self.destinationDisplay_Label, 2, 0) # --> Label 
 
        self.destinationDisplay = QLineEdit(parent = self.centralWidget) 
        self.destinationDisplay.setAlignment(Qt.AlignCenter) 
        self.destinationDisplay.setReadOnly(True)    
        self.innerlayout_1.addWidget(self.destinationDisplay, 3, 0, 1, 5 )# --> Display 
 
        self.destinationBrowseButton = QPushButton(parent = self.centralWidget, text= 'Browse') 
        self.innerlayout_1.addWidget(self.destinationBrowseButton, 3, 5, 1, 1) # --> Button 
 
    def addFileWidgets(self): 
        self.fileName_Label = QLabel(parent = self.centralWidget, text ='File Name:') 
        self.innerlayout_1.addWidget(self.fileName_Label, 4, 0, 1, 3) # --> File Name Label 
 
        self.fileType_Label = QLabel(parent = self.centralWidget, text ='File Type:') 
        self.innerlayout_1.addWidget(self.fileType_Label, 4, 3, 1, 3) # --> File Type Label 
 
        self.fileName = QLineEdit(parent = self.centralWidget) 
        self.fileName.setPlaceholderText('Enter the File Name') 
        self.fileName.setAlignment(Qt.AlignCenter) 
        self.innerlayout_1.addWidget(self.fileName, 5, 0, 1, 3) # --> File Name Widget 
 
        self.fileType = QComboBox(parent = self.centralWidget) 
        self.fileType.addItems(['JPEG', 'PNG', 'BMP']) 
        self.innerlayout_1.addWidget(self.fileType, 5, 3, 1, 3) # # --> File Type Widget 
 
    def createTabsWidgets(self):
        self.tabs = QTabWidget(self.centralWidget)
        self.mergeTab = QWidget()
        self.annotateTab = QWidget()
        self.tabs.addTab(self.mergeTab, 'Merge')
        self.tabs.addTab(self.annotateTab, 'Annotate')
        self.general_Layout.addWidget(self.tabs)

    def addMergeCalendar(self):
        self.mergeTab_Layout = QGridLayout()
        self.mergeTab_Layout.setAlignment(Qt.AlignTop)
        
        self.recordStartTime_Label = QLabel(parent = self.mergeTab , text = 'Record Start Time:')
        self.mergeTab_Layout.addWidget(self.recordStartTime_Label, 0, 0)

        #---------------------------Calendar Start-------------------------------#
        self.recordStartTime = QDateTimeEdit(QDate.currentDate(), parent = self.mergeTab)
        self.recordStartTime.setMaximumDate(QDate.currentDate().addDays(365))
        self.recordStartTime.setMinimumDate(QDate.currentDate().addDays(-365))
        self.recordStartTime.setCalendarPopup(True)
        self.recordStartTime.setDisplayFormat('yyyy/MM/dd HH:mm')
        self.recordStartTime.setAlignment(Qt.AlignCenter)
        self.mergeTab_Layout.addWidget(self.recordStartTime)
        self.mergeTabMain_Layout.addLayout(self.mergeTab_Layout)
        #---------------------------Calendar End---------------------------------#

    def addMergeIntervalOptions(self):
        #---------------------------Display Interval Start-----------------------#
        self.dateTimeDiplayInterval = QGroupBox(parent= self.mergeTab, title = 'Display Interval:')
        self.thirtyMin = QRadioButton(parent = self.dateTimeDiplayInterval, text = '&3&0 Minutes')
        self.oneHour = QRadioButton(parent = self.dateTimeDiplayInterval, text = '&1 Hour')
        self.ninetyMin = QRadioButton(parent = self.dateTimeDiplayInterval, text = '&9&0 Minutes')
        self.twoHour = QRadioButton(parent = self.dateTimeDiplayInterval, text = '&2 Hours')
        self.thirtyMin.setChecked(True)

        self.dateTimeDiplayInterval_Layout = QVBoxLayout(self.dateTimeDiplayInterval)
        self.dateTimeDiplayInterval_Layout.addWidget(self.thirtyMin)
        self.dateTimeDiplayInterval_Layout.addWidget(self.oneHour)
        self.dateTimeDiplayInterval_Layout.addWidget(self.ninetyMin)
        self.dateTimeDiplayInterval_Layout.addWidget(self.twoHour)

        self.dateTimeDiplayInterval.setLayout(self.dateTimeDiplayInterval_Layout)
        self.mergeTabMain_Layout.addWidget(self.dateTimeDiplayInterval)
        #---------------------------Display Interval End-------------------------#
        
        self.mergeButton = QPushButton(parent = self.mergeTab, text = 'Merge')
        self.mergeTabMain_Layout.addWidget(self.mergeButton)

    def addAnnotateWidgets(self):
        self.annotateTab_Layout = QGridLayout()
        self.annotateTab_Layout.setAlignment(Qt.AlignTop)

        #---------------------------Start Time Start-----------------------------#
        self.startTime_Label = QLabel(parent = self.annotateTab, text = 'Start Time:')
        self.annotateTab_Layout.addWidget(self.startTime_Label, 0, 0, 1, 1)

        # self.color_Label = QLabel(parent = self.annotateTab, text = 'Color:')
        # self.annotateTab_Layout.addWidget(self.color_Label, 0, 5, 1, 1)

        self.startTime = QTimeEdit(parent = self.annotateTab)
        self.startTime.setDisplayFormat('HH:mm:ss')
        self.startTime.setAlignment(Qt.AlignCenter)
        self.annotateTab_Layout.addWidget(self.startTime, 0, 1, 1, 4)

        self.color = QComboBox(parent = self.annotateTab)
        self.color.addItems(['Blue', 'Red', 'Green', 'Black', 'White', 'Yellow'])
        self.annotateTab_Layout.addWidget(self.color, 0, 5, 1, 1)
        #--------------------------Start Time End--------------------------------#

        #---------------------------End Time Start-------------------------------#
        self.endTime_Label = QLabel(parent = self.annotateTab,  text = 'End Time:')
        self.annotateTab_Layout.addWidget(self.endTime_Label, 1, 0, 1, 1)

        self.endTime = QTimeEdit(parent = self.annotateTab)
        self.endTime.setDisplayFormat('HH:mm:ss')
        self.endTime.setAlignment(Qt.AlignCenter)
        self.annotateTab_Layout.addWidget(self.endTime, 1, 1, 1, 4)

        self.endTimeRadio = QRadioButton(parent = self.annotateTab)
        self.endTimeRadio.setChecked(True)
        self.annotateTab_Layout.addWidget(self.endTimeRadio, 1, 5, 1, 1, Qt.AlignRight)
        #--------------------------End Time End----------------------------------#

        #---------------------------Time length Start----------------------------#
        self.timeLength_Label = QLabel(self.annotateTab, text = 'Time Length:')
        self.annotateTab_Layout.addWidget(self.timeLength_Label, 2, 0, 1, 1)

        self.timeLength = QTimeEdit(parent = self.annotateTab)
        self.timeLength.setDisplayFormat('HH:mm:ss')
        self.timeLength.setAlignment(Qt.AlignCenter)
        self.annotateTab_Layout.addWidget(self.timeLength, 2, 1, 1, 4)

        self.timeLengthRadio = QRadioButton(parent=self.annotateTab)
        self.annotateTab_Layout.addWidget(self.timeLengthRadio, 2, 5, 1, 1, Qt.AlignRight)
        #---------------------------Time Length End------------------------------#

        #-----------------------------Comment Start------------------------------#
        # self.comment_Label = QLabel(parent = self.annotateTab, text = 'Comment:')
        # self.annotateTab_Layout.addWidget(self.comment_Label, 3, 0, 1, 1)

        self.comment = QPlainTextEdit(parent = self.annotateTab)
        self.comment.setUndoRedoEnabled(True)
        self.comment.setPlaceholderText('Enter Comment')
        self.annotateTab_Layout.addWidget(self.comment, 4, 0, 1, 6)
        #-----------------------------Comment End--------------------------------#

        #-----------------------------Comment Start------------------------------# 
        self.readButton = QPushButton(parent =self.annotateTab, text = '+Add')
        self.annotateTab_Layout.addWidget(self.readButton, 5, 0, 1, 3)
        self.annotateButton = QPushButton(parent = self.annotateTab,  text = 'Annotate')
        self.annotateTab_Layout.addWidget(self.annotateButton, 5, 3, 1, 3)
        #-----------------------------Comment End--------------------------------# 


        self.annotateTabMain_Layout.addLayout(self.annotateTab_Layout)



def main():
    app = QApplication()
    GUI = MainWin()
    GUI.show()
    sys.exit(app.exec())
        
if __name__ == '__main__':
    main()