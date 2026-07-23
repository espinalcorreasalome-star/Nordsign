import cv2

class Camara:

    def __init__(self):
        self.cap = None
        self.activa = False

    def abrir(self, indice=0):
        if self.cap is None:
            self.cap = cv2.VideoCapture(indice)

            if self.cap.isOpened():
                self.activa= True
                return True
        return False

    def leer(self):
        if not self.activa:
            return None

        ok, frame = self.cap.read()

        if not ok:
            return None

        frame = cv2.flip(frame, 1)

        return frame

    def cerrar(self):
        if self.cap is not None:
            self.cap.release()
            self.cap= None

        self.activa = False
