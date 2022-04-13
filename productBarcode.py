# MODULE FOR CREATING AND SCALING EAN AND CODE 128 BARCODE IMAGES
# ---------------------------------------------------------------

# LIBRARIES AND MODULES TO IMPORT

# Code 128 and EAN
from barcode import Code128, ean

# ImageWriter to generate an image file
from barcode.writer import ImageWriter

# FUNCTIONS

# Function that creates code 128 or EAN code and returns it as PNG or SVG image
def barCode2Image(productId, codeType='Code128', pictureType='PNG'):
    """Creates image of barcode from a string

    Args:
        productId (str): String which will be encoded into a barcode
        codeType (str, optional): Type of the barcode. Defaults to 'Code128'.
        pictureType (str, optional): Type of image. Defaults to 'PNG'.

    Returns:
        object: image object
    """
    bCodeImage = Code128(productId, writer=ImageWriter(format=pictureType))
    return bCodeImage

# Some Quick Tests
if __name__ == '__main__':

    # Product ID to encode
    productid = 'Kotu-12345'

    # Create Code 128 barcode with checksum default PNG file in RGB color space
    barCode = Code128(productid, writer=ImageWriter())

    # Save it as png file
    barCode.save('BcodePNG')