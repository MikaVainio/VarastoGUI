# Studentcard

This branch is for developping a stand alone GUI and an application to create and print student cards with a specialized card printer.

The GUI is designed as follows:

![image](https://user-images.githubusercontent.com/24242044/163401203-7d13ca9d-44e3-44b7-8f20-f05d487c44e2.png)

The User types the student number into text edit Opiskelijanumero (1). Student information is updated to labels (9) and bar code (12) is drawn at the bottom of the white preview frame (4). This area will be printed on the physical student card. When Hae Kuva (Load picture) Button is pressed the photograph of the student is shown in a label (8) which is inside a Raseko coloured frame (5). The frame is created by using Qlabel frame properties and styles. Logo (6) and some fixed information (7, 10) is allways shown on the card prewiew. Stripe (11) is coloured frame with a label. If all information and the photo is OK, user can print the card with Tulosta (Print) Button (3). When Opiskelijanumero (1) is being edited picture (8), bar code (12) and all dynamic labels (9) are cleared.

Previous picture is the original design. Some alterations has been made in the 2nd version `studentCardv2.ui`. There are some fields added so the user can type in student information. In the final version all font sizes should be carefully inspected. The size of the card is 86 x 54 mm. Propably RASEKO's VAT number and perhaps the course name are too small in that size.

![image](https://github.com/MikaVainio/VarastoGUI/blob/dev-studentcard/Opiskelijakorttisovellus.png)

This branch has 2 python files  and 2 versions of UI file and most current files are:

| Library or module | Purpose |
|---|---|
productBarcode.py | For generating and saving barcodes
studentCard.py | Applications main module
studentCardv2.ui | Current UI definitions for the app

Some image files are needed for logos and as placeholders.

* Omakuva2.png -> placeholder for student photo
* Raseko-logo-vaaka.png -> The logo of our school

