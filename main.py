#!/usr/bin/env python3
# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
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

class More_Button(ButtonBehavior, Image):
    pass

class CircleButton(ButtonBehavior, Widget):
    color = ListProperty([1., 1., 1.])
    make_bigger = BooleanProperty(True)
    button_more = ObjectProperty()
    button_more_x = 349
    button_more_y= 270

    text_label_x = None
    text_label_y = None
    # app = App.get_running_app().root
    target = None
    # origin_pos = ListProperty()
    # animated_pos = ListProperty()
    # size_bigger = NumericProperty(300)
    is_animating = BooleanProperty()
    name = StringProperty()
    title = StringProperty()
    edgedet_text ="Während der Kantendetektion wird versucht, flächige Bereiche auf einem Bild voneinander zu trennen, wenn sie sich ausreichend in Farb- oder Grauwert, Helligkeit oder Textur voneinander unterscheiden."
    preproc_text = "Bei vielen Aufgaben der Computer Vision ist es hilfreich, die Schärfe des Bildes zu reduzieren (weichzeichnen), das Bild enstprechend skalieren und diese verschiedenen Schärfegrade separat zu analysieren."
    hog_text = "Anhand der zuvor berechneten Bilder wird mithilfe eines Convolutional Neural Networks, einem Tool zur Klassifizierung von Daten, Objekte auf Bildern zu erkennen"
    cam_text= "Der gesamte Prozess der Gesichtserkennung wird nun anhand Live-Bildern des Ausstellungsraums visualisiert. "

    def __init__(self, **kwargs):
        super(CircleButton, self).__init__(**kwargs)
        self.app = App.get_running_app()
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
        self.camt_label = Label(size_hint=(None, None),
                                   width=326, height=170,
                                   x=23,
                                   y=100,
                                   text=self.cam_text,
                                   font_size='18sp',
                                   text_size=(326, 170),
                                   valign='top')
        # button_pos_tl = (279, Window.height-270)
        # button_pos_tr = ()
        # self.button_more = More_Button()

        # mehr-button positionen: tr = 1847, 277 (w: 71.77 h: 20)
        # bl: 309, 1010
        # br: 1847, 1010,
        # tl: 279, 270 (290)
        # self.preproc_text = Label(size_hint=(None, None), width=326, height=170, x=25, y=100)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Touched!!!")
            print("CircleButton {} touched at {}".format(self.name, touch.pos))
            self.trigger_action()
        elif self.button_more:
            print("Button!!! {}".format(self.button_more.pos))
            if self.button_more.collide_point(*touch.pos):
                print("Button Touched!!!")
                self.button_more.trigger_action()
        elif not self.make_bigger:
            self.toggle_button_behavior()


        return super(CircleButton, self).on_touch_down(touch)

    def open_hogScreen(self, touch):
        self.app.manager.current = 'hogScreen'

    def open_camScreen(self, touch):
        self.app.manager.current = 'camScreen'

    def open_edgedetScreen(self, touch):
        self.app.manager.current = 'edgeScreen'

    def open_preprocScreen(self, touch):
        self.app.manager.current = 'preprocScreen'

    def toggle_button(self, anim, widget):
        self.is_animating = not self.is_animating
        if not self.is_animating and not self.make_bigger:
            self.ids.circle_title.font_size = '24sp'

            if self.name == 'tl':
                self.button_more= More_Button(right=self.preproc_label.right, top=Window.height-self.button_more_y)
                # self.button_more= More_Button(x=self.button_more_x, top=Window.height-self.button_more_y)
                self.target = self.open_preprocScreen
                self.add_widget(self.preproc_label)
            elif self.name == 'br':
                self.button_more = More_Button(x=self.facedet_label.x, y=self.button_more_y)
                # self.button_more = More_Button(right=Window.width-self.button_more_x, y=self.button_more_y)
                self.target = self.open_hogScreen
                self.add_widget(self.facedet_label)
            elif self.name == 'tr':
                self.button_more = More_Button(x=self.edgedet_label.x, top=Window.height-self.button_more_y)
                # self.button_more = More_Button(right=Window.width-self.button_more_x, top=Window.height-self.button_more_y)
                self.add_widget(self.edgedet_label)
                self.target = self.open_edgedetScreen
            elif self.name =='bl':
                self.button_more = More_Button(right=self.preproc_label.right, y=self.button_more_y)
                # self.button_more = More_Button(x=self.button_more_x, y=self.button_more_y)
                self.target = self.open_camScreen
            self.add_widget(self.button_more)
            self.button_more.bind(on_press=self.target)


        elif self.is_animating and self.make_bigger:
            self.ids.circle_title.font_size = '18sp'
            self.remove_widget(self.button_more)
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


class PreprocScreen(Screen):
    preproc = ObjectProperty()
    # def on_touch_down(self, touch):
    #     print("PreprocScreen(Screen) touched at {}".format(touch.pos))
    #     # return super(PreprocScreen, self).on_touch_down(touch)
    #     return True
    # def build(self):
    # def __init__(self, **kwargs):
    #     super(PreprocScreen, self).__init__(**kwargs)
    #     self.app = App.get_runing_app()
    #

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

    # def build_stuff(self):
    #     self.app = App.get_running_app()
    #     preproc = Preproc_Anim()
    #     menu = Menu()
    #     button = Button(size_hint=(None, None),
    #                          center=(Window.width/2, Window.height/4),
    #                          text="open popup")
    #
    #     preproc_screen = Screen(name="preprocScreen")
    #     preproc_screen.add_widget(menu, index=0)
    #     preproc_screen.add_widget(preproc, index=2)
    #     preproc_screen.add_widget(button, index=0)
    #     button.bind(on_press=self.app.manager.preproc_popup())
    #     self.add_widget(preproc_screen)
    #     self.add_widget(CamScreen(name="camScreen"))
    #     self.add_widget(EdgedetScreen(name="edgeScreen"))
    #     self.add_widget(HogScreen(name="hogScreen"))

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
