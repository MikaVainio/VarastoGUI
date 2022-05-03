# SIMPLE APP FOR TAKING SQUARE PICTURES FOR STUDENT CARDS


# LIBRARIES AND MODULES
import cv2 # For OpenCV video and picture manipulation
import sys # For accessing system parameters
from PyQt5 import QtWidgets, uic # For the UI
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For creating multiple threads and signaling between UI and Video thread
from PyQt5.QtCore import Qt, QRect # For image scaling and cropping
from PyQt5.QtGui import QImage, QPixmap, QTransform # For image handling

# GLOBAL VARIABLES

# SEPARATE THREAD FOR VIDEO CAPTURE
class VideoThread(QThread):

    # Create signal to change the image field in the UI
    changePixmap = pyqtSignal(QImage)

    # The runner function
    def run(self):

        # Create a videocapture object and set capture dimensions to 1280 x 720
        # Mika's work computer cameras 0:Cannon, 1:ThinkPad Internal, 2:Logitech external
        
        videoStream = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        videoStream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        videoStream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, frame = videoStream.read()
            if ret:
                # Mirror the video and convert video to UI
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR -> RGB
                height, width, channels = rgbImage.shape # Image size & number of channels
                bytesPerLine = channels * width # Calculate how many bytes per video line
                inQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888) # Change format
                mirroredImage = inQtFormat.mirrored() # Mirror the video to help putting face to correct position
                transformatation = QTransform() # Create a transformation object
                transformatation.rotate(180) # Mirrored image is upside down so it must be rotated
                videoOut= mirroredImage.transformed(transformatation) # Do the transformation
                self.changePixmap.emit(videoOut) # Signal out the video


# APPLICATION CLASS FOR THE UI
class App(QtWidgets.QWidget):
    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        # Load the ui file
        uic.loadUi('StudentPotrait.ui', self)

        # UI elements (Direct assignment to properties)
        self.picture = self.videoImage
        self.student = self.studentId
        # self.camera = self.cameraIxSpinBox
        self.preview = self.photoPreview
        # self.barCode = self.bcLabel
        self.captureButton.setEnabled(True)
        # self.saveToDbButton.setEnabled(False)
        
        # Start Capture button signal to capture slot -> call capture function
        self.captureButton.clicked.connect(self.capture)

        # Save image to a file with still button 
        self.stillButton.clicked.connect(self.saveStill)

        # Set the Window Title and initialize the UI
        self.title = 'Student picture from video'
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
        
    # Save curent frame as a JPG file: started by signal from stillButton
    def saveStill(self):
        # Create a pixmap to be saved
        stillImage = self.picture.pixmap()
        # Transform the pixmap for the preview field (potrait
        transformation = QTransform() # Create transformation object
        transformation.scale(0.5, 0.5) # Set scale
        scaledImage = stillImage.transformed(transformation) # Run the transformation
        cropArea = QRect(0, 0, 360, 360) # Define cropping box
        squarePixmap = scaledImage.copy(cropArea) # Copy the cropped image pixels
        fileName = self.student.text() + '.jpg'

        # Check the length of the filename: must contain at least one chr and extension .jpg
        if len(fileName) > 4:
            squarePixmap.save(fileName, 'jpg')
            # Read the file as pixmap for previewing
            self.preview.setPixmap(squarePixmap) # Set the label

            
        # TODO: check for illegal characters in product code 

    

    # Slot for receiving the video: signaled by videoThread
    @pyqtSlot(QImage) # @ decorator ie. function takes another function as argument and returns a function
    def setImage(self, image):
        self.picture.setPixmap(QPixmap.fromImage(image))
        self.captureButton.setEnabled(False)
        fileName = self.student.text() + '.jpg'
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
