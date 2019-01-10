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
from kivy.properties import ObjectProperty, NumericProperty

import cv2
import numpy as np
import time



Builder.load_string('''

<Root>
    Images

<Images>:
    Image:
        id: original
        pos: 10, root.pos_y - 538/2
        size: 778, 583
        source: 'images/orig.JPEG'
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}



    Image:
        id: grey
        texture: root.create_texture('grey')
        pos: 10, root.pos_y - 538/2
        size: 778, 583
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}

    Image:
        id: blur
        texture: root.create_texture('blur')
        pos: 10, root.pos_y - 538/2
        size: 778, 583
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}

    Image:
        id: grey2alpha
        texture: root.create_texture('grey')
        pos: 10, root.pos_y - 538/2
        size: 778, 583
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}


    Image:
        id: orig2alpha
        texture: root.create_texture('orig')
        pos: 10, root.pos_y - 538/2
        size: 778, 583
        allow_stretch: False
        keep_ratio: True
        pos_hint: {'center_x', 'center_y'}
''')


class Root(Widget):
    pass
    # def do_layout(self, *args):
    #     num_children = len(self.children)
    #
    # def on_pos(self, *args):
    #     self.do_layout()
    #
    # def add_widget(self, widget):
    #     super(Root, self).add_widget(widget)
    #     self.do_layout()
    # def remove_widget(self, widget):
    #     super(Root, self).remove_widget(widget)
    #     self.do_layout()

class OriginalImg(Widget):
    #
    pos_y = ObjectProperty(Window.height/2)
    # def __init__(self, **kwargs):
    #     super(OriginalImg, self).__init__(**kwargs)
    #     self.pos = (300, 400)




class Images(Widget):
    pos_y = ObjectProperty(Window.height/2)
    def __init__(self, **kwargs):
        super(Images, self).__init__(**kwargs)

        self.img = cv2.imread('images/orig.JPEG')
        # self.create_textures()


    def create_texture(self, img_name):
        img = cv2.flip(self.img, 0)
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        colorfmt = 'luminance'

        if img_name == 'orig':
            buf = img.tostring()
            colorfmt = 'bgr'

        if img_name == 'grey':
            buf = img_grey.tostring()

        # img_grey = np.dstack([grey, grey, grey])
        if img_name == "blur":
            img_grey = cv2.GaussianBlur(img_grey, (5, 5), 0)
            buf = img_grey.tostring()


        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt='ubyte')

        return texture

        # self.ids['grey'].texture = texture
        # self.ids['grey2alpha'].texture = texture
        #
        # img_blur =
        # img_blur = np.dstack([img_blur, img_blur, img_blur])
        # buf = img_blur.tostring()
        # texture = Texture.create(size=(img_grey.shape[1], img_grey.shape[0]), colorfmt='bgr')
        # texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # self.ids['blur'].texture = texture




    def move_ani(self):
        """ Moves all image instances """

        Animation.cancel_all(self)
        target_x = 800

        ani = Animation(x=target_x, duration=1, t='in_out_sine')
        ani.start(self.ids['grey'])
        ani.start(self.ids['orig2alpha'])
        ani.start(self.ids['blur'])
        ani.start(self.ids['grey2alpha'])

    def alpha_ani(self):
        """ reduces opacity of overlaying original image """



        ani2 = Animation(opacity=0, duration=1, t='in_out_sine')
        ani2.start(self.ids['orig2alpha'])

    def move_blur_ani(self):
        """ moves 2nd grey image and blur image
        """
        ani3 = Animation(x=Window.width-900, duration=1, t='in_out_sine')
        ani3.start(self.ids['blur'])
        ani3.start(self.ids['grey2alpha'])
        # time.sleep(1)

    def alpha_blur(self):
        """ reduces opacity of grey image to show blurred image """

        ani4 = Animation(opacity=0, duration=1, t='in_out_sine')
        ani4.start(self.ids['grey2alpha'])

    def pyr_ani(self):
        pass

    aniNum = 0
    ani_dict = {0:move_ani , 1:alpha_ani, 2:move_blur_ani, 3:alpha_blur}
    ani_iter = iter(ani_dict.items())

    def on_touch_down(self, touch):
        print("touched")

        try:
            ani = self.ani_iter.__next__()[1]
            ani(self)
        except StopIteration:
            pass
        self.aniNum +=1







runTouchApp(Root())
