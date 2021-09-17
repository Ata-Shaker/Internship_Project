from Internship_Project_Ctrl import MainWinCtrl
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDateTimeEdit, QDialogButtonBox, QGroupBox, QLabel, QMainWindow, QRadioButton, QTimeEdit
from PySide6.QtWidgets import QGridLayout, QPushButton, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QPlainTextEdit
from PySide6.QtCore import QDate, Qt 
import sys


class myPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
    def keyPressEvent(self, e):
        '''This class is designed considering the limitations of merged images. '''


        if len(self.toPlainText()) < 100 and str(self.toPlainText()).count('\n') < 3 :
            if str(self.toPlainText()).count('\n') == 2 and e.key() == 16777220: # 16777220 is Numeric representaion of Qt.Key_Enter.
                return None
            else:
                return super().keyPressEvent(e)
            # print(str(self.toPlainText()).count('\n'))
        else:
            if e.key() in [Qt.Key_Delete, Qt.Key_Backspace, Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right, 
                           Qt.Key_PageDown, Qt.Key_PageDown, Qt.Key_Home, Qt.Key_End]:
                return super().keyPressEvent(e)

class MainWin(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        #----------------------------General Setup Start--------------------------#
        self.setWindowTitle('New Photo Editor') 
        self.setFixedSize(440, 460) 
        self.centralWidget = QWidget(self) 
        self.setCentralWidget(self.centralWidget) 
 
        self.general_Layout = QVBoxLayout(parent = self) 
        self.innerlayout_1 = QGridLayout() 
        self.innerlayout_1.setAlignment(Qt.AlignTop) 
        
        #----------------------------Mutual Setup Start----------------------------#
        self.addSourceWidgets() 
        self.addDestinationWidgets() 
        self.addFileWidgets() 
        self.general_Layout.addLayout(self.innerlayout_1)

        self.createTabsWidgets() #-----> Creating Tabs

        #----------------------------Merge Tab Start-------------------------------#
        self.mergeTabMain_Layout = QVBoxLayout(parent=self.mergeTab)
        self.mergeTabMain_Layout.setAlignment(Qt.AlignTop)
        self.addMergeCalendar()
        self.addMergeIntervalOptions()
        self.mergeTab.setLayout(self.mergeTabMain_Layout)

        #----------------------------Annotate Tab Start----------------------------#
        self.annotateTabMain_Layout = QVBoxLayout(self.annotateTab)
        self.addAnnotateTimeWidgets()
        self.addAnnotateCommentWidget()
        self.annotateTab.setLayout(self.annotateTabMain_Layout)
                
        #----------------------------Close Button Start----------------------------#
        self.closeButton = QDialogButtonBox(QDialogButtonBox.Close, parent = self)
        self.general_Layout.addWidget(self.closeButton)


        self.centralWidget.setLayout(self.general_Layout)

    #-------------------------------Display and Label Functions Start-----------------------------#
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
        self.innerlayout_1.addWidget(self.destinationDisplay_Label, 2, 0) # --> Destination Label 
 
        self.destinationDisplay = QLineEdit(parent = self.centralWidget) 
        self.destinationDisplay.setAlignment(Qt.AlignCenter) 
        self.destinationDisplay.setReadOnly(True)    
        self.innerlayout_1.addWidget(self.destinationDisplay, 3, 0, 1, 5 )# --> Destination Display 
 
        self.destinationBrowseButton = QPushButton(parent = self.centralWidget, text= 'Browse') 
        self.innerlayout_1.addWidget(self.destinationBrowseButton, 3, 5, 1, 1) # --> Destination Browse Button 
 
    def addFileWidgets(self): 
        self.fileName_Label = QLabel(parent = self.centralWidget, text ='File Name:') 
        self.innerlayout_1.addWidget(self.fileName_Label, 4, 0, 1, 3) # --> File Name Label 
 
        self.fileType_Label = QLabel(parent = self.centralWidget, text ='File Type:') 
        self.innerlayout_1.addWidget(self.fileType_Label, 4, 3, 1, 3) # --> File Type Label 
 
        self.fileName = QLineEdit(parent = self.centralWidget) 
        self.fileName.setMaxLength(30)
        self.fileName.setPlaceholderText('Enter the File Name') 
        self.fileName.setAlignment(Qt.AlignCenter) 
        self.innerlayout_1.addWidget(self.fileName, 5, 0, 1, 3) # --> File Name Widget 
 
        self.fileType = QComboBox(parent = self.centralWidget) 
        self.fileType.addItems(['JPEG', 'PNG', 'BMP']) 
        self.innerlayout_1.addWidget(self.fileType, 5, 3, 1, 3) # # --> File Type Widget 
 
    #-----------------------------------------TABS Start------------------------------------------#
    def createTabsWidgets(self):
        self.tabs = QTabWidget(self.centralWidget)
        self.mergeTab = QWidget()
        self.annotateTab = QWidget()
        self.tabs.addTab(self.mergeTab, 'Merge')
        self.tabs.addTab(self.annotateTab, 'Annotate')
        self.general_Layout.addWidget(self.tabs)
    
    #-------------------------------Merge Tab Functions Start---------------------------#
    def addMergeCalendar(self):
        self.recordStartTime_Label = QLabel(parent = self.mergeTab , text = 'Record Start Time:')
        self.mergeTabMain_Layout.addWidget(self.recordStartTime_Label) # --> Calendar Label

        #---------------------------Calendar Start---------------------------------#
        self.recordStartTime = QDateTimeEdit(QDate.currentDate(), parent = self.mergeTab)
        self.recordStartTime.setMaximumDate(QDate.currentDate().addDays(365))
        self.recordStartTime.setMinimumDate(QDate.currentDate().addDays(-365))
        self.recordStartTime.setCalendarPopup(True)
        self.recordStartTime.setDisplayFormat('yyyy/MM/dd HH:mm')
        self.recordStartTime.setAlignment(Qt.AlignCenter)
        self.mergeTabMain_Layout.addWidget(self.recordStartTime)
        #---------------------------Calendar End---------------------------------#
        
    def addMergeIntervalOptions(self):
        #---------------------------Display Interval Start-------------------------#
        self.dateTimeDiplayInterval = QGroupBox(parent= self.mergeTab, title = 'Display Interval:')
        self.thirtyMin = QRadioButton(parent = self.dateTimeDiplayInterval, text = '30 Minutes')
        self.oneHour = QRadioButton(parent = self.dateTimeDiplayInterval, text = '1 Hour')
        self.ninetyMin = QRadioButton(parent = self.dateTimeDiplayInterval, text = '90 Minutes')
        self.twoHours = QRadioButton(parent = self.dateTimeDiplayInterval, text = '2 Hours')
        self.thirtyMin.setChecked(True)

        self.dateTimeDiplayInterval_Layout = QVBoxLayout(self.dateTimeDiplayInterval)
        self.dateTimeDiplayInterval_Layout.addWidget(self.thirtyMin)
        self.dateTimeDiplayInterval_Layout.addWidget(self.oneHour)
        self.dateTimeDiplayInterval_Layout.addWidget(self.ninetyMin)
        self.dateTimeDiplayInterval_Layout.addWidget(self.twoHours)

        self.dateTimeDiplayInterval.setLayout(self.dateTimeDiplayInterval_Layout)
        self.mergeTabMain_Layout.addWidget(self.dateTimeDiplayInterval)
        #---------------------------Display Interval End-------------------------#

        self.mergeTabMain_Layout.addSpacing(17) # --> Spacing for Aesthtic Reasons. 
        # If the Window size changes the command above must be adjusted accordingly as well.
        
        #---------------------------Merge Button Start-----------------------------#
        self.mergeButton = QPushButton(parent = self.mergeTab, text = 'Merge')
        self.mergeTabMain_Layout.addWidget(self.mergeButton, alignment = Qt.AlignBottom)
        #---------------------------Merge Button Start---------------------------#

    #-------------------------------Annotate Tab Functions Start------------------------#
    def addAnnotateTimeWidgets(self):
        self.annotateTab_Layout = QGridLayout()
        self.annotateTab_Layout.setAlignment(Qt.AlignTop)

        #---------------------------Start Time Start-------------------------------#
        self.startTime_Label = QLabel(parent = self.annotateTab, text = 'Start Time:')
        self.annotateTab_Layout.addWidget(self.startTime_Label, 0, 0, 1, 1)

        # self.color_Label = QLabel(parent = self.annotateTab, text = 'Color:')
        # self.annotateTab_Layout.addWidget(self.color_Label, 0, 5, 1, 1)

        self.startTime = QTimeEdit(parent = self.annotateTab)
        self.startTime.setDisplayFormat('HH:mm:ss')
        self.startTime.setAlignment(Qt.AlignCenter)
        self.annotateTab_Layout.addWidget(self.startTime, 0, 1, 1, 3)

        #-----------------------------Color Start----------------------------------#
        self.color = QComboBox(parent = self.annotateTab)
        self.color.addItems(['Blue', 'Red', 'Green', 'Black', 'White', 'Yellow'])
        self.annotateTab_Layout.addWidget(self.color, 0, 4, 1, 2)
        
        #---------------------------End Time or Time Length Start------------------#
        self.endTimeOrTimeLength_Label = QLabel(parent = self.annotateTab,  text = 'Finish Time:  ')
        self.annotateTab_Layout.addWidget(self.endTimeOrTimeLength_Label, 1, 0, 1, 1)

        self.endTimeOrTimeLength = QTimeEdit(parent = self.annotateTab)
        self.endTimeOrTimeLength.setDisplayFormat('HH:mm:ss')
        self.endTimeOrTimeLength.setAlignment(Qt.AlignCenter)
        self.annotateTab_Layout.addWidget(self.endTimeOrTimeLength, 1, 1, 1, 3)

        # self.endTimeRadio = QRadioButton(parent = self.annotateTab)
        # self.endTimeRadio.setChecked(True)
        # self.annotateTab_Layout.addWidget(self.endTimeRadio, 1, 5, 1, 1, Qt.AlignRight)
        
        self.endTimeOrTimeLengthCheck = QCheckBox(parent = self.annotateTab, text = 'Finish Time/Time Length')
        self.annotateTab_Layout.addWidget(self.endTimeOrTimeLengthCheck, 1, 4, 1, 2, Qt.AlignRight)

        #---------------------------UNUSED RADIO BUTTONS Start---------------------#
        # self.timeLength_Label = QLabel(self.annotateTab, text = 'Time Length:')
        # self.annotateTab_Layout.addWidget(self.timeLength_Label, 2, 0, 1, 1)

        # readOnlyPalette = QtGui.QPalette()
        # readOnlyPalette.setColor(QtGui.QPalette.Text, Qt.darkGray)

        # self.timeLength = QTimeEdit(parent = self.annotateTab)
        # self.timeLength.setDisplayFormat('HH:mm:ss')
        # self.timeLength.setAlignment(Qt.AlignCenter)
        # self.timeLength.setReadOnly(True)
        # self.timeLength.setPalette(readOnlyPalette)
        # self.annotateTab_Layout.addWidget(self.timeLength, 2, 1, 1, 4)

        # self.timeLengthRadio = QRadioButton(parent=self.annotateTab)
        # self.annotateTab_Layout.addWidget(self.timeLengthRadio, 2, 5, 1, 1, Qt.AlignRight)

    def addAnnotateCommentWidget(self):
        #-----------------------------Comment Start--------------------------------#
        # self.comment_Label = QLabel(parent = self.annotateTab, text = 'Comment:')
        # self.annotateTab_Layout.addWidget(self.comment_Label, 2, 0, 1, 1)
        self.comment = myPlainTextEdit(parent = self.annotateTab)
        self.comment.setUndoRedoEnabled(True)
        self.comment.setPlaceholderText('Enter Comment')
        self.annotateTab_Layout.addWidget(self.comment, 2, 0, 1, 6)

        self.characterCount_Label = QLabel(parent = self.annotateTab, text = '0/100')
        self.annotateTab_Layout.addWidget(self.characterCount_Label, 3, 5, 1, 1, Qt.AlignRight)

        #-----------------------------Buttons Start------------------------------# 
        self.addButton = QPushButton(parent =self.annotateTab, text = '+Add')
        self.annotateTab_Layout.addWidget(self.addButton, 4, 0, 1, 3)
        self.annotateButton = QPushButton(parent = self.annotateTab,  text = 'Annotate')
        self.annotateTab_Layout.addWidget(self.annotateButton, 4, 3, 1, 3)

        self.annotateTabMain_Layout.addLayout(self.annotateTab_Layout)

def main():
    app = QApplication()
    GUI = MainWin()
    ctrl = MainWinCtrl(GUI)
    GUI.show()
    sys.exit(app.exec())
        
if __name__ == '__main__':
    main()