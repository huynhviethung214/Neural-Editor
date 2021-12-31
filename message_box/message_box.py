from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class MessageBox(Popup):
    def __init__(self, message='', message_type='Error Message'):
        super(MessageBox, self).__init__()
        self.size_hint = (0.3, 0.2)
        self.title = message_type

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text=message))

        self.cancel_button = Button(text='Cancel',
                                    size_hint_y=0.2)
        self.cancel_button.bind(on_press=lambda obj: self.dismiss())

        self.layout.add_widget(self.cancel_button)
        self.add_widget(self.layout)
