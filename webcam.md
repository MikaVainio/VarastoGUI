# Vebcam branch

This branch is for developping a module for processing videostream from a webcam and contains several files:

| File | Purpose |
|---|---|
videoWidget.ui | QT Designer file for the UI
widgedGui.py | UI uses a separate Window to show the videostream
singleWindowGui.py | The videostream is shown directly in QT UI and video processing is done in a separate thread

## Dependencies

Module has several dependencies:

| Library or Module | Installation command or remark |
|---|---|
PyQT5 | `pip install pyqt5`
OpenCV | `pip install opencv-python`
qimage2ndarray | `pip install qimage2dnarray`
photo | DIY module `photo.py`
