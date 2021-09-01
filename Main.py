import sys, os
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QMainWindow, QPlainTextEdit, QTabWidget, QVBoxLayout, QFrame
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QGridLayout, QMessageBox
from PySide6.QtCore import QLine, Qt

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('New Photo Editor')
        self.setFixedSize(360, 430)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.general_Layout = QVBoxLayout(parent = self.centralWidget)
        self.innerlayout_1 = QGridLayout(parent = self.centralWidget)
        self.innerlayout_1.setAlignment(Qt.AlignTop)
        
        self.addSourceWidgets()
        self.addDestinationWidgets()
        self.addFileWidgets()
        self.createWindowContainer


        self.general_Layout.addLayout(self.innerlayout_1)
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
        self.tabs = QTabWidget(parent = self.centralWidget)
        self.mergeTab = QWidget()
        self.annotateTab = QWidget()
        self.tabs.addTab(self.mergeTab, 'Merge')
        self.tabs.addTab(self.annotateTab, 'Annotate')



def main():
    app = QApplication(sys.argv)
    GUI = MainWin()
    GUI.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()