from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.core.window import Window

# Импортируем классы страниц
from about_page import AboutPage
from select_task_page import SelectTaskPage
from theory_page import TheoryPage


class MainApp(MDApp):
    def build(self):
        # Главный layout - используем AnchorLayout для правильного позиционирования drawer
        self.root_layout = AnchorLayout()

        # Основной контейнер с контентом
        self.main_container = BoxLayout(orientation='vertical')
        self.root_layout.add_widget(self.main_container)

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

        # Добавляем в основной контейнер
        self.main_container.add_widget(self.toolbar)
        self.main_container.add_widget(self.main_content)

        # Навигационное меню
        self.create_navigation_drawer()

        return self.root_layout

    def show_main_page(self):
        """Показывает главную страницу с 3 блоками"""
        self.main_content.clear_widgets()
        self.toolbar.title = "Главная страница"

        # Создаем ScrollView для контента
        scroll_view = ScrollView(do_scroll_x=False)

        # Создаем контейнер для блоков
        content_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )

        # Устанавливаем высоту контента
        content_layout.height = dp(120) * 3 + dp(20) * 4  # 3 блока + отступы

        # Первый блок
        info_block1 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.9, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2
        )
        info_block1.add_widget(MDLabel(
            text="Теория",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        info_block1.add_widget(MDLabel(
            text="Изучите теоретические материалы перед выполнением заданий",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Второй блок
        info_block2 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.95, 0.98, 0.95, 1),
            radius=[dp(15)],
            elevation=2
        )
        info_block2.add_widget(MDLabel(
            text="Задания",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        info_block2.add_widget(MDLabel(
            text="Практикуйтесь на различных заданиях разного уровня сложности",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Третий блок
        info_block3 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(1, 0.95, 0.95, 1),
            radius=[dp(15)],
            elevation=2
        )
        info_block3.add_widget(MDLabel(
            text="О нас",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        info_block3.add_widget(MDLabel(
            text="Узнайте больше о нашем приложении и его возможностях",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Добавляем блоки в контейнер
        content_layout.add_widget(info_block1)
        content_layout.add_widget(info_block2)
        content_layout.add_widget(info_block3)

        scroll_view.add_widget(content_layout)
        self.main_content.add_widget(scroll_view)

    def show_about_page(self):
        """Показывает страницу 'О нас'"""
        self.main_content.clear_widgets()
        self.toolbar.title = "О нас"
        about_page = AboutPage(main_app=self)
        self.main_content.add_widget(about_page)

    def show_select_task_page(self):
        """Показывает страницу 'Выбрать задание'"""
        self.main_content.clear_widgets()
        self.toolbar.title = "Выбрать задание"
        select_task_page = SelectTaskPage(main_app=self)
        self.main_content.add_widget(select_task_page)

    def show_theory_page(self):
        """Показывает страницу 'Ознакомление с теорией'"""
        self.main_content.clear_widgets()
        self.toolbar.title = "Ознакомление с теорией"
        theory_page = TheoryPage(main_app=self)
        self.main_content.add_widget(theory_page)

    def create_navigation_drawer(self):
        self.nav_drawer = MDNavigationDrawer(
            size_hint=(0.8, 1),
            elevation=20,
            radius=(0, 16, 16, 0),
            state="close"
        )

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
            "Главная", "Выбрать задание", "Ознакомление с теорией", "О нас"
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

        # Добавляем drawer в корневой AnchorLayout (он будет поверх основного контента)
        self.root_layout.add_widget(self.nav_drawer)
        self.nav_drawer.set_state('close')

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
        elif item == "Выбрать задание":
            self.show_select_task_page()
        elif item == "Ознакомление с теорией":
            self.show_theory_page()
        elif item == "О нас":
            self.show_about_page()


if __name__ == '__main__':
    MainApp().run()