from functools import partial

from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, StripLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from time import sleep


class TabManager(TabbedPanel):
    def __init__(self, default_tab=True, **kwargs):
        super(TabManager, self).__init__()
        self.do_default_tab = False
        self.tab_pos = 'top_left'
        self.tab_height = 30
        self.tab_width = 200

        # Format: `Tab's name`: [0, 1, 2, 3, ... (index of tab)]
        self.tab_dict = {}

        self.default_name = kwargs.get('default_name')
        self.fkwargs = kwargs.get('_fkwargs')

        self.func = kwargs.get('func')

        if default_tab:
            self.add_tab(func_name=self.default_name,
                         _fkwargs=self.fkwargs)

        add_button_layout = BoxLayout()
        add_button = Button(text='+',
                            size_hint_x=0.2,
                            background_down=Button().background_normal)
        add_button.bind(on_press=lambda obj: self.add_tab(func_name=self.default_name,
                                                          _fkwargs=self.fkwargs))

        add_button_layout.add_widget(Label(size_hint_x=0.8))
        add_button_layout.add_widget(add_button, 1)
        self._tab_strip.add_widget(add_button_layout)

    def get_tabs_name(self):
        tabs_name = []

        for tab in self.tab_list:
            if type(tab) == CustomHeader:
                tabs_name.append(tab.text)

        return tabs_name

    @staticmethod
    def get_missing_idx(list_of_index):
        list_of_index = sorted(list_of_index)

        for i in range(max(list_of_index) - 1):
            if list_of_index[i + 1] - list_of_index[i] != 1:
                return i + 1

        if 0 not in list_of_index:
            return 0

        return len(list_of_index)

    def add_tab(self, **fkwargs):
        func_name = fkwargs.get('func_name')
        _fkwargs = fkwargs.get('_fkwargs')
        missing_idx = 0

        # tabs_name = self.get_tabs_name()

        if func_name not in list(self.tab_dict.keys()):
            self.tab_dict.update({func_name: [0]})
        else:
            missing_idx = self.get_missing_idx(self.tab_dict[func_name])
            self.tab_dict[func_name].insert(missing_idx, missing_idx)

        func_name = f'{func_name} {missing_idx}'

        header = CustomHeader(func_name=func_name,
                              tabbed_panel=self,
                              _fkwargs=_fkwargs)
        # print(func_name, _fkwargs)
        header.content = self.func(**_fkwargs)

        self.add_widget(header, len(self.children) - 1)

        # Wait for the newly created header to be initialized
        # Switch to the newly created header 1 frame after the header is being initialized
        Clock.schedule_once(partial(self.switch, header), 0)
        # self.tab_name_list.append(func_name)

    # Let the widget initiate completely and then add your tabs
    def switch(self, header, *args):
        self.switch_to(header)


class CloseButton(Button):
    def __init__(self, **kwargs):
        super(CloseButton, self).__init__()
        self.size_hint_x = 0.15
        self.border = (0, 0, 0, 0)
        self.tabbed_panel = kwargs.get('tabbed_panel')
        self.text = 'x'

        self.header_name = kwargs.get('header_name')
        self._fkwargs = kwargs.get('_fkwargs')

    def switch(self, header, *args):
        self.tabbed_panel.switch_to(header)

    def on_press(self):
        # print(self.parent.text, self.tabbed_panel.tab_name_list)
        # self.tabbed_panel.tab_name_list.remove(self.parent.text)
        tab_name = self.parent.text[:-2]
        tab_idx = self.parent.text[-1]

        self.tabbed_panel.tab_dict[tab_name].remove(int(tab_idx))

        if len(self.tabbed_panel.tab_list) == 2:
            self.tabbed_panel.remove_widget(self.parent)
            self.tabbed_panel.add_tab(func_name=self.header_name,
                                      _fkwargs=self._fkwargs)

        elif len(self.tabbed_panel.tab_list) > 2:
            if self.tabbed_panel.current_tab == self.parent:
                widgets = list(self.tabbed_panel.tab_list)
                widgets.reverse()

                index = widgets.index(self.parent)

                if index == 0:
                    self.tabbed_panel.remove_widget(self.parent)
                    self.tabbed_panel.switch_to(widgets[index + 1])
                else:
                    self.tabbed_panel.remove_widget(self.parent)
                    self.tabbed_panel.switch_to(widgets[index - 1])
            else:
                self.tabbed_panel.remove_widget(self.parent)

        return True


class CustomHeader(BoxLayout, TabbedPanelHeader):
    def __init__(self, **kwargs):
        super(CustomHeader, self).__init__()
        self.text = kwargs.get('func_name')
        # print(self.text)
        self.padding = 2
        self.spacing_obj = Label(size_hint_x=0.7)
        self.close_button = CloseButton(tabbed_panel=kwargs.get('tabbed_panel'),
                                        _fkwargs=kwargs.get('_fkwargs'),
                                        header_name=self.text)

        self.add_widget(self.spacing_obj)
        self.add_widget(self.close_button)
        # self.add_widget(Button(text='+',
        #                        size_hint_x=0.15))

    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos) and touch.is_double_tap:
    #         self.remove_widget(self.spacing_obj)
    #         self.remove_widget(self.close_button)
    #         
    #         self.add_widget(TextInput())
    #         self.add_widget(self.close_button)
    #     
    #     return True
