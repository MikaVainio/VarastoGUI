# FUNCTIONS FOR WEB CAMERA IMAGE MANIPULATION
# -------------------------------------------

# MODULES AND LIBRARIES:

# OpenCV for image and video manipulatation, external library must be installed with pip: pip install opencv-python
import cv2

# NumPy for array and matrix operations, will be installed automatically with openCV
import numpy

# Library converting numpy arrays to qimages, must be installed: pip install qimage2ndarray
import qimage2ndarray

# SOME GLOBAL VARIABLES TO AVOID WSCODE WARNINGS
stop_capture = False

# FUNCTIONS:

# 1. TAKE A STILL IMAGE WITH WEB CAMERA AND SAVE IT AS JPG FILE


def take_still(cam_ix, view_scale, margin, file_name, save_scale):
    """Takes a still image with web camera and saves it as jpg. 
    Capture window has a safe area rectangle to give propper margins for the final image.
    Lines of thirds are present in the preview window. Center point of safe area is also
    marked with a circle.

    Args:
        cam_ix (int): Index of the web camera, 1st camera is 0
        view_scale (float): Factor for scaling the capture window 0,5 half size, 2 double size
        margin (int): Safety margin in pixels from the edge of the picture to the safe area rectangle 
        file_name (string): name of the output file
        save_scale (float): Factor for scaling the the final image 0,5 half size, 2 double size

    Returns:
        dict: Satus and picture dimensions
    """
    # Creating a VideoCapture object for the wideo stream from the Web camera
    video_stream = cv2.VideoCapture(cam_ix)

    # Loop until iterrupted by keystroke s -> save
    while (video_stream.isOpened()):

        # Capture the stream frame by frame, read() fuction returns true if reading is successfull and a wideo frame
        ret, frame = video_stream.read()

        # Check if capture is successfull
        if ret == True:

            # Find out frame dimensions and number of channels (for proportional resizing)
            orig_height, orig_width, channels = frame.shape

            # Dimensions for the video window and the still image
            width = int(round(orig_width * view_scale, 0))
            height = int(round(orig_height * view_scale, 0))

            # Resize the frame for preview using bicubic interpolation
            frame = cv2.resize(frame, (width, height),
                               fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

            # Draw a red safe area rectangle into the frame (BGR colour space, line width 4 px)
            top_left = (margin, margin)
            bottom_right = (width - margin,
                            height - margin)
            cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 4)

            # Draw a center circle into the frame (radius 40 px, line width 1 px)
            center_x = int(round(width / 2, 0))
            center_y = int(round(height / 2, 0))
            cv2.circle(frame, (center_x, center_y), 40, (0, 0, 255), 1)

            # Define dividing lines for thirds to help positioning objects into safe area

            # Calculate starting and ending coordinates for vertical lines
            safe_area_width = int(round(width - margin * 2, 0))
            safe_area_height = int(round(height - margin * 2, 0))

            v_line_1_top_x = int(round(margin + safe_area_width / 3, 0))
            v_line_1_top_y = margin
            v_line_1_bottom_x = int(round(margin + safe_area_width / 3, 0))
            v_line_1_bottom_y = height - margin

            v_line_2_top_x = int(round(margin + safe_area_width / 3 * 2, 0))
            v_line_2_top_y = margin
            v_line_2_bottom_x = int(
                round(margin + safe_area_width / 3 * 2,  0))
            v_line_2_bottom_y = height - margin

            # Create end points for vertical lines
            v_line_1_top = (v_line_1_top_x, v_line_1_top_y)
            v_line_1_bottom = (v_line_1_bottom_x, v_line_1_bottom_y)

            v_line_2_top = (v_line_2_top_x, v_line_2_top_y)
            v_line_2_bottom = (v_line_2_bottom_x, v_line_2_bottom_y)

            # Calculate starting and ending coordinates for horizontal lines
            h_line_1_left_x = margin
            h_line_1_left_y = int(round(margin + safe_area_height / 3, 0))
            h_line_1_right_x = margin + safe_area_width
            h_line_1_right_y = int(round(margin + safe_area_height / 3, 0))

            h_line_2_left_x = margin
            h_line_2_left_y = int(round(margin + safe_area_height / 3 * 2, 0))
            h_line_2_right_x = margin + safe_area_width
            h_line_2_right_y = int(round(margin + safe_area_height / 3 * 2, 0))

            # Create end points for horizontal lines
            h_line_1_left = (h_line_1_left_x, h_line_1_left_y)
            h_line_1_right = (h_line_1_right_x, h_line_1_right_y)

            h_line_2_left = (h_line_2_left_x, h_line_2_left_y)
            h_line_2_right = (h_line_2_right_x, h_line_2_right_y)

            # Draw lines (1 pix red)
            cv2.line(frame, v_line_1_top, v_line_1_bottom, (0, 0, 255), 1)
            cv2.line(frame, v_line_2_top, v_line_2_bottom, (0, 0, 255), 1)
            cv2.line(frame, h_line_1_left, h_line_1_right, (0, 0, 255), 1)
            cv2.line(frame, h_line_2_left, h_line_2_right, (0, 0, 255), 1)

            # Display the video frame in a window named Video stream
            cv2.imshow('Video stream with safe area', frame)

        # Define a key stroke s as the save and exit from video streaming, wait 25 ms for key storke
        if cv2.waitKey(25) & 0xFF == ord('s'):
            break

    # Save the last captured frame as jpg image (without rectangle)
    ret, frame = video_stream.read()
    if ret == True:

        # Dimensions for the the still image
        final_width = int(round(orig_width * save_scale, 0))
        final_height = int(round(orig_height * save_scale, 0))

        # Resize the frame for final image using bicubic interpolation
        frame = cv2.resize(frame, (final_width, final_height),
                           fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

        # Save the final image
        cv2.imwrite(file_name, frame)

    # Release the video capture object
    video_stream.release()

    # Read the still image and show it in a new window
    still_image = cv2.imread(file_name)
    cv2.imshow('Still image', still_image)

    # Wait for key stroke q to close all open video and picture windows
    while True:
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Closes all the windows currently opened.
    cv2.destroyAllWindows()

    # Return image information
    capture_info = {'original width': orig_width, 'original height': orig_height, 'final width': final_width,
                    'final height': final_height, 'channels': channels}
    return capture_info

# 2. CREATE VIEW FINDER GRAPHICS FOR A WEBCAM


def create_view_finder(frame, width, height, margin, color):
    """Create a view finder graphics to wideo stream. Contains a safe area rectangle,
    lines of thrirds and a center circle

    Args:
        frame (pixel matrix): video frame to draw
        width (int): width of the video frame in pixels
        height (int): height of the video frame in pixels
        margin (int): distance from edge of the frame to the safe area rectangle in pixels
        color (list): BGR-color of the view finder
    """
    # Draw a safe area rectangle into the frame (BGR colour space, line width 4 px)
    top_left = (margin, margin)
    bottom_right = (width - margin,
                    height - margin)
    cv2.rectangle(frame, top_left, bottom_right, color, 4)

    # Draw a center circle into the frame (radius 1/12 of the frame height, line width 1 px)
    center_x = int(round(width / 2, 0))
    center_y = int(round(height / 2, 0))
    circle_radius = int(round(height / 12, 0))
    cv2.circle(frame, (center_x, center_y), circle_radius, color, 1)

    # Define dividing lines for thirds to help positioning objects into safe area

    # Calculate starting and ending coordinates for vertical lines
    safe_area_width = int(round(width - margin * 2, 0))
    safe_area_height = int(round(height - margin * 2, 0))

    v_line_1_top_x = int(round(margin + safe_area_width / 3, 0))
    v_line_1_top_y = margin
    v_line_1_bottom_x = int(round(margin + safe_area_width / 3, 0))
    v_line_1_bottom_y = height - margin

    v_line_2_top_x = int(round(margin + safe_area_width / 3 * 2, 0))
    v_line_2_top_y = margin
    v_line_2_bottom_x = int(round(margin + safe_area_width / 3 * 2,  0))
    v_line_2_bottom_y = height - margin

    # Create end points for vertical lines
    v_line_1_top = (v_line_1_top_x, v_line_1_top_y)
    v_line_1_bottom = (v_line_1_bottom_x, v_line_1_bottom_y)

    v_line_2_top = (v_line_2_top_x, v_line_2_top_y)
    v_line_2_bottom = (v_line_2_bottom_x, v_line_2_bottom_y)

    # Calculate starting and ending coordinates for horizontal lines
    h_line_1_left_x = margin
    h_line_1_left_y = int(round(margin + safe_area_height / 3, 0))
    h_line_1_right_x = margin + safe_area_width
    h_line_1_right_y = int(round(margin + safe_area_height / 3, 0))

    h_line_2_left_x = margin
    h_line_2_left_y = int(round(margin + safe_area_height / 3 * 2, 0))
    h_line_2_right_x = margin + safe_area_width
    h_line_2_right_y = int(round(margin + safe_area_height / 3 * 2, 0))

    # Create end points for horizontal lines
    h_line_1_left = (h_line_1_left_x, h_line_1_left_y)
    h_line_1_right = (h_line_1_right_x, h_line_1_right_y)

    h_line_2_left = (h_line_2_left_x, h_line_2_left_y)
    h_line_2_right = (h_line_2_right_x, h_line_2_right_y)

    # Draw lines for thirds, line width 1 px
    cv2.line(frame, v_line_1_top, v_line_1_bottom, color, 1)
    cv2.line(frame, v_line_2_top, v_line_2_bottom, color, 1)
    cv2.line(frame, h_line_1_left, h_line_1_right, color, 1)
    cv2.line(frame, h_line_2_left, h_line_2_right, color, 1)

# 3.GET BGR COLOR VALUES BY COMMON COLOR NAMES
def color_bgr_values(color_name):
    """Function returns BGR values of given color name

    Args:
        color_name (string): common name of the color

    Returns:
        list: list of BGR values
    """

    # Dictionary of common colors and their BGR values
    common_colors = {'red' : (0, 0, 255), 'green' : (0, 255, 0),
                    'blue': (255, 0, 0), 'yellow' : (0, 255, 255),
                    'violet' : (255, 0, 255), 'orange' : (0, 127, 255),
                    'gray': (127, 127,127), 'light gray' : (181, 181, 181),
                    'black' : (0, 0, 0), 'white' : (255, 255, 255)}
    
    return common_colors[color_name]

# 4. SIMPLE VIDEO CAPTURE WITH WEB CAMERA

def video_to_still_image(file_name, cam_ix, margin, color):
    """Captures Video from Web camera and saves the last frame as a jpg file

    Args:
        file_name (string): The name of the output file without jpg extension
        cam_ix (integer): Web Camera index, 1st cam is 0
        margin (integer): number of pixels from the edge of the frame to safe area
        color (string): name of the color for the view finder graphics
    """
    video_stream = cv2.VideoCapture(cam_ix)
    stop_capture_flag = False
    while (video_stream.isOpened()):
    
        # Capture the stream frame by frame, read() fuction returns true if reading is successfull and a wideo frame
        ret, frame = video_stream.read()

        # Check if capture is successfull and return a frame
        if ret == True:

            # read dimensions of the frame
            height, width, channels = frame.shape
            color = color_bgr_values('orange')

            # Add a view finder
            create_view_finder(frame, width, height, margin, color)

            cv2.imshow('frame', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):

                break  
    
    # Save the frame to a file
    jpg_file = file_name + '.jpg'
    cv2.imwrite(jpg_file, frame)

# 5. SIMPLE VIDEO CAPTURE WITH WEB CAMERA. LIVE VIDEO IN SEPARATE VINDOW, RETURNS A STILL PICTURE FOR QT5 UI

def qt_video_capture(cam_ix, margin, color):
    """Shows a video stream in OpenCV window and returns QImage
       The live video window has a view finder to help positioning objects in the frame

    Args:
        cam_ix (integer): Camera index 1st web camera is 0
        margin (integer): Distance from edge of the video frame to view finder in pixels
        color (string): Name of the color used in the view finder

    Returns:
        QImage: last frame of the stream as QImage
    """
    video_stream = cv2.VideoCapture(cam_ix)

    while (video_stream.isOpened()):
    
        # Capture the stream frame by frame, read() fuction returns true if reading is successfull and a wideo frame
        ret, frame = video_stream.read()

        # Check if capture is successfull and return a frame
        if ret == True:

            # read dimensions of the frame
            height, width, channels = frame.shape
            vf_color = color_bgr_values(color)

            # Add a view finder
            create_view_finder(frame, width, height, margin, vf_color)

            cv2.imshow('frame -PRESS q TO EXIT', frame)

            # Stop caputing when key q is pressed and convert to Qimage format
            if cv2.waitKey(25) & 0xFF == ord('q'):
                ret, frame = video_stream.read() # clean frame without view finder
                rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert last frame to RGB
                photo = qimage2ndarray.array2qimage(rgbFrame) # Convert the pixel array to QImage format
                break 
    # return last frame as a photograph
    return photo
    


# QUICK TESTS INSIDE THIS MODULE TO BE REMOVED WHEN IN PRODUCTION
if __name__ == '__main__':

    # Otetaan kuva kameralla 2 (indeksi 1), 2 x suurennos 50 px suoja-alue ja lopullinen koko 2 x
    #picture_info = take_still(0, 1, 50, 'testi.jpg', 1)
    #print(picture_info)

    drawing_color = color_bgr_values('orange')
    print('Piirtoväri on', drawing_color)

    video = video_to_still_image('KoTu 12345', 1, 30, 'orange')

    