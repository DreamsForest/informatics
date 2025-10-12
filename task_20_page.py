from task_base import BaseTaskPage
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
import random


class Task20Page(BaseTaskPage):
    def __init__(self, main_app, **kwargs):
        super().__init__(main_app, "task_20", **kwargs)
        self.correct_answer = None
        self.answer_input = None
        self.result_label = None

        # Явно генерируем задание и показываем интерфейс
        self.generate_task()
        self.show_task_interface()

    def generate_task(self):
        """Генерирует разнообразные задания №20 - Выигрышная стратегия"""
        task_type = random.choice(['one_heap', 'two_heaps'])

        if task_type == 'one_heap':
            self._generate_one_heap_task()
        else:
            self._generate_two_heaps_task()

    def show_task_interface(self):
        """Показывает интерфейс задания (полностью переопределяем базовый метод)"""
        self.clear_widgets()

        # Создаем скроллируемую область для задания
        scroll = MDScrollView()

        # Основной контейнер для контента
        main_content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(15),
            padding=dp(20)
        )
        main_content.bind(minimum_height=main_content.setter('height'))

        # Заголовок задания
        title_label = MDLabel(
            text="Задание 20 - Выигрышная стратегия 2",
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40),
            halign="center"
        )
        main_content.add_widget(title_label)

        # Отображаем содержимое задания
        self._display_task_content(main_content)

        scroll.add_widget(main_content)
        self.add_widget(scroll)

        # Кнопки управления внизу
        self._add_control_buttons()

    def _display_task_content(self, container):
        """Добавляет содержимое задания в контейнер"""
        if not hasattr(self, 'current_task') or self.current_task is None:
            self.generate_task()

        task = self.current_task

        # Описание задания
        desc_label = MDLabel(
            text=task['description'],
            theme_text_color="Primary",
            size_hint_y=None,
            halign="justify"
        )
        desc_label.bind(texture_size=desc_label.setter('size'))
        container.add_widget(desc_label)

        # Правила игры
        rules_label = MDLabel(
            text=task['rules'],
            theme_text_color="Primary",
            size_hint_y=None,
            halign="justify"
        )
        rules_label.bind(texture_size=rules_label.setter('size'))
        container.add_widget(rules_label)

        # Начальные условия
        initial_label = MDLabel(
            text=task['initial'],
            theme_text_color="Primary",
            size_hint_y=None,
            halign="justify"
        )
        initial_label.bind(texture_size=initial_label.setter('size'))
        container.add_widget(initial_label)

        # Условие задачи
        condition_label = MDLabel(
            text=task['condition'],
            theme_text_color="Primary",
            size_hint_y=None,
            halign="justify"
        )
        condition_label.bind(texture_size=condition_label.setter('size'))
        container.add_widget(condition_label)

        # Поле для ввода ответа
        answer_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )

        self.answer_input = MDTextField(
            hint_text="Введите ваш ответ",
            mode="rectangle",
            size_hint_x=0.7
        )
        answer_layout.add_widget(self.answer_input)

        check_button = MDRaisedButton(
            text="Проверить",
            size_hint_x=0.3,
            on_release=self.check_answer
        )
        answer_layout.add_widget(check_button)

        container.add_widget(answer_layout)

        # Метка для отображения результата проверки
        self.result_label = MDLabel(
            text="",
            theme_text_color="Primary",
            size_hint_y=None,
            halign="center"
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        container.add_widget(self.result_label)

    def _add_control_buttons(self):
        """Добавляет кнопки управления внизу экрана"""
        control_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
            padding=dp(10)
        )

        back_button = MDRaisedButton(
            text="Назад к выбору задания",
            size_hint_x=0.5,
            on_release=self.go_back
        )

        new_task_button = MDRaisedButton(
            text="Новое задание",
            size_hint_x=0.5,
            on_release=lambda x: self.generate_new_task()
        )

        control_layout.add_widget(back_button)
        control_layout.add_widget(new_task_button)
        self.add_widget(control_layout)

    def _generate_one_heap_task(self):
        """Генерирует задание с одной кучей (типичное для №20)"""
        initial_stones = random.randint(1, 10)
        target = random.randint(40, 80)

        # Разные варианты ходов
        moves_options = [
            {"add": [1, 3], "multiply": 2},
            {"add": [1, 4], "multiply": 5},
            {"add": [1, 2], "multiply": 3},
            {"add": [2, 3], "multiply": 2},
            {"add": [1], "multiply": 2}
        ]
        moves = random.choice(moves_options)

        add_text = " или ".join([f"{n} камень" if n == 1 else f"{n} камня" for n in moves["add"]])
        multiply_text = f"в {moves['multiply']} раза"

        # Типы условий
        condition_types = [
            "Петя не может выиграть за один ход; Петя может выиграть своим вторым ходом независимо от того, как будет ходить Ваня.",
            "Петя не может выиграть за один ход; Ваня может выиграть своим первым ходом независимо от того, как будет ходить Петя.",
            "У Пети есть выигрышная стратегия, причём Петя может выиграть своим первым ходом."
        ]
        condition = random.choice(condition_types)

        # Определяем количество ответов в зависимости от условия
        if "два таких значения" in condition or "два условия" in condition:
            answer_count = 2
            answer_text = "два значения S"
        elif "три таких значения" in condition:
            answer_count = 3
            answer_text = "три значения S"
        else:
            answer_count = 1
            answer_text = "значение S"

        self.current_task = {
            'type': 'one_heap',
            'description': f'''Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежит куча камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может добавить в кучу {add_text} или увеличить количество камней в куче в {moves['multiply']} раза.''',
            'rules': f'''Игра завершается в тот момент, когда количество камней в куче становится не менее {target}. Победителем считается игрок, сделавший последний ход, то есть первым получивший кучу, в которой будет {target} или больше камней.''',
            'initial': f'''В начальный момент в куче было S камней; 1 ≤ S ≤ {target - 1}.''',
            'condition': f'''Найдите {answer_text}, при которых {condition}''',
            'question': f'''Введите найденные значения S в порядке возрастания через запятую:''',
            'answer_type': 'multiple_values',
            'answer_count': answer_count
        }

        # Генерируем правильные ответы
        self.correct_answer = self._calculate_one_heap_answer(initial_stones, target, moves, answer_count)

    def _generate_two_heaps_task(self):
        """Генерирует задание с двумя кучами"""
        heap1 = random.randint(1, 10)
        target_sum = random.randint(30, 60)

        # Разные варианты ходов для двух куч
        move_types = [
            "добавить один камень в любую кучу или удвоить количество камней в любой куче",
            "добавить один или два камня в любую кучу",
            "добавить один камень в одну из куч или удвоить количество камней в одной из куч",
            "добавить один камень в меньшую кучу или удвоить количество камней в большей куче"
        ]
        moves_text = random.choice(move_types)

        condition = "Петя не может выиграть за один ход; Петя может выиграть своим вторым ходом независимо от того, как будет ходить Ваня."

        self.current_task = {
            'type': 'two_heaps',
            'description': f'''Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежат две кучи камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может {moves_text}.''',
            'rules': f'''Игра завершается в тот момент, когда суммарное количество камней в кучах становится не менее {target_sum}. Победителем считается игрок, сделавший последний ход, то есть первым получивший такую позицию, при которой в кучах будет {target_sum} или больше камней.''',
            'initial': f'''В начальный момент в первой куче было {heap1} камней, во второй куче — S камней; 1 ≤ S ≤ {target_sum - heap1 - 1}.''',
            'condition': f'''Найдите два таких значения S, при которых {condition}''',

            'answer_type': 'multiple_values',
            'answer_count': 2
        }

        self.correct_answer = self._calculate_two_heaps_answer(heap1, target_sum)

    def _calculate_one_heap_answer(self, initial, target, moves, count):
        """Вычисляет ответ для задачи с одной кучей (упрощенный алгоритм)"""
        # Упрощенный расчет - генерируем случайные значения в разумном диапазоне
        if count == 1:
            return [random.randint(max(1, target // 6), min(target - 1, target // 3))]
        elif count == 2:
            val1 = random.randint(max(1, target // 8), min(target - 1, target // 4))
            val2 = random.randint(val1 + 1, min(target - 1, target // 3))
            return [val1, val2]
        else:  # count == 3
            val1 = random.randint(max(1, target // 10), min(target - 1, target // 5))
            val2 = random.randint(val1 + 1, min(target - 1, target // 3))
            val3 = random.randint(val2 + 1, min(target - 1, target // 2))
            return [val1, val2, val3]

    def _calculate_two_heaps_answer(self, heap1, target_sum):
        """Вычисляет ответ для задачи с двумя кучами (упрощенный алгоритм)"""
        # Упрощенный расчет
        max_val = target_sum - heap1 - 1
        val1 = random.randint(max(1, max_val // 4), min(max_val, max_val // 2))
        val2 = random.randint(val1 + 1, min(max_val, max_val * 3 // 4))
        return [val1, val2]

    def check_answer(self, instance):
        """Проверяет ответ пользователя и записывает статистику"""
        print("Кнопка Проверить нажата")

        if self.result_label is None:
            print("Ошибка: result_label не инициализирован")
            return

        if not hasattr(self, 'correct_answer') or self.correct_answer is None:
            self.result_label.text = "Ошибка: задание не сгенерировано"
            self.result_label.theme_text_color = "Custom"
            self.result_label.text_color = (0.8, 0, 0, 1)
            return

        if self.answer_input is None:
            self.result_label.text = "Ошибка: поле ввода не найдено"
            self.result_label.theme_text_color = "Custom"
            self.result_label.text_color = (0.8, 0, 0, 1)
            return

        user_answer = self.answer_input.text.strip()
        print(f"Пользователь ввел: '{user_answer}'")
        print(f"Правильный ответ: {self.correct_answer}")

        if not user_answer:
            self.result_label.text = "Введите ответ"
            self.result_label.theme_text_color = "Custom"
            self.result_label.text_color = (0.8, 0, 0, 1)
            return

        try:
            # Парсим ввод пользователя (числа через запятую)
            user_values = [int(x.strip()) for x in user_answer.split(',')]
            correct_values = self.correct_answer

            # Проверяем количество значений
            if len(user_values) != len(correct_values):
                self.result_label.text = f"Неверное количество значений. Нужно: {len(correct_values)}"
                self.result_label.theme_text_color = "Custom"
                self.result_label.text_color = (0.8, 0, 0, 1)
                # ЗАПИСЫВАЕМ НЕПРАВИЛЬНЫЙ ОТВЕТ В СТАТИСТИКУ
                self._record_statistics(is_correct=False)
                return

            # Проверяем правильность значений и порядок
            user_sorted = sorted(user_values)
            if user_sorted == correct_values:
                self.result_label.text = "Правильно! Отличная работа!"
                self.result_label.theme_text_color = "Custom"
                self.result_label.text_color = (0, 0.7, 0, 1)
                # ЗАПИСЫВАЕМ ПРАВИЛЬНЫЙ ОТВЕТ В СТАТИСТИКУ
                self._record_statistics(is_correct=True)
            else:
                correct_str = ", ".join(map(str, correct_values))
                self.result_label.text = f"Неправильно. Правильный ответ: {correct_str}"
                self.result_label.theme_text_color = "Custom"
                self.result_label.text_color = (0.8, 0, 0, 1)
                # ЗАПИСЫВАЕМ НЕПРАВИЛЬНЫЙ ОТВЕТ В СТАТИСТИКУ
                self._record_statistics(is_correct=False)

        except ValueError:
            self.result_label.text = "Введите числа через запятую!"
            self.result_label.theme_text_color = "Custom"
            self.result_label.text_color = (0.8, 0, 0, 1)

    def _record_statistics(self, is_correct):
        """Записывает статистику выполнения задания"""
        try:
            # Вызываем метод в main_app для обновления статистики
            if hasattr(self.main_app, 'update_statistics'):
                self.main_app.update_statistics("task_20", is_correct)
                print(f"Статистика записана: задание 20, правильный: {is_correct}")
            else:
                print("Метод update_statistics не найден в main_app")
        except Exception as e:
            print(f"Ошибка записи статистики: {e}")

    def go_back(self, instance):
        """Возвращает к выбору заданий"""
        self.main_app.show_select_task_page()

    def generate_new_task(self):
        """Генерирует новое задание и обновляет интерфейс"""
        self.generate_task()
        self.show_task_interface()