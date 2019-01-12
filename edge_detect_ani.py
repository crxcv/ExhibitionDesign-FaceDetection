# coding: utf-8

# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.core.window import Window
from kivy.properties import ObjectProperty, ListProperty

import cv2
import dlib
import numpy as np
import time

import warnings

from skimage import img_as_float, img_as_int, img_as_uint, img_as_ubyte

Builder.load_string('''

<Root>
    Images

<Images>:
    Image:
        id: mag
        texture: root.create_texture('mag')
        pos: 2*root.win_width/4, 10
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}
    Image:
        id: angle
        texture: root.create_texture('angle')
        pos: 2*root.win_width/4, root.win_height/2
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}

    Image:
        id: sobel_y
        texture: root.create_texture('sobel_y')
        pos: 1*root.win_width/4, 10
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}
    Image:
        id: sobel_x
        texture: root.create_texture('sobel_x')
        pos: 1*root.win_width/4, root.win_height/2
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}

    Image:
        id: blurred
        texture: root.create_texture('blur')
        pos: 10, root.pos_y - 538/2
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}
''')


class Root(Widget):
    pass


class Images(Widget):
    img = cv2.imread('images/orig.JPEG')
    img = cv2.flip(img, 0)
    # img = cv2.resize(img, None, fx=0.7, fy=0.7)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



    img = cv2.medianBlur(img, 11)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

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



    img_blur = cv2.GaussianBlur(img, (5, 5), 0)

    win_width = ObjectProperty(Window.width)
    win_height = ObjectProperty( Window.height)

    pos_y = ObjectProperty(Window.height/2)
    orig_size = ListProperty((img.shape[0], img.shape[1]))


    def create_texture(self, img_name=None, image=None):
        bufferfmt='ubyte'
        colorfmt = 'luminance'

        # def float_to_int(imgi):
        #     min = np.min(imgi)
        #     print("np.min: ".format(np.min(imgi)))
        #     img = imgi - min
        #     max = np.max(img)
        #     print("np.max: ".format(max))
        #     div = max/float(255)
        #     print("np.div: ".format(div))
        #     img = np.float16(np.round(img/div))
        #     print(img)
        #     img = imgi.astype(np.float16)
        #
        #     return imgi


        if image is None:
            img = self.img
        else:
            img = image
        print(img_name)
        print(img.dtype)

        if img_name == "blur":
            img = self.img_blur
            print("blur: {}".format(img.dtype))

        elif img_name == "sobel_x":
            img = self.sobelx
            print(img.dtype)
            print(img)

        elif img_name == "sobel_y":
            img = self.sobely

        elif img_name == "angle":
            img = self.angle
            print ("angle depth")
            print (img.dtype)

        elif img_name == "mag":
            img = self.mag
            print ("mag depth")
            print (img.dtype)

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt=bufferfmt)

        return texture

runTouchApp(Root())
