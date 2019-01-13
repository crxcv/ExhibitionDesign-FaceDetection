# coding: utf-8

# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.graphics import *

from kivy.app import App
from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatter import Scatter
from kivy.graphics import Rectangle

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.core.window import Window
from kivy.properties import ObjectProperty, ListProperty, StringProperty

import cv2
import dlib
import numpy as np
import time

import warnings

from skimage import img_as_float, img_as_int, img_as_uint, img_as_ubyte

Builder.load_file('edge_detect_ani.kv')

class Picture(Scatter):
    texture = ObjectProperty(None)
    name = StringProperty("")


class Root(Widget):
    img = cv2.imread('images/orig.JPEG')
    img = cv2.flip(img, 0)
    print("shape: {}".format(img.shape))
    # img = cv2.resize(img, None, fx=0.7, fy=0.7)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.medianBlur(grey, 11)
    sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)

    angle = np.arctan2(sobely, sobelx) * (180 / np.pi)
    # angle = np.absolute(angle)
    angle = np.uint8(angle)

    mag = np.sqrt(sobelx**2.0 + sobely**2.0)
    mag = np.absolute(mag)
    mag = np.uint8(mag)

    sobelx = np.absolute(sobelx)
    sobelx = np.uint8(sobelx)
    # sobelx = 255 - sobelx
    sobely = np.absolute(sobely)
    sobely = np.uint8(sobely)
    # sobely = 255 - sobely

    img_blur = cv2.GaussianBlur(grey, (5, 5), 0)

    pos_y = ObjectProperty(int(Window.height/2))
    pos_x = ObjectProperty(Window.width/3)
    orig_size = ListProperty((img.shape[1], img.shape[0]))
    win_width = ObjectProperty(Window.width)
    win_height = ObjectProperty( Window.height)
    scale = ObjectProperty(2)

    grabbed = {}

    pic_pos = ObjectProperty([10, Window.height/2])
    blur_pos = ObjectProperty([10, 10])
    rect_pos = ObjectProperty([10, 10])
    rect_size = ObjectProperty([0, 0])
    rect_h = ObjectProperty(0)
    rect_w = ObjectProperty(0)

    def get_pos(self):
        return self.rect_pos[0], se

    def check_pos(self, *args):
        img_pos, img_scale, img_size, stenc_pos = [i for i in args]
        print("check pos {}".format(args))
        self.scale = img_scale

        self.rect_size = [i * 1/img_scale for i in img_size]

        # p = img_pos - tuple(stenc_pos) #
        print("p: {}, {}".format(img_pos[0] - stenc_pos[0], img_pos[1] - stenc_pos[1]))
        p = [stenc_pos[0] - img_pos[0], stenc_pos[1] - img_pos[1]]  # [i-j for i, j in (img_pos, stenc_pos)]# tuple((img_pos[0] - stenc_pos[0], img_pos[1] - stenc_pos[1]))
        self.rect_pos= [i * 1/img_scale for i in p]
        # self.rect_pos = [self.blur_pos[0] + self.rect_pos[0], self.blur_pos[1] + self.rect_pos[1]]  # [i + j for i, j in (self.blur_pos, self.rect_pos)]

        print("rect pos, size; {}, {}".format(self.rect_pos, self.rect_size))



    def on_touch_down(self, touch):
        # print("id: {},  type: {}".format(self.id, type(self)))
        # # print("siblings: {}".format(self.parent.children))
        # print("children: {}".format(self.children))
        # print("ids: {}".format(self.ids))
        if self.ids['stenc_blur'].collide_point(*touch.pos):
            touch.grab(self)
            touch.grabbed = self.ids['stenc_blur']
            print("touch in stenc_blur by {}".format(touch.grabbed.children))
            print(self.grabbed)
            return  True
        elif self.ids['stenc_grey'].collide_point(*touch.pos):
            touch.grab(self)
            self.grabbed = self.ids['grey']
            print(self.grabbed)
            return True

        else:
            print("touch not in parent")
            return super(Root, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # print('moving ')
            self.grabbed.pos = [self.grabbed.pos[0] + touch.dx, self.grabbed.pos[1] + touch.dy]
            # touch.grabbed.pos.y += touch.dy

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True

    def create_texture(self, img_name=None, image=None):
        bufferfmt='ubyte'
        colorfmt = 'luminance'

        if image is None:
            img = self.img
        else:
            img = image
        # print(img_name)
        # print(img.dtype)

        if img_name == "blur":
            img = self.img_blur

        if img_name == "grey":
            img = self.grey
            # print("blur: {}".format(img.dtype))

        elif img_name == "sobel_x":
            img = self.sobelx
            # print(img.dtype)
            # print(img)

        elif img_name == "sobel_y":
            img = self.sobely

        elif img_name == "angle":
            img = self.angle
            # print ("angle depth")
            # print (img.dtype)

        elif img_name == "mag":
            img = self.mag
            # print ("mag depth")
            # print (img.dtype)

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt=bufferfmt)

        return texture

runTouchApp(Root())
