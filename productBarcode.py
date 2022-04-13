# Reguires Pillow library to be installed to work correctly

# LIBRARIES AND MODULES TO IMPORT

# Code 128 
from barcode import Code128

# ImageWriter to generate an image file
from barcode.writer import ImageWriter

# Product ID to encode
productid = 'Kotu-12345'

# Create Code 128 barcode with checksum default PNG file in RGB color space
barCode = Code128(productid, writer=ImageWriter())

# Save it as png file
barCode.save('BcodePNG')