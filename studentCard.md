# Studentcard

This branch is for developping a stand alone GUI and an application for creating and printing student cards with a specialized card printer.

The GUI is designed as follows:

![image](https://user-images.githubusercontent.com/24242044/168024179-dd738592-da38-4d0a-9417-b1ce5f71ecee.png)

The User types a student number into text edit Opiskelijanumero (1). Student information is updated to labels (9) and bar code (12) is drawn at the bottom of the white preview frame (4). This area will be printed on the physical student card. When Hae Kuva (Load picture) Button (2) is pressed the photograph of the student is shown in a label (8) which is inside a Raseko coloured frame (5). The frame is created by using Qlabel frame properties and styles. Logo (6) and some fixed information (7, 10) is allways shown on the card prewiew. Stripe (11) is coloured frame with a label. If all information and the photo is OK, user can print the card with Tulosta (Print) Button (3). When Opiskelijanumero (1) is being edited picture (8), bar code (12) and all dynamic labels (9) are cleared.

Previous picture is the original design. Some alterations has been made in the 2nd version studentCardv2.ui. There are some fields added so the user can type in all necessary student information. Hae Kuva button (2) opens a file dialog for choosing a photograph of the student. In the 1st version intention was to retrieve picture from a dabase but there is no need to store student pictures in the database. Only minimum of personal informatios will be stored (student ID, name, responsible instructor's email address and class name) Class name is not printed to student card.

In the final version all font sizes should be carefully inspected. The size of the card is 86 x 54 mm. Propably RASEKO's VAT number and perhaps the course name are too small in that size. Printing can be done with high resolution or normal printer settings. When high resolution printing is used the size of preview frame (# 4 in the first picture) must be scaled approximately 2.5 times for correct print size. If normal printing is used scaling factor is 0.3. Final values depend on resolutions of the monitor and the card printer. Typically the monitor resolution is 96 dpi and the printing resolution 300 dpi.

In the 2nd version all dynamic labels are bound to line edit elements by QTSignals. Singnals and slots are created graphically in the QTEditor. Both buttons have dedicated slots defined in the code using `openPicture(self)` and `printCard(self)` functions. Barcode is generated alfter user has pressed the Hae Kuva button. This button is activated when there is a student number in the line edit. After printing student's personal information is cleared. Season and study information is kept for next student card to be created.

![image](https://user-images.githubusercontent.com/24242044/168024527-d5bbd408-cdee-4e93-9e60-8cba515e9fc5.png)

This branch has 3 python files and 2 ui files. Most current files are:

| Library or module | Purpose |
|---|---|
code128Bcode.py |	For generating barcodes with Libre 128 Barcode font, included in studentCardv2.py
studentCardv2.py |	Applications main module, contains function in code128Bcode.py
studentCardv2.ui |	Current UI definitions for the app
studentPicture.py |	A small application for taking photos for the student card
studentPicture.ui | UI for the photo taking application

Some image files are needed for logos and as placeholders.

* Omakuva2.png -> placeholder for student photo
* Raseko-logo-vaaka.png -> The logo of our school

## Distribution
For distributing applications we need the `PyInstaller` library. It can be installed into the virtual environment `pip install PyInstaller`. Applications for this branch use quite many external libraries so it is not vise to distiribute the application in single standalone exe file. With separate `dll` link libraries the file size of the exe's file size is much smaller thus there are many files in the distribution directory. When creating an application with a separate ui file it is essential to copy manually the ui file into dist folder. PyInstaller does not copy it and running the exe fails. When build first time the `.specfile` of the current build is created. Additional files can be added to the `datas` section of this file for next time builds. The following example is from `studentCardv2.spec`. Successfull build needs the ui file studentCardv2.ui, placeholder picture omakuva2.png and the logo of Raseko Raseko-Logo-vaaka.png. The datas section is a list of tupplets. A tupplet contains a filename and the destination folder in the `dist` folder. Root of the dist folder is `.`.
```
a = Analysis(
    ['studentCardv2.py'],
    pathex=[],
    binaries=[],
    datas=[('studentCardv2.ui', '.'), ('omakuva2.png', '.'), ('Raseko-Logo-vaaka.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```

## Single container application

To create single container application run the following command PyInstaller --onefile main.py where the main.py is the name of the file containing the main window definition. This command creates a large exe file containing all components of the application.

## Application and separate libraries
In Our case commands are:
```
PyInstaller --windowed studentPicture.py
PyInstaller --windowed studentCardv2.py
```
Building executables creates several files to `build` folder. The executable and necessary dll files can be found in the `dist` folder. Build settings can be found in a `.spec` file in the projects root directory. It is handy to give build commands without `--windowed` argument. Then you have Python console for debugging. When everything works as expected we can edit the `.spec` file and set `console=False` in the `EXE` part of the file.

⚠️ When using QT UI recources which are not precompiled into python file you must copy resources like ui or picture files manually into `dist` folder in the first build of your application. If you create modules they must either reside in the `libs` folder of the virtual environment or you must add your own python modules into the `.spec` file to copy them automatically during the build process. Alfter 1st build you can edit the created `.spec` file. When you have a `.spec` file you can build with command `PyInstaller studentPicture.spec` or what ever is your build specification file.

File and path |	Purpose
|---|---|
dist\studentPicture\studentPicture.exe |	Executable to run picture taking application
dist\studentPicture\studentPotrait.ui |	Ui file manually copied to this folder
dist\studentCardv2\studentCardv2.exe |	Executable to run card printing application
dist\studentCardv2\studentCardv2.ui |	Ui file manually copied to this folder
studentPicture.spec	| Settings for building picture taking application
studentCardv2.spec | Settings for building picture taking application

If python console is needed it can be enabled by editing `.spec` file and altering `exe = EXE()` block. Change console option to `console=True`.

⚠️ Windows Defender might claim that there is a trojan in the executable. This is a known false positive. Most of computers in the school have FSecure Safe as malware detection software. It does not give any alerts concerning the executable. Defender users may find this article useful: https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184.

## Spec files
`.spec` files are ignored by git. Full build specifications are as follows:

### studentPicture.exe

Build specification file `studentPicture.spec` contains instructions below:
```
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['studentPicture.py'],
    pathex=[],
    binaries=[],
    datas=[('studentPicture.ui', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='studentPicture',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='studentPicture',
)

```

### studentCardv2.exe

Build specification file `studentCardv2.spec` contains instructions below:

```
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['studentCardv2.py'],
    pathex=[],
    binaries=[],
    datas=[('studentCardv2.ui', '.'), ('omakuva2.png', '.'), ('Raseko-Logo-vaaka.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='studentCardv2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='studentCardv2',
)

```

## Installer
Applications can be distributed with or without an installer. When used without an installer contents of the distribution folder are copied to the other computer. Some of the files are shown in the picture below:

![image](https://user-images.githubusercontent.com/24242044/168031298-51e47538-b4a7-4a97-9837-cc349822a9e7.png)

Distribution can be made with zipped folder containing installation instructions and contents of the distribution folder. Creating an installer is more sophisticated way of delivering the application to a client. Free installer building application is **InstallForge**. You can load it from https://installforge.net/download/. There is a nice tutorial at https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/ about using `PyInstaller` and `InstallForge` It is essential to add instructions for installing **Libre Code 128** font from Goolgle. Font can be found at https://fonts.google.com/specimen/Libre+Barcode+128+Text.

