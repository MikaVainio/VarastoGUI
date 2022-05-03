# APPLICATION FOR CREATING AND PRINTING STUDENT CARDS

# LIBRARIES AND MODULES
import productBarcode # Functions for barcodes
import sys # For accessing system parameters
import os # To do OS operations
from PyQt5 import QtWidgets, uic # For the UI
from PyQt5.QtCore import Qt # For image scaling
from PyQt5.QtGui import QImage, QPixmap, QTransform # For image handling

# CLASS DEFINITIONS

# The Application
class App(QtWidgets.QWidget):

    # Constructor
    def __init__(self):
        super().__init__()

        # Load the UI
        uic.loadUi('studentCardv2.ui', self)

        # UI elements 
        self.bCode = self.studentBarcode
        self.student = self.studentNumberEdit
        self.picture = self.pictureLabel

        # Signals
        # self.student.textEdited.connect(self.setBarcode)
        self.loadPictureButton.clicked.connect(self.setBarcode)

         # Set the Window Title and initialize the UI
        self.title = 'Opiskelijakortti'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()

    def setBarcode(self):
         # Student ID to encode
        id = self.student.text()
        codeType = 'Code128'
        pictureType = 'PNG'

        # Set Writer options. Height 5 mm, text 1 mm from code, text 12 pt
        writerOptions = productBarcode.setWriterOptions(5,1,8)
    
        # Create Code 128 barcode and save it into temporary file
        barCode = productBarcode.barCode2Image(id, codeType, pictureType)
        tempBarcode = barCode.save('tmpbarcode', writerOptions)
        
        # Update the  bar code label
        barCodePixmap = QPixmap(tempBarcode)
        self.bCode.setPixmap(barCodePixmap)

        # Remove the temporary file
        os.remove('tmpbarcode.png')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainwindow = App()
    app.exec_()    