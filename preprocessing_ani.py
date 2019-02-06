#!/usr/bin/env python3
# coding: utf-8

# fullscreen
if __name__ == '__main__':
    from kivy.config import Config
    Config.set('graphics', 'fullscreen', 'auto')

from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock

from kivy.graphics import *
from kivy.metrics import *

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.stencilview import StencilView
from kivy.uix.modalview import ModalView
import kivy.graphics.stencil_instructions
from kivy.graphics.texture import Texture

from kivy.animation import Animation

from kivy.core.window import Window
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import cv2
import imutils
import numpy as np
from skimage.transform import pyramid_gaussian
from skimage.draw import circle
from matplotlib import pyplot as plt


Builder.load_file('preprocessing.kv')


class Root(Widget):
    pass




class Preproc_Anim(Widget):

    img = ObjectProperty()
    img = cv2.imread('images/orig.JPEG')
    # img = cv2.flip(img, 0)

    h = 350  #ObjectProperty(350)
    w = int(img.shape[1] * (h/img.shape[0]))
    target_w = ObjectProperty(w)
    target_h = ObjectProperty(h)

    x1 = Window.width/4
    x2 = x1*2 -h/2
    x3 = x1*3 -h/2
    img_x = x1 - ((w - h)/2 )

    img = cv2.resize(img, (w, h), cv2.INTER_AREA)
    print("ing size: {}".format(img.shape))

    # convert size to inch for figuresize (pyplot)
    dpi = inch(1)
    h_inch = int(h/dpi)

    # cut out square
    dist = int((img.shape[1] - h) / 2)
    img = img[:, dist:dist+h]

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (7, 7), 0)

    orig_ov = np.zeros(img.shape)
    grey_ov = np.zeros(grey.shape)
    blur_ov = np.zeros(blur.shape)


    pos_y = ObjectProperty(Window.height/2 + 100)
    orig_size = ListProperty((img.shape[0], img.shape[1]))
    img_pyr = []
    im_in_pyr = 0

    # pixel coords round part in big img
    mid_x = int(img.shape[0]/2)
    mid_y = int(img.shape[1]/2)
    rr, cc = circle(mid_x, mid_y, mid_y, (350, 350))

    orig_ov[rr, cc] = img[rr, cc]
    grey_ov[rr, cc] = grey[rr, cc]
    blur_ov[rr, cc] = blur[rr, cc]

    plt.rcParams['savefig.pad_inches'] = 0
    plt.style.use(['dark_background'])

    orig_fig = plt.figure(figsize=(h_inch, h_inch))
    ax_o = plt.axes([0,0,1,1], frameon=False)
    ax_o.get_xaxis().set_visible(False)
    ax_o.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)
    plt.imshow(orig_ov, 'brg')

    grey_fig = plt.figure(figsize=(h_inch, h_inch))
    ax_grey = plt.axes([0,0,1,1], frameon=False)
    ax_grey.get_xaxis().set_visible(False)
    ax_grey.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)
    plt.imshow(grey_ov, 'gray')


    blur_fig = plt.figure(figsize=(h_inch, h_inch))
    ax_blur = plt.axes([0,0,1,1], frameon=False)
    ax_blur.get_xaxis().set_visible(False)
    ax_blur.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)
    plt.imshow(blur_ov, 'gray')

    text_orig = "Wir Menschen erkennen Objekte oder auch Muster meist auf den ersaten Blick. "
    text_orig += "Computer hingegen müssen zuerst das ganze Bild, also jeden einzelnen Pixel "
    text_orig += "analysieren und auf verschiedene Weise miteinander vergleichen um zu analysieren, "
    text_orig +="ob und wo sich Objekte wie Menschen oder auch deren Gesichter auf dem Bild befinden."
    text_orig = StringProperty(text_orig)

    text_grey = "Zuerst wird dem Bild die Farbe entzogen. So hat man ausreichend Bildinformationen "
    text_grey += "um Kanten, und so auch Gesichter, zu erkennen und spart außerdem Rechenleistung"
    text_grey = StringProperty(text_grey)

    text_blur = "Anschließend wird die Bildschärfe reduziert. Der Vorteil hiervon ist, "
    text_blur += "dass zusammenhängende Flächen besser zu erkennen sind"
    text_blur = StringProperty(text_blur)

    def __init__(self, **kwargs):
        super(Preproc_Anim, self).__init__(**kwargs)

        y_img = Window.height - 106
        cx1 = 417
        cx2 = Window.width/2
        cx3 = Window.width - cx1

        layout = FloatLayout(size_hint=(None, None))
        orig = FigureCanvasKivyAgg(figure=self.orig_fig, size_hint=(None, None))
        orig.size = (self.w, self.h)
        orig.top = y_img
        orig.centrer_x = cx1
        layout.add_widget(orig)

        grey = FigureCanvasKivyAgg(figure=self.grey_fig, size_hint=(None, None))
        grey.size = (self.w, self.h)
        grey.top = y_img
        grey.center_x = cx2
        layout.add_widget(grey)

        blur = FigureCanvasKivyAgg(figure=self.grey_fig, size_hint=(None, None))
        blur.size = (self.w, self.h)
        blur.top = y_img
        blur.center_x = cx3
        layout.add_widget(blur)

        self.add_widget(layout)

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
            img = cv2.GaussianBlur(img, (7, 7), 0)

        buf = img.tostring()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt=colorfmt)
        texture.blit_buffer(buf, colorfmt=colorfmt, bufferfmt='ubyte')

        # print("texture type of {}: {}".format(img_name, type(texture)))

        return texture


    def move_ani(self, dt=None):
        """ Moves all image instances """
        # print("type: {}".format(type(self)))
        # print("children: {}".format(self.children))
        Animation.cancel_all(self)
        target_x = 800

        ani = Animation(x=self.x2, duration=1, t='in_out_sine')
        ani.start(self.ids.grey)
        ani.start(self.ids.orig2alpha)
        ani.start(self.ids.blur)
        ani.start(self.ids.grey2alpha)

    def alpha_ani(self, dt=None):
        """ reduces opacity of overlaying original image """
        ani2 = Animation(opacity=0, duration=.5, t='in_out_sine')
        ani2.start(self.ids.orig2alpha)

    def move_blur_ani(self, dt=None):
        """ moves 2nd grey image and blur image
        """
        ani3 = Animation(x=self.x3, duration=1, t='in_out_sine')
        ani3.start(self.ids.blur)
        ani3.start(self.ids.grey2alpha)

    def alpha_blur(self, dt=None):
        """ reduces opacity of grey image to show blurred image """

        ani4 = Animation(opacity=0, duration=.5, t='in_out_sine')
        ani4.start(self.ids.grey2alpha)

    def pyramid(self,  image, scale=1.5, min_size=(30, 30)):
        # yield image
        self.im_in_pyr = 0
        while True:
            w = int(image.shape[1]/scale)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = imutils.resize(image, width=w)
            image = cv2.GaussianBlur(image, (5, 5), 0)
            texture = self.create_texture(image=image, is_colored=False)

            # print("texture type of img_pyr {}".format( type(texture)))


            if image.shape[0] < min_size[1] or image.shape[1] < min_size[0]:
                break
            # new = Factory.Images()
            # texture=texture, pos=self.ids['blur'].pos, id=
            im = RoundImage()
            im.texture = texture
            im.pos = (0, 0)
            im.id = 'pyr_{}'.format(self.im_in_pyr)
            im.size = [image.shape[1], image.shape[0]]

            self.img_pyr.append(im)
            self.add_widget(im)
            # self.add_widget(im, index=self.im_in_pyr)
            # self.img_pyr.append(i)
            self.im_in_pyr += 1


    def pyr_gaussian(self):
        grey = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        for (i, resized) in enumerate(pyramid_gaussian(grey, downscale=1.2)):

            if resized.shape[0] < 100 or resized.shape[1] < 100:
                break
            # print("resizex {}".format(resized.shape))

            # !!!!
            # https://stackoverflow.com/questions/33299374/opencv-convert-cv-8u-to-cv-64f
            min = np.min(resized)
            resized = resized-min #to have only positive values
            max=np.max(resized)
            div = max / float(255)
            img = np.uint8(np.round(resized / div))

            texture = self.create_texture(image=img, is_colored=False)

            im = RoundImage()
            im.texture = texture
            im.pos = self.ids['blur'].pos
            im.id = 'pyr_{}'.format(self.im_in_pyr)
            im.size = [resized.shape[1], resized.shape[0]]
            # im.allow_stretch = False
            self.img_pyr.append(im)
            self.add_widget(im)

    def pyr_ani(self, dt=None):
        self.pyr_gaussian()

        # self.pyramid(self.img)
        anis = []
        # print("children: {}".format(len(self.children)))

        # self.pyramid(self.img)
        # print("im in pyr: {}".format(self.im_in_pyr))
        # for (i, resized) in enumerate(pyramid_gaussian(self.ids.blur, downscale=2)):
        for i in range(self.im_in_pyr):



            x = Window.height/len(self.img_pyr)*i if i>0 else 0
            anis.append(Animation(x=x,
                        y=Window.height/4,
                        duration=1,
                        t='in_out_sine')
            )
            anis[i].start(self.img_pyr[i])
            # anis[i].start(im)
            i += 1
        # print("IDs: {}".format(self.ids))

    def rescale_pyr(self):
        anis = []
        for img in self.img_pyr:
            img.allow_stretch = True
            ani = Animation(size=self.orig_size,
                        duration=1,
                        t='in_out_sine')
            ani.start(img)
            anis.append(ani)





    def start(self):
        pass
    #     self.ani_dict = {0:self.move_ani , 1:self.alpha_ani, 2:self.move_blur_ani, 3:self.alpha_blur, 4:self.pyr_ani}

    # aniNum = 0
    # ani_dict = {0:move_ani , 1:alpha_ani, 2:move_blur_ani, 3:alpha_blur} # , 4:pyr_ani, 5:rescale_pyr}
    # ani_iter = iter(ani_dict.items())

#    def on_touch_down(self, touch):

        # print("touched")

        # try:
        #     (i, ani) = self.ani_iter.__next__()
        #     # print("Ani: {}".format(self.ani_dict[i]))
        #     ani(self)
        # except StopIteration:
        #     pass
        # self.aniNum +=1

        # for key in self.ani_dict:
        #     Clock.schedule_once(self.ani_dict[key], key*2)
    # aniNum = 0
    # ani_dict = {0:move_ani , 1:alpha_ani, 2:move_blur_ani, 3:alpha_blur, 4:pyr_ani}
    # ani_iter = iter(ani_dict.items())
    #
    # def on_touch_down(self, touch):
    #
    #     print("touched")
    #
    #     try:
    #         ani = self.ani_iter.__next__()[1]
    #         ani(self)
    #     except StopIteration:
    #         pass
    #     self.aniNum +=1






if __name__ == '__main__':
    runTouchApp(Root())
