#!/usr/bin/env python3
# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

# local libraries
from edge_detect_ani import EdgeDetect
from preprocessing_ani import Preproc_Anim
from faceDetect import CameraScreen
from hog_detect import Hog_Detect
from shadow_circle import MaterialWidget



root_widget = Builder.load_file('mmain.kv')



class CircleButton(ButtonBehavior, Widget):
    color = ListProperty([1., 1., 1.])
    make_bigger = BooleanProperty(True)
    target = ObjectProperty()

    def __init__(self, **kwargs):
        super(CircleButton, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Touched!!!")
            print("CircleButton {} touched at {}".format(self.name, touch.pos))
            self.trigger_action()

        else:
            return super(CircleButton, self).on_touch_down(touch)

    def toggle_button_behavior(self):

        if self.make_bigger:
            print("bigger")
            x, y = self.x, self.y
            if self.name == 'tl' or self.name == 'tr':
                y = self.y - 300
            if self.name == 'tr' or self.name == 'br':
                x = self.x - 300

            anim = Animation(size=(600, 600), radius=300, x=x, y=y,
                             t='in_elastic', duration=.4)
            anim.start(self)

            self.make_bigger = False
        else:
            self.make_bigger = True
            x, y = self.x, self.y
            if self.name == 'tl' or self.name == 'tr':
                y = self.y + 300
            if self.name == 'tr' or self.name == 'br':
                x = self.x + 300

            anim = Animation(size=(300, 300), radius=150, x=x, y=y,
                             t='out_elastic', duration=.4)
            anim.start(self)


class Menu(Widget):
    pass
    # def on_touch_down(self, touch):
    #     print("Menu touched at {}".format(touch.pos))
    #     return super(Menu, self).on_touch_down(touch)


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
    #     # return super(PreprocScreen, self).on_touch_down(touch)
    #     return True

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


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(PreprocScreen(name="preprocScreen"))
        self.add_widget(CamScreen(name="camScreen"))
        self.add_widget(EdgedetScreen(name="edgeScreen"))
        self.add_widget(HogScreen(name="hogScreen"))

    def preproc_popup(self):
        preproc_popup = ModalView(size_hint=(None, 1),
                                       width=Window.height)
        preproc_popup.background_color = (0, 0, 0, 0)
        preproc_popup.background = "images/circle_white_shadow.png"

        content = FloatLayout()

        button = Button(text="close", size_hint=(None, None),
                        size=(100, 50),
                        pos_hint={'center_x':.5,
                        'center_y':.25})
        content.add_widget(button)
        preproc_popup.add_widget(content)
        button.bind(on_press=preproc_popup.dismiss)

        # preproc_popup.background = "atlas://data/images/defaulttheme/background-transparent"
        # preproc_popup.border = MaterialWidget(elevation=2)
        preproc_popup.open()
        # self.add_widget(self.preproc_popup)




class MainApp(App):
        # def on_touch_down(self, touch):
        #     print("main touched at {}".format(touch.pos))
        #     return super(MainApp, self).on_touch_down(touch)

    def build(self):
        self.manager = ScreenManagement()
        # self.manager.add_widget(PreprocScreen(name="preprocScreen"))
        # self.manager.add_widget(CamScreen(name="camScreen"))
        # self.manager.add_widget(EdgedetScreen(name="edgeScreen"))
        # self.manager.add_widget(HogScreen(name="hogScreen"))


        return self.manager

    # def preproc_popup(self):
    #     self.preproc_popup = ModalView(size_hint=(None, 1),
    #                                    width=Window.height)
    #     self.preproc_popup.open()
    #     # self.add_widget(self.preproc_popup)
    #
    # def preproc_pop_close(self):
    #     self.preproc_popup.dismiss()


    def edgedetect_popup(ModalView):
        pass

    def hog_popup(ModalView):
        pass


MainApp().run()
