from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class TheoryPage(MDBoxLayout):
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
        """Показывает контент страницы с теорией"""
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
        content_container.height = dp(120) * 5 + dp(20) * 6  # 5 блоков + отступы

        # Блок 1 - Основы программирования
        theory_block1 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.9, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2
        )
        theory_block1.add_widget(MDLabel(
            text="Основы программирования",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        theory_block1.add_widget(MDLabel(
            text="Переменные, типы данных, операторы и базовые конструкции",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Блок 2 - Алгоритмы
        theory_block2 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.95, 0.98, 0.95, 1),
            radius=[dp(15)],
            elevation=2
        )
        theory_block2.add_widget(MDLabel(
            text="Алгоритмы и анализ сложности",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        theory_block2.add_widget(MDLabel(
            text="Сортировки, поиск, O-нотация и оценка эффективности алгоритмов",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Блок 3 - Структуры данных
        theory_block3 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(1, 0.95, 0.95, 1),
            radius=[dp(15)],
            elevation=2
        )
        theory_block3.add_widget(MDLabel(
            text="Структуры данных",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        theory_block3.add_widget(MDLabel(
            text="Массивы, списки, деревья, хэш-таблицы и графы",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Блок 4 - ООП
        theory_block4 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.98, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2
        )
        theory_block4.add_widget(MDLabel(
            text="Объектно-ориентированное программирование",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        theory_block4.add_widget(MDLabel(
            text="Классы, объекты, наследование, полиморфизм и инкапсуляция",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Блок 5 - Базы данных
        theory_block5 = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.95, 1, 0.95, 1),
            radius=[dp(15)],
            elevation=2
        )
        theory_block5.add_widget(MDLabel(
            text="Базы данных и SQL",
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        theory_block5.add_widget(MDLabel(
            text="Реляционные базы данных, нормализация, запросы и оптимизация",
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))

        # Добавляем блоки в контейнер
        content_container.add_widget(theory_block1)
        content_container.add_widget(theory_block2)
        content_container.add_widget(theory_block3)
        content_container.add_widget(theory_block4)
        content_container.add_widget(theory_block5)

        scroll_view.add_widget(content_container)
        self.content_layout.add_widget(scroll_view)