# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

# local libraries
from edge_detect_ani import EdgeDetect
from preprocessing_ani import Preproc_Anim
from faceDetect import KivyCamera


root_widget = Builder.load_file('mmain.kv')


class Circles(ButtonBehavior, Widget):
    color = ListProperty([1., 1., 1.])
    # target = ObjectProperty(None)

    # def on_touch_down(self, touch):
    #     # print("Circles touched at {}".format(touch.pos))
    #
    #     if self.collide_point(*touch.pos):
    #         self.pressed = touch.pos
    #         print('circle {} pressed at {}'.format(self.id, touch.pos))
    #         return True  # self.on_touch_up()
    #     return super(Circles, self).on_touch_down(touch)


class Menu(Widget):
    pass


class ScreenManagement(ScreenManager):
    pass


class CamScreen(Screen):
    cam = ObjectProperty()

    def on_enter(self):
        print("entering camscreen")
        print('ids: {}'.format(self.ids))
        print('children: {}'.format(self.children))

        self.cam.start()
        self.clock = Clock.schedule_interval(self.cam.update, 1/30)

    def on_leave(self):
        print("leaving camscreen")
        self.cam.stop()

    # def on_touch_down(self, touch):
    #     print("CamScreen touched at {}".format(touch.pos))
    #     return super(CamScreen, self).on_touch_down(touch)


class PreprocScreen(Screen):
    def on_enter(self):
        print("entering preprocScreen")

    def on_leave(self):
        print("leaving preprocScreen")


class EdgedetScreen(Screen):
    def on_enter(self):
        print("entering edgedetectScreen")

    def on_leave(self):
        print("leaving edgedetectScreen")


class MainApp(App):
    def on_touch_down(self, touch):
        print("main touched at {}".format(touch.pos))
        return super(MainApp, self).on_touch_down(touch)

    def build(self):
        self.manager = ScreenManager()
        self.manager.add_widget(CamScreen(name="camScreen"))
        self.manager.add_widget(PreprocScreen(name="preprocScreen"))
        self.manager.add_widget(EdgedetScreen(name="edgeScreen"))

        return self.manager


MainApp().run()
