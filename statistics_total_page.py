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

        # Рассчитываем общую статистику
        total_correct = sum(task["correct"] for task in stats.values())
        total_incorrect = sum(task["incorrect"] for task in stats.values())
        total_attempts = sum(task["total"] for task in stats.values())
        total_percentage = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

        # === Сравнительная гистограмма по заданиям ===
        comparison_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20)],
            elevation=4,
            height=dp(450)
        )

        comparison_title = MDLabel(
            text="Сравнительная статистика по заданиям",
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height=dp(40),
            halign="center",
            bold=True
        )
        comparison_card.add_widget(comparison_title)

        comparison_chart = ComparisonBarChart(stats, size_hint_y=None, height=dp(350))
        comparison_card.add_widget(comparison_chart)
        content_container.add_widget(comparison_card)

        # === Общая круговая диаграмма ===
        total_pie_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20)],
            elevation=4,
            height=dp(400)
        )

        total_pie_title = MDLabel(
            text="Общая статистика выполнения",
            theme_text_color='Primary',
            font_style='H6',
            size_hint_y=None,
            height=dp(40),
            halign="center",
            bold=True
        )
        total_pie_card.add_widget(total_pie_title)

        total_pie_chart = FixedPieChartTotal(total_correct, total_incorrect, size_hint_y=None, height=dp(250))
        total_pie_card.add_widget(total_pie_chart)

        # Легенда для общей круговой диаграммы
        legend_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40),
                                  spacing=dp(20), padding=dp(10))

        # Правильные
        correct_legend = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(150), spacing=dp(10))
        correct_color = ColorBox(color=(0.3, 0.69, 0.31, 1), size_hint_x=None, width=dp(20))
        correct_legend.add_widget(correct_color)
        correct_legend.add_widget(MDLabel(
            text=f"Правильно: {total_correct}",
            theme_text_color='Primary',
            font_style='Body2'
        ))

        # Неправильные
        incorrect_legend = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(150), spacing=dp(10))
        incorrect_color = ColorBox(color=(0.96, 0.26, 0.21, 1), size_hint_x=None, width=dp(20))
        incorrect_legend.add_widget(incorrect_color)
        incorrect_legend.add_widget(MDLabel(
            text=f"Неправильно: {total_incorrect}",
            theme_text_color='Primary',
            font_style='Body2'
        ))

        legend_layout.add_widget(correct_legend)
        legend_layout.add_widget(incorrect_legend)
        total_pie_card.add_widget(legend_layout)

        content_container.add_widget(total_pie_card)

        # === Детальная статистика текстом ===
        stats_text = f"""ОБЩАЯ СТАТИСТИКА ПО ВСЕМ ЗАДАНИЯМ

Всего правильных ответов: {total_correct}
Всего неправильных ответов: {total_incorrect}
Всего попыток: {total_attempts}
"""

        if total_attempts > 0:
            stats_text += f"Общий процент правильных ответов: {total_percentage:.1f}%\n\n"

            # Статистика по каждому заданию
            stats_text += "СТАТИСТИКА ПО ЗАДАНИЯМ:\n"
            for i, task_key in enumerate(['task_19', 'task_20', 'task_21']):
                task_stats = stats.get(task_key, {"correct": 0, "incorrect": 0, "total": 0})
                task_name = f"Задание {i + 19}"
                if task_stats['total'] > 0:
                    task_percentage = (task_stats['correct'] / task_stats['total']) * 100
                    stats_text += f"{task_name}: {task_stats['correct']}/{task_stats['total']} ({task_percentage:.1f}%)\n"
                else:
                    stats_text += f"{task_name}: нет данных\n"

            # Добавляем общую рекомендацию
            if total_percentage >= 80:
                stats_text += "\nОтличные результаты! Вы хорошо освоили все задания!"
            elif total_percentage >= 60:
                stats_text += "\nХорошие результаты! Продолжайте практиковаться!"
            elif total_percentage >= 40:
                stats_text += "\nНеплохие результаты! Обратите внимание на проблемные задания!"
            else:
                stats_text += "\nРекомендуем повторить теорию и уделить больше времени практике!"

        stats_label = MDLabel(
            text=stats_text,
            theme_text_color='Primary',
            font_style='Body1',
            size_hint_y=None,
            halign="center",
            valign="center"
        )
        stats_label.bind(texture_size=stats_label.setter('size'))
        stats_label.height = dp(250)

        stats_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(0.95, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2,
            height=dp(300)
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
# СРАВНИТЕЛЬНАЯ ГИСТОГРАММА ПО ЗАДАНИЯМ
# ===========================
class ComparisonBarChart(Widget):
    def __init__(self, stats, **kwargs):
        super().__init__(**kwargs)
        self.stats = stats
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
            # Размеры для графика
            chart_height = self.height * 0.7
            chart_width = self.width * 0.8
            start_x = self.x + self.width * 0.1
            start_y = self.y + self.height * 0.2

            # Данные для отображения
            tasks = ['Зад. 19', 'Зад. 20', 'Зад. 21']
            colors = [(0.33, 0.67, 0.93, 1),  # #2196F3 - синий
                      (1.0, 0.6, 0.0, 1),  # #FF9800 - оранжевый
                      (0.61, 0.15, 0.69, 1)]  # #9C27B0 - фиолетовый

            percentages = []
            correct_answers = []
            total_answers = []

            for task_key in ['task_19', 'task_20', 'task_21']:
                task_stats = self.stats.get(task_key, {"correct": 0, "incorrect": 0, "total": 0})
                correct_answers.append(task_stats["correct"])
                total_answers.append(task_stats["total"])
                if task_stats["total"] > 0:
                    percentages.append((task_stats["correct"] / task_stats["total"]) * 100)
                else:
                    percentages.append(0)

            # Находим максимальное значение для масштабирования
            max_percentage = max(percentages) if any(percentages) else 100

            # Рисуем столбцы
            bar_width = chart_width / 5
            spacing = bar_width / 3

            for i, (task, percentage, color) in enumerate(zip(tasks, percentages, colors)):
                bar_x = start_x + i * (bar_width + spacing)

                if total_answers[i] > 0:
                    # Столбец с процентом
                    bar_height = (percentage / max_percentage) * chart_height if max_percentage > 0 else 0
                    Color(*color)
                    Rectangle(pos=(bar_x, start_y), size=(bar_width, bar_height))
                else:
                    # Серый столбец если нет данных
                    Color(0.88, 0.88, 0.88, 1)
                    Rectangle(pos=(bar_x, start_y), size=(bar_width, chart_height * 0.3))

            # Сетка
            Color(0.7, 0.7, 0.7, 0.3)
            for i in range(1, 6):
                y_pos = start_y + (chart_height * i / 5)
                Line(points=[start_x, y_pos, start_x + chart_width, y_pos], width=dp(0.5))

        # Добавляем подписи
        self.add_chart_labels(start_x, start_y, bar_width, spacing, chart_width, chart_height,
                              tasks, percentages, correct_answers, total_answers)

    def add_chart_labels(self, start_x, start_y, bar_width, spacing, chart_width, chart_height,
                         tasks, percentages, correct_answers, total_answers):
        """Добавляет подписи к гистограмме"""

        # Находим максимальное значение для масштабирования
        max_percentage = max(percentages) if any(percentages) else 100

        # Подписи заданий и процентов
        for i, (task, percentage, correct, total) in enumerate(zip(tasks, percentages, correct_answers, total_answers)):
            bar_x = start_x + i * (bar_width + spacing)
            bar_height = (percentage / max_percentage * chart_height) if max_percentage > 0 else chart_height * 0.3

            # Название задания
            task_label = MDLabel(
                text=task,
                halign="center",
                theme_text_color="Primary",
                font_style="Body2",
                bold=True,
                size_hint=(None, None)
            )
            task_label.size = (bar_width * 1.2, dp(20))
            task_label.pos = (
                bar_x - bar_width / 10,
                start_y - dp(25)
            )
            self.add_widget(task_label)
            self.labels.append(task_label)

            # Процент
            if total > 0:
                percent_label = MDLabel(
                    text=f"{percentage:.1f}%",
                    halign="center",
                    theme_text_color="Primary",
                    font_style="Body2",
                    bold=True,
                    size_hint=(None, None)
                )
                percent_label.size = (bar_width * 1.2, dp(20))
                percent_label.pos = (
                    bar_x - bar_width / 10,
                    start_y + bar_height + dp(5)
                )
                self.add_widget(percent_label)
                self.labels.append(percent_label)

            # Количество ответов
            count_label = MDLabel(
                text=f"{correct}/{total}",
                halign="center",
                theme_text_color="Secondary",
                font_style="Body2",
                size_hint=(None, None)
            )
            count_label.size = (bar_width * 1.2, dp(20))
            count_label.pos = (
                bar_x - bar_width / 10,
                start_y - dp(45)
            )
            self.add_widget(count_label)
            self.labels.append(count_label)

        # Подпись оси Y
        y_axis_label = MDLabel(
            text="Процент правильных (%)",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint=(None, None)
        )
        y_axis_label.size = (dp(120), dp(30))
        y_axis_label.pos = (
            start_x - dp(70),
            start_y + chart_height / 2 - dp(15)
        )
        self.add_widget(y_axis_label)
        self.labels.append(y_axis_label)


# ===========================
# ОБЩАЯ КРУГОВАЯ ДИАГРАММА
# ===========================
class FixedPieChartTotal(Widget):
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

            # Фон
            Color(0.95, 0.95, 0.95, 1)
            Ellipse(pos=self.pos, size=self.size)

            if total == 0:
                # Если нет данных - серый круг
                Color(0.88, 0.88, 0.88, 1)
                Ellipse(pos=self.pos, size=self.size)
                Color(0.6, 0.6, 0.6, 1)
                Line(circle=(self.center_x, self.center_y, min(self.width, self.height) / 2), width=dp(2))
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

                # Обводка белая
                Color(1, 1, 1, 1)
                Line(circle=(self.center_x, self.center_y, min(self.width, self.height) / 2), width=dp(3))

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
            font_style="Body1",
            bold=True,
            size_hint=(None, None)
        )

        # Позиционируем по центру
        label_size = (dp(100), dp(60))
        self.center_label.size = label_size
        self.center_label.pos = (
            self.center_x - label_size[0] / 2,
            self.center_y - label_size[1] / 2
        )
        self.add_widget(self.center_label)