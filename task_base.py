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
        """Показывает интерфейс задания"""
        self.clear_widgets()

        # Кнопка назад
        back_button = MDRaisedButton(
            text="Назад к выбору заданий",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5}
        )
        back_button.bind(on_release=lambda x: self.main_app.show_select_task_page())
        self.add_widget(back_button)

        # Карточка с заданием
        task_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(300),
            padding=dp(20),
            spacing=dp(15),
            elevation=2,
            radius=[dp(15)]
        )

        task_card.add_widget(MDLabel(
            text=f"Задание {self.task_type.upper().replace('_', ' ')}",
            theme_text_color='Primary',
            font_style='H4',
            size_hint_y=None,
            height=dp(40)
        ))

        task_card.add_widget(MDLabel(
            text=self.current_task['description'],
            theme_text_color='Secondary',
            font_style='Body1',
            size_hint_y=None,
            height=dp(150)
        ))

        task_card.add_widget(MDLabel(
            text=f"Вопрос: {self.current_task['question']}",
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height=dp(60)
        ))

        self.add_widget(task_card)

        # Кнопка для генерации нового задания
        new_task_button = MDRaisedButton(
            text="Новое задание",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5}
        )
        new_task_button.bind(on_release=lambda x: self.generate_new_task())
        self.add_widget(new_task_button)

    def generate_new_task(self):
        """Генерирует новое задание и обновляет интерфейс"""
        self.generate_task()
        self.show_task_interface()