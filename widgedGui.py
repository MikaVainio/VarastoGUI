# EXAMPLE OF QT WIDGET FOR TAKING PRODUCT IMAGES WITH WEB CAMERA

# LIBRARIES AND MODULES

from PyQt5 import QtWidgets, uic # For the UI, PyQT must be installed with pip first
from PyQt5.QtGui import QPixmap # For creating pixel maps from files
import sys # For accessing system parameters
import cv2
import photo # Home brew module for video capture


# CLASS DEFINITIONS

# Class for the widget window
class Ui(QtWidgets.QWidget):

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        # Load the ui file
        uic.loadUi('videoWidget.ui', self)

        # Flags for enbling & disabling controls
        self.valid_product_id = False
        self.capturing = False
        self.still_taken = False
        self.still_saved = False
       

        # UI OBJECTS

        # Set all buttons inital state to disabled
        self.captureButton.setEnabled(False)
        self.stillButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        # Controls and their corresponding UI elements (direct assignment to properties)
        self.product = self.productId
        
 
        # Indicators (direct assignment to properties)
        self.picture = self.productImage

        # Set the product image to no image
        self.pixmap = QPixmap('none.png') # Create pixmap from png file
        self.picture.setPixmap(self.pixmap) # Update product picture
        

        # SIGNALS & SLOTS

        # Start Capture button signal to capture slot -> call capture function
        self.captureButton.clicked.connect(self.capture)

        # If there has been change in the product field enable Start Capture button -> call show_start_button function
        self.product.textChanged.connect(self.show_start_button) 

        # Take Still button signal to exit capture mode and save the image -> call save_image function
        self.stillButton.clicked.connect(self.take_picture)

        self.saveButton.clicked.connect(self.save_picture)
        # MAKE UI VISIBLE
        self.show()

    # METHODS

    # Capture video
    def capture(self):
       
        # Start Video Capture and convert output to QImage format
        self.photo = photo.qt_video_capture(1, 20, 'yellow') # Capture and add a view finder, last frame out without view finder
        
        # Enable Take Still button and change focus to it
        self.stillButton.setEnabled(True)
        self.stillButton.setFocus()
         
        # Disable Start Video Capture button
        self.captureButton.setEnabled(False)

    # Enable Start Capture button and disable other buttons if valid product id  
    def show_start_button(self):
        self.captureButton.setEnabled(False) # Disable Capture button before checking product
        characters_in_id = self.product.text()
        characters_not_allowed = [',', '.', '/', '\\', ':']
        found_illegal_character = any(symbol in characters_in_id for symbol in characters_not_allowed)
        if found_illegal_character == False and characters_in_id != '':
            self.valid_product_id = True
        if self.valid_product_id == True:
            self.captureButton.setEnabled(True)
            self.stillButton.setEnabled(False)
            self.saveButton.setEnabled(False)   

    # Take a still image and show it in the GUI
    def take_picture(self):
        pixmap = QPixmap(self.photo)
        self.picture.setPixmap(pixmap)
        # Check if picture name is valid and enable save button and disable still
        pic_file_name = self.product.text() + '.jpg'
        if len(pic_file_name) > 4:
            self.saveButton.setEnabled(True)
            self.saveButton.setFocus()
            self.stillButton.setEnabled(False)
            cv2.destroyAllWindows()

    # Save the image file
    def save_picture(self):
            pic_file_name = self.product.text() + '.jpg'
            self.pixmap.save(pic_file_name, 'jpg')
            self.product.setFocus()
            self.saveButton.setEnabled(False)

# CREATE & RUN THE UI

app = QtWidgets.QApplication(sys.argv)
mainwindow = Ui()
app.exec_()