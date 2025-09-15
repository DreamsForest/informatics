from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp


class TheoryPage(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'
        self.spacing = 0

        # Панель инструментов
        self.toolbar = MDTopAppBar(
            title="Ознакомление с теорией",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            elevation=10,
            md_bg_color=(0.2, 0.6, 0.8, 1),
            size_hint_y=None,
            height=dp(56)
        )

        # Контейнер для контента
        self.content_layout = MDBoxLayout(orientation='vertical', size_hint_y=1)



        # Добавляем виджеты
        self.add_widget(self.toolbar)

        self.add_widget(self.content_layout)

    def toggle_nav_drawer(self):
        self.main_app.toggle_nav_drawer()