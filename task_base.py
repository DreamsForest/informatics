from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import random


class BaseTaskPage(MDBoxLayout):
    def __init__(self, main_app, task_type, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.task_type = task_type
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)

        # Инициализируем current_task
        self.current_task = None

        # Генерируем задание и показываем интерфейс
        self.generate_task()
        self.show_task_interface()

    def generate_task(self):
        """Генерирует задание (будет переопределен в дочерних классах)"""
        self.current_task = {
            'description': 'Базовое описание задания',
            'question': 'Базовый вопрос',
            'answer': None
        }

    def show_task_interface(self):
        """Показывает интерфейс задания (базовая реализация)"""
        self.clear_widgets()

        # Простой интерфейс по умолчанию
        self.add_widget(MDLabel(
            text=f"Задание {self.task_type}",
            theme_text_color='Primary',
            font_style='H5',
            halign='center'
        ))

        if self.current_task:
            self.add_widget(MDLabel(
                text=self.current_task['description'],
                theme_text_color='Secondary'
            ))

            self.add_widget(MDLabel(
                text=f"Вопрос: {self.current_task['question']}",
                theme_text_color='Primary'
            ))

        # Кнопки управления
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )

        back_button = MDRaisedButton(
            text="Назад",
            size_hint_x=0.5
        )
        back_button.bind(on_release=lambda x: self.main_app.show_select_task_page())

        new_task_button = MDRaisedButton(
            text="Новое задание",
            size_hint_x=0.5
        )
        new_task_button.bind(on_release=lambda x: self.generate_new_task())

        buttons_layout.add_widget(back_button)
        buttons_layout.add_widget(new_task_button)
        self.add_widget(buttons_layout)

    def generate_new_task(self):
        """Генерирует новое задание и обновляет интерфейс"""
        self.generate_task()
        self.show_task_interface()