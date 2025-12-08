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


class StatisticsTotalPage(MDBoxLayout):
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
            text="Общая статистика",
            theme_text_color='Primary',
            font_style='H4',
            size_hint_y=None,
            height=dp(50),
            halign="center",
            bold=True
        )
        content_container.add_widget(title_label)

        # Получаем статистику через main_app
        stats = self.main_app.get_statistics()

        # === Вертикальное расположение круговых диаграмм ===
        # Диаграмма для задания 19
        task_19_stats = stats.get("task_19", {"correct": 0, "incorrect": 0, "total": 0})
        correct_19, incorrect_19, total_19 = task_19_stats["correct"], task_19_stats["incorrect"], task_19_stats["total"]
        pie_chart_19_card = self.create_pie_chart_card(
            "Задание 19",
            correct_19,
            incorrect_19,
            "pie_chart_19"
        )
        content_container.add_widget(pie_chart_19_card)

        # Диаграмма для задания 20
        task_20_stats = stats.get("task_20", {"correct": 0, "incorrect": 0, "total": 0})
        correct_20, incorrect_20, total_20 = task_20_stats["correct"], task_20_stats["incorrect"], task_20_stats["total"]
        pie_chart_20_card = self.create_pie_chart_card(
            "Задание 20",
            correct_20,
            incorrect_20,
            "pie_chart_20"
        )
        content_container.add_widget(pie_chart_20_card)

        # Диаграмма для задания 21
        task_21_stats = stats.get("task_21", {"correct": 0, "incorrect": 0, "total": 0})
        correct_21, incorrect_21, total_21 = task_21_stats["correct"], task_21_stats["incorrect"], task_21_stats["total"]
        pie_chart_21_card = self.create_pie_chart_card(
            "Задание 21",
            correct_21,
            incorrect_21,
            "pie_chart_21"
        )
        content_container.add_widget(pie_chart_21_card)

        # === Общая сводка ===
        total_correct = correct_19 + correct_20 + correct_21
        total_incorrect = incorrect_19 + incorrect_20 + incorrect_21
        total_all = total_19 + total_20 + total_21
        total_percentage = (total_correct / total_all * 100) if total_all > 0 else 0

        summary_text = f"""ОБЩАЯ СВОДКА

Всего попыток: {total_all}
Из них правильных: {total_correct}
Из них неправильных: {total_incorrect}
Общий процент правильных: {total_percentage:.1f}%
"""

        summary_label = MDLabel(
            text=summary_text,
            theme_text_color='Primary',
            font_style='Body1',
            size_hint_y=None,
            halign="center",
            valign="center"
        )
        summary_label.bind(texture_size=summary_label.setter('size'))
        summary_label.height = dp(120)

        summary_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(0.95, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2,
            height=dp(180)
        )
        summary_card.add_widget(summary_label)
        content_container.add_widget(summary_card)

        # === Детальная статистика по заданиям ===
        # Форматируем текст с проверкой на ноль
        details_text_19 = f"Задание 19: {correct_19} правильных из {total_19}"
        if total_19 > 0:
            details_text_19 += f" ({(correct_19 / total_19 * 100):.1f}%)"

        details_text_20 = f"Задание 20: {correct_20} правильных из {total_20}"
        if total_20 > 0:
            details_text_20 += f" ({(correct_20 / total_20 * 100):.1f}%)"

        details_text_21 = f"Задание 21: {correct_21} правильных из {total_21}"
        if total_21 > 0:
            details_text_21 += f" ({(correct_21 / total_21 * 100):.1f}%)"

        details_text = f"""ДЕТАЛЬНАЯ СТАТИСТИКА ПО ЗАДАНИЯМ

{details_text_19}
{details_text_20}
{details_text_21}
"""

        if total_all > 0:
            # Добавляем рекомендацию
            if total_percentage >= 80:
                details_text += "\nОтличный результат! Вы отлично справляетесь со всеми заданиями!"
            elif total_percentage >= 60:
                details_text += "\nХороший результат! Продолжайте в том же духе!"
            elif total_percentage >= 40:
                details_text += "\nНеплохо! Есть над чем поработать!"
            else:
                details_text += "\nРекомендуем повторить теорию и попрактиковаться!"

        details_label = MDLabel(
            text=details_text,
            theme_text_color='Primary',
            font_style='Body1',
            size_hint_y=None,
            halign="center",
            valign="center"
        )
        details_label.bind(texture_size=details_label.setter('size'))
        details_label.height = dp(200)

        details_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(0.95, 0.98, 0.95, 1),
            radius=[dp(15)],
            elevation=2,
            height=dp(240)
        )
        details_card.add_widget(details_label)
        content_container.add_widget(details_card)

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

    def create_pie_chart_card(self, title, correct, incorrect, chart_id):
        """Создает карточку с круговой диаграммой"""
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15)],
            elevation=3,
            height=dp(320)  # Уменьшил высоту для вертикального расположения
        )

        # Заголовок задания
        title_label = MDLabel(
            text=title,
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40),
            halign="center",
            bold=True
        )
        card.add_widget(title_label)

        # Создаем круговую диаграмму
        if chart_id == "pie_chart_19":
            pie_chart = FixedPieChart19(correct, incorrect, size_hint_y=None, height=dp(180))
        elif chart_id == "pie_chart_20":
            pie_chart = FixedPieChart20(correct, incorrect, size_hint_y=None, height=dp(180))
        else:  # pie_chart_21
            pie_chart = FixedPieChart21(correct, incorrect, size_hint_y=None, height=dp(180))

        card.add_widget(pie_chart)

        # Легенда
        legend_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(20),
            padding=dp(10)
        )

        # Правильные
        correct_legend = BoxLayout(orientation='horizontal', size_hint_x=0.5, spacing=dp(10))
        correct_color = ColorBox(color=(0.3, 0.69, 0.31, 1), size_hint_x=None, width=dp(20))
        correct_legend.add_widget(correct_color)
        correct_legend.add_widget(MDLabel(
            text=f"Правильно: {correct}",
            theme_text_color='Primary',
            font_style='Body2'
        ))

        # Неправильные
        incorrect_legend = BoxLayout(orientation='horizontal', size_hint_x=0.5, spacing=dp(10))
        incorrect_color = ColorBox(color=(0.96, 0.26, 0.21, 1), size_hint_x=None, width=dp(20))
        incorrect_legend.add_widget(incorrect_color)
        incorrect_legend.add_widget(MDLabel(
            text=f"Неправильно: {incorrect}",
            theme_text_color='Primary',
            font_style='Body2'
        ))

        legend_layout.add_widget(correct_legend)
        legend_layout.add_widget(incorrect_legend)
        card.add_widget(legend_layout)

        # Общая информация
        total = correct + incorrect
        percentage = (correct / total * 100) if total > 0 else 0
        info_label = MDLabel(
            text=f"Всего попыток: {total} • Процент правильных: {percentage:.1f}%",
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(30),
            halign="center"
        )
        card.add_widget(info_label)

        return card


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
# КРУГОВАЯ ДИАГРАММА ДЛЯ ЗАДАНИЯ 19 (БЕЗ ЛИШНЕЙ ОБВОДКИ)
# ===========================
class FixedPieChart19(Widget):
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
                Color(0.88, 0.88, 0.88, 1)
                Ellipse(pos=self.pos, size=self.size)
            else:
                # Правильные ответы (зеленый)
                correct_angle = 360 * (self.correct / total)
                Color(0.3, 0.69, 0.31, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=0,
                    angle_end=correct_angle
                )

                # Неправильные ответы (красный)
                Color(0.96, 0.26, 0.21, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=correct_angle,
                    angle_end=360
                )

        # Центральный текст с процентами
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
            font_style="Body2",
            bold=True,
            size_hint=(None, None)
        )

        # Позиционируем по центру
        label_size = (dp(80), dp(50))
        self.center_label.size = label_size
        self.center_label.pos = (
            self.center_x - label_size[0] / 2,
            self.center_y - label_size[1] / 2
        )
        self.add_widget(self.center_label)


# ===========================
# КРУГОВАЯ ДИАГРАММА ДЛЯ ЗАДАНИЯ 20 (БЕЗ ЛИШНЕЙ ОБВОДКИ)
# ===========================
class FixedPieChart20(Widget):
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
                Color(0.88, 0.88, 0.88, 1)
                Ellipse(pos=self.pos, size=self.size)
            else:
                # Правильные ответы (зеленый)
                correct_angle = 360 * (self.correct / total)
                Color(0.3, 0.69, 0.31, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=0,
                    angle_end=correct_angle
                )

                # Неправильные ответы (красный)
                Color(0.96, 0.26, 0.21, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=correct_angle,
                    angle_end=360
                )

        # Центральный текст с процентами
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
            font_style="Body2",
            bold=True,
            size_hint=(None, None)
        )

        # Позиционируем по центру
        label_size = (dp(80), dp(50))
        self.center_label.size = label_size
        self.center_label.pos = (
            self.center_x - label_size[0] / 2,
            self.center_y - label_size[1] / 2
        )
        self.add_widget(self.center_label)


# ===========================
# КРУГОВАЯ ДИАГРАММА ДЛЯ ЗАДАНИЯ 21 (БЕЗ ЛИШНЕЙ ОБВОДКИ)
# ===========================
class FixedPieChart21(Widget):
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
                Color(0.88, 0.88, 0.88, 1)
                Ellipse(pos=self.pos, size=self.size)
            else:
                # Правильные ответы (зеленый)
                correct_angle = 360 * (self.correct / total)
                Color(0.3, 0.69, 0.31, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=0,
                    angle_end=correct_angle
                )

                # Неправильные ответы (красный)
                Color(0.96, 0.26, 0.21, 1)
                Ellipse(
                    pos=self.pos,
                    size=self.size,
                    angle_start=correct_angle,
                    angle_end=360
                )

        # Центральный текст с процентами
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
            font_style="Body2",
            bold=True,
            size_hint=(None, None)
        )

        # Позиционируем по центру
        label_size = (dp(80), dp(50))
        self.center_label.size = label_size
        self.center_label.pos = (
            self.center_x - label_size[0] / 2,
            self.center_y - label_size[1] / 2
        )
        self.add_widget(self.center_label)