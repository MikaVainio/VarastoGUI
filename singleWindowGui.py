# EXAMPLE OF QT APPICATION FOR TAKING PRODUCT IMAGES IN SEPARATE THREAD USING WEB CAMERA

# LIBRARIES AND MODULES
import cv2 # For OpenCV video and picture manipulation
import sys # For accessing system parameters
from PyQt5 import QtWidgets, uic # For the UI
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For creating multiple threads and signaling between UI and Video thread
from PyQt5.QtCore import Qt # For image scaling
from PyQt5.QtGui import QImage, QPixmap # For image handling
# from PIL import ImageQt # For saving QLabel to file

# SEPARATE THREAD FOR VIDEO CAPTURE
class VideoThread(QThread):

    # Create signal to change the image field in the UI
    changePixmap = pyqtSignal(QImage)

    # The runner function
    def run(self):

        # Create a videocapture object and set capture dimensions to 1280 x 720
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
    # Constructor for the UI
    def __init__(self):
        super().__init__()

        # Load the ui file
        uic.loadUi('videoWidget.ui', self)

        # UI elements (Direct assignment to properties)
        self.picture = self.productImage
        self.productCode = self.productId
        self.captureButton.setEnabled(True)
        self.stillButton.setEnabled(True)

        # Start Capture button signal to capture slot -> call capture function
        self.captureButton.clicked.connect(self.capture)

        # Save image to a file 
        self.stillButton.clicked.connect(self.saveStill)

        self.title = 'OpenCV video in QT window'
        self.initUI()

    # Capture video
    def capture(self):
        # Create a thread for video
        videoThread = VideoThread(self)
        videoThread.changePixmap.connect(self.setImage)
        videoThread.start()

    # Save curent frame as a png file
    def saveStill(self):
        # Create a pixmap to be saved
        #stillImage = ImageQt.fromqpixmap(self.picture.pixmap()) # Using PIL library
        stillImage = self.picture.pixmap()
        stillImage.save('tuote.jpg', 'jpg')

    

    # Slot for receiving the video 
    @pyqtSlot(QImage) # @ decorator ie. function takes another function as argument and returns a function
    def setImage(self, image):
        self.picture.setPixmap(QPixmap.fromImage(image))
        self.captureButton.setEnabled(False)

    def initUI(self):
        self.setWindowTitle(self.title)
        # videoThread = VideoThread(self)
        # videoThread.changePixmap.connect(self.setImage)
        # videoThread.start()
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = App()
    app.exec_()