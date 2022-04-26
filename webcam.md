# Webcam branch

This branch is for developping a module for processing videostream from a webcam and it contains several files:

| File | Purpose |
|---|---|
videoWidget.ui | QT Designer file for the UI with separate video window
videoWidgedv2.ui | QT Design for UI with single window for both UI and video
widgedGui.py | UI uses a separate Window to show the videostream
singleWindowGui.py | The videostream is shown directly in QT UI and video processing is done in a separate thread
photo.py | Functions to handle videostream and adding view finder to stream
productBarcode.py | Routines for creating SVG or PNG bar codes. Supports Code 128 and EAN codes

## Production code
The UI for taking product pictures is ultimatelly implemented in `singleWindowGui.py` file and layout of the UI can be found in `videoWidgedv2.ui` file.

## Dependencies

Branch has several dependencies:

| Library or Module | Installation command or remark | Needed for module |
|---|---|---|
PyQT5 | `pip install pyqt5` | widgedGui.py and singleWindowGui.py
OpenCV | `pip install opencv-python` | widgedGui.py and singleWindowGui.py
qimage2ndarray | `pip install qimage2dnarray` | photo.py
photo | DIY module `photo.py` | widgedGui.py
