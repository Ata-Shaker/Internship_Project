import sys
import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog
from PySide6.QtCore import QLine, Qt



class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.LAST_INNER_LAYOUT_POSITION = 4

        # General Setup
        self.setWindowTitle("Photo Editor")
        self.setFixedSize(400, 400)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setAlignment(Qt.AlignTop)
        
        self.pathLabel = QLabel('Path:')
        self.generalLayout.insertWidget(0, self.pathLabel)

        #General Layout
        self.layout = QHBoxLayout() 
        self.pathDisplay = QLineEdit()
        self.pathDisplay.setReadOnly(True)
        self.browseButton = QPushButton('Browse')
        self.layout.addWidget(self.pathDisplay)
        self.layout.addWidget(self.browseButton)
        self.generalLayout.insertLayout(1, self.layout)
        self.runButton = QPushButton('Run')
        self.generalLayout.insertWidget(2, self.runButton)
        self.generalLayout.insertSpacing(3, 20)

        # self.runButton

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

    def _connectSignals(self):
        self._view.browseButton.clicked.connect(self.browse)

    def browse(self):
        self.folderName = QFileDialog.getExistingDirectory(self._view, 'Select a Folder', QtCore.QDir.rootPath())
        self._view.pathDisplay.setText(self.folderName[0])







def main():
    app  = QApplication(sys.argv)
    GUI = MainWin()
    Ctrl = MainWinCtrl(GUI)
    GUI.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()