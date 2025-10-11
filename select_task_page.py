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
            # Если началось движение - это скролл, отменяем клик
            if abs(touch.dx) > 5 or abs(touch.dy) > 5:  # порог для определения скролла
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


class SelectTaskPage(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'

        self.content_layout = MDBoxLayout(orientation='vertical', size_hint_y=1)
        self.add_widget(self.content_layout)
        self.show_content()

    def create_task_block(self, title, description, bg_color, image_path, on_click_func):
        card = ClickableCard(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(140),  # Увеличил высоту для лучшего отображения
            padding=dp(15),
            spacing=dp(15),
            md_bg_color=bg_color,
            radius=[dp(15)],
            elevation=3,  # Увеличил elevation для лучшего визуального эффекта
        )

        # Изображение слева
        card.add_widget(Image(
            source=image_path,
            size_hint_x=None,
            width=dp(110),  # Увеличил ширину изображения
            allow_stretch=True,
            keep_ratio=True
        ))

        # Текст справа
        text_box = MDBoxLayout(orientation='vertical', spacing=dp(8))
        text_box.add_widget(MDLabel(
            text=title,
            halign='left',
            theme_text_color='Primary',
            font_style='H5',  # Увеличил размер шрифта
            size_hint_y=None,
            height=dp(35),
            bold=True
        ))
        text_box.add_widget(MDLabel(
            text=description,
            halign='left',
            theme_text_color='Secondary',
            font_style='Body1',  # Увеличил размер шрифта
            size_hint_y=None,
            height=dp(60),
        ))
        card.add_widget(text_box)

        card.on_click = on_click_func
        return card

    def show_content(self):
        self.content_layout.clear_widgets()

        # Настроенный ScrollView
        scroll_view = ScrollView(
            do_scroll_x=False,
            scroll_distance=10,  # Минимальное расстояние для начала скролла
            scroll_timeout=200  # Таймаут для определения скролла
        )

        content_container = MDBoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(25),
            size_hint_y=None
        )

        # Автоматическая высота контейнера
        content_container.bind(minimum_height=content_container.setter('height'))



        # Блоки заданий
        task_block1 = self.create_task_block(
            "Задание №19",
            "Выигрышная стратегия 1. Задания с одной и двумя кучами. Базовый уровень сложности.",
            (0.9, 0.95, 1, 1),  # нежно-голубой
            "free-icon-computer-science-7897147.png",
            lambda: self.main_app.show_task_page("task_19")
        )

        task_block2 = self.create_task_block(
            "Задание №20",
            "Выигрышная стратегия 2. Задания с одной и двумя кучами. Средний уровень сложности.",
            (0.95, 0.98, 0.95, 1),  # нежно-зеленый
            "free-icon-computer-scientist-2316086.png",
            lambda: self.main_app.show_task_page("task_20")
        )

        task_block3 = self.create_task_block(
            "Задание №21",
            "Выигрышная стратегия 3. Задания с одной и двумя кучами. Продвинутый уровень сложности.",
            (1, 0.95, 0.95, 1),  # нежно-розовый
            "free-icon-informatics-8824184.png",
            lambda: self.main_app.show_task_page("task_21")
        )

        content_container.add_widget(task_block1)
        content_container.add_widget(task_block2)
        content_container.add_widget(task_block3)

        # Описание страницы
        description_label = MDLabel(
            text="Выберите задание для практики. Каждое задание генерируется случайным образом с разными параметрами.",
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