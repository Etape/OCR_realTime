
from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#pointe sur l'application d'extraction de texte


#fonction de traitement des trames d'images
def ocr_core(filename):
    try:
        text = pytesseract.image_to_string(Image.open(
            filename))  # on utilise Pillow pour ouvrir l'image et pytesseract pour detecter des textes
        return text  # puis on affiche l'image
    except Exception as e:
        return str(e)
