from flask import Response
from flask import Flask
from flask import render_template

try:
    from PIL import Image
except:
    import Image

import pytesseract
import cv2
import threading

outputFrame = None
lock = threading.Lock()
app = Flask(__name__)

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

#generation des trames pour les captures video (streaming)
def gen_frames():
    txt = ""
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        (success, frame1) = camera.read()
        frame = frame1
        with lock:
            if not success:
                continue
            else:
                file = 'live.png'
                cv2.imwrite(file, frame)
                txt = ocr_core(file)
                if len(txt)!= 0:
                    print(txt)
                (ret, jpeg) = cv2.imencode('.jpg', frame1)
                cv2.imshow('frame', frame)
                frame1 = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'\Content-Type: image/jpeg\r\n\r\n'
                       + bytearray(frame1)
                       + b'\r\n\r\n')

#page d'accueil
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

#gestion des erreurs de serveur Flask
@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return str(err), 500


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    # si le serveur Flask est lancé, on lance l'app
    app.run(debug=True)
    camera.stop()
