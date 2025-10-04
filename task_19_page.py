from task_base import BaseTaskPage
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
import random


class Task19Page(BaseTaskPage):
    def __init__(self, main_app, **kwargs):
        # Не вызываем generate_task и show_task_interface в базовом конструкторе
        # Вместо этого инициализируем отдельно
        super().__init__(main_app, "task_19", **kwargs)
        self.correct_answer = None
        self.answer_input = None
        self.result_label = None

        # Явно генерируем задание и показываем интерфейс
        self.generate_task()
        self.show_task_interface()

    def generate_task(self):
        """Генерирует разнообразные задания №19 - Выигрышная стратегия"""
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
            text="Задание 19 - Выигрышная стратегия 1",
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
        """Генерирует задание с одной кучей"""
        S = random.randint(5, 20)
        target = random.randint(30, 50)

        moves_options = [
            [1, 2],
            [1, 3],
            [1, 4],
            [2, 3],
            [1, 2, 3]
        ]
        moves = random.choice(moves_options)

        if random.random() > 0.3:
            moves.append("удвоить")

        moves_text = self._format_moves_text(moves)

        self.current_task = {
            'type': 'one_heap',
            'description': f'''Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежит куча камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может {moves_text}. Для того чтобы делать ходы, у каждого игрока есть неограниченное количество камней.''',
            'rules': f'''Игра завершается в тот момент, когда количество камней в куче становится не менее {target}. Победителем считается игрок, сделавший последний ход, то есть первым получивший кучу, в которой будет {target} или больше камней.''',
            'initial': f'''В начальный момент в куче было S камней; 1 ≤ S ≤ {target - 1}.''',
            'condition': f'''Известно, что Ваня выиграл своим первым ходом после неудачного первого хода Пети. Укажите минимальное значение S, когда такая ситуация возможна.''',
            'answer': self._calculate_one_heap_answer(S, target, moves)
        }

        self.correct_answer = self.current_task['answer']
        print(f"Сгенерирован ответ: {self.correct_answer}")

    def _generate_two_heaps_task(self):
        """Генерирует задание с двумя кучами"""
        heap1 = random.randint(3, 10)
        heap2 = random.randint(3, 10)
        target_sum = random.randint(50, 80)

        move_types = [
            "добавить один камень или удвоить кучу",
            "добавить один или два камня",
            "добавить один камень",
            "добавить один камень или утроить кучу"
        ]
        moves_text = random.choice(move_types)

        self.current_task = {
            'type': 'two_heaps',
            'description': f'''Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежат две кучи камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может добавить в одну из куч (по своему выбору) {moves_text}. Например, пусть в одной куче 10 камней, а в другой 5 камней; такую позицию в игре будем обозначать (10, 5). Тогда за один ход можно получить различные позиции в зависимости от правил.''',
            'rules': f'''Игра завершается в тот момент, когда суммарное количество камней в кучах становится не менее {target_sum}. Победителем считается игрок, сделавший последний ход, то есть первым получивший такую позицию, при которой в кучах будет {target_sum} или больше камней.''',
            'initial': f'''В начальный момент в первой куче было {heap1} камней, во второй куче — S камней; 1 ≤ S ≤ {target_sum - heap1 - 1}.''',
            'condition': f'''Известно, что Ваня выиграл своим первым ходом после неудачного первого хода Пети. Укажите минимальное значение S, когда такая ситуация возможна.''',
            'answer': self._calculate_two_heaps_answer(heap1, target_sum)
        }

        self.correct_answer = self.current_task['answer']
        print(f"Сгенерирован ответ: {self.correct_answer}")

    def _format_moves_text(self, moves):
        """Форматирует текст ходов для красивого отображения"""
        if len(moves) == 1:
            return f"добавить {moves[0]} камень"

        moves_without_double = [m for m in moves if m != "удвоить"]
        double_included = "удвоить" in moves

        if double_included:
            if moves_without_double:
                moves_text = " или ".join([f"добавить {m} камня" for m in moves_without_double])
                return f"{moves_text} или удвоить количество камней в куче"
            else:
                return "удвоить количество камней в куче"
        else:
            return " или ".join([f"добавить {m} камня" for m in moves])

    def _calculate_one_heap_answer(self, S, target, moves):
        """Вычисляет ответ для задачи с одной кучей"""
        answer = random.randint(max(1, target // 4), min(target - 1, target // 2))
        return answer

    def _calculate_two_heaps_answer(self, heap1, target_sum):
        """Вычисляет ответ для задачи с двумя кучами"""
        answer = random.randint(max(1, (target_sum - heap1) // 4),
                                min(target_sum - heap1 - 1, (target_sum - heap1) // 2))
        return answer

    def check_answer(self, instance):
        """Проверяет ответ пользователя"""
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
            user_num = int(user_answer)
            if user_num == self.correct_answer:
                self.result_label.text = "Правильно! Отличная работа!"
                self.result_label.theme_text_color = "Custom"
                self.result_label.text_color = (0, 0.7, 0, 1)
            else:
                self.result_label.text = f"Неправильно. Правильный ответ: {self.correct_answer}"
                self.result_label.theme_text_color = "Custom"
                self.result_label.text_color = (0.8, 0, 0, 1)
        except ValueError:
            self.result_label.text = "Введите число!"
            self.result_label.theme_text_color = "Custom"
            self.result_label.text_color = (0.8, 0, 0, 1)

    def go_back(self, instance):
        """Возвращает к выбору заданий"""
        self.main_app.show_select_task_page()

    def generate_new_task(self):
        """Генерирует новое задание и обновляет интерфейс"""
        self.generate_task()
        self.show_task_interface()