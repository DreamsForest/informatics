from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty


class Statistics19Page(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        self.show_content()

    def show_content(self):
        """Показывает контент страницы"""
        self.clear_widgets()

        scroll_view = ScrollView(do_scroll_x=False)
        content_container = MDBoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(20),
            size_hint_y=None
        )
        content_container.bind(minimum_height=content_container.setter('height'))

        # Заголовок
        title_label = MDLabel(
            text="Статистика: Задание 19",
            theme_text_color='Primary',
            font_style='H4',
            size_hint_y=None,
            height=dp(50),
            halign="center",
            bold=True
        )
        content_container.add_widget(title_label)

        # Получаем статистику
        stats = self.main_app.get_statistics().get("task_19", {"correct": 0, "incorrect": 0, "total": 0})
        correct, incorrect, total = stats["correct"], stats["incorrect"], stats["total"]
        percentage = (correct / total * 100) if total > 0 else 0

        # === Круговая диаграмма ===
        pie_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20)],
            elevation=4,
            height=dp(400)
        )

        pie_title = MDLabel(
            text="Соотношение правильных и неправильных ответов",
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height=dp(40),
            halign="center",
            bold=True
        )
        pie_card.add_widget(pie_title)

        pie_chart = FixedPieChart(correct, incorrect, size_hint_y=None, height=dp(250))
        pie_card.add_widget(pie_chart)

        # Легенда для круговой диаграммы
        legend_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40),
                                  spacing=dp(20), padding=dp(10))

        # Правильные
        correct_legend = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(150), spacing=dp(10))
        correct_color = ColorBox(color=(0.26, 0.8, 0.26, 1), size_hint_x=None, width=dp(20))
        correct_legend.add_widget(correct_color)
        correct_legend.add_widget(MDLabel(
            text=f"Правильно: {correct}",
            theme_text_color='Primary',
            font_style='Body2'
        ))

        # Неправильные
        incorrect_legend = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(150), spacing=dp(10))
        incorrect_color = ColorBox(color=(0.9, 0.2, 0.2, 1), size_hint_x=None, width=dp(20))
        incorrect_legend.add_widget(incorrect_color)
        incorrect_legend.add_widget(MDLabel(
            text=f"Неправильно: {incorrect}",
            theme_text_color='Primary',
            font_style='Body2'
        ))

        legend_layout.add_widget(correct_legend)
        legend_layout.add_widget(incorrect_legend)
        pie_card.add_widget(legend_layout)

        content_container.add_widget(pie_card)

        # === Улучшенная гистограмма ===
        bar_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20)],
            elevation=4,
            height=dp(400)
        )

        bar_title = MDLabel(
            text="Количество и процент правильных ответов",
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height=dp(40),
            halign="center",
            bold=True
        )
        bar_card.add_widget(bar_title)

        enhanced_bar_chart = FixedBarChart(correct, incorrect, size_hint_y=None, height=dp(300))
        bar_card.add_widget(enhanced_bar_chart)
        content_container.add_widget(bar_card)

        # === Детальная текстовая статистика ===
        stats_text = f"""ДЕТАЛЬНАЯ СТАТИСТИКА - ЗАДАНИЕ 19

Правильных ответов: {correct}
Неправильных ответов: {incorrect}
Всего попыток: {total}
"""

        if total > 0:
            stats_text += f"Процент правильных: {percentage:.1f}%\n\n"

            # Добавляем рекомендацию
            if percentage >= 80:
                stats_text += "Отличный результат! Вы отлично справляетесь с заданием!"
            elif percentage >= 60:
                stats_text += "Хороший результат! Продолжайте в том же духе!"
            elif percentage >= 40:
                stats_text += "Неплохо! Есть над чем поработать!"
            else:
                stats_text += "Рекомендуем повторить теорию и попрактиковаться!"

        stats_label = MDLabel(
            text=stats_text,
            theme_text_color='Primary',
            font_style='Body1',
            size_hint_y=None,
            halign="center",
            valign="center"
        )
        stats_label.bind(texture_size=stats_label.setter('size'))
        stats_label.height = dp(180)

        stats_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(0.95, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2,
            height=dp(220)
        )
        stats_card.add_widget(stats_label)
        content_container.add_widget(stats_card)

        # Кнопка назад
        back_button = MDRaisedButton(
            text="Назад к статистике",
            size_hint_y=None,
            height=dp(50),
            on_release=lambda x: self.main_app.show_statistics_main_page()
        )
        content_container.add_widget(back_button)

        scroll_view.add_widget(content_container)
        self.add_widget(scroll_view)


# Виджет для отображения цветного квадратика в легенде
class ColorBox(Widget):
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(20), dp(20))
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            Rectangle(pos=self.pos, size=self.size)


# ===========================
# ИСПРАВЛЕННАЯ КРУГОВАЯ ДИАГРАММА (БЕЗ ЛИШНЕЙ ОБВОДКИ)
# ===========================
class FixedPieChart(Widget):
    def __init__(self, correct, incorrect, **kwargs):
        super().__init__(**kwargs)
        self.correct = correct
        self.incorrect = incorrect
        self.center_label = None
        self.bind(pos=self.update_chart, size=self.update_chart)

    def update_chart(self, *args):
        self.canvas.clear()

        # Удаляем старую центральную подпись
        if self.center_label and self.center_label in self.children:
            self.remove_widget(self.center_label)

        with self.canvas:
            total = self.correct + self.incorrect

            if total == 0:
                # Если нет данных - серый круг
                Color(0.8, 0.8, 0.8, 1)
                Ellipse(pos=self.pos, size=self.size)
            else:
                # Правильные ответы (зеленый)
                correct_angle = 360 * (self.correct / total)
                Color(0.26, 0.8, 0.26, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=0,
                    angle_end=correct_angle
                )

                # Неправильные ответы (красный)
                Color(0.9, 0.2, 0.2, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=correct_angle,
                    angle_end=360
                )

        # Центральный текст с процентами (добавляем как виджет)
        if total > 0:
            percentage = (self.correct / total * 100)
            center_text = f"{self.correct}/{total}\n({percentage:.1f}%)"
        else:
            center_text = "Нет\nданных"

        self.center_label = MDLabel(
            text=center_text,
            halign="center",
            valign="center",
            theme_text_color="Primary",
            font_style="Body1",
            bold=True,
            size_hint=(None, None)
        )

        # Позиционируем по центру относительно текущего размера
        label_size = (dp(80), dp(50))
        self.center_label.size = label_size
        self.center_label.pos = (
            self.center_x - label_size[0] / 2,
            self.center_y - label_size[1] / 2
        )
        self.add_widget(self.center_label)


# ===========================
# ИСПРАВЛЕННАЯ ГИСТОГРАММА
# ===========================
class FixedBarChart(Widget):
    def __init__(self, correct, incorrect, **kwargs):
        super().__init__(**kwargs)
        self.correct = correct
        self.incorrect = incorrect
        self.labels = []
        self.bind(pos=self.update_chart, size=self.update_chart)

    def clear_labels(self):
        """Очищает все текстовые метки"""
        for label in self.labels:
            if label in self.children:
                self.remove_widget(label)
        self.labels.clear()

    def update_chart(self, *args):
        self.canvas.clear()
        self.clear_labels()

        with self.canvas:
            total = self.correct + self.incorrect

            # Фон
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Размеры для столбцов
            chart_height = self.height * 0.6  # 60% высоты для столбцов
            chart_width = self.width * 0.8  # 80% ширины для столбцов
            start_x = self.x + self.width * 0.1  # Отступ 10% слева
            start_y = self.y + self.height * 0.1  # Отступ 10% снизу

            bar_width = chart_width / 4
            spacing = bar_width / 2

            if total == 0:
                # Если нет данных - серые полосы
                Color(0.8, 0.8, 0.8, 1)
                h1 = chart_height * 0.3
                h2 = chart_height * 0.2

                Rectangle(pos=(start_x + spacing, start_y), size=(bar_width, h1))
                Rectangle(pos=(start_x + 2 * spacing + bar_width, start_y), size=(bar_width, h2))
            else:
                max_value = max(self.correct, self.incorrect) or 1

                # Правильные ответы (зеленый)
                h1 = (self.correct / max_value) * chart_height
                Color(0.26, 0.8, 0.26, 1)
                rect1_pos = (start_x + spacing, start_y)
                rect1_size = (bar_width, h1)
                Rectangle(pos=rect1_pos, size=rect1_size)

                # Неправильные ответы (красный)
                h2 = (self.incorrect / max_value) * chart_height
                Color(0.9, 0.2, 0.2, 1)
                rect2_pos = (start_x + 2 * spacing + bar_width, start_y)
                rect2_size = (bar_width, h2)
                Rectangle(pos=rect2_pos, size=rect2_size)

            # Сетка
            Color(0.7, 0.7, 0.7, 0.3)
            for i in range(1, 6):
                y_pos = start_y + (chart_height * i / 5)
                Line(points=[start_x, y_pos, start_x + chart_width, y_pos], width=dp(0.5))

        # Добавляем подписи
        self.add_chart_labels(start_x, start_y, bar_width, spacing, chart_width, total)

    def add_chart_labels(self, start_x, start_y, bar_width, spacing, chart_width, total):
        """Добавляет подписи к гистограмме"""

        # Подпись для правильных
        correct_label = MDLabel(
            text=f"Правильно\n{self.correct}",
            halign="center",
            theme_text_color="Primary",
            font_style="Body2",
            bold=True,
            size_hint=(None, None)
        )
        correct_label.size = (bar_width * 1.5, dp(40))
        correct_label.pos = (
            start_x + spacing - bar_width / 4,
            start_y - dp(35)
        )
        self.add_widget(correct_label)
        self.labels.append(correct_label)

        # Подпись для неправильных
        incorrect_label = MDLabel(
            text=f"Неправильно\n{self.incorrect}",
            halign="center",
            theme_text_color="Primary",
            font_style="Body2",
            bold=True,
            size_hint=(None, None)
        )
        incorrect_label.size = (bar_width * 1.5, dp(40))
        incorrect_label.pos = (
            start_x + 2 * spacing + bar_width - bar_width / 4,
            start_y - dp(35)
        )
        self.add_widget(incorrect_label)
        self.labels.append(incorrect_label)

        # Процент правильных
        percentage = (self.correct / total * 100) if total > 0 else 0
        percentage_label = MDLabel(
            text=f"Процент правильных: {percentage:.1f}%",
            halign="center",
            theme_text_color="Primary",
            font_style="H6",
            bold=True,
            size_hint=(None, None)
        )
        percentage_label.size = (chart_width, dp(40))
        percentage_label.pos = (
            start_x,
            start_y + self.height * 0.6 + dp(20)
        )
        self.add_widget(percentage_label)
        self.labels.append(percentage_label)