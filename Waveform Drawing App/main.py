import kivy
from kivy.app import App
from kivy.app import Widget


class SampleSlider(Widget):
    def on_touch_move(self, touch):
        print("Mouse moved to", touch.pos)


class SamplerApp(App):
    pass


kv = SamplerApp()
kv.run()
