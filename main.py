from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.core.window import Window

# Импортируем класс страницы "О нас"
from about_page import AboutPage


class MainApp(MDApp):
    def build(self):
        # Главный layout
        self.root_layout = BoxLayout(orientation='vertical')

        # Панель инструментов
        self.toolbar = MDTopAppBar(
            title="Главная страница",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            elevation=10,
            md_bg_color=(0.2, 0.6, 0.8, 1),
            size_hint_y=None,
            height=dp(56)
        )

        # Контейнер для основного контента
        self.main_content = BoxLayout(orientation='vertical', size_hint_y=1)

        # Главная страница по умолчанию
        self.show_main_page()

        # Добавляем в корневой layout
        self.root_layout.add_widget(self.toolbar)
        self.root_layout.add_widget(self.main_content)

        # Навигационное меню
        self.create_navigation_drawer()

        return self.root_layout

    def show_main_page(self):
        """Показывает главную страницу"""
        self.main_content.clear_widgets()
        self.toolbar.title = "Главная страница"

        # Содержимое главной страницы
        content = MDLabel(
            text="Добро пожаловать в наше приложение!",
            halign='center',
            valign='middle',
            theme_text_color='Primary',
            font_style='H5'
        )
        self.main_content.add_widget(content)

    def show_about_page(self):
        """Показывает страницу 'О нас'"""
        self.main_content.clear_widgets()
        self.toolbar.title = "О нас"

        # Создаем экземпляр страницы "О нас"
        about_page = AboutPage()

        # Привязываем метод возврата
        about_page.go_back = lambda x: self.show_main_page()

        self.main_content.add_widget(about_page)

    def create_navigation_drawer(self):
        self.nav_drawer = MDNavigationDrawer(
            size_hint=(0.8, None),
            elevation=20,
            radius=(0, 16, 16, 0),
            state="close"
        )
        self.nav_drawer.height = Window.height - dp(56)

        drawer_content = BoxLayout(orientation='vertical', spacing=0)

        header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=[20, 15, 20, 10],
            spacing=8
        )
        header.add_widget(MDLabel(
            text="Меню",
            halign='center',
            theme_text_color='Primary',
            font_style='H4',
            size_hint_y=None,
            height=dp(40)
        ))
        header.add_widget(MDLabel(
            text="Добро пожаловать!",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body1',
            size_hint_y=None,
            height=dp(30)
        ))

        scroll = ScrollView(do_scroll_x=False)
        menu_list = MDList(spacing=1)
        menu_list.size_hint_y = None
        menu_list.bind(minimum_height=menu_list.setter('height'))

        menu_items = [
            "Главная", "О нас"
        ]

        for item in menu_items:
            list_item = OneLineListItem(
                text=item,
                on_release=lambda x, item=item: self.menu_item_clicked(item),
                theme_text_color="Primary",
                _no_ripple_effect=False,
                height=dp(56),
                size_hint_y=None
            )
            menu_list.add_widget(list_item)

        scroll.add_widget(menu_list)

        footer = BoxLayout(size_hint_y=None, height=dp(60), padding=[20, 10, 20, 15])
        close_button = MDRaisedButton(
            text="Закрыть",
            size_hint=(None, None),
            size=(dp(120), dp(48)),
            on_release=lambda x: self.nav_drawer.set_state('close')
        )
        footer.add_widget(BoxLayout())
        footer.add_widget(close_button)
        footer.add_widget(BoxLayout())

        drawer_content.add_widget(header)
        drawer_content.add_widget(scroll)
        drawer_content.add_widget(footer)

        self.nav_drawer.add_widget(drawer_content)
        self.root_layout.add_widget(self.nav_drawer)
        self.nav_drawer.set_state('close')

        Window.bind(on_resize=self.on_window_resize)

    def on_window_resize(self, window, width, height):
        if hasattr(self, 'nav_drawer'):
            self.nav_drawer.height = height - dp(56)

    def toggle_nav_drawer(self):
        if self.nav_drawer.state == 'open':
            self.nav_drawer.set_state('close')
        else:
            self.nav_drawer.set_state('open')

    def menu_item_clicked(self, item):
        print(f"Выбран пункт: {item}")
        self.nav_drawer.set_state('close')

        # Обработка выбора пунктов меню
        if item == "Главная":
            self.show_main_page()
        elif item == "О нас":
            self.show_about_page()


if __name__ == '__main__':
    MainApp().run()