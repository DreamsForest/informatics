from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.core.image import Image as CoreImage
from io import BytesIO
import matplotlib.pyplot as plt
import json
import os


class StatisticsTotalPage(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        self.stats_file = "user_statistics.json"
        self.show_content()

    def load_statistics(self):
        """Загружает статистику"""
        default_stats = {
            "task_19": {"correct": 0, "incorrect": 0, "total": 0},
            "task_20": {"correct": 0, "incorrect": 0, "total": 0},
            "task_21": {"correct": 0, "incorrect": 0, "total": 0}
        }
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default_stats
        except:
            return default_stats

    def create_comparison_chart_image(self):
        """Создает сравнительную диаграмму по всем заданиям"""
        stats = self.load_statistics()

        tasks = ['Задание 19', 'Задание 20', 'Задание 21']
        correct_answers = [
            stats["task_19"]["correct"],
            stats["task_20"]["correct"],
            stats["task_21"]["correct"]
        ]
        total_answers = [
            stats["task_19"]["total"],
            stats["task_20"]["total"],
            stats["task_21"]["total"]
        ]

        # Процент правильных ответов
        percentages = []
        for i in range(3):
            if total_answers[i] > 0:
                percentages.append((correct_answers[i] / total_answers[i]) * 100)
            else:
                percentages.append(0)

        # Создаем фигуру с улучшенным дизайном
        fig, ax = plt.subplots(figsize=(12, 6), facecolor='#F5F5F5')
        ax.set_facecolor('#FAFAFA')

        # Столбцы для процентов правильных ответов
        colors = ['#2196F3', '#FF9800', '#9C27B0']
        bars = ax.bar(tasks, percentages, color=colors, alpha=0.8, edgecolor='white', linewidth=2)

        # Добавляем значения на столбцы
        for i, (bar, percentage, correct, total) in enumerate(zip(bars, percentages, correct_answers, total_answers)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                    f'{percentage:.1f}%', ha='center', va='bottom',
                    fontsize=14, color='#212121', weight='bold')
            # Добавляем количество ответов под названием задания
            ax.text(bar.get_x() + bar.get_width() / 2., -5,
                    f'{correct}/{total}', ha='center', va='top',
                    fontsize=11, color='#757575', weight='bold')

        ax.set_ylabel('Процент правильных ответов (%)', color='#212121', fontsize=14, weight='bold')
        ax.set_ylim(0, 100)
        ax.set_title('Сравнительная статистика по всем заданиям',
                     color='#1976D2', fontsize=16, pad=25, weight='bold')

        # Настройка внешнего вида
        ax.tick_params(colors='#212121', labelsize=12)
        ax.grid(True, linestyle='--', alpha=0.3, color='#BDBDBD')

        for spine in ax.spines.values():
            spine.set_color('#BDBDBD')
            spine.set_linewidth(1)

        # Убираем верхнюю и правую границу для более чистого вида
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        # Сохраняем в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                    facecolor='#F5F5F5', edgecolor='none')
        buf.seek(0)
        image = CoreImage(buf, ext='png')
        plt.close(fig)
        return image

    def create_total_pie_chart_image(self):
        """Создает общую круговую диаграмму"""
        stats = self.load_statistics()

        total_correct = sum(task["correct"] for task in stats.values())
        total_incorrect = sum(task["incorrect"] for task in stats.values())
        total_attempts = sum(task["total"] for task in stats.values())

        if total_attempts == 0:
            sizes = [1]
            colors = ['#E0E0E0']
            labels = ['Нет данных']
            explode = (0,)
            autopct = None
        else:
            sizes = [total_correct, total_incorrect]
            colors = ['#4CAF50', '#F44336']
            labels = [f'Правильно\n{total_correct}', f'Неправильно\n{total_incorrect}']
            explode = (0.1, 0)
            autopct = '%1.1f%%'

        # Создаем фигуру с улучшенным дизайном
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='#F5F5F5')
        ax.set_facecolor('#FAFAFA')

        if total_attempts > 0:
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, colors=colors, autopct=autopct,
                startangle=90, explode=explode,
                textprops={'fontsize': 14, 'color': 'black', 'weight': 'bold'},
                shadow=True,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2}
            )

            # Улучшаем отображение процентов
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(12)
                autotext.set_weight('bold')
        else:
            wedges, texts = ax.pie(
                sizes, labels=labels, colors=colors,
                startangle=90,
                textprops={'fontsize': 14, 'color': 'black', 'weight': 'bold'},
                wedgeprops={'edgecolor': 'white', 'linewidth': 2}
            )

        ax.set_title('Общая статистика выполнения',
                     fontsize=16, color='#1976D2', pad=25, weight='bold')

        # Сохраняем в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                    facecolor='#F5F5F5', edgecolor='none')
        buf.seek(0)
        image = CoreImage(buf, ext='png')
        plt.close(fig)
        return image

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

        # Сравнительная диаграмма
        try:
            comparison_image = self.create_comparison_chart_image()
            comparison_widget = Image(
                texture=comparison_image.texture,
                size_hint=(1, None),
                height=dp(400),
                allow_stretch=True,
                keep_ratio=True
            )
        except Exception as e:
            print(f"Ошибка создания сравнительной диаграммы: {e}")
            comparison_widget = MDLabel(
                text="Ошибка загрузки диаграммы",
                theme_text_color='Error',
                halign='center',
                size_hint_y=None,
                height=dp(100)
            )

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
        comparison_card.add_widget(comparison_widget)
        content_container.add_widget(comparison_card)

        # Общая круговая диаграмма
        try:
            total_pie_image = self.create_total_pie_chart_image()
            total_pie_widget = Image(
                texture=total_pie_image.texture,
                size_hint=(1, None),
                height=dp(350),
                allow_stretch=True,
                keep_ratio=True
            )
        except Exception as e:
            print(f"Ошибка создания общей круговой диаграммы: {e}")
            total_pie_widget = MDLabel(
                text="Ошибка загрузки диаграммы",
                theme_text_color='Error',
                halign='center',
                size_hint_y=None,
                height=dp(100)
            )

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
        total_pie_card.add_widget(total_pie_widget)
        content_container.add_widget(total_pie_card)

        # Детальная статистика текстом
        stats = self.load_statistics()

        total_correct = sum(task["correct"] for task in stats.values())
        total_incorrect = sum(task["incorrect"] for task in stats.values())
        total_attempts = sum(task["total"] for task in stats.values())

        stats_text = f"""ОБЩАЯ СТАТИСТИКА ПО ВСЕМ ЗАДАНИЯМ

Всего правильных ответов: {total_correct}
Всего неправильных ответов: {total_incorrect}
Всего попыток: {total_attempts}
"""

        if total_attempts > 0:
            total_percentage = (total_correct / total_attempts) * 100
            stats_text += f"Общий процент правильных ответов: {total_percentage:.1f}%\n\n"

            # Статистика по каждому заданию
            stats_text += "СТАТИСТИКА ПО ЗАДАНИЯМ:\n"
            for i, task_key in enumerate(['task_19', 'task_20', 'task_21']):
                task_stats = stats[task_key]
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

        # Устанавливаем минимальную высоту для текстовой статистики
        stats_label.height = dp(200)

        stats_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(0.95, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2,
            height=dp(250)
        )
        stats_card.add_widget(stats_label)
        content_container.add_widget(stats_card)

        # Кнопка назад
        from kivymd.uix.button import MDRaisedButton
        back_button = MDRaisedButton(
            text="Назад к статистике",
            size_hint_y=None,
            height=dp(50),
            on_release=lambda x: self.main_app.show_statistics_main_page()
        )
        content_container.add_widget(back_button)

        scroll_view.add_widget(content_container)
        self.add_widget(scroll_view)