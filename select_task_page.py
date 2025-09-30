from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image   # заменили FitImage на обычный Image
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class ClickableCard(MDCard):
    """Кликабельная карточка с анимацией нажатия"""

    def __init__(self, task_type="", **kwargs):
        super().__init__(**kwargs)
        self.task_type = task_type

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.elevation = 1
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.elevation = 3
            if hasattr(self, 'on_click'):
                self.on_click()
            return True
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
            height=dp(120),
            padding=dp(10),
            spacing=dp(15),
            md_bg_color=bg_color,
            radius=[dp(15)],
            elevation=2,
        )

        # Изображение слева
        card.add_widget(Image(
            source=image_path,
            size_hint_x=None,
            width=dp(100),
            allow_stretch=True,
            keep_ratio=True
        ))

        # Текст справа
        text_box = MDBoxLayout(orientation='vertical', spacing=dp(5))
        text_box.add_widget(MDLabel(
            text=title,
            halign='left',
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height=dp(30),
        ))
        text_box.add_widget(MDLabel(
            text=description,
            halign='left',
            theme_text_color='Secondary',
            font_style='Body2',
        ))
        card.add_widget(text_box)

        card.on_click = on_click_func
        return card

    def show_content(self):
        self.content_layout.clear_widgets()
        scroll_view = ScrollView(do_scroll_x=False)

        content_container = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )
        content_container.height = dp(140) * 3 + dp(20) * 4

        # Примеры блоков
        task_block1 = self.create_task_block(
            "Задание №19",
            "Выигрышная стратегия 1. Задания с одной и двумя кучами.",
            (0.85, 0.92, 1, 1),  # нежно-голубой
            "free-icon-computer-science-7897147.png",
            lambda: self.main_app.show_task_page("task_19")
        )

        task_block2 = self.create_task_block(
            "Задание №20",
            "Выигрышная стратегия 2. Задания с одной и двумя кучами.",
            (0.8, 0.9, 1, 1),  # другой голубой
            "free-icon-computer-scientist-2316086.png",
            lambda: self.main_app.show_task_page("task_20")
        )

        task_block3 = self.create_task_block(
            "Задание №21",
            "Выигрышная стратегия 3. Задания с одной и двумя кучами.",
            (0.75, 0.85, 1, 1),  # ещё темнее голубой
            "free-icon-informatics-8824184.png",
            lambda: self.main_app.show_task_page("task_21")
        )

        content_container.add_widget(task_block1)
        content_container.add_widget(task_block2)
        content_container.add_widget(task_block3)

        scroll_view.add_widget(content_container)
        self.content_layout.add_widget(scroll_view)
