from kivy.app import App
from kivy.app import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty
import math


class SampleSlider(Widget):
    num_sliders = NumericProperty(1)

    def __init__(self, **kwargs):
        super(SampleSlider, self).__init__(**kwargs)
        self.tracks = []
        self.slides = []

        self.bind(num_sliders=self.initialize_rects)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def initialize_rects(self, *args):
        with self.canvas:
            Color(0.83, 0.83, 0.83)
            self.tracks = [Rectangle() for i in range(self.num_sliders)]
            Color(0, 0, 1)
            self.slides = [Rectangle() for i in range(self.num_sliders)]

    def update_rect(self, *args):
        num = len(self.tracks)
        for i in range(num):
            size = (self.size[0] / num, self.size[1])
            position = (self.pos[0] + (size[0] * i), self.pos[1])
            self.tracks[i].size = size
            self.tracks[i].pos = position

        num = len(self.slides)
        for i in range(num):
            size = (self.size[0] / self.num_sliders, self.size[1] / 10)
            position = (self.pos[0] + (size[0] * i), self.pos[1] + self.pos[1] / 2)
            self.slides[i].size = size
            self.slides[i].pos = position

    def on_touch_move(self, touch):
        print("Mouse moved to", touch.pos)

    def on_touch_down(self, touch):
        # Get index of slider based on click position
        slider_index = math.floor(touch.pos[0] / (self.width / self.num_sliders))
        # Get height relative to the slides based on click position
        slider_height = math.floor(touch.pos[1] - (self.pos[1] + self.pos[1] / 2))
        print("Mouse click at index", slider_index)
        print("Mouse click at height", slider_height)


class SamplerApp(App):
    pass


kv = SamplerApp()
kv.run()
