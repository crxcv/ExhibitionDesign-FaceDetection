# coding: utf-8

# fullscreen
if __name__ == '__main__':
    from kivy.config import Config
    Config.set('graphics', 'fullscreen', 'auto')

from kivy.metrics import *
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
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import cv2
import dlib
import numpy as np
from skimage.draw import circle
from matplotlib import pyplot as plt

import warnings

from skimage import img_as_float, img_as_int, img_as_uint, img_as_ubyte

Builder.load_file('edge_detect_ani.kv')



class Picture(Scatter):
    texture = ObjectProperty(None)
    name = StringProperty("")
    #


class EdgeDetect(Widget):
    name = StringProperty('edgedetectScreen')
    img = cv2.imread('images/orig.JPEG')

    # resize proportionally
    h = 350  #ObjectProperty(350)
    w = int(778 * (h/583))
    target_w = NumericProperty(w)
    target_h = NumericProperty(h)
    x1 = Window.width/4  - h/2
    y1 = Window.height/3 * 2  - h/2
    img_x = x1 - ((w - h)/2 )
    img = cv2.resize(img, (w, h), cv2.INTER_AREA)

    # convert size to inch for figuresize (pyplot)
    dpi = inch(1)
    h_inch = int(h/dpi)

    # cut out square
    dist = int((img.shape[1] - h) / 2)
    img = img[:, dist:dist+h]

    # get images
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(grey, 11)
    img_blur = cv2.GaussianBlur(grey, (5, 5), 0)
    sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(sobelx**2.0 + sobely**2.0)
    angle = np.arctan2(sobely, sobelx) * (180 / np.pi)

    # arrays for round img
    grey_ov = np.full((h, h), -1937.0)
    sx_ov = np.full((h, h), -1937.0)
    sy_ov = np.full((h, h), -1937.0)
    angle_ov = np.full((h, h), -1937.0)
    mag_ov = np.full((h, h), 0)

    # pixel coords round part in big img
    mid_x = int(img.shape[0]/2)
    mid_y = int(img.shape[1]/2)
    rr, cc = circle(mid_x, mid_y, mid_y, (350, 350))


    # create black square for each image to add round texture
    # grey_ov[rr, cc] = grey[rr, cc]
    sx_ov[rr, cc] = sobelx[rr, cc]
    sy_ov[rr, cc] = sobely[rr, cc]
    angle_ov[rr, cc] = angle[rr, cc]
    mag_ov[rr, cc] = mag[rr, cc]

    plt.rcParams['savefig.pad_inches'] = 0
    plt.style.use(['dark_background'])
    sx_fig= plt.figure(figsize=(h_inch, h_inch))
    print("size inch: {}".format(h_inch))

    # Then we set up our axes (the plot region, or the area in which we plot things).
    # Usually there is a thin border drawn around the axes, but we turn it off with `frameon=False`.
    ax_sx = plt.axes([0,0,1,1], frameon=False)
    # Then we disable our xaxis and yaxis completely. If we just say plt.axis('off'),
    # they are still used in the computation of the image padding.
    ax_sx.get_xaxis().set_visible(False)
    ax_sx.get_yaxis().set_visible(False)

    # Even though our axes (plot region) are set to cover the whole image with [0,0,1,1],
    # by default they leave padding between the plotted data and the frame. We use tigher=True
    # to make sure the data gets scaled to the full extents of the axes.
    plt.autoscale(tight=True)
    plt.imshow(sx_ov, 'gray')


    sy_fig = plt.figure(figsize=(h_inch, h_inch))
    ax_sy = plt.axes([0,0,1,1], frameon=False)
    ax_sy.get_xaxis().set_visible(False)
    ax_sy.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)
    plt.imshow(sy_ov, 'gray')

    angle_fig = plt.figure()
    ax_ang = plt.axes([0,0,1,1], frameon=False)
    ax_ang.get_xaxis().set_visible(False)
    ax_ang.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)
    plt.imshow(angle_ov, 'gray')

    mag_fig = plt.figure()
    ax_mag = plt.axes([0,0,1,1], frameon=False)
    ax_mag.get_xaxis().set_visible(False)
    ax_mag.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)
    plt.imshow(mag_ov, 'gray')

    pos_y = ObjectProperty(int(Window.height/2))
    pos_x = ObjectProperty(Window.width/3)
    orig_size = ListProperty((img.shape[1], img.shape[0]))
    win_width = ObjectProperty(Window.width)
    win_height = ObjectProperty( Window.height)
    scale = ObjectProperty(2)

    grabbed = ObjectProperty({})

    pic_pos = ObjectProperty([10, Window.height/2])
    blur_pos = ObjectProperty([10, 10])
    rect_pos = ObjectProperty([10, 10])
    rect_size = ObjectProperty([0, 0])
    rect_h = ObjectProperty(0)
    rect_w = ObjectProperty(0)

    text_sobel = StringProperty()
    text_angleMag = StringProperty()
    text_sobel = "Aus dem zuvor erstellten Graustufenbild wird nun das sogenannte Gradient Image errechnet. "
    text_sobel += "Dies beschreibt die Veränderung der Helligkeitswerte an jedem einzelnen Punkt des Bildes, wobei keine oder nur eine geringe Veränderung bedeutet, dass hier eine Fläche vorliegt, wobei eine große Änderung ein Hinweis auf eine Kante darstellt. "
    text_sobel += "Erreicht wird dies durch einen sogenannten Faltungsalgorithmus"

    text_angleMag = "Anhand des Gradient Images werden nun an jedem Pixel zwei Masse bestimmt: "
    text_angleMag += "Die Richtung der Größten Helligkeitsaenderung sowie "
    text_angleMag += "dessen Stärke, wobei das obere Bild die Richtung der Helligkeitsänderung beschreibt, das untere Bild die Bereiche der Größten Änderung."

    def __init__(self, **kwargs):
        super(EdgeDetect, self).__init__(**kwargs)

        layout = FloatLayout(size_hint=(None, None))
        sx = FigureCanvasKivyAgg(figure=self.sx_fig, size_hint=(None, None))
        sx.size = (self.w, self.h)
        sx.center = (722.25, Window.height-332.5)
        layout.add_widget(sx)

        sy = FigureCanvasKivyAgg(figure=self.sy_fig, size_hint=(None, None))
        sy.size = (self.w, self.h)
        sy.center = (722.25, Window.height-747.25)
        layout.add_widget(sy)

        ang = FigureCanvasKivyAgg(figure=self.angle_fig, size_hint=(None, None))
        ang.size = (self.w, self.h)
        ang.center = (1186.25, Window.height-332.5)
        layout.add_widget(ang)

        mag = FigureCanvasKivyAgg(figure=self.mag_fig, size_hint=(None, None))
        mag.size = (self.w, self.h)
        mag.center = (1186.25, Window.height-747.25)
        layout.add_widget(mag)

        self.add_widget(layout)

    def check_pos(self, *args):
        img_pos, img_scale, img_size, stenc_pos = [i for i in args]
        # print("check pos {}".format(args))
        self.scale = img_scale

        self.rect_size = [i * 1/img_scale for i in img_size]

        # p = img_pos - tuple(stenc_pos) #
        # print("p: {}, {}".format(img_pos[0] - stenc_pos[0], img_pos[1] - stenc_pos[1]))
        p = [stenc_pos[0] - img_pos[0], stenc_pos[1] - img_pos[1]]  # [i-j for i, j in (img_pos, stenc_pos)]# tuple((img_pos[0] - stenc_pos[0], img_pos[1] - stenc_pos[1]))
        self.rect_pos= [i * 1/img_scale for i in p]
        # self.rect_pos = [self.blur_pos[0] + self.rect_pos[0], self.blur_pos[1] + self.rect_pos[1]]  # [i + j for i, j in (self.blur_pos, self.rect_pos)]

        # print("rect pos, size; {}, {}".format(self.rect_pos, self.rect_size))



    # def on_touch_down(self, touch):
    #     # print("id: {},  type: {}".format(self.id, type(self)))
    #     # # print("siblings: {}".format(self.parent.children))
    #     # print("children: {}".format(self.children))
    #     # print("ids: {}".format(self.ids))
    #     if self.ids['stenc_blur'].collide_point(*touch.pos):
    #         touch.grab(self)
    #         touch.grabbed = self.ids['stenc_blur']
    #         print("touch in stenc_blur by {}".format(touch.grabbed.children))
    #         print(self.grabbed)
    #         return  True
    #     elif self.ids['stenc_grey'].collide_point(*touch.pos):
    #         touch.grab(self)
    #         self.grabbed = self.ids['grey']
    #         print(self.grabbed)
    #         return True

    #     else:
    #         print("touch not in parent")
    #         return super(EdgeDetect, self).on_touch_down(touch)

    # def on_touch_move(self, touch):
    #     if touch.grab_current is self:
    #         # print('moving ')
    #         self.grabbed.pos = [self.grabbed.pos[0] + touch.dx, self.grabbed.pos[1] + touch.dy]
    #         # touch.grabbed.pos.y += touch.dy

    # def on_touch_up(self, touch):
    #     if touch.grab_current is self:
    #         touch.ungrab(self)
    #         return True

    def create_texture(self, img_name=None, image=None):
        bufferfmt='ubyte'
        colorfmt = 'luminance'
        # http://scikit-image.org/docs/dev/api/skimage.exposure.html?highlight=rescale_intensity#skimage.exposure.rescale_intensity
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

if __name__ == '__main__':
    runTouchApp(EdgeDetect())
