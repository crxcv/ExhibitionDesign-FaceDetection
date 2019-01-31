#!/usr/bin/env python3
# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import (ListProperty, StringProperty, ObjectProperty,
                             BooleanProperty, NumericProperty)
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
    # origin_pos = ListProperty()
    # animated_pos = ListProperty()
    # size_bigger = NumericProperty(300)
    is_animating = BooleanProperty()
    name = StringProperty()
    title = StringProperty()
    preproc_text = "Bevor der Computer das Bild verarbeiten kann, muss es zuerst vorbereitet werden. "
    edgedet_text = "Mehrere Schritte sind nötig, um zu analysieren, wo sich auf dem Bild Kanten befinden. Alle diese Schritte sind erforderlich, um anschließend Objekte auf dem Bild zu erkennen."
    hog_text = "Anhand der zuvor berechneten Bilder wird mithilfe eines Convolutional Neural Networks, einem Tool zur Klassifizierung von Daten, Objekte auf Bildern zu erkennen"

    def __init__(self, **kwargs):
        super(CircleButton, self).__init__(**kwargs)
        self.origin_pos = self.pos
        self.animated_pos = self.origin_pos
        self.is_animating = False

        self.preproc_label = Label(size_hint=(None, None),
                                  width=326, height=170,
                                  #center_x=188, #
                                  x=23,
                                  top=Window.height-100,
                                  text = self.preproc_text,
                                  text_size=(326, 170),
                                  font_size='18sp',
                                  valign="top")  # LIGHT!!!
        self.facedet_label = Label(size_hint=(None, None),
                                   width=326, height=170,
                                   text=self.hog_text,
                                   right=Window.width-23,
                                   y=100,
                                   font_size='18sp',
                                   text_size=(326, 170),
                                   valign='top')
        self.edgedet_label = Label(size_hint=(None, None),
                                   width=326, height=170,
                                   right=Window.width-23,
                                   top=Window.height-100,
                                   text=self.edgedet_text,
                                   font_size='18sp',
                                   text_size=(326, 170),
                                   valign='top')
        # self.preproc_text = Label(size_hint=(None, None), width=326, height=170, x=25, y=100)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Touched!!!")
            print("CircleButton {} touched at {}".format(self.name, touch.pos))
            self.trigger_action()

        else:
            return super(CircleButton, self).on_touch_down(touch)

    def toggle_button(self, anim, widget):
        self.is_animating = not self.is_animating
        if not self.is_animating and not self.make_bigger:
            self.ids.circle_title.font_size = '24sp'
            if self.name == 'tl':
                self.add_widget(self.preproc_label)
            elif self.name == 'br':
                self.add_widget(self.facedet_label)
            elif self.name == 'tr':
                self.add_widget(self.edgedet_label)

        elif self.is_animating and self.make_bigger:
            self.ids.circle_title.font_size = '18sp'
            if self.name == 'tl':
                self.remove_widget(self.preproc_label)
            elif self.name == 'br':
                self.remove_widget(self.facedet_label)
            elif self.name == 'tr':
                self.remove_widget(self.edgedet_label)

    def toggle_button_behavior(self):
        if not self.is_animating:
            if self.make_bigger:
                print("bigger")
                x, y = self.x, self.y
                if self.name == 'tl' or self.name == 'tr':
                    y = self.y - 300
                if self.name == 'tr' or self.name == 'br':
                    x = self.x - 300
                anim = Animation(size=(600, 600), radius=300,
                                 x=x,
                                 y=y,
                                 t='in_elastic', duration=.4)
                # anim = Animation(size=(600, 600), radius=300,
                #                  x=self.animated_pos[0],
                #                  y=self.animated_pos[1],
                #                  t='in_elastic', duration=.4)
                anim.bind(on_start=self.toggle_button,
                          on_complete=self.toggle_button)
                anim.start(self)
                self.make_bigger = False

            else:
                self.make_bigger = True
                x, y = self.x, self.y
                if self.name == 'tl' or self.name == 'tr':
                    y = self.y + 300
                if self.name == 'tr' or self.name == 'br':
                    x = self.x + 300
                anim = Animation(size=(300, 300), radius=150,
                                 x=x,
                                 y=y,
                                 t='out_elastic', duration=.4)
                anim.bind(on_start=self.toggle_button,
                          on_complete=self.toggle_button)
                # anim = Animation(size=(300, 300), radius=150,
                #                  x=self.origin_pos[0],
                #                  y=self.origin_pos[1],
                #                  t='out_elastic', duration=.4)
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


# class PreprocScreen(Screen):
#     preproc = ObjectProperty()
#     # def on_touch_down(self, touch):
#     #     print("PreprocScreen(Screen) touched at {}".format(touch.pos))
#     #     # return super(PreprocScreen, self).on_touch_down(touch)
#     #     return True
#     # def build(self):
#     # def __init__(self, **kwargs):
#     #     super(PreprocScreen, self).__init__(**kwargs)
#     #     self.app = App.get_runing_app()
#     #
#
#     def on_enter(self):
#         print("entering preprocScreen")
#         # self.preproc.start()
#
#     def on_leave(self):
#         print("leaving preprocScreen")


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
        app = App.get_running_app()
        preproc = Preproc_Anim()
        menu = Menu()
        button = Button(size_hint=(None, None),
                             center=(Window.width/2, Window.height/4),
                             text="open popup")

        preproc_screen = Screen(name="preprocScreen")
        preproc_screen.add_widget(menu, index=0)
        preproc_screen.add_widget(preproc, index=2)
        preproc_screen.add_widget(button, index=0)
        # button.bind(on_press=app.manager.preproc_popup())
        self.add_widget(preproc_screen)
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



    def edgedetect_popup(ModalView):
        pass

    def hog_popup(ModalView):
        pass


MainApp().run()
