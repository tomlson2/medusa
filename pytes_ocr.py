from PIL import Image
import cv2 as cv
import pytesseract



def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\tomls\\AppData\\Local\\Programs\\Python\\Python38\\Scripts\\pytesseract.exe'
    im = Image.open(filename)

    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


# im = cv.imread('tesseract\\logs.png')

# im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)





print(ocr_core('tesseract\\logs.png'))

