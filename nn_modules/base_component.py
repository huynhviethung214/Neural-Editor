from kivy.uix.treeview import TreeViewLabel
from utility.utils import get_obj


class Component(TreeViewLabel):
	def __init__(self, **kwargs):
		super(Component, self).__init__()
		# self.interface = get_obj(self, 'TabManager')
		
	# def generate_obj(self):
	# 	return type(self.text,
	# 				(self._attachment,),
	# 				{})

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			interface = get_obj(self, 'TabManager').current_tab.content.children[-1]
			
			interface._node = self.attachment
			interface._state = 1

		return True
