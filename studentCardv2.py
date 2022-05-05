# APPLICATION FOR CREATING AND PRINTING STUDENT CARDS
# ---------------------------------------------------

# LIBRARIES AND MODULES
from barcode import Code128, ean # For creating bar codes
from barcode.writer import ImageWriter, SVGWriter # Writers to generate an image files from bar codes
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
        # self.student.textEdited.connect(self.setBarcode)
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
        writerOptions = setWriterOptions(5,1,8)
    
        # Create Code 128 barcode and save it into a temporary file
        barCode = barCode2Image(id, codeType, pictureType)
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
            # scaling parameters (resolution into UI's Options Menu) Also check margins now 10 dots

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
        if fileName:
            
            studentPhoto = QPixmap(fileName)
            self.picture.setPixmap(studentPhoto)

            self.setBarcode()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()

# FUNCTIONS FOR GENERATING BAR CODES        

def barCode2Image(productId, codeType='Code128', pictureType='PNG'):
        """Creates image of barcode from a string. Funtion supports Code 128 and EAN 13

        Args:
        productId (str): String which will be encoded into a barcode
        codeType (str, optional): Type of the barcode. Defaults to 'Code128'.
        pictureType (str, optional): Type of image. Defaults to 'PNG'.

        Returns:
        object: image object
        """
        # Create a PNG file
        if pictureType == 'PNG':

            # Check the barcode type
            if codeType == 'Code128':

                # Create Code 128 barcode in RGB Color space (no transparency)
                bCodeImage = Code128(
                productId, writer=ImageWriter(pictureType, 'RGB'))
            else:
                # Create EAN 13 barcode in RGB Colour space
                bCodeImage = ean.EuropeanArticleNumber13(
                    productId, writer=ImageWriter(pictureType, 'RGB'), no_checksum=False)

        # Create a SVG file
        else:
            # Check the barcode type
            if codeType == 'Code128':

                # Create Code 128 barcode
                bCodeImage = Code128(productId, writer=SVGWriter())
            else:
                # Create EAN 13 barcode
                bCodeImage = ean.EuropeanArticleNumber13(
                    productId, writer=SVGWriter, no_checksum=False)

        return bCodeImage

    # Function to define barcode dimensions and the font size
def setWriterOptions(height=7, textDistance=2, fontSize=10):
        """Creates a dictionary for pyhton-barcode Writer

        Args:
            height (int, optional): Height of the barcode in mm. Defaults to 7.
            textDistance (int, optional): Distance between bars and plain text presentation in mm. Defaults to 2.
            fontSize (int, optional): Size of the plain text in pt. Defaults to 10.

        Returns:
            dict: Barcode Writer Options 
        """
        writerOptions = {'module_height' : height, 'text_distance' : textDistance, 'font_size' : fontSize}
        return writerOptions



 # CREATING AND STARTING THE APPLICATION  
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainwindow = App()
    app.exec_()