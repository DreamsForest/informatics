from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class ClickableCard(MDCard):
    """Кликабельная карточка с анимацией нажатия"""

    def __init__(self, task_type="", **kwargs):
        super().__init__(**kwargs)
        self.task_type = task_type
        self.is_touching = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_touching = True
            self.elevation = 1
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.is_touching:
            if abs(touch.dx) > 5 or abs(touch.dy) > 5:
                self.is_touching = False
                self.elevation = 3
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.is_touching and self.collide_point(*touch.pos):
            self.elevation = 3
            if hasattr(self, 'on_click'):
                self.on_click()
            self.is_touching = False
            return True
        self.is_touching = False
        return super().on_touch_up(touch)


class StatisticsMainPage(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'

        # Контейнер для контента
        self.content_layout = MDBoxLayout(orientation='vertical', size_hint_y=1)
        self.add_widget(self.content_layout)

        # Показываем контент страницы
        self.show_content()

    def create_stat_block(self, title, description, bg_color, image_path, on_click_func):
        """Создает блок статистики"""
        card = ClickableCard(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(140),
            padding=dp(15),
            spacing=dp(15),
            md_bg_color=bg_color,
            radius=[dp(15)],
            elevation=3,
        )

        # Изображение слева
        card.add_widget(Image(
            source=image_path,
            size_hint_x=None,
            width=dp(110),
            allow_stretch=True,
            keep_ratio=True
        ))

        # Текст справа
        text_box = MDBoxLayout(orientation='vertical', spacing=dp(8))

        # Заголовок
        text_box.add_widget(MDLabel(
            text=title,
            halign='left',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(35),
            bold=True
        ))

        # Описание
        text_box.add_widget(MDLabel(
            text=description,
            halign='left',
            theme_text_color='Secondary',
            font_style='Body1',
            size_hint_y=None,
            height=dp(60),
        ))

        card.add_widget(text_box)
        card.on_click = on_click_func
        return card

    def show_content(self):
        """Показывает главную страницу статистики"""
        self.content_layout.clear_widgets()

        # Создаем ScrollView для контента
        scroll_view = ScrollView(
            do_scroll_x=False,
            scroll_distance=10,
            scroll_timeout=200
        )

        # Создаем контейнер для блоков
        content_container = MDBoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(25),
            size_hint_y=None
        )

        # Автоматическая высота контейнера
        content_container.bind(minimum_height=content_container.setter('height'))

        # Заголовок страницы
        header_label = MDLabel(
            text="Статистика выполнения заданий",
            theme_text_color='Primary',
            font_style='H4',
            size_hint_y=None,
            height=dp(50),
            halign="center",
            bold=True
        )
        content_container.add_widget(header_label)

        # Блок 1 - Статистика по заданию 19
        stat_block1 = self.create_stat_block(
            "Статистика: Задание 19",
            "Детальная статистика по выполнению задания 19. Графики и анализ прогресса.",
            (0.9, 0.95, 1, 1),
            "free-icon-stats-223407.png",
            lambda: self.main_app.show_statistics_detail_page("statistics_19")
        )

        # Блок 2 - Статистика по заданию 20
        stat_block2 = self.create_stat_block(
            "Статистика: Задание 20",
            "Детальная статистика по выполнению задания 20. Графики и анализ прогресса.",
            (0.95, 0.98, 0.95, 1),
            "free-icon-stats-223407.png",
            lambda: self.main_app.show_statistics_detail_page("statistics_20")
        )

        # Блок 3 - Статистика по заданию 21
        stat_block3 = self.create_stat_block(
            "Статистика: Задание 21",
            "Детальная статистика по выполнению задания 21. Графики и анализ прогресса.",
            (1, 0.95, 0.95, 1),
            "free-icon-stats-223407.png",
            lambda: self.main_app.show_statistics_detail_page("statistics_21")
        )

        # Блок 4 - Общая статистика
        stat_block4 = self.create_stat_block(
            "Общая статистика",
            "Сводная статистика по всем заданиям. Сравнительный анализ прогресса.",
            (0.98, 0.95, 1, 1),
            "free-icon-stats-223407.png",
            lambda: self.main_app.show_statistics_detail_page("statistics_total")
        )

        # Добавляем блоки в контейнер
        content_container.add_widget(stat_block1)
        content_container.add_widget(stat_block2)
        content_container.add_widget(stat_block3)
        content_container.add_widget(stat_block4)

        # Описание страницы
        description_label = MDLabel(
            text="Выберите раздел для просмотра детальной статистики выполнения заданий",
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60),
            halign="center"
        )
        description_label.bind(texture_size=description_label.setter('size'))
        content_container.add_widget(description_label)

        scroll_view.add_widget(content_container)
        self.content_layout.add_widget(scroll_view)