from kivy.clock import Clock
from kivy.graphics import Bezier, Line
from kivy.uix.widget import Widget


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

        self.bbox_offset_y = 40
        self.bbox_offset_x = 30

        self.segments = segments
        self.bounding_boxes = []

        self.debug = False

        with self.canvas:
            self.bezier = Bezier(points=points,
                                 segments=self.segments)

        self._points = self.bezier.points
        self.trigger = Clock.create_trigger(self.redraw_bezier)

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
            self.bezier = Bezier(points=self._points,
                                 segments=self.segments)

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
        if self.collide_point(*touch.pos):
            print('Collide')
