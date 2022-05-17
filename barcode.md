# Barcode branch

This branch is for developping tools to create, show and print barcodes in the app. Due to design flaws in the previously used Python-barcode library a new custom made module was created. At the moment all barcodes are created with **Libre Code128 barcode** font. Module creates appropriate letters for the font and calculates the checksum needed by the wands verifying algorithm. Module contains a single function `string2barcode()` to create a string for the barcode font. All three variations of the Code128 (A, B and C) are supported. User can also choose how letters are chosen according to 3 differenc schemes: common, uncommon or barcodesoft. For more information check the following article https://en.wikipedia.org/wiki/Code_128. 

## Generating barcodes
`string2barcode()` function defauts to code128 B type of barcode using common character set.
The function can be used as follows:

```Python
# With all arguments
string2barcode('Kotu-12345', 'B', 'common')

# Or with a single argument
string2barcode('Kotu-12345')

```
When using a wand like USB barcode reader device user must set reader to use national characters (Zebex Z 3100: Suomenkieliset merkit). This setting is made with a barcode on the leaflet found in the packade of the wand. Codes for progrmanning the wand can also be found on the manufacturers web site https://www.zebex.com/en/support/download/?tid=0&pid=10.



