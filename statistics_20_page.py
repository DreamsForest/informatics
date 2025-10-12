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


class Statistics20Page(MDBoxLayout):
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

    def create_pie_chart_image(self):
        """Создает круговую диаграмму и возвращает как изображение Kivy"""
        stats = self.load_statistics()
        task_stats = stats["task_20"]
        correct = task_stats["correct"]
        incorrect = task_stats["incorrect"]
        total = task_stats["total"]

        if total == 0:
            sizes = [1]
            colors = ['#E0E0E0']
            labels = ['Нет данных']
            explode = (0,)
            autopct = None
        else:
            sizes = [correct, incorrect]
            colors = ['#4CAF50', '#F44336']
            labels = [f'Правильно\n{correct}', f'Неправильно\n{incorrect}']
            explode = (0.1, 0)
            autopct = '%1.1f%%'

        # Создаем фигуру с улучшенным дизайном
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='#F5F5F5')
        ax.set_facecolor('#FAFAFA')

        if total > 0:
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

        ax.set_title('Соотношение правильных и неправильных ответов',
                     fontsize=16, color='#1976D2', pad=25, weight='bold')

        # Сохраняем в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                    facecolor='#F5F5F5', edgecolor='none')
        buf.seek(0)

        # Создаем изображение Kivy
        image = CoreImage(buf, ext='png')
        plt.close(fig)
        return image

    def create_comparison_chart_image(self):
        """Создает улучшенную гистограмму только для задания 20"""
        stats = self.load_statistics()
        task_stats = stats["task_20"]

        correct = task_stats["correct"]
        incorrect = task_stats["incorrect"]
        total = task_stats["total"]

        if total > 0:
            percentage = (correct / total) * 100
        else:
            percentage = 0

        # Создаем фигуру с улучшенным дизайном
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), facecolor='#F5F5F5')

        # Первый график - количество ответов
        categories = ['Правильные', 'Неправильные']
        values = [correct, incorrect]
        colors = ['#4CAF50', '#F44336']

        bars1 = ax1.bar(categories, values, color=colors, alpha=0.8,
                        edgecolor='white', linewidth=2)
        ax1.set_title('Количество ответов', fontsize=16, color='#1976D2',
                      pad=20, weight='bold')
        ax1.set_ylabel('Количество', fontsize=14, color='#212121', weight='bold')

        # Добавляем значения на столбцы
        for bar, value in zip(bars1, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                     f'{value}', ha='center', va='bottom',
                     fontsize=16, weight='bold', color='#212121')

        # Второй график - процент правильных ответов
        if total > 0:
            categories_percent = ['Правильные']
            values_percent = [percentage]
            colors_percent = ['#4CAF50']
        else:
            categories_percent = ['Нет данных']
            values_percent = [100]
            colors_percent = ['#E0E0E0']

        bars2 = ax2.bar(categories_percent, values_percent, color=colors_percent,
                        alpha=0.8, edgecolor='white', linewidth=2)
        ax2.set_title('Процент правильных ответов', fontsize=16, color='#1976D2',
                      pad=20, weight='bold')
        ax2.set_ylabel('Процент (%)', fontsize=14, color='#212121', weight='bold')
        ax2.set_ylim(0, 100)

        # Добавляем значения на столбцы для процентов
        for bar, value in zip(bars2, values_percent):
            height = bar.get_height()
            if total > 0:
                ax2.text(bar.get_x() + bar.get_width() / 2., height + 1,
                         f'{value:.1f}%', ha='center', va='bottom',
                         fontsize=16, weight='bold', color='#212121')
            else:
                ax2.text(bar.get_x() + bar.get_width() / 2., height / 2,
                         'Нет данных', ha='center', va='center',
                         fontsize=14, weight='bold', color='#757575')

        # Настройка внешнего вида обоих графиков
        for ax in [ax1, ax2]:
            ax.grid(True, linestyle='--', alpha=0.3, color='#BDBDBD')
            ax.tick_params(axis='both', which='major', labelsize=12, colors='#212121')
            ax.set_facecolor('#FAFAFA')

            # Настройка границ
            for spine in ax.spines.values():
                spine.set_color('#BDBDBD')
                spine.set_linewidth(1)

            # Убираем верхнюю и правую границу для более чистого вида
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        plt.tight_layout(pad=3.0)

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
            text="Статистика: Задание 20",
            theme_text_color='Primary',
            font_style='H4',
            size_hint_y=None,
            height=dp(50),
            halign="center",
            bold=True
        )
        content_container.add_widget(title_label)

        # Круговая диаграмма
        try:
            pie_image = self.create_pie_chart_image()
            pie_widget = Image(
                texture=pie_image.texture,
                size_hint=(1, None),
                height=dp(350),
                allow_stretch=True,
                keep_ratio=True
            )
        except Exception as e:
            print(f"Ошибка создания круговой диаграммы: {e}")
            pie_widget = MDLabel(
                text="Ошибка загрузки диаграммы",
                theme_text_color='Error',
                halign='center',
                size_hint_y=None,
                height=dp(100)
            )

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
        pie_card.add_widget(pie_widget)
        content_container.add_widget(pie_card)

        # График сравнения (теперь только для задания 20)
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
            print(f"Ошибка создания графика: {e}")
            comparison_widget = MDLabel(
                text="Ошибка загрузки графика",
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

        # Детальная статистика текстом
        stats = self.load_statistics()
        task_stats = stats["task_20"]

        stats_text = f"""ДЕТАЛЬНАЯ СТАТИСТИКА - ЗАДАНИЕ 20

Правильных ответов: {task_stats['correct']}
Неправильных ответов: {task_stats['incorrect']}
Всего попыток: {task_stats['total']}
"""

        if task_stats['total'] > 0:
            percentage = (task_stats['correct'] / task_stats['total']) * 100
            stats_text += f"Процент правильных ответов: {percentage:.1f}%\n\n"

            # Добавляем рекомендацию (без эмодзи)
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

        # Устанавливаем минимальную высоту для текстовой статистики
        stats_label.height = dp(150)

        stats_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(0.95, 0.95, 1, 1),
            radius=[dp(15)],
            elevation=2,
            height=dp(200)
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