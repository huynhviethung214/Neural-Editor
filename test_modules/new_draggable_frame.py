from kivy.app import App
from kivy.uix.stencilview import StencilView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.transformation import Matrix


class Frame(StencilView):
    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__()
        self.add_widget(Button(pos=(100, 100)))
        self.add_widget(Button(pos=(300, 300)))
        self.add_widget(Button(pos=(800, 800)))

        self.origin = ()
        self.damping_factor = 0.3

        self.bind(on_touch_down=self.set_origin)
        self.bind(on_touch_move=self.move)

    def set_origin(self, obj, touch):
        self.origin = self.to_local(*touch.pos)
        return True

    def move(self, obj, touch):
        local_pos = self.to_local(*touch.pos)

        for children in self.children:
            m = Matrix()
            vec = (local_pos[0] - self.origin[0], local_pos[1] - self.origin[1])

            m.translate(vec[0], vec[1], 0)
            children._apply_transform(m)

            # if newX >= 100 or newY >= 100:
            #     children.pos = (newX, newY)

        return True

    # def on_touch_up(self, touch):
    #     local_pos = self.to_local(*touch.pos)
    #
    #     for children in self.children:
    #         newX = (local_pos[0] - self.origin[0] + children.pos[0]) * self.damping_factor
    #         newY = (local_pos[1] - self.origin[1] + children.pos[1]) * self.damping_factor
    #
    #         if newX >= 100 or newY >= 100:
    #             children.pos = (newX, newY)
    #
    #     return True


class _app(App):
    def build(self):
        return Frame()


if __name__ == '__main__':
    _app().run()
