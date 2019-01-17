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
from kivy.properties import ObjectProperty, ListProperty

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
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True

    Image:
        id: grey
        texture: root.create_texture('grey', make_grey=True)
        pos: 10, root.pos_y
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True

    Image:
        id: blur
        texture: root.create_texture('blur', make_grey=True)
        pos: 10, root.pos_y
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True

    Image:
        id: grey2alpha
        texture: root.create_texture('grey', make_grey=True)
        pos: 10, root.pos_y
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True

    Image:
        id: orig2alpha
        texture: root.create_texture('orig', is_colored=True)
        pos: 10, root.pos_y
        size: root.orig_size
        allow_stretch: False
        keep_ratio: True

''')


class Root(Widget):
    pass



class Preproc_Anim(Widget):
    img = cv2.imread('images/orig.JPEG')
    img = cv2.flip(img, 0)

    pos_y = ObjectProperty(Window.height/2 + 100)
    orig_size = ListProperty((img.shape[0], img.shape[1]))
    img_pyr = []
    im_in_pyr = 0

    def __init__(self, **kwargs):
        super(Preproc_Anim, self).__init__(**kwargs)

        self.img = cv2.imread('images/orig.JPEG')
        self.img = cv2.flip(self.img, 0)



    def create_texture(self, img_name=None, image=None, is_colored=False, make_grey=False):
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

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt='ubyte')

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

        # self.pyramid(self.img)
        anis = []
        print("children: {}".format(len(self.children)))
        grey = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        for (i, resized) in enumerate(pyramid_gaussian(grey, downscale=1.2)):

            if resized.shape[0] < 100 or resized.shape[1] < 100:
                break
            print("resizex {}".format(resized.shape))

            # !!!!
            # https://stackoverflow.com/questions/33299374/opencv-convert-cv-8u-to-cv-64f
            min = np.min(resized)
            resized = resized-min #to have only positive values
            max=np.max(resized)
            div = max / float(255)
            img = np.uint8(np.round(resized / div))

            texture = self.create_texture(image=img, is_colored=False)



            im = Image(source=None)
            im.texture = texture
            im.pos = self.ids['blur'].pos
            im.id = 'pyr_{}'.format(self.im_in_pyr)
            im.allow_stretch = False
            self.img_pyr.append(im)
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
        print("IDs: {}".format(self.ids))

    def rescale_pyr(self):
        anis = []
        for img in self.img_pyr:
            img.allow_stretch = True
            ani = Animation(size=self.orig_size,
                        duration=1,
                        t='in_out_sine')
            ani.start(img)
            anis.append(ani)






    aniNum = 0
    ani_dict = {0:move_ani , 1:alpha_ani, 2:move_blur_ani, 3:alpha_blur, 4:pyr_ani, 5:rescale_pyr}
    ani_iter = iter(ani_dict.items())

    def on_touch_down(self, touch):
        print("touched")

        try:
            (i, ani) = self.ani_iter.__next__()
            print("Ani: {}".format(self.ani_dict[i]))
            ani(self)
        except StopIteration:
            pass
        self.aniNum +=1







runTouchApp(Root())
