# Barcode branch

This branch is for developping tools for creating, showing and printing barcodes in the app. Basict barcode functionality is based on `python-barcode 0.13.1`. This shold be installed with pip prior using functions from the module `productBarcode.py`. Python-barcode is depending on `pillow` imaging library.  

## Installing dependencies

First update pip in the virtual environment. Type `pip install --upgrade pip` You might to do this twice due to a permission error.
`python-barcode 0.13.1` installation can be made to virtual environment by typing `pip install python-barcode` in the terminal. `pillow 9.1.0` can be installed by typing `pip install pillow` or typing `pip install --upgrade pillow`.

## Modules

The branch contains a single module with 2 functions to produce EAN or Code 128 barcodes.
Barcodes are SVG or PNG objects that have save() method for outputting files:

* barCode2Image creates barcode image from product ID or any legal EAN or Code 128 string.  
* setWriterOptions sets barcode dimensions

```python
# Using functions

# Set Writer options. A dictionary for the writer: height 5 mm, text 1 mm from barcode, fontsize 12
writerOptions = setWriterOptions(5,1,12)

# Product ID to encode
productid = 'Kotu-12345'
codeType = 'Code128'
pictureType = 'PNG'

# Create Code 128 barcode as png file
barCode = barCode2Image(productid, codeType, pictureType)

# Save it to a file with defined dimensios. Do not use extensions in names
barCode.save('Barcode', writerOptions)
```
