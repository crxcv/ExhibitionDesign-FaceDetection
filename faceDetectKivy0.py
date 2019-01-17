# coding: utf-8

# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.lang import Builder

from kivy.core.window import Window
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter


from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from imutils import face_utils
import numpy as np
import cv2
import dlib

from skimage.draw import circle
from imutils.object_detection import non_max_suppression
from imutils import paths

Builder.load_file('faceDetect.kv')
# Builder.load_string('''
# <MainWindow>
#     orientation: 'vertical'
#     ActionBar:
#         id: actBar
#         pos_hint: {'top':1}
#         Slider:
#             id: Opera
# ''')
#
# class MainWindow(FloatLayout):
#     pass



class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.videostream = capture
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Clock.schedule_interval(self.update, 1.0/fps)





    def morphology_transform(self, img, morph_operator=2, element=1, ksize=18):
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

            r = (w + w/2) / 2
            c_y = x + w/2
            c_x = y + h/2

            rr, cc = circle(c_x, c_y, r, frame.shape)
            morphed_frame[rr, cc] = frame[rr, cc]

            # face_img = frame[y:y+h, x:x+w]
            # face_img = self.morphology_transform(face_img)
            # morphed_frame[y:y+h, x:x+w] = face_img

            # frame = face_utils.visualize_facial_landmarks(morphed_frame, shape)

        # if not faces:

        # convert to texture
        buf1 = cv2.flip(morphed_frame, -1)
        # buf1 = cv2.flip(frame, 1)
        buf = buf1.tostring()
        # if self.f < 1:
        #     print("type buf1: {}".format(type(buf1)))
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='bgr'
        )
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display img
        self.texture = image_texture
        # self.fps.update()
        # self.f += 1

class Rings(Scatter):
    diameter = NumericProperty(10)

    def update(self, pos_x, pos_y, dia_x):
        self.pos = [pos_x, pos_y]
        self.diameter = dia_x

class Screen(FloatLayout):
        def __init__(self):
            super(FloatLayout, self).__init__(**kwargs)
            self.videostream = WebcamVideoStream().start()
            # self.fps = FPS().start()
            self.camera = KivyCamera(capture=self.videostream, fps=30)

            Clock.schedule_interval(self.update, 1.0/fps)

        def update(self):
            


        def destroy(self):
            self.videostream.stop()

class CamApp(App):
    # def build_config(self, config):
    #     config.set_defaults('section1', {
    #         'key1': 'val1',
    #         'key2': 'val2'
    #     })

    def build(self):
        # self.videostream = WebcamVideoStream().start()
        # # self.fps = FPS().start()
        # self.camera = KivyCamera(capture=self.videostream, fps=30)
        self.screen = Screen()
        return self.screen

    def on_stop(self):
        # self.videostream.Screen()
        self.screen.destroy()
if __name__ == '__main__':
    CamApp().run()
