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
            # Если началось движение — это скролл, отменяем клик
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


class TheoryPage(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'

        self.content_layout = MDBoxLayout(orientation='vertical', size_hint_y=1)
        self.add_widget(self.content_layout)
        self.show_theory_selection()

    def create_theory_block(self, title, description, bg_color, image_path, on_click_func):
        """Создает адаптивный блок теории"""
        card = ClickableCard(
            orientation='horizontal',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(20),
            md_bg_color=bg_color,
            radius=[dp(20)],
            elevation=3,
            adaptive_height=True  # автоматическая высота карточки
        )

        # Изображение слева
        card.add_widget(Image(
            source=image_path,
            size_hint_x=None,
            width=dp(130),
            allow_stretch=True,
            keep_ratio=True
        ))

        # Текст справа
        text_box = MDBoxLayout(orientation='vertical', spacing=dp(10), adaptive_height=True)

        # Заголовок
        title_label = MDLabel(
            text=title,
            halign='left',
            theme_text_color='Primary',
            font_style='H5',
            bold=True,
            adaptive_height=True
        )

        # Описание
        desc_label = MDLabel(
            text=description,
            halign='left',
            theme_text_color='Secondary',
            font_style='Body1',
            adaptive_height=True
        )

        text_box.add_widget(title_label)
        text_box.add_widget(desc_label)
        card.add_widget(text_box)

        card.on_click = on_click_func
        return card

    def show_theory_selection(self):
        """Показывает страницу выбора теории"""
        self.content_layout.clear_widgets()

        scroll_view = ScrollView(
            do_scroll_x=False,
            scroll_distance=10,
            scroll_timeout=200
        )

        content_container = MDBoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(30),
            size_hint_y=None
        )

        content_container.bind(minimum_height=content_container.setter('height'))

        # Блок 1 — Теория задания 19
        theory_block1 = self.create_theory_block(
            "Теория: Задание 19",
            "Выигрышная стратегия — базовый уровень. Основные понятия и методы решения простых задач с одной кучей камней.",
            (0.9, 0.95, 1, 1),
            "free-icon-theory-1900182.png",
            lambda: self.show_theory_19()
        )

        # Блок 2 — Теория задания 20
        theory_block2 = self.create_theory_block(
            "Теория: Задание 20",
            "Выигрышная стратегия — средний уровень. Анализ на 2 хода вперед, поиск нескольких значений S.",
            (0.95, 0.98, 0.95, 1),
            "free-icon-case-study-9238747.png",
            lambda: self.show_theory_20()
        )

        # Блок 3 — Теория задания 21
        theory_block3 = self.create_theory_block(
            "Теория: Задание 21",
            "Выигрышная стратегия — продвинутый уровень. Сложные двойные условия, анализ на 3–4 хода вперед.",
            (1, 0.95, 0.95, 1),
            "free-icon-theory-9660577.png",
            lambda: self.show_theory_21()
        )

        # Добавляем блоки
        content_container.add_widget(theory_block1)
        content_container.add_widget(theory_block2)
        content_container.add_widget(theory_block3)

        # Подпись внизу
        description_label = MDLabel(
            text="Выберите задание для изучения теории. Каждый раздел содержит подробные объяснения, примеры решений и готовый код на 4 языках программирования.",
            theme_text_color='Secondary',
            font_style='Body1',
            halign="center",
            adaptive_height=True,
            size_hint_y=None,
        )
        content_container.add_widget(description_label)

        scroll_view.add_widget(content_container)
        self.content_layout.add_widget(scroll_view)

    def show_theory_19(self):
        self.main_app.show_theory_detail_page("theory_19")

    def show_theory_20(self):
        self.main_app.show_theory_detail_page("theory_20")

    def show_theory_21(self):
        self.main_app.show_theory_detail_page("theory_21")
