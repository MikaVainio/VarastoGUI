# Mainwindow branch
This branch is for developping the main window with QT Designer. It consist of 2 files `lendApp.ui` and `lendApp.py`.

## Default tab 
When user opens the app the following window appears:

![Sovelluksen oletussivu](https://github.com/MikaVainio/VarastoGUI/blob/dev-mainwindow/docs/pictures/DefaultPage.png)

On top of the window there is a Menubar (1)and tabs for different tasks (2). Lainaus (Lending) page is opened by default. User chooses the transaction type from Tapahtuma (Transaction) ComboBox (3). This populates Varastosta (from Warehouse) (4) and Varastoon (to Warehouse) (5) fields. Student id Asiakasnumero (6) is read from student cards barcode with barcode reader. Asiakkaan nimi (Client name) (7) is populated according to Studen id from the database. Tuotekoodi (Product id) (8) is read with barcodereader and Product information is retrieved from the database and shown in Nimike (Product Name) (9), Tuotekuva (Product Image) (10) fields. Yksikkö (Unit) field (11) is also updated. User enters the amount into Määrä field (12). Tapahtumapäivä (Transaction date) is automatically updated (13). Palautuspäivä (Date of return) is entered by the user (14), default is the same day. A Calendar Control is for convience of checking  dates, week numbers or week days (15). Transaction is commited with Tallenna (Save) button (17). A receipt can be printed with Kuitti button (18). Every transaction has UUID shown at the bottom of the window (16).
