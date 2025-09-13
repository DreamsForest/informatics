from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout


class MainApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Создаем метку
        label = MDLabel(
            text='Hello, World',
            halign='center',
            theme_text_color='Primary',
            font_style='H5'
        )

        # Создаем кнопку (выберите один из стилей)
        button = MDRaisedButton(
            text='CLICK ME',
            pos_hint={'center_x': 0.5},
            size_hint=(None, None),
            size=(150, 51)
        )

        # Или другие стили кнопок:
        # button = MDFlatButton(text='Flat Button')
        # button = MDRectangleFlatButton(text='Rectangle Button')

        layout.add_widget(label)
        layout.add_widget(button)
        return layout


MainApp().run()