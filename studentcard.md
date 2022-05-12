# Studentcard

This branch is for developping a stand alone GUI and an application  for creating and printing student cards with a specialized card printer.

The GUI is designed as follows:

![image](https://user-images.githubusercontent.com/24242044/163401203-7d13ca9d-44e3-44b7-8f20-f05d487c44e2.png)

The User types a student number into text edit Opiskelijanumero (1). Student information is updated to labels (9) and bar code (12) is drawn at the bottom of the white preview frame (4). This area will be printed on the physical student card. When Hae Kuva (Load picture) Button (2) is pressed the photograph of the student is shown in a label (8) which is inside a Raseko coloured frame (5). The frame is created by using Qlabel frame properties and styles. Logo (6) and some fixed information (7, 10) is allways shown on the card prewiew. Stripe (11) is coloured frame with a label. If all information and the photo is OK, user can print the card with Tulosta (Print) Button (3). When Opiskelijanumero (1) is being edited picture (8), bar code (12) and all dynamic labels (9) are cleared. 

Previous picture is the original design. Some alterations has been made in the 2nd version `studentCardv2.ui`. There are some fields added so the user can type in all necessary student information. Hae Kuva button (2) opens a file dialog for choosing a photograph of the student. In the 1st version intention was to retrieve picture from a dabase but there is no need to store student pictures in the database. Only minimum of personal informatios will be stored (student ID, name, responsible instructor's email address and class name) Class name is not printed to student card.

In the final version all font sizes should be carefully inspected. The size of the card is 86 x 54 mm. Propably RASEKO's VAT number and perhaps the course name are too small in that size. Printing can be done with high resolution or normal printer settings. When high resolution printing is used the size of preview frame (# 4 in the first picture) must be scaled approximately 2.5 times for correct print size. If normal printing is used scaling factor is 0.3. Final values depend on resolutions of the monitor and the card printer. Typically the monitor resolution is 96 dpi and the printing resolution 300 dpi.

In the 2nd version all dynamic labels are bound to line edit elements by QTSignals. Singnals and slots are created graphically in the QTEditor.

![image](https://github.com/MikaVainio/VarastoGUI/blob/dev-studentcard/Opiskelijakorttisovellus.png)

This branch has 3 python files and 3 ui files. Most current files are:

| Library or module | Purpose |
|---|---|
code128Bcode.py | For generating and saving barcodes
studentCard.py | Applications main module
studentCardv2.ui | Current UI definitions for the app
studentPicture.py | A small application for taking photos for the student card
studentPicture.ui | UI for the photo taking application

Some image files are needed for logos and as placeholders.

* Omakuva2.png -> placeholder for student photo
* Raseko-logo-vaaka.png -> The logo of our school

# Distribution

For distributing applications we need the `PyInstaller` library. It can be installed into the virtual environment `pip install PyInstaller`. Applications for this branch use quite many external libraries so it is not vise to distiribute the application in single standalone `exe` file. With separate `dll` link libraries the file size of the exe's file size is much smaller thus there are many files in the distribution directory. When creating an application with a separate `ui` file it is essential to copy manually the `ui` file into `dist` folder. `PyInstaller` does not copy it and running the `exe` fails.

## Single container application 
To create single container application run the following command `PyInstaller --onefile main.py` where the `main.py` is the name of the file containing the main window definition. This command creates a large `exe` file containing all components of the application.

## Application and separate libraries

In Our case commands are:
* `PyInstaller --windowed studentPicture.py`
* `PyInstaller --windowed studentCard.py`

Building executables creates several files to `build` folder. The executable and necessary `dll` files can be found in the `dist` folder. Build settings can be found in a `.spec` file in the projects root directory.

:warning: When using QT UI recources which are not precompiled into python file you must copy resources like ui or picture files manually into `dist` folder. If you create modules they must reside in the libs folder of the virtual environment.

| File and path| Purpose |
|---|---|
dist\studentPicture\studentPicture.exe | Executable to run picture taking application
dist\studentPicture\studentPotrait.ui | Ui file manually copied to this folder
dist\studentCard\studentCard.exe | Executable to run card printing application
dist\studentCard\studentCardv2.ui |  Ui file manually copied to this folder
studentPicture.spec | Settings for building picture taking application
studentCard.spec | Settings for building picture taking application

If python console is needed it can be enabled by editing `spec` file and altering `exe = EXE()` block. Change console option to `console=True`

:warning: Windows Defender might claim that there is a trojan in the executable. This is a known false positive. Most of computers in the school have FSecure Safe as malware detection software. It does not give any alerts concerning the executable. Defender users may find this article useful: https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184.
