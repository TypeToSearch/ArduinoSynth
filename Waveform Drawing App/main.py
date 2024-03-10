import kivy
from kivy.app import App
from kivy.app import Widget
from kivy.graphics import *


class SampleSlider(Widget):
    def __init__(self, num_sliders=1, default=0.5, minimum=0, maximum=1, **kwargs):
        super(SampleSlider, self).__init__(**kwargs)
        self.tracks = []
        # Create slider tracks
        with self.canvas:
            Color(0.83, 0.83, 0.83)
            for i in range(num_sliders):
                size = (self.size[0] / num_sliders, self.size[1])
                position = (self.pos[0] + (size[0] * i), self.pos[1])
                self.tracks.append(Rectangle(pos=position, size=size))
                Color(0, 0, 1)

        self.bind(pos=self.update_rect, size=self.update_rect)

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
