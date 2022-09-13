from kivy.clock import Clock
from kivy.graphics import Bezier, Line, Color
from kivy.uix.widget import Widget

from utility.rightclick_toolbar.rightclick_toolbar import RightClickMenu
from utility.utils import get_obj


class BoundingBox:
    def __init__(self, x0, y0, x1, y1, offset_y, offset_x):
        self.offset_y = offset_y
        self.offset_x = offset_x

        self.x0 = x0 - self.offset_x
        self.y0 = y0 - self.offset_y

        self.x1 = x1 + self.offset_x
        self.y1 = y1 + self.offset_y

    def get_bbox_coord(self):
        return [self.x0, self.y0, self.x1, self.y0,
                self.x1, self.y1, self.x0, self.y1,
                self.x0, self.y0]


class CustomBezier(Widget):
    def __init__(self, points, segments, **kwargs):
        super(CustomBezier, self).__init__(**kwargs)
        self.begin = None
        self.end = None
        self.debug = False

        self.bbox_offset_y = 40
        self.bbox_offset_x = 30

        self.segments = segments
        self.bounding_boxes = []

        self.r = 1
        self.g = 1
        self.b = 1

        self.rightclick_menu = {
            'Delete Connection': self.delete_connection
        }

        with self.canvas:
            self.bezier = Bezier(points=points,
                                 segments=self.segments)

        self.trigger = Clock.create_trigger(self.redraw_bezier)

        self._points = self.bezier.points
        self.set_bounding_boxes()

    def delete_connection(self, obj):
        interface = get_obj(self, 'Interface')
        interface.remove_bezier(self)
        return True

    def set_bezier_color_cyan(self):
        self.r = 0
        self.g = 1
        self.b = 1

    def set_bezier_color_white(self):
        self.r = 1
        self.g = 1
        self.b = 1

    def set_bezier_color(self, color: str):
        if color == 'white':
            self.set_bezier_color_white()
        else:
            self.set_bezier_color_cyan()
        self.redraw_bezier(-1)

    def set_bounding_boxes(self):
        self.bounding_boxes = [
            BoundingBox(*self._points[0:4],
                        self.bbox_offset_y,
                        self.bbox_offset_x),
            BoundingBox(*self._points[2:6],
                        self.bbox_offset_y,
                        self.bbox_offset_x),
            BoundingBox(*self._points[4:8],
                        self.bbox_offset_y,
                        self.bbox_offset_x)
        ]

    def clear_canvas(self):
        for ins in self.canvas.children:
            if type(ins) == Bezier and ins.points != self._points:
                self.canvas.children.remove(ins)
            if type(ins) == Line and [*ins.points] != [*self._points]:
                self.canvas.children.remove(ins)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, _points):
        self._points = _points
        self.set_bounding_boxes()
        self.trigger()

    @staticmethod
    def check_bezier_collision(bounding_box: BoundingBox, pos):
        if (bounding_box.x0 < pos[0] < bounding_box.x1) and (bounding_box.y0 < pos[1] < bounding_box.y1) or \
                (bounding_box.x0 < pos[0] < bounding_box.x1) and (bounding_box.y1 < pos[1] < bounding_box.y0):
            return True
        return False

    def redraw_bezier(self, dt):
        self.clear_canvas()

        with self.canvas:
            Color(self.r, self.g, self.b)
            self.bezier = Bezier(points=self._points,
                                 segments=self.segments)
            Color(1, 1, 1)

            if self.debug:
                for bbox in self.bounding_boxes:
                    Line(points=bbox.get_bbox_coord())

    def collide_point(self, x, y):
        x, y = self.to_local(x, y)

        for bbox in self.bounding_boxes:
            if self.check_bezier_collision(bbox, (x, y)):
                return True
        return False

    def on_touch_down(self, touch):
        overlay = get_obj(self, 'Overlay')

        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.set_bezier_color('cyan')
                menu = RightClickMenu(pos=overlay.to_overlay_coord(touch, self),
                                      button_width=140,
                                      funcs=self.rightclick_menu)
                overlay.open_menu(menu)
            else:
                self.set_bezier_color('white')
                overlay.clear_menu()
            return True
        else:
            self.set_bezier_color('white')
            return False
