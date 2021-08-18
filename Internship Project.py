import sys
import PySide6
from PySide6.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit, QVBoxLayout, QGridLayout, QWidget, QPushButton, QLineEdit, QDialogButtonBox
from PySide6.QtCore import QLine, Qt


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        # General Setup
        self.setWindowTitle("Photo Editor")
        self.setFixedSize(400, 300)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout = QVBoxLayout()
        
        # 1st Layout 
        self.layout1 = QHBoxLayout() 
        self.pathDisplay = QLineEdit()
        self.pathDisplay.setReadOnly(True)
        self.browseButton = QPushButton('Browse')
        self.layout1.addWidget(self.pathDisplay)
        self.layout1.addWidget(self.browseButton)

        # 2nd Layout Labels
        self.layout2Labels = QHBoxLayout()
        self.startTimeLabel = QLabel('Start Time:')
        self.endTimeLabel = QLabel('End Time:')
        self.colorComboLabel = QLabel('Color:')
        self.layout2Labels.addWidget(self.startTimeLabel)
        self.layout2Labels.addWidget(self.endTimeLabel)
        self.layout2Labels.addWidget(self.colorComboLabel)
        self.layout2Labels.insertSpacing(1,95)
        self.layout2Labels.insertSpacing(3,94)



        # 2nd Layout
        self.layout2 = QHBoxLayout()
        self.startTime = QLineEdit()
        self.endTime = QLineEdit()
        self.colorCombo = QComboBox()
        self.colorCombo.addItem('Black')
        self.colorCombo.addItem('White')
        self.colorCombo.addItem('Green')
        self.colorCombo.addItem('Red')
        self.colorCombo.addItem('Blue' )
        self.colorCombo.addItem('Yellow')
        self.layout2.addWidget(self.startTime)
        self.layout2.addWidget(self.endTime)
        self.layout2.addWidget(self.colorCombo)

        self.stdBtns = QDialogButtonBox()
        self.stdBtns.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        

        # Wrapping UP

        self.pathLabel = QLabel('Path:')
        self.generalLayout.addWidget(self.pathLabel)


        self.generalLayout.addLayout(self.layout1)
        self.generalLayout.addSpacing(20)
        self.generalLayout.addLayout(self.layout2Labels)
        self.generalLayout.addLayout(self.layout2)
        self.generalLayout.setAlignment(Qt.AlignTop)
       
        self.plainTextLabel = QLabel('Note')
        self.generalLayout.addWidget(self.plainTextLabel)
        self.plainText = QPlainTextEdit()
        self.generalLayout.addWidget(self.plainText)

        self.generalLayout.addWidget(self.stdBtns)
        
        self._centralWidget.setLayout(self.generalLayout)











def main():
    app  = QApplication(sys.argv)
    GUI = MainWin()
    GUI.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()