# Webcam branch

This branch is for developping a module for processing videostream from a webcam and it contains several files:

| File | Purpose |
|---|---|
videoWidget.ui | QT Designer file for the UI
widgedGui.py | UI uses a separate Window to show the videostream
singleWindowGui.py | The videostream is shown directly in QT UI and video processing is done in a separate thread
photo.py | Functions to handle videostream and adding view finder to stream

## Dependencies

Branch has several dependencies:

| Library or Module | Installation command or remark | Needed for module |
|---|---|---|
PyQT5 | `pip install pyqt5` | widgedGui.py and singleWindowGui.py
OpenCV | `pip install opencv-python` | widgedGui.py and singleWindowGui.py
qimage2ndarray | `pip install qimage2dnarray` | photo.py
photo | DIY module `photo.py` | widgedGui.py
