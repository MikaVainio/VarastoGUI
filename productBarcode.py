# MODULE FOR CREATING AND SCALING EAN AND CODE 128 BARCODE IMAGES
# ---------------------------------------------------------------

# LIBRARIES AND MODULES TO IMPORT

# Code 128 and EAN
from barcode import Code128, ean

# Writers to generate an image files. ImageWriter produces png and jpg files
from barcode.writer import ImageWriter, SVGWriter

# FUNCTIONS

# Function that creates code 128 or EAN code and returns it as PNG or SVG image


def barCode2Image(productId, codeType='Code128', pictureType='PNG'):
    """Creates image of barcode from a string. Funtion supports Code 128 and EAN 13

    Args:
        productId (str): String which will be encoded into a barcode
        codeType (str, optional): Type of the barcode. Defaults to 'Code128'.
        pictureType (str, optional): Type of image. Defaults to 'PNG'.

    Returns:
        object: image object
    """
    # Create a PNG file
    if pictureType == 'PNG':

        # Check the barcode type
        if codeType == 'Code128':

            # Create Code 128 barcode in RGB Color space (no transparency)
            bCodeImage = Code128(
                productId, writer=ImageWriter(pictureType, 'RGB'))
        else:
            # Create EAN 13 barcode in RGB Colour space
            bCodeImage = ean.EuropeanArticleNumber13(
                productId, writer=ImageWriter(pictureType, 'RGB'), no_checksum=False)

    # Create a SVG file
    else:
        # Check the barcode type
        if codeType == 'Code128':

            # Create Code 128 barcode
            bCodeImage = Code128(productId, writer=SVGWriter())
        else:
            # Create EAN 13 barcode
            bCodeImage = ean.EuropeanArticleNumber13(
                productId, writer=SVGWriter, no_checksum=False)

    return bCodeImage

# Function to define barcode dimensions and the font size
def setWriterOptions(height=7, textDistance=2, fontSize=10):
    """Creates a dictionary for pyhton-barcode Writer

    Args:
        height (int, optional): Height of the barcode in mm. Defaults to 7.
        textDistance (int, optional): Distance between bars and plain text presentation in mm. Defaults to 2.
        fontSize (int, optional): Size of the plain text in pt. Defaults to 10.

    Returns:
        dict: Barcode Writer Options 
    """
    writerOptions = {'module_height' : height, 'text_distance' : textDistance, 'font_size' : fontSize}
    return writerOptions


# Some Quick Tests
if __name__ == '__main__':

    # Product ID to encode
    productid = 'Kotu-12345'
    codeType = 'Code128'
    pictureType = 'SVG'

    # Set Writer options. A dictionary values for the writer: height 5 mm, margin to text 1mm, text size 12 pt
    writerOptions = setWriterOptions(5,1,12)
    
    # Create Code 128 barcode as png file
    barCode = barCode2Image(productid, codeType, pictureType)

    # Save the file
    barCode.save('Barcode' + pictureType, writerOptions)
