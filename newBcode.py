# MODULE FOR CREATING CODE 128  BARCODES FOR LIBRE BARCODE 128 FONT

# Function for generating start symbol
def addStartCode(type='A', fontPosition='common'):

    """Creates a start character and its numerical value for checksum calculation

    Args:
        type (str, optional): Type of barcode Code 128, value can be A, B or C Defaults to 'A'
        fontPosition (str, optional): System to calculate ASCII or Unicode value: common, uncommon or barcodesoft. Defaults to 'common'

    Returns:
        tuple: numeric value of start symbol and charcter for the font
    """
    
    startCodeList = {'A' : 103, 'B' : 104, 'C' : 105}
    fontPositionList = {'common' : 100, 'uncommon' : 105, 'barcodesoft' : 145}
    numericValue = startCodeList.get(type)
    shiftValue = fontPositionList.get(fontPosition)
    character = chr(numericValue + shiftValue)
    data =  (numericValue, character)
    return data

# Function for generating stop symbol
def addStopCode(fontPosition='common'):
    """Creates a start character and its numerical value 
    Argument fontposition's default value is common

    Args:
        fontPosition (str, optional): System to calculate ASCII or Unicode value. Defaults to 'common'.

    Returns:
        tuple: numeric value of stop symbol and charcter for the font
    """
    fontPositionList = {'common' : 100, 'uncommon' : 105, 'barcodesoft' : 145}
    numericValue = 106 # Is allways 106
    shiftValue = fontPositionList.get(fontPosition)
    character = chr(numericValue + shiftValue)
    data =  (numericValue, character)
    return data

def encodeData(plainText, type='A', fontPosition='common'):
    """

    Args:
        plainText (_type_): _description_
        type (str, optional): Type of Code 128. Defaults to 'A'.
        fontPosition (str, optional): System to calculate ASCII or Unicode value. Defaults to 'common'.

    Returns:
        str: characters for the barcode font
    """
    startCodeList = {'A' : 103, 'B' : 104, 'C' : 105}
    fontPositionList = {'common' : 100, 'uncommon' : 105, 'barcodesoft' : 145}
    sumValue = 0
    charPosition = 0
    encodedString = ''
    for latinCharacter in plainText:
        charPosition += 1 
        print(charPosition)
        asciiValue = ord(latinCharacter)
        if asciiValue < 127:
            barCodeValue = asciiValue #- 32
               
        else:
            barCodeValue = asciiValue - fontPositionList.get(fontPosition)
        encodedChar = chr(barCodeValue)
        sumValue += charPosition * barCodeValue
        print('painotettu arvo on', sumValue)
        encodedString += encodedChar
     
    data = (sumValue, encodedString)
    return data

def text2barcode(plainText, type='A', fontPosition='common'):
    """Creates whole text for the barcode font. Contains start, data, checksum and stop portions

    Args:
        plainText (str): Text to encode into Code 128 barcode
        type (str, optional): Type of Code 128. Defaults to 'A'.
        fontPosition (str, optional): System to calculate ASCII or Unicode value. Defaults to 'common'.

    Returns:
        str: A text for barcode font
    """
    fontPositionList = {'common' : 100, 'uncommon' : 105, 'barcodesoft' : 145}
    # Create the check sum for a barcode
    startSum = addStartCode(type, fontPosition)[0]
    textSum = encodeData(plainText, type, fontPosition)[0]
    checkSum = (startSum + textSum) % 103 # Checksum is the reminder when divided by 103 -> Mod operator
    if checkSum < 95:
        print('muuttamaton varmistussumma on', checkSum)
        checkSum += 32
    else:
        checkSum += fontPositionList.get(fontPosition)
    print('varmistussumma on', checkSum) 
    # Build a string to print the barcode
    startMark = addStartCode(type, fontPosition)[1]
    textPart = encodeData(plainText, type, fontPosition)[1]
    checkSumMark = chr(checkSum)
    stopMark = addStopCode(fontPosition)[1]
    barcode = startMark + textPart + checkSumMark + stopMark
    return barcode 

if __name__ == '__main__':

    barcode = text2barcode('PJJ123C','B', 'common')
    print('Ja viivakoodi on', barcode)