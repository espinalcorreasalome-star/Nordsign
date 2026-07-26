import cv2

class Camara:

    def __init__(self):
        self.cap = None
        self.activa = False

    def abrir(self, indice=0):
        if self.activa:
            return True
        
        if self.cap is not None:
            self.cerrar()

        self.cap = cv2.VideoCapture(
            indice,
            cv2.CAP_DSHOW
        )

        if not self.cap.isOpened():
                self.cap.release()
                self.cap= None
                self.activa= False
                return False
        
        self.activa= True
        return True

    def leer(self):
        if(
             not self.activa
             or self.cap is None
             or not self.cap.isOpened()
        ):
            return None

        ok, frame = self.cap.read()

        if not ok or frame is None :
            return None

        frame = cv2.flip(frame, 1)

        return frame

    def cerrar(self):
        if self.cap is not None:
            self.cap.release()
            self.cap= None

        self.activa = False

