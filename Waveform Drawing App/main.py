import kivy
from kivy.app import App
from kivy.app import Widget
from kivy.graphics import *


class SampleSlider(Widget):
    def __init__(self, **kwargs):
        super(SampleSlider, self).__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_move(self, touch):
        print("Mouse moved to", touch.pos)


class SamplerApp(App):
    pass


kv = SamplerApp()
kv.run()
