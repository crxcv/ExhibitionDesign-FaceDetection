# coding: utf-8

# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.uix.image import Image
from kivy.uix.widget import Widget
# from kivy.graphics.texture import Texture

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.core.window import Window




Builder.load_string('''
<Root>

    Image:
        pos: 300, 400
        size: 778, 583
        source: 'images/img_grey.JPEG'
        allow_stretch: False
        keep_ratio: True

    Image:
        pos: 300, 400
        size: 778, 583
        source: 'images/orig.JPEG'
        allow_stretch: False
        keep_ratio: True

    Image:
        pos: 300, 400
        size: 778, 583
        source: 'images/orig.JPEG'
        allow_stretch: False
        keep_ratio: True
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

runTouchApp(Root())
