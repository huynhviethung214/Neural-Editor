import os
from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.widget import Widget

from utility.custom_input.custom_input import CustomTextInput

from utility.custom_tabbedpanel import TabManager
from utility.utils import get_obj


class ScriptingToolBar(BoxLayout):
    def __init__(self, **kwargs):
        super(ScriptingToolBar, self).__init__()
        self.size_hint_y = 0.05

        self.save_button = Button(size_hint_x=0.2, text='Save')
        self.open_file_button = Button(size_hint_x=0.2, text='Open File')
        self.save_as_button = Button(size_hint_x=0.2, text='Save As')

        self.save_button.bind(on_press=self.save)
        self.save_as_button.bind(on_press=self.save_as)
        self.open_file_button.bind(on_press=self.open_file)

        self.add_widget(Label(size_hint_x=0.4))
        self.add_widget(self.save_button)
        self.add_widget(self.open_file_button)
        self.add_widget(self.save_as_button)

    def file_info(self):
        current_tab = get_obj(self, 'TabManager').current_tab
        file_name = current_tab.text
        file_content = current_tab.content.text

        return current_tab, file_name, file_content

    def save(self, obj):
        # CHOOSE FILE PATH IN THE FUTURE
        current_tab, file_name, file_content = self.file_info()

        if file_name + '.py' not in os.listdir('algorithms'):
            save_popup = SavePopup(file_name=current_tab.text,
                                   file_content=file_content,
                                   parent=self,
                                   link_type=1)
            save_popup.open()

        else:
            file_path = 'algorithms\\{0}'.format(file_name + '.py')
            with open(file_path, 'w') as f:
                f.write(file_content)

    def save_as(self, obj):
        current_tab, file_name, file_content = self.file_info()

        save_popup = SavePopup(file_name=file_name,
                               file_content=file_content,
                               obj=current_tab,
                               link_type=0)
        save_popup.open()

    def open_file(self, obj):
        file_chooser = _FileChooser(tab_manager=get_obj(self, 'TabManager'),
                                    root_path='algorithms')
        file_chooser.open()


class Editor(BoxLayout):
    def __init__(self, **kwargs):
        super(Editor, self).__init__()
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 5

        # print('err')
        self.tab_manager = TabManager(func=CodeInput,
                                      default_name='New File',
                                      _fkwargs={'text': ''})
        # self.tab_manager.add_tab(func_name='New File',
        #                          _fkwargs={'text': ''})

        self.tool_bar = ScriptingToolBar()

        self.add_widget(self.tab_manager)
        self.add_widget(self.tool_bar)


# SAVE NOTIFICATION WHENEVER WE CLOSE AN UNSAVED FILE
# class CloseButton(Button):
# 	def __init__(self, **kwargs):
# 		super(CloseButton, self).__init__()
# 		self.size_hint_x = 0.15
# 		self.border = (0, 0, 0, 0)
# 		self.root = kwargs.get('root')
# 		self.text = 'X'

# 	def on_press(self):
# 		self.root.tab_name_list.remove(self.parent.text)

# 		if len(self.root.tab_list) == 1:
# 			self.root.remove_widget(self.parent)
# 			self.root.add_tab()

# 		else:
# 			index = self.root.tab_list.index(self.root.current_tab)
# 			self.root.remove_widget(self.parent)

# 			if self.root.current_tab == self.parent:
# 				self.root.switch_to(self.root.tab_list[index])


# class CustomHeader(BoxLayout, TabbedPanelHeader):
# 	def __init__(self, **kwargs):
# 		super(CustomHeader, self).__init__()
# 		self.text = kwargs.get('fname')
# 		self.padding = 2
# 		self.spacing_obj = Label(size_hint_x=0.85)

# 		self.add_widget(self.spacing_obj)
# 		self.add_widget(CloseButton(root=kwargs.get('root')))


class _FileChooser(Popup):
    def __init__(self, size_hint=(0.6, 0.6), **kwargs):
        super(_FileChooser, self).__init__()
        self.tab_manager = kwargs.get('tab_manager')
        get_obj(self, 'FileChooserIconView').rootpath = kwargs.get('root_path')

        self.size_hint = size_hint
        self.title = 'File Chooser'

    # self.parent = kwargs.get('parent')

    # def get_obj(self, w_name):
    # 	for widget in self.walk_reverse(loopback=True):
    # 		if w_name in str(widget):
    # 			return widget

    def _submit(self):
        # DEAL WITH MULTIPLE FILES SELECTION
        # selection = self.children[-1].children[0].children[0].children[0].selection
        selection = get_obj(self, 'FileChooserIconView').selection

        try:
            with open(selection[0], 'r') as f:
                file_content = f.read()

            self.tab_manager.add_tab(func_name=selection[0].split('\\')[-1],
                                     _fkwargs={'text': file_content})

        except AttributeError as e:
            raise e


class SavePopup(Popup):
    def __init__(self, **kwargs):
        super(SavePopup, self).__init__()
        self.size_hint = (0.8, 0.7)

        self.file_name = kwargs.get('file_name')
        self.file_content = kwargs.get('file_content')
        self._type = kwargs.get('link_type')
        self.current_tab = kwargs.get('obj')

        self.title = 'Save Form'
        self.current_path = 'D:\\Python Projects\\Project Alpha\\Neural Editor\\algorithms'

        self.main_layout = BoxLayout(orientation='horizontal',
                                     spacing=5)

        self.sub_layout = BoxLayout(orientation='vertical',
                                    spacing=5,
                                    size_hint=(0.4, 1))

        self.save_button = Button(text='Confirm',
                                  size_hint_y=0.05)
        self.save_button.bind(on_press=self.save)

        self.file_chooser = FileChooserIconView(size_hint=(0.6, 1),
                                                dirselect=True,
                                                path=self.current_path)
        self.file_chooser.bind(on_touch_up=self.select_path)

        self.selected_path_label = Label(text=self.current_path,
                                         size_hint=(1, 0.05))

        self.file_name_input = CustomTextInput(size_hint=(1, 0.05),
                                               text=self.file_name,
                                               multiline=False,
                                               max_length=50)
        self.file_name_input.bind(text=lambda obj, value: setattr(self,
                                                                  'file_name',
                                                                  value))

        self.sub_layout.add_widget(self.selected_path_label)
        self.sub_layout.add_widget(self.file_name_input)
        self.sub_layout.add_widget(self.save_button)
        self.sub_layout.add_widget(Widget(size_hint=(1, 0.9)))

        self.main_layout.add_widget(self.file_chooser)
        self.main_layout.add_widget(self.sub_layout)
        self.add_widget(self.main_layout)

        # self.children[-1].children[0].children[0].children[1].text = self.default_name
        # self.children[-1].spacing = 4

    def select_path(self, obj, touch):
        if self.file_chooser.selection:
            selected = self.file_chooser.selection[0]
            if self.file_chooser.file_system.is_dir(selected):
                self.selected_path_label.text = self.current_path = selected

    def save(self, obj):
        with open(self.current_path + f'\\{self.file_name}', 'w') as f:
            f.write(self.file_content)
        self.current_tab.text = self.file_name

        self.dismiss()

# class TabManager(TabbedPanel):
# 	def __init__(self, **kwargs):
# 		super(TabManager, self).__init__()
# 		self.size_hint_y = 0.95
# 		self.do_default_tab = False
# 		self.tab_pos = 'top_left'
# 		self.tab_height = 30
# 		self.tab_width = 200
# 		self.tab_name_list = []

# 		self.add_tab()

# 	def add_tab(self, fname='New File', fcontent=''):
# 		if fname not in self.tab_name_list:
# 			header = CustomHeader(fname=fname, root=self)
# 			header.content = CodeInput(text=fcontent)
# 			self.add_widget(header)
# 			Clock.schedule_once(lambda *args: self.switch_to(header))
# 			self.tab_name_list.append(fname)
