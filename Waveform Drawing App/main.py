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
        self.first_touch_pos = (0, 0)

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
            size = (self.size[0] / self.num_sliders, 0)
            position = (self.pos[0] + (size[0] * i), self.pos[1] + self.size[1] / 2)
            self.slides[i].size = size
            self.slides[i].pos = position

    def to_local_index(self, x_pos):
        return math.floor(x_pos / (self.width / self.num_sliders))

    def to_local_height(self, y_pos):
        return math.floor(y_pos - (self.pos[1] + self.size[1] / 2))

    def on_touch_move(self, touch):
        """Implements linear interpolation to estimate position of sliders skipped because drag speed is too high"""
        ndx_dif = self.to_local_index((touch.pos[0])) - self.to_local_index(self.first_touch_pos[0])
        # If no difference between current index and last index, just set the size
        if ndx_dif == 0:
            self.set_size(touch.pos)
            return

        slope = (touch.pos[1] - self.first_touch_pos[1]) / ndx_dif
        direction = 1 if ndx_dif > 0 else -1  # Need to determine drag direction for iteration in range function
        for i in range(0, ndx_dif, direction):
            # Use linear interpolation to estimate skipped sliders
            x_pos = self.first_touch_pos[0] + (self.width / self.num_sliders) * i
            height = i * slope + self.first_touch_pos[1]
            self.set_size((x_pos, height))
        # Update first_touch_pos to use the current position which now has no gaps before it
        self.first_touch_pos = touch.pos

    def on_touch_down(self, touch):
        self.first_touch_pos = touch.pos  # Update first_touch_pos in case the user starts dragging
        self.set_size(touch.pos)

    def set_size(self, touch_pos: tuple):
        """Takes a touch position and sets the size of the slider at the appropriate index to the height indicated
        by that touch position.
        """
        slider_index = self.to_local_index(touch_pos[0])
        slider_height = self.to_local_height(touch_pos[1])
        if slider_height > self.height/2:
            slider_height = int(self.height/2)
        elif slider_height < -self.height/2:
            slider_height = int(-self.height/2)
        self.slides[slider_index].size = (self.slides[slider_index].size[0], slider_height)

    def get_values(self) -> list:
        """Returns a list containing the values of every slider in this element. The size of the list is equal to the
        num_sliders property. Each slider's value ranges from -(self.height/2) to +(self.height/2).
        """
        return [slider.size[1] for slider in self.slides]

    def get_scaled_values(self, max_magnitude=1.0) -> list:
        """Returns a list containing the values of every slider in this element, scaled as specified."""
        max_height = self.height / 2
        return [slider.size[1] / max_height * max_magnitude for slider in self.slides]


class SamplerApp(App):
    pass


kv = SamplerApp()
kv.run()
