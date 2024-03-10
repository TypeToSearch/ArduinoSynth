import kivy
from kivy.app import App
from kivy.app import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty


class SampleSlider(Widget):
    num_sliders = NumericProperty(1)

    def __init__(self, **kwargs):
        super(SampleSlider, self).__init__(**kwargs)
        self.tracks = []

        self.bind(num_sliders=self.initialize_tracks)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def initialize_tracks(self, *args):
        self.tracks = []
        with self.canvas:
            Color(0.83, 0.83, 0.83)
            for i in range(self.num_sliders):
                size = (self.size[0] / self.num_sliders, self.size[1])
                position = (self.pos[0] + (size[0] * i), self.pos[1])
                self.tracks.append(Rectangle(pos=position, size=size))

    def update_rect(self, *args):
        sliders = len(self.tracks)
        for i in range(sliders):
            size = (self.size[0] / sliders, self.size[1])
            position = (self.pos[0] + (size[0] * i), self.pos[1])
            self.tracks[i].size = size
            self.tracks[i].pos = position

    def on_touch_move(self, touch):
        print("Mouse moved to", touch.pos)


class SamplerApp(App):
    pass


kv = SamplerApp()
kv.run()
