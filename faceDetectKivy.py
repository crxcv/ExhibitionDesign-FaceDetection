# coding: utf-8

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

import dlib






# class MainWindow(FloatLayout):
#     pass


class KivyCamera(Image):
    circle_pos = ListProperty([0, 0])
    # circle_y = NumericProperty(0)
    circle_r = NumericProperty(0)
    # videostream = ObjectProperty(None)

    def __init__(self,  **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        # self.videostream = capture
        self.videostream = WebcamVideoStream().start()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            "shape_predictor_68_face_landmarks.dat")

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Clock.schedule_interval(self.update, 1.0/fps)

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

    # def get_circle_vals(self):
    #     # vals = [self.to_parent(self.circle_y, self.circle_x), self.circle_r]
    #     vals = [[self.circle_y, self.circle_x], self.circle_r]
    #     print("circle vals in KvCam: {}".format(vals))
    #     print("circle toparent in KvCam: {}".format(
    #         self.to_parent(self.circle_y, self.circle_x)))
    #     return vals

    def update(self):
        frame = self.videostream.read()
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # keep all 3 channels:
        # gray = np.dstack([gray, gray, gray])
        faces = self.detector(gray, 1)
        morphed_frame = self.morphology_transform(frame.copy())

        for (i, face) in enumerate(faces):
            # shape = self.predictor(gray, face)
            # shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(face)
            # for (x, y) in shape:
            #     cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            self.circle_r = (w + w / 2) / 2
            circle_x = x + w / 2
            circle_y = y + h / 2

            rr, cc = circle(circle_y, circle_x, self.circle_r, frame.shape)
            morphed_frame[rr, cc] = frame[rr, cc]

            # x, y: 132, 116
            # cx, cy: 209.5, 193.0
            # cx/y parent: (209.5, 193.0)
            # cx/y to window: (209.5, 193.0)
            # x, y: 153, 139
            # x, y widget (153, 139)
            # cx, cy: 217.5, 203.5
            # cx/y parent: (217.5, 203.5)
            # cx/y to window: (217.5, 203.5)
            # x, y: 150, 116
            # x, y widget (150, 116)
            # cx, cy: 227.0, 193.0
            # cx/y parent: (227.0, 193.0)
            # cx/y to window: (227.0, 193.0)

            # x, y: 440, 239
            # x, y widget (440, 239)
            # cx, cy: 504.5, 303.5
            # cx/y parent: (504.5, 303.5)
            # cx/y to window: (504.5, 30
            # this works, circle a few px under face
            # c_pos = self.to_window((x+w/2), y+h)
            # self.circle_pos = self.to_window(frame.shape[1] - circle_x, frame.shape[0] - circle_y)
            self.circle_pos = self.to_window(x+w/2-self.circle_r, y+w/2+self.circle_r)
            print("x, y: {}, {}\nx, y widget {}\ncx, cy: {}, {}\ncx/y parent: {}\ncx/y to window: {}".format(x, y, self.to_widget(x, y), circle_x, circle_y, self.to_parent(circle_x, circle_y), self.to_window(circle_x, circle_y)))
            # face_img = frame[y:y+h, x:x+w]
            # face_img = self.morphology_transform(face_img)
            # morphed_frame[y:y+h, x:x+w] = face_img

            # frame = face_utils.visualize_facial_landmarks(morphed_frame, shape)

        # if not faces:

        # convert to texture
        # buf1 = cv2.flip(frame, 1)
        # buf1 = cv2.flip(morphed_frame, -1)

        buf = morphed_frame.tostring()
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
    def stop(self):
        self.videostream.stop()


class Rings(Widget):
    radius = NumericProperty(10)
    update_pos = True

    # def update(self, vals):
    #
    #     if self.update_pos:
    #         self.pos, self.radius = vals
    #         self.pos = self.pos[0] - self.radius, self.pos[1] - self.radius
    #         # self.pos = [Window.width - self.pos[0],
    #                       Window.height - self.pos[1]]
    #         print("circle in rings: {}".format(self.pos))


class Screen(FloatLayout):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.fps = FPS().start()

        Clock.schedule_interval(self.update, 1.0 / 30)

    def update(self, dt):
        # print("screen ids: {}".format(self.ids))
        self.ids.cam.update()

    def destroy(self):
        self.ids.cam.stop()


class CamApp(App):
    def build(self):
        self.screen = Screen()
        return self.screen

    def on_stop(self):
        self.screen.destroy()


if __name__ == '__main__':
    CamApp().run()
