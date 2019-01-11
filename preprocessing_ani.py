# coding: utf-8

# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.graphics.texture import Texture

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty

import cv2
import imutils
import numpy as np
from skimage.transform import pyramid_gaussian


Builder.load_string('''

<Root>:
    Preproc_Anim


<Preproc_Anim>:
    Image:
        id: original
        texture: root.create_texture('orig', is_colored=True)
        pos: 10, root.pos_y
        size: 778, 583
        allow_stretch: False
        keep_ratio: True

    Image:
        id: grey
        texture: root.create_texture('grey')
        pos: 10, root.pos_y
        size: 778, 583
        allow_stretch: False
        keep_ratio: True

    Image:
        id: blur
        texture: root.create_texture('blur')
        pos: 10, root.pos_y
        size: 778, 583
        allow_stretch: False
        keep_ratio: True

    Image:
        id: grey2alpha
        texture: root.create_texture('grey')
        pos: 10, root.pos_y
        size: 778, 583
        allow_stretch: False
        keep_ratio: True

    Image:
        id: orig2alpha
        texture: root.create_texture('orig', is_colored=True)
        pos: 10, root.pos_y
        size: 778, 583
        allow_stretch: False
        keep_ratio: True

''')


class Root(Widget):
    pass



class Preproc_Anim(Widget):
    pos_y = ObjectProperty(Window.height/2 + 100)
    img_pyr = []
    im_in_pyr = 0

    def __init__(self, **kwargs):
        super(Preproc_Anim, self).__init__(**kwargs)

        self.img = cv2.imread('images/orig.JPEG')
        self.img = cv2.flip(self.img, 0)



    def create_texture(self, img_name=None, image = None, is_colored = False):
        if image is None:
            img = self.img
        else:
            img = image

        if is_colored:
            colorfmt = 'bgr'
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            colorfmt = 'luminance'

        if img_name == "blur":
            img = cv2.GaussianBlur(img, (5, 5), 0)

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt='ubyte')
        print("texture type of {}: {}".format(img_name, type(texture)))

        return texture


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

    def alpha_blur(self):
        """ reduces opacity of grey image to show blurred image """

        ani4 = Animation(opacity=0, duration=1, t='in_out_sine')
        ani4.start(self.ids['grey2alpha'])

    def pyramid(self, image, scale=1.5, min_size=(30, 30)):
        # yield image
        self.im_in_pyr = 0
        while True:
            w = int(image.shape[1]/scale)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = imutils.resize(image, width=w)
            image = cv2.GaussianBlur(image, (5, 5), 0)
            texture = self.create_texture(image=image, is_colored=False)
            print("texture type of img_pyr {}".format( type(texture)))


            if image.shape[0] < min_size[1] or image.shape[1] < min_size[0]:
                break
            # new = Factory.Images()
            # texture=texture, pos=self.ids['blur'].pos, id=
            im = Image(source=None)
            im.texture = texture
            im.pos = (0, 0)
            im.id = 'pyr_{}'.format(self.im_in_pyr)

            self.img_pyr.append(im)
            self.add_widget(im)
            # self.add_widget(im, index=self.im_in_pyr)
            # self.img_pyr.append(i)
            self.im_in_pyr += 1

    def pyr_ani(self):

        anis = []
        self.pyramid(self.img)
        print("children: {}".format(self.children))
        print("im in pyr: {}".format(self.im_in_pyr))
        for (i, resized) in enumerate(pyramid_gaussian(image, downscale=2)):
            texture = self.create_texture(image=resized, is_colored=False)
            if resized.shape[0] < 30 or resized.shape[1] < 30:
                break

            im = Image(source=None)
            im.texture = texture
            im.pos = (0, 0)
            im.id = 'pyr_{}'.format(self.im_in_pyr)
            self.add_widget(im)


            x = Window.height/len(self.img_pyr)*i if i>0 else 0
            anis.append(Animation(x=x,
                        y=Window.height/4,
                        duration=1,
                        t='in_out_sine')
            )
            # anis[i].start(self.img_pyr[i])
            anis[i].start(im)
            i += 1



    aniNum = 0
    ani_dict = {0:move_ani , 1:alpha_ani, 2:move_blur_ani, 3:alpha_blur, 4:pyr_ani}
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
