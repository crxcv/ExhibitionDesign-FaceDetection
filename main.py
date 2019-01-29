#!/usr/bin/env python3
# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.clock import Clock

# local libraries
from edge_detect_ani import EdgeDetect
from preprocessing_ani import Preproc_Anim
from faceDetect import CameraScreen
from hog_detect import Hog_Detect



root_widget = Builder.load_file('mmain.kv')



class CircleButton(ButtonBehavior, Widget):
    color = ListProperty([1., 1., 1.])
    make_bigger = BooleanProperty(True)
    target = ObjectProperty()

    def __init__(self, **kwargs):
        super(CircleButton, self).__init__(**kwargs)
        self.popup = Popup(title="test", size_hint=(.5, .5))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Touched!!!")
            print("CircleButton {} touched at {}".format(self.name, touch.pos))
            self.trigger_action()
            pass
        else:
            return super(CircleButton, self).on_touch_down(touch)

    def toggle_button_behavior(self):

        if self.make_bigger:
            print("bigger")
            # self.popup.open()
            x, y = self.x, self.y
            if self.name == 'tl' or self.name == 'tr':
                y = self.y - 300
            if self.name == 'tr' or self.name == 'br':
            #     y = self.y - 150
                x = self.x - 300
            # if self.name == 'br':
                # x = self.x - 150
            anim = Animation(size=(600, 600), radius=300, x=x, y=y, t='in_elastic', duration=.4)
            anim.start(self)

            self.make_bigger = False
        else:
            self.make_bigger = True
            x, y = self.x, self.y
            if self.name == 'tl' or self.name == 'tr':
                y = self.y + 300
            if self.name == 'tr' or self.name == 'br':
            #     y = self.y + 150
                x = self.x + 300
            # elif self.name == 'br':
            #     x = self.x + 150
            anim = Animation(size=(300, 300), radius=150, x=x, y=y, t='out_elastic', duration= .4)
            anim.start(self)
            # MainApp.manager.current = screen_name
            print("changing to camScreen")
    # target = ObjectProperty(None)

    # def on_touch_down(self, touch):
    #     # print("CircleButton touched at {}".format(touch.pos))
    #
    #     if self.collide_point(*touch.pos):
    #         self.pressed = touch.pos
    #         print('circle {} pressed at {}'.format(self.id, touch.pos))
    #         return True  # self.on_touch_up()
    #     return super(CircleButton, self).on_touch_down(touch)


class Menu(Widget):
    pass
    # def on_touch_down(self, touch):
    #     print("Menu touched at {}".format(touch.pos))
    #     return super(Menu, self).on_touch_down(touch)


class ScreenManagement(ScreenManager):
    pass


class CamScreen(Screen):
    cam = ObjectProperty()

    # def on_touch_down(self, touch):
    #     print("CamScreen(Screen) touched at {}".format(touch.pos))
    #     return super(CamScreen, self).on_touch_down(touch)

    def on_pre_enter(self):
        print("entering camscreen")

        self.cam.start()
        # self.clock = Clock.schedule_interval(self.cam.update, 1/30)

    def on_leave(self):
        print("leaving camscreen")
        self.cam.destroy()

    # def on_touch_down(self, touch):
    #     print("CamScreen touched at {}".format(touch.pos))
    #     return super(CamScreen, self).on_touch_down(touch)


class PreprocScreen(Screen):
    preproc = ObjectProperty()
    # def on_touch_down(self, touch):
    #     print("PreprocScreen(Screen) touched at {}".format(touch.pos))
    #     return super(PreprocScreen, self).on_touch_down(touch)

    def on_enter(self):
        print("entering preprocScreen")
        # self.preproc.start()

    def on_leave(self):
        print("leaving preprocScreen")


class EdgedetScreen(Screen):
    edgedet = ObjectProperty()
    # def on_touch_down(self, touch):
    #     print("EdgeDetectScreen(Screen) touched at {}".format(touch.pos))
    #     return super(EdgedetScreen, self).on_touch_down(touch)

    def on_enter(self):
        print("entering edgedetectScreen")

    def on_leave(self):
        print("leaving edgedetectScreen")


class HogScreen(Screen):
    # def on_touch_down(self, touch):
    #     print("HogScreen(Screen) touched at {}".format(touch.pos))
    #     return super(HogScreen, self).on_touch_down(touch)

    hog = ObjectProperty()

    def on_enter(self):
        print("entering hogScreen")

    def on_leave(self):
        print("leaving hogScreen")


class MainApp(App):
        # def on_touch_down(self, touch):
        #     print("main touched at {}".format(touch.pos))
        #     return super(MainApp, self).on_touch_down(touch)

    def build(self):
        self.manager = ScreenManager()
        self.manager.add_widget(PreprocScreen(name="preprocScreen"))
        self.manager.add_widget(CamScreen(name="camScreen"))
        self.manager.add_widget(EdgedetScreen(name="edgeScreen"))
        self.manager.add_widget(HogScreen(name="hogScreen"))

        return self.manager


MainApp().run()
