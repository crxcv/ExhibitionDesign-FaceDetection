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
    name = StringProperty(None)
    # img = cv2.imread('images/orig.JPEG')
    # img = cv2.flip(img, 0)
    # print("shape: {}".format(img.shape))
    # # img = cv2.resize(img, None, fx=0.7, fy=0.7)
    # grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # blur = cv2.medianBlur(grey, 11)
    # sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    # sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    #
    # angle = np.arctan2(sobely, sobelx) * (180 / np.pi)
    # # angle = np.absolute(angle)
    # angle = np.uint8(angle)
    #
    # mag = np.sqrt(sobelx**2.0 + sobely**2.0)
    # mag = np.absolute(mag)
    # mag = np.uint8(mag)
    #
    # sobelx = np.absolute(sobelx)
    # sobelx = np.uint8(sobelx)
    # # sobelx = 255 - sobelx
    # sobely = np.absolute(sobely)
    # sobely = np.uint8(sobely)
    # # sobely = 255 - sobely
    #
    # img_blur = cv2.GaussianBlur(grey, (5, 5), 0)
    #
    # pos_y = ObjectProperty(Window.height/2)
    # orig_size = ListProperty((img.shape[0], img.shape[1]))
    # win_width = ObjectProperty(Window.width)
    # win_height = ObjectProperty( Window.height)
    #
    # def create_texture(self, img_name=None, image=None):
    #     bufferfmt='ubyte'
    #     colorfmt = 'luminance'
    #
    #     if image is None:
    #         img = self.img
    #     else:
    #         img = image
    #     # print(img_name)
    #     # print(img.dtype)
    #
    #     if img_name == "blur":
    #         img = self.img_blur
    #
    #     if img_name == "grey":
    #         img = self.grey
    #         # print("blur: {}".format(img.dtype))
    #
    #     elif img_name == "sobel_x":
    #         img = self.sobelx
    #         # print(img.dtype)
    #         # print(img)
    #
    #     elif img_name == "sobel_y":
    #         img = self.sobely
    #
    #     elif img_name == "angle":
    #         img = self.angle
    #         # print ("angle depth")
    #         # print (img.dtype)
    #
    #     elif img_name == "mag":
    #         img = self.mag
    #         print ("mag depth")
    #         print (img.dtype)
    #
    #     buf = img.tostring()
    #     texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
    #     texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt=bufferfmt)
    #
    #     return texture

class Images(Widget):
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

    pos_y = ObjectProperty(Window.height/2)
    orig_size = ListProperty((img.shape[0], img.shape[1]))
    win_width = ObjectProperty(Window.width)
    win_height = ObjectProperty( Window.height)




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
            print ("mag depth")
            print (img.dtype)

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt=bufferfmt)

        return texture

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

    pos_y = ObjectProperty(Window.height/2)
    orig_size = ListProperty((img.shape[0], img.shape[1]))
    win_width = ObjectProperty(Window.width)
    win_height = ObjectProperty( Window.height)

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
            print ("mag depth")
            print (img.dtype)

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt=bufferfmt)

        return texture
    # def build(self):
    #     return Images()
# if __name__== "__main__":
#     Root().run()
runTouchApp(Root())
