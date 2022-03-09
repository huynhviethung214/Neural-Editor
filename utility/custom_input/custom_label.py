from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout


class CustomLabel(BoxLayout):
    def __init__(self, size_hint=(0.4, 1), **kwargs):
        super(CustomLabel, self).__init__()
        self.size_hint = size_hint

        self.label = Label(**kwargs,
                           size_hint=(1, 1))
        self.add_widget(self.label)
