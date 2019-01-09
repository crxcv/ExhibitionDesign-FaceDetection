from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from imutils import face_utils
import numpy as np
import cv2
import dlib

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.videostream = capture
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        Clock.schedule_interval(self.update, 1.0/fps)

    def morphology_transform(self, img, morph_operator=4, element=2, ksize=12):
        morph_op_dic = {0: cv2.MORPH_OPEN, 1: cv2.MORPH_CLOSE, 2: cv2.MORPH_GRADIENT, 3: cv2.MORPH_TOPHAT, 4: cv2.MORPH_BLACKHAT}

        if element == 0:
            morph_elem = cv2.MORPH_RECT
        elif element == 1:
            morph_elem = cv2.MORPH_CROSS
        elif element == 2:
            morph_elem = cv2.MORPH_ELLIPSE

        elem = cv2.getStructuringElement(morph_elem, (2 * ksize + 1, 2* ksize + 1), (ksize, ksize))
        operation = morph_op_dic[morph_operator]
        dst = cv2.morphologyEx(img, operation, elem)

        return dst


    def update(self, dt):
        frame = self.videostream.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # keep all 3 channels:
        gray = np.dstack([gray, gray, gray])

        faces = self.detector(gray, 1)

        morphed_frame = self.morphology_transform(frame.copy())

        for (i, face) in enumerate(faces):
            # shape = self.predictor(gray, face)
            # shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(face)
            # for (x, y) in shape:
            #     cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            face_img = morphed_frame[y:y+h, x:x+w]
            # face_img = self.morphology_transform(face_img)
            frame[y:y+h, x:x+w] = face_img

            # frame = face_utils.visualize_facial_landmarks(morphed_frame, shape)

        # convert to texture
        buf1 = cv2.flip(frame, -1)
        # buf1 = cv2.flip(frame, 1)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='bgr'
        )
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display img
        self.texture = image_texture
        # self.fps.update()


class CamApp(App):
    def build(self):
        self.videostream = WebcamVideoStream().start()
        # self.fps = FPS().start()
        self.camera = KivyCamera(capture=self.videostream, fps=30)
        return self.camera

    def on_stop(self):
        self.videostream.stop()

if __name__ == '__main__':
    CamApp().run()
