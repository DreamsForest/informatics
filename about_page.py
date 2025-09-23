from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class AboutPage(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'
        self.spacing = 0

        # Контейнер для контента (без своей панели инструментов)
        self.content_layout = MDBoxLayout(orientation='vertical', size_hint_y=1)

        # Добавляем контент
        self.add_widget(self.content_layout)

        # Показываем контент страницы
        self.show_content()

    def show_content(self):
        """Показывает контент страницы 'О нас'"""
        self.content_layout.clear_widgets()

        # Создаем ScrollView для контента
        scroll_view = ScrollView(do_scroll_x=False)

        # Создаем контейнер для блоков
        content_container = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )

        # Устанавливаем высоту контента
        content_container.height = dp(120) * 4 + dp(20) * 5  # 4 блока + отступы

        # Блок 1 - О приложении
        about_block1 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.9, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2
        )
        about_block1.add_widget(MDLabel(
            text="О нашем приложении",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        about_block1.add_widget(MDLabel(
            text="Образовательная платформа для изучения программирования",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Блок 2 - Наша миссия
        about_block2 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.95, 0.98, 0.95, 1),
            radius=[dp(15)],
            elevation=2
        )
        about_block2.add_widget(MDLabel(
            text="Наша миссия",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        about_block2.add_widget(MDLabel(
            text="Сделать обучение программированию доступным для каждого",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Блок 3 - Возможности
        about_block3 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(1, 0.95, 0.95, 1),
            radius=[dp(15)],
            elevation=2
        )
        about_block3.add_widget(MDLabel(
            text="Возможности платформы",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        about_block3.add_widget(MDLabel(
            text="Теория, практические задания и отслеживание прогресса",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Блок 4 - Контакты
        about_block4 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.98, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2
        )
        about_block4.add_widget(MDLabel(
            text="Контакты и поддержка",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        about_block4.add_widget(MDLabel(
            text="Мы всегда готовы помочь и ответить на ваши вопросы",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Добавляем блоки в контейнер
        content_container.add_widget(about_block1)
        content_container.add_widget(about_block2)
        content_container.add_widget(about_block3)
        content_container.add_widget(about_block4)

        scroll_view.add_widget(content_container)
        self.content_layout.add_widget(scroll_view)