# APPLICATION FOR CREATING AND PRINTING STUDENT CARDS

# LIBRARIES AND MODULES
import productBarcode # Functions for barcodes
import sys # For accessing system parameters
import os # For directory and file handling
from PyQt5 import QtWidgets, uic , QtPrintSupport # For the UI and printing
from PyQt5.QtGui import QPixmap, QTransform, QPainter # For image handling

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
        self.student.textEdited.connect(self.setBarcode)
        self.printButton.clicked.connect(self.printCard)
        self.loadPictureButton.clicked.connect(self.openPicture)

        # Set the Window Title and initialize the UI
        self.title = 'Opiskelijakortti'
        self.initUI()

    # Slots
    def setBarcode(self):
         # Student ID to encode
        id = self.student.text()
        codeType = 'Code128'
        pictureType = 'PNG'

        # Set Writer options. Height 5 mm, text 1 mm from code, text 8 pt
        writerOptions = productBarcode.setWriterOptions(5,1,8)
    
        # Create Code 128 barcode and save it into a temporary file
        barCode = productBarcode.barCode2Image(id, codeType, pictureType)
        tempBarcode = barCode.save('tmpbarcode', writerOptions)

        # Draw the barcode
        barCodePixmap = QPixmap(tempBarcode)
        self.bCode.setPixmap(barCodePixmap)

        # Remove the temporary file
        os.remove('tmpbarcode.png')

    def printCard(self):
        # Create a printer object as painter device, High resolution printing
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)

        # Create a printer dialog object
        printDialog = QtPrintSupport.QPrintDialog(printer, self)

        # Check if user starts printing
        if printDialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:

            # Create a painter object for creating a page to print
            painter = QPainter()

            # TODO: This should be tested with card printer with and without  HighResolution by using
            # printers own scaling options ie scale to fit found in print dialog. In the future put 
            # scaling parameters (resolutininto UI's Options Menu

            # Start creating an image to print from cardFrame in the UI
            painter.begin(printer) # Start the painter using the printer device
            card = self.cardFrame.grab() # Grab the UI element to print
            transformation = QTransform() # Create transformation object for scaling the image
            transformation.scale(2.4, 2.4) # Set resizing factors for credit card size, values according to test printer
            sizedCard = card.transformed(transformation) # Apply the transformation
            painter.drawPixmap(10, 10, sizedCard) # Create a pixmap to print
            painter.end() # Close the priter

    def openPicture(self):
        
        fileName, check = QtWidgets.QFileDialog.getOpenFileName(None)
        if filename:
            print(fileName)
            studentPhoto = QPixmap(fileName)
            self.picture.setPixmap(studentPhoto)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()

            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    mainwindow = App()
    app.exec_()