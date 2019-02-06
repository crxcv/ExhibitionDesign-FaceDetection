# coding: utf-8

# fullscreen
if __name__ == '__main__':
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
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty

from kivy.uix.screenmanager import Screen

import cv2
import dlib
import numpy as np

import warnings

from skimage import img_as_float, img_as_int, img_as_uint, img_as_ubyte

Builder.load_file('edge_detect_ani.kv')


class RoundImage(Widget):
    texture = ObjectProperty(None)
    h = 350  #ObjectProperty(350)
    w = int(778 * (h/583))
    target_w = NumericProperty(w)
    target_h = NumericProperty(h)
    x1 = Window.width/4 - h/2
    y1 = Window.height/3 * 2 - h/2
    img_x = x1 - ((w - h)/2)
    print("win size: {}".format((Window.width, Window.height)))

class Picture(Scatter):
    texture = ObjectProperty(None)
    name = StringProperty("")
    #
    # def check_trans(self, matrix):
    #     pos_matrix = Matrix().translate(self.pos[0], self.pos[1], 0)
    #     pos = matrix.multiply(pos_matrix).get[12:14]
    #
    #     if pos[0] > 0 or pos[1] > 0:
    #         return False
    #     elif pos[0] + self.width * self.scale < Window.size[0] or pos[1] + self.height*self.scale < Window.size[1]:
    #         return False
    #     else:
    #         return True
    #
    # def transform_with_touch(self, touch):
    #     # just do a simple one-finger-touch
    #     changed = False
    #     if len(self._touches) == self.translation_touches:
    #         # _last_touch_pos has last pos in correct parent space
    #         # just like incoming touch
    #         dx = (touch.x - self._last_touch_pos[0]) \
    #                 * self.do_translation_x
    #         dy = (touch.y - self._last_touch_pos[1]) \
    #                 * self.do_translation_y
    #         dx = dx / self.translation_touches
    #         dy = dy / self.translation_touches
    #
    #         m = Matrix().translate(dx, dy, 0)
    #
    #         if self.check_trans(m):
    #             self.apply_transform(Matrix().translate(dx, dy, 0))
    #         else:
    #             pass
    #
        # if len(self._touches) == 1:
        #     return changed
        #
        # we have more than 1 touch .. list of last known touches
        # points = [Vector(self._last_touch_pos[t]) for t in self._touches if t is not touch]
        #
        # # add current to last touch
        # points.append(Vector(touch.pos))
        # # we only want to transform if the touch is part of the two touches
        # # farthest apart! So first we find anchor, the point to transform
        # # around as another touch farthest away from current touch's pos
        # anchor = max(points[:-1], key = lambda p: p.distance(touch.pos))
        #
        # # now we find the touch farthest away from anchor, if its not the
        # # same as touch. Touch is not one of the two touches used to transform
        # farthest = max(points, key=anchor.distance)
        # if farthest is not points[:-1]:
        #     return changed
        #
        # # ok, so we have touch, and anchor, so we can actually compute the
        # # transformation
        # old_line = Vector(*touch.ppos) - anchor
        # new_line = Vector(*touch.pos) - anchor
        # if not old_line.length():  # divide by zero
        #     return changed
        #
        # angle = radians(new_line.angle(old_line)) * self.do_rotation
        # self.apply_transform(Matrix().rotate(angle, 0, 0, 1), anchor=anchor)
        #
        # if self.do_scale:
        #     scale = new_line.length() / old_line.length()
        #     new_scale = scale * self.scale
        #     if new_scale < self.scale_min:
        #         scale = self.scale_min / self.scale
        #     elif new_scale > self.scale_max:
        #         scale = self.scale_max / self.scale
        #     m = Matrix().scale(scale, scale, scale)
        #     if self.check_trans(m):
        #         self.apply_transform(Matrix().scale(scale, scale, scale),
        #                              anchor=anchor)
        #         changed = True
        #     else:
        #         pass
        # return changed

class EdgeDetect(Widget):
    name = StringProperty('edgedetectScreen')
    img = cv2.imread('images/orig.JPEG')
    img = cv2.flip(img, 0)
    h = 350  #ObjectProperty(350)
    w = int(778 * (h/583))
    target_w = NumericProperty(w)
    target_h = NumericProperty(h)
    x1 = Window.width/4  - h/2
    y1 = Window.height/3 * 2  - h/2
    img_x = x1 - ((w - h)/2 )

    img = cv2.resize(img, (w, h), cv2.INTER_AREA)
    # print("[edge detect] shape: {}".format(img.shape))
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
    text_angleMag += "Die Richtung der Größten Helligkeitsaenderung sowie dessen Stärke, wobei das obere Bild die Richtung der Helligkeitsänderung beschreibt, das untere Bild die Bereiche der Größten Änderung."

    def get_pos(self):
        return self.rect_pos[0], se

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
