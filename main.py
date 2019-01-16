# fullscreen
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

# local libraries
from edge_detect_ani import EdgeDetect
from preprocessing_ani import Preproc_Anim
from faceDetect import KivyCamera

# root_widget = Builder.load_file('main.kv')


class MainApp(App):

    def goto_preproc_screen(self):
        pass
    def goto_edgedetect_screen(self):
        pass
    def goto_cam_screen(self):
        pass

    def build(self):
        self.manager = ScreenManager()

        cam_view = KivyCamera()
        cam_screen = Screen(name='camScreen')
        cam_screen.on_enter(cam_view.start())
        cam_screen.on_pre_leave(cam_view.stop())
        cam_screen.add_widget(cam_view)
        self.manager.add_widget(cam_screen)

        preproc = Preproc_Anim()
        preproc_screen = Screen(name='preprocScreen')
        preproc_screen.add_widget(preproc)
        self.manager.add_widget(preproc_screen)

        edge_det = EdgeDetect()
        edge_det_screen = Screen(name='edgeScreen')
        edge_det_screen.add_widget(edge_det)
        self.manager.add_widget(edge_det_screen)

        Clock.schedule_once(self.screen_switch_one, 2)
        Clock.schedule_once(self.screen_switch_two, 4)
        Clock.schedule_once(self.screen_switch_three, 6)
        Clock.schedule_once(self.screen_switch_one, 8)

        layout = FloatLayout()
        layout.add_widget(self.manager)
        return layout

    def screen_switch_one(self, dt):
        self.manager.current = 'camScreen'
    def screen_switch_two(self, dt):
        self.manager.current = 'preprocScreen'
    def screen_switch_three(self, dt):
        self.manager.current = 'edgeScreen'

MainApp().run()
