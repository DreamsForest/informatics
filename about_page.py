from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton


class AboutPage(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # Заголовок
        title = MDLabel(
            text="О нас",
            halign='center',
            theme_text_color='Primary',
            font_style='H4'
        )

        # Описание
        description = MDLabel(
            text="Это наше замечательное мобильное приложение!\n\n"
                 "Мы создаем качественные приложения с использованием Python и KivyMD.\n\n"
                 "Версия: 1.0.0",
            halign='center',
            theme_text_color='Secondary'
        )

        # Кнопка назад
        back_button = MDRaisedButton(
            text="Назад",
            size_hint=(None, None),
            size=(120, 48),
            on_release=self.go_back
        )

        self.add_widget(title)
        self.add_widget(description)
        self.add_widget(back_button)

    def go_back(self, instance):
        # Этот метод будет реализован в main.py
        pass