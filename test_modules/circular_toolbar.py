from kivy.app import runTouchApp
from kivy.animation import Animation, AnimationTransition
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class b1(AnchorLayout):
	def __init__(self, **kwargs):
		super(b1, self).__init__()
		self.anchor_y = 'bottom'
		self.anchor_x = 'right'
		self.opacity = 0
		self.di = 6
		self.add_widget(Button(text='b1',
							size_hint=(None, None),
							width=100,
							height=100))


class b2(AnchorLayout):
	def __init__(self, **kwargs):
		super(b2, self).__init__()
		self.anchor_y = 'bottom'
		self.anchor_x = 'left'
		self.opacity = 0
		self.di = 8
		self.add_widget(Button(text='b2',
							size_hint=(None, None),
							width=100,
							height=100))


class b3(AnchorLayout):
	def __init__(self, **kwargs):
		super(b3, self).__init__()
		self.anchor_y = 'top'
		self.anchor_x = 'left'
		self.opacity = 0
		self.di = 2
		self.add_widget(Button(text='b3',
							size_hint=(None, None),
							width=100,
							height=100))


class b4(AnchorLayout):
	def __init__(self, **kwargs):
		super(b4, self).__init__()
		self.anchor_y = 'top'
		self.anchor_x = 'right'
		self.opacity = 0
		self.di = 4
		self.add_widget(Button(text='b4',
							size_hint=(None, None),
							width=100,
							height=100))


class b5(AnchorLayout):
	def __init__(self, **kwargs):
		super(b5, self).__init__()
		self.anchor_y = 'center'
		self.anchor_x = 'center'
		self.opacity = 0
		self.di = 7
		self.add_widget(Button(text='b5',
							size_hint=(None, None),
							width=100,
							height=100))


class b6(AnchorLayout):
	def __init__(self, **kwargs):
		super(b6, self).__init__()
		self.anchor_y = 'center'
		self.anchor_x = 'center'
		self.opacity = 0
		self.di = 3
		self.add_widget(Button(text='b6',
							size_hint=(None, None),
							width=100,
							height=100))


class b7(AnchorLayout):
	def __init__(self, **kwargs):
		super(b7, self).__init__()
		self.anchor_y = 'center'
		self.anchor_x = 'left'
		self.opacity = 0
		self.di = 1
		# self.size_hint = (None, None)
		self.add_widget(Button(text='b7',
							size_hint=(None, None),
							width=100,
							height=100))


class b8(AnchorLayout):
	def __init__(self, **kwargs):
		super(b8, self).__init__()
		self.anchor_y = 'center'
		self.anchor_x = 'right'
		# self.size_hint = (None, None)
		self.opacity = 0
		self.di = 5
		self.add_widget(Button(text='b8',
							size_hint=(None, None),
							width=100,
							height=100))


class gridlayout(GridLayout):
	def __init__(self, **kwargs):
		super(gridlayout, self).__init__()
		self.rows = 3
		self.cols = 3
		self.opacity = 0

		self.add_widget(b1())
		self.add_widget(b5())
		self.add_widget(b2())
		self.add_widget(b8())
		self.add_widget(middle_label())
		self.add_widget(b7())
		self.add_widget(b4())
		self.add_widget(b6())
		self.add_widget(b3())


class middle_label(AnchorLayout):
	def __init__(self, **kwargs):
		super(middle_label, self).__init__()
		# self.size_hint = (None, None)
		self.anchor_y = 'center'
		self.anchor_x = 'center'
		# self.size_hint = (None, None)
		# self.opacity = 0
		self.di = 0
		# self.butt = Button(text='test_button',
		# 					size_hint=(None, None),
		# 					width=100,
		# 					height=100)
		self.label = Label(text='test_button',
							size_hint=(None, None),
							width=100,
							height=100)
		self.add_widget(self.label)
		# self.butt.bind(on_press=lambda val: print('Test'))

	# def on_touch_down(self, pos):
	# 	if self.collide_point(*pos.pos):
	# 		print('Test1')

	# 	self.opacity = 0
	# 	self.disabled = True

	# def on_press(self):
	# 	# print('pressed')
	# 	if self.opacity == 0:
	# 		pass
	# 	else:
	# 		print('pressed')


class custom_button(Image, ButtonBehavior):
	def __init__(self, **kwargs):
		super(custom_button, self).__init__()

from kivy.clock import Clock


class plane(AnchorLayout):
	def __init__(self, **kwargs):
		super(plane, self).__init__()
		self.size_hint= (1, 1)
		self.anchor_x = 'center'
		self.anchor_y = 'center'
		self.anim = Animation(opacity=1)
		# self.add_widget(Button(text='Test',
		# 						size_hint=(None, None),
		# 						width=100,
		# 						height=100,
		# 						opacity=0)) #USING OPACITY TO ACHIEVE DESIRE EFFECT
		# self.add_widget(test_button())
		self.add_widget(gridlayout())
		self.anim.start(self.children[0])
		# self.anim.cancel(self.children[0])
		Clock.schedule_once(self.test, 2.5)

	def test(self, dt):
		self.anim.cancel(self.children[0])

	# def on_touch_down(self, touch):
	# 	if self.collide_point(*touch.pos) and self.children[0].opacity == 0:
	# 		# print(touch.is_double_tap)
	# 		# self.children[0].opacity = 1
	# 		self.anim.start(self.children[0])

# runTouchApp(plane())

t = [['bottom', 'right', 6],
['center', 'center', 7],
['bottom', 'left', 8],
['center', 'right', 5],
['center', 'center', 0],
['center', 'left', 1],
['top', 'right', 4],
['center', 'center', 3],
['top', 'left', 2]]

# print(t)


class _template(AnchorLayout):
	def __init__(self, **kwargs):
		super(_template, self).__init__()
		self.di = kwargs.get('di')
		self.name = kwargs.get('name')
		self.opacity = 0
		self.anchor_x = kwargs.get('anchor_x')
		self.anchor_y = kwargs.get('anchor_y')

		if self.di != 0:
			self.button = Button(text=self.name,
								width=100,
								height=100,
								size_hint=(None, None))
			self.button.bind(on_press=self._change)
			self.add_widget(self.button)

		else:
			self.label = Label(text='test_button',
							size_hint=(None, None),
							width=100,
							height=100)
			self.opacity = 1
			self.add_widget(self.label)

	def _change(self, obj):
		self.parent.children[4].children[0].text = self.name
		# self.parent.parent.reverse_animation()
		# print(self.parent.parent)
		self.parent.parent.anim.start(self.parent.children[3])
		# self.parent.parent.anim1.bind(on_complete=self.parent.parent.reverse_animation)


# THERE WILL BE TWO TYPES OF BUTTON: (FUNCTION TYPE) AND (CATEGORY TYPE)
# CATEGORY TYPE: DISPLAY FUNCTIONS WITHIN ITSEFT LIKE A MENU OF FUNCTIONS
# FUNCTION TYPE: USING FOR TRIGGER AN EVENT OF SOME SORT OR AN ACTION THAT THE CREATOR WANT
# ADDING (CATEGORY TYPE) OR (FUNCTION TYPE) TO THE MENU (AKA CIRCULAR MENU)

class test_grid(GridLayout, Widget):
	def __init__(self, **kwargs):
		super(test_grid, self).__init__()
		self.cols = 3
		self.rows = 3
		self._class = 'category'
		self._list = []
		self.opacity = 0
		self.add_buttons()

	def add_buttons(self):
		for i, info in enumerate(t):
			self.add_widget(_template(di=info[2],
									name=str(i),
									anchor_y=info[0],
									anchor_x=info[1]))

	def add_custom_buttons(self):
		pass


class subclass(AnchorLayout, Widget):
	def __init__(self, **kwargs):
		super(subclass, self).__init__()
		self.size_hint = (1, 1)
		self.anchor_x = 'center'
		self.anchor_y = 'center'

		self.anim_list = [Animation(opacity=1, duration=0.6),
						Animation(opacity=0, duration=0.6)]
		self.anim = self.anim_list[0]
		self.index = 1

		self.grid = test_grid()
		self.add_widget(self.grid)

		self.anim_list[0].bind(on_complete=self._animation)
		self.anim_list[1].bind(on_complete=self._animation)

	def choose_grid(self, grid):
		self.grid = grid

	def _animation(self, animation, obj):
		try:
			for child in self.grid.children:
				if child.di == self.index and child.di != (0 and 1):
					self.anim.start(child)
					self.index += 1
					break

				if self.index == 9:
					raise IndexError

		except IndexError as e:
			self.index = 1
			self.anim = self.anim_list[1]


class layout(GridLayout, Widget):
	def __init__(self, **kwargs):
		super(layout, self).__init__()
		self.rows = 3
		self.cols = 3
		self.is_displayed = 0
		self.add_widget(subclass())

	def on_touch_up(self, touch):
		if self.collide_point(*touch.pos):
			if self.is_displayed == 0:
				self.children[0].grid.opacity = 1
				self.children[0].anim.start(self.children[0].grid.children[4])
				self.is_displayed = 1
				
			else:
				self.children[0].grid.opacity = 0
				for child in self.children[0].grid.children:
					child.opacity = 0
				self.is_displayed = 0
				self.children[0].index = 1
				self.children[0].anim = self.children[0].anim_list[0]


runTouchApp(layout())