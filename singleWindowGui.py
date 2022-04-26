# EXAMPLE OF QT APPICATION FOR TAKING PRODUCT IMAGES IN SEPARATE THREAD USING WEB CAMERA

# LIBRARIES AND MODULES
from types import CodeType
import productBarcode
import cv2 # For OpenCV video and picture manipulation
import sys # For accessing system parameters
from PyQt5 import QtWidgets, uic # For the UI
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For creating multiple threads and signaling between UI and Video thread
from PyQt5.QtCore import Qt # For image scaling
from PyQt5.QtGui import QImage, QPixmap, QTransform # For image handling

# GLOBAL VARIABLES

# SEPARATE THREAD FOR VIDEO CAPTURE
class VideoThread(QThread):

    # Create signal to change the image field in the UI
    changePixmap = pyqtSignal(QImage)

    # The runner function
    def run(self):

        # Create a videocapture object and set capture dimensions to 1280 x 720
        # TODO: followind parameters of the camera must be read from preferences or fields of the UI
        videoStream = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        videoStream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        videoStream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, frame = videoStream.read()
            if ret:
                # Resize and convert video to UI
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR -> RGB
                height, width, channels = rgbImage.shape # Image size & number of channels
                bytesPerLine = channels * width # Calculate how many bytes per video line
                inQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
                videoOut = inQtFormat.scaled(640, 360, Qt.KeepAspectRatio) # Size of picture is 50% of original
                self.changePixmap.emit(videoOut) # Signal out the video


# APPLICATION CLASS FOR THE UI
class App(QtWidgets.QWidget):
    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        # Load the ui file
        uic.loadUi('videoWidgetv2.ui', self)

        # UI elements (Direct assignment to properties)
        self.picture = self.productImage
        self.productCode = self.productId
        # self.camera = self.cameraIxSpinBox
        self.preview = self.catalogPreview
        self.barCode = self.bcLabel
        self.captureButton.setEnabled(True)
        self.saveToDbButton.setEnabled(False)
        
        # Set the camera index
        # self.camera.valueChanged.connect(self.setCamIx)
        # Start Capture button signal to capture slot -> call capture function
        self.captureButton.clicked.connect(self.capture)

        # Save image to a file with still button 
        self.stillButton.clicked.connect(self.saveStill)

        # Set the Window Title and initialize the UI
        self.title = 'OpenCV video in QT window'
        self.initUI()

    # SLOTS

    # Set the camera index
    '''def setCamIx(self):
        camIx = self.camera.value()
        print(camIx)'''

    # Capture video: started by signal from captureButton
    def capture(self):
        # Create a thread for video
        videoThread = VideoThread(self)
        videoThread.changePixmap.connect(self.setImage)
        videoThread.start()
        
    # Save curent frame as a png file: started by signal from stillButton
    def saveStill(self):
        # Create a pixmap to be saved
        stillImage = self.picture.pixmap()
        fileName = self.productCode.text() + '.jpg'

        # Check the length of the filename: must contain at least one chr and extension .jpg
        if len(fileName) > 4:
            stillImage.save(fileName, 'jpg')

            # Read the file as pixmap for previewing
            landscapePixmap = QPixmap(fileName)

            # Transform the pixmap for the preview field (potrait)
            transformation = QTransform() # Create transformation object
            transformation.scale(0.5, 0.5) # Scale to half size
            transformation.rotate(90) # Rotate to potrait
            potraitPixmap = landscapePixmap.transformed(transformation) # Run the transformation
            self.preview.setPixmap(potraitPixmap) # Set the label

            # Create the barcode with options: type Code 128 and output format PNG
            productId = self.productCode.text()
            codeType = 'Code128'
            pictureType = 'PNG'
            
            # Set Writer options. A dictionary values for the writer: height 5 mm, margin to text 1mm, text size 10 pt
            writerOptions = productBarcode.setWriterOptions(5,1,10)
    
            # Create Code with given options
            barCode = productBarcode.barCode2Image(productId, codeType, pictureType)

            # Save the file
            barCode.save(productId, writerOptions)

            # Show it on the GUI
            bcodeImage = QPixmap(productId + '.'+ pictureType) # Pixmap from the file
            bcTransformation = QTransform() # Create transformation object
            bcTransformation.scale(0.5, 0.5) # Set scale to half size
            bcodeImage = bcodeImage.transformed(bcTransformation) # Do the transformation
            self.barCode.setPixmap(bcodeImage) # Show on label
            self.saveToDbButton.setEnabled(True)

        else:
            # Show error message about the file name
            alarmWindow = QtWidgets.QMessageBox()
            alarmWindow.setIcon(QtWidgets.QMessageBox.Critical)
            alarmWindow.setWindowTitle('Virheellinen tai puuttuva tuotekoodi')
            alarmWindow.setText('Tuotekoodissa on oltava vähintään 1 merkki!')
            alarmWindow.exec_()
        # TODO: check for illegal characters in product code 

    

    # Slot for receiving the video: signaled by videoThread
    @pyqtSlot(QImage) # @ decorator ie. function takes another function as argument and returns a function
    def setImage(self, image):
        self.picture.setPixmap(QPixmap.fromImage(image))
        self.captureButton.setEnabled(False)
        fileName = self.productCode.text() + '.jpg'
        if len(fileName) > 4:
            self.stillButton.setEnabled(True)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainwindow = App()
    app.exec_()