#!/usr/bin/env python3

# coding: utf-8
if __name__ == '__main__':
    # fullscreen
    from kivy.config import Config
    Config.set('graphics', 'fullscreen', 'auto')


import cv2
import numpy as np
from imutils import face_utils, paths
from imutils.object_detection import non_max_suppression
from imutils.video import FPS, WebcamVideoStream
from kivy.app import App
from kivy.clock import Clock

from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from skimage.draw import circle

from kivy.metrics import *

import dlib

Builder.load_file('faceDetect.kv')


class KivyCamera(Image):
    circle_pos = ListProperty([0, 0])
    # circle_y = NumericProperty(0)
    circle_r = NumericProperty(0)
    rect_pos = ListProperty([0, 0])
    coords_left = ListProperty()
    coords_bottom = ListProperty()
    coords_right = ListProperty()
    coords_top = ListProperty()
    widths = ListProperty()


    def __init__(self,  **kwargs):
        super(KivyCamera, self).__init__(**kwargs)

    def start(self):
        # self.videostream = capture
        self.videostream = WebcamVideoStream(0).start()
        # Clock.schedule_interval(self.update, 1.0/30)
        print("starting video capture")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            "shape_predictor_68_face_landmarks.dat")

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}



    def morphology_transform(self, img, morph_operator=2, element=1, ksize=18):
        morph_op_dic = {0: cv2.MORPH_OPEN, 1: cv2.MORPH_CLOSE,
                        2: cv2.MORPH_GRADIENT, 3: cv2.MORPH_TOPHAT, 4: cv2.MORPH_BLACKHAT}

        if element == 0:
            morph_elem = cv2.MORPH_RECT
        elif element == 1:
            morph_elem = cv2.MORPH_CROSS
        elif element == 2:
            morph_elem = cv2.MORPH_ELLIPSE

        elem = cv2.getStructuringElement(morph_elem,
                                         (2 * ksize + 1, 2 * ksize + 1),
                                         (ksize, ksize))
        operation = morph_op_dic[morph_operator]
        dst = cv2.morphologyEx(img, operation, elem)

        return dst

    # https://blog.kivy.org/2014/01/positionsize-of-widgets-in-kivy/
    def ring_pos(self, *args):
        pass

    def ring_size(self, *args):
        pass

    def update(self, dt):
        frame = self.videostream.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #
        # print("color depth: {}".format(gray.dtype))
        # keep all 3 channels:
        # gray = np.dstack([gray, gray, gray])
        faces = self.detector(gray, 1)
        morphed_frame = self.morphology_transform(frame.copy())
        # print("shape morphed frame {}".format(morphed_frame.shape))
        # print("shape frame {}".format(frame.shape))

        #  (1024, 1280, 3) 583, 778  1.756, 1.645   0.52539, 0,6078125
        self.coords_lb = []
        self.coords_tr = []
        self.widths = []

        for (i, face) in enumerate(faces):
            # shape = self.predictor(gray, face)
            # shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(face)
            # for (x, y) in shape:
            #     cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            self.circle_r = (w + w / 2)/2
            self.rect_pos = [face.right()/2, face.top()/2]
            circle_x = (x + w / 2)
            circle_y = (y + h / 2)

            rr, cc = circle(circle_y, circle_x, self.circle_r, morphed_frame.shape)
            morphed_frame[rr, cc] = frame[rr, cc]
            # morphed_frame[rr, cc] = frame[rr, cc]


            # http://robertour.com/2013/07/19/10-things-you-should-know-about-the-kivy-canvas/
            # https://blog.kivy.org/2014/01/positionsize-of-widgets-in-kivy/

            cx = dp(circle_x+self.circle_r)  #
            cy = dp(circle_y-self.circle_r)  # /2-self.circle_r



            self.circle_r = dp(self.circle_r)  # face_img = frame[y:y+h, x:x+w]
            # face_img = self.morphology_transform(face_img)
            # morphed_frame[y:y+h, x:x+w] = face_img

            # frame = face_utils.visualize_facial_landmarks(morphed_frame, shape)

        # if not faces:
        self.coords_left = [frame.shape[1] - face.left() for face in faces]
        self.coords_bottom=[(frame.shape[0] - face.bottom()) for face in faces]
        self.coords_right = [frame.shape[1] - face.right() for face in faces]
        self.coords_top = [frame.shape[0] - face.top() for face in faces]
        self.widths= [face.width() for face in faces]

        # convert to texture
        # buf1 = cv2.flip(frame, 1)
        buf1 = cv2.flip(morphed_frame, -1)
        # buf1 = morphed_frame
        buf = buf1.tostring()

        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='bgr'
        )
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display img
        self.texture = image_texture

        # self.fps.update()
        # self.f += 1
    def stop(self):
        print("stopping video capture")
        self.videostream.stop()

    # def on_touch_down(self, touch):
    #     print("KivyCamera touched at {}".format(touch.pos))
    #     return super(KivyCamera, self).on_touch_down(touch)


class Rings(Widget):
    radius = NumericProperty(10)
    height = NumericProperty(0)
    update_pos = True

    # def update(self, vals):
    #
    #     if self.update_pos:
    #         self.pos, self.radius = vals
    #         self.pos = self.pos[0] - self.radius, self.pos[1] - self.radius
    #         # self.pos = [Window.width - self.pos[0],
    #                       Window.height - self.pos[1]]
    #         print("circle in rings: {}".format(self.pos))


class CameraScreen(Widget):

    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)

        print("win size: {}".format((Window.width, Window.height)))

        self.fps = FPS().start()
        self.cam = KivyCamera( size=(778, 583),
                              center_x=Window.width/2,
                              center_y=Window.height/2)
        self.cam.start()
        print("facedect.py camscreen init")
        Clock.schedule_interval(self.update, 1.0 / 30)

        self.add_widget(self.cam)
        self.rect = Rings()
        self.add_widget(self.rect)


    def update(self, dt):
        # print("screen ids: {}".format(self.ids))
        self.cam.update(dt)
        if self.cam.widths:
            for i in range(len(self.cam.widths)):
                self.rect.pos = (self.cam.x + self.cam.coords_left[i], self.cam.y + self.cam.coords_bottom[i])
                self.rect.height = self.cam.widths[i]
                # self.add_widget(ring)

    def destroy(self):
        self.cam.stop()


class CamApp(App):
    def build(self):
        self.screen = CameraScreen()
        return self.screen

    def on_stop(self):
        self.screen.destroy()


if __name__ == '__main__':
    CamApp().run()
