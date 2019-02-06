#!/usr/bin/env python3
# coding: utf-8

# fullscreen
if __name__ == '__main__':
    from kivy.config import Config
    Config.set('graphics', 'fullscreen', 'auto')

from kivy.clock import Clock
import kivy.metrics as metrics
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
import kivy.graphics.stencil_instructions
from kivy.uix.stencilview import StencilView
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty, BooleanProperty

import cv2
import dlib
import imutils
import numpy as np
# from skimage.transform import pyramid_gaussian

from skimage import exposure
from skimage import feature

Builder.load_file('hog_detect.kv')

img = cv2.imread('images/orig.JPEG')
cv2_hog_face = cv2.imread('images/hog_face.png')

h = 350  # ObjectProperty(350)
w = int(img.shape[1] * (h/img.shape[0]))
img = cv2.resize(img, (w, h), cv2.INTER_AREA)
cv2_img = cv2.flip(img, 0)
cv2_img_grey = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

(H, hogImage) = feature.hog(cv2_img_grey, orientations=9,
                            pixels_per_cell=(8, 8),
                            cells_per_block=(8, 8),
                            transform_sqrt=True,
                            block_norm="L1",
                            visualize=True)

hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
hogImage = hogImage.astype('uint8')

buf = hogImage.tostring()
hog_texture = Texture.create(size=(hogImage.shape[1],
                                   hogImage.shape[0]),
                             colorfmt='luminance')

hog_texture.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')

detector = dlib.get_frontal_face_detector()
faces = detector(img, 0)

# coords_rt = [(img.shape[1] - face.left(), img.shape[0] - face.bottom()) for face in faces]
# coords_lb = [(img.shape[1] - face.right(), img.shape[0] - face.top()) for face in faces]
coords_lb = [(face.left(), img.shape[0] - face.bottom()) for face in faces]
coords_rt = [(face.right(), img.shape[0] - face.top()) for face in faces]


widths = [face.width() for face in faces]

print('coords_lb: {}'.format(coords_lb))
print('coords_rt: {}'.format(coords_rt))
print('widths: {}'.format(widths))




class RoundImage(Widget):
    texture = ObjectProperty(None)

    target_w = NumericProperty(w)
    target_h = NumericProperty(h)
    x1 = Window.width/4 - h/2
    y1 = Window.height/3 * 2 - h/2
    img_x = x1 - ((w - h)/2)



class Hog_Anim(Widget):
    img_size = [cv2_img.shape[1], cv2_img.shape[0]]
    hog_face_size = [cv2_hog_face.shape[1], cv2_hog_face.shape[0]]

    face1_coords = coords_lb[1]
    face1_width = widths[1]
    face0_coords = coords_lb[0]
    face0_width = widths[0]

    texture = ObjectProperty(hog_texture)
    texture_mini = hog_texture.get_region(0, img_size[1]-face1_width, face1_width, face1_width)

    face_found = BooleanProperty(False)


    spacing = 20
    size = [img_size[0]+ hog_face_size[0] + spacing, img_size[1]+spacing]
    # print("widgetsize: {}".format(size))
    print("im_size: {}".format(img_size))
    # print("local size: {}".format(FloatLayout.to_local(size[0], size[1], relative=True)))
    layoutSize = ListProperty(size)


    rect_x = NumericProperty(0)
    rect_y = NumericProperty(img_size[1] - face1_width)

    hog_rect =

    def __init__(self, **kwargs):
        # self.texture_mini.add_reload_observer(self.populate_texture)
        super(Hog_Anim, self).__init__(**kwargs)

        Clock.schedule_interval(self.move_rect, 1.0/15)
        self.rect_x = self.img_size[0]
        self.rect_y = self.img_size[1] - self.face1_width



    def move_rect(self, dt):
        if self.rect_x + self.face1_width < self.img_size[0]:
            self.rect_x += 5
        elif (self.rect_x + self.face1_width > self.img_size[1]) and self.rect_y > 0:
            self.rect_x = 0
            self.rect_y -= 5
        else:
            self.rect_x = 0
            self.rect_y = self.img_size[1] - self.face1_width
        self.populate_texture()
        # self.texture_mini = self.texture# hog_texture.get_region(self.rect_x, self.rect_y, self.face1_width, self.face1_width)
        # self.texture_mini.blit_buffer()
        # self.ids.hog_cut.texture = self.texture_mini
        # self.ids.hog_cut.canvas.ask_update()

    def populate_texture(self):
        # print("populate_texture")
        image = self.ids.hog_cut
        self.texture_mini = self.texture.get_region(self.rect_x, self.rect_y, self.face1_width, self.face1_width)
        # texture.blit_buffer(buf, (self.face1_width, self.face1_width), colorfmt='luminance', pos=(self.rect_x, self.rect_y))
        image.texture = self.texture_mini
        self.remove_widget(self.ids.hog_cut)
        self.add_widget(image)

    def update_texture(self):
        self.texture_mini = hog_texture.get_region(self.rect_x, self.rect_y, self.face1_width, self.face1_width)
        self.ids.hog_cut.texture = self.texture_mini
        self.ids.hog_cut.canvas.ask_update()
    #
    # def on_touch_up(self, touch):
    #     self.rect_x = self.ids.im_stenc.rect_x
    #     self.rect_y = self.ids.im_stenc.rect_y
    #     # self.ids.hog_cut.texture.add_reload_observer(self.update_texture)
    #     Clock.schedule_interval(self.move_rect, 1.0/15)


class Hog_Detect(FloatLayout):
    img = ObjectProperty()
    img = cv2_img

    target_w = ObjectProperty(w)
    target_h = ObjectProperty(h)
    texture = ObjectProperty(hog_texture)

    x1 = Window.width/4
    x2 = x1*2 - h/2
    x3 = x1*3 - h/2
    img_x = x1 - ((w - h)/2)
    print("ing size: {}".format(img.shape))

    def create_texture(self, img_name=None, image=None,
                       is_colored=False, make_grey=False):
        if image is None:
            img = self.img
        else:
            img = image

        if make_grey:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if is_colored:
            colorfmt = 'bgr'
        else:
            colorfmt = 'luminance'

        if img_name == "blur":
            img = cv2.GaussianBlur(img, (5, 5), 0)
        elif img_name == 'hog':
            img = hogImage

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1],
                                       img.shape[0]),
                                 colorfmt=colorfmt)

        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt='ubyte')
        # print("texture type of {}: {}".format(img_name, type(texture)))
        return texture


if __name__ == '__main__':
    runTouchApp(Hog_Detect())
