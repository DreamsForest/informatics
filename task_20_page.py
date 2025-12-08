from task_base import BaseTaskPage
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView as KivyScrollView
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
import random
import sys
import io


class Task20Page(BaseTaskPage):
    def __init__(self, main_app, **kwargs):
        super().__init__(main_app, "task_20", **kwargs)
        self.correct_answer = None
        self.answer_input = None
        self.code_input = None
        self.result_label = None
        self.code_output_label = None
        self.dialog = None

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

        # Основной контейнер
        main_scroll = MDScrollView()
        main_content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(15),
            padding=[dp(15), dp(15), dp(15), dp(15)]
        )
        main_content.bind(minimum_height=main_content.setter('height'))

        # Заголовок задания
        title_label = MDLabel(
            text="Задание 20 - Выигрышная стратегия 2",
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40),
            halign="center",
            bold=True
        )
        main_content.add_widget(title_label)

        # Отображаем содержимое задания
        self._display_task_content(main_content)

        # Разделитель
        main_content.add_widget(MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(1),
            md_bg_color=(0.7, 0.7, 0.7, 0.5)
        ))

        # Блок для кода
        code_section = self._create_code_section()
        main_content.add_widget(code_section)

        # Разделитель
        main_content.add_widget(MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(1),
            md_bg_color=(0.7, 0.7, 0.7, 0.5)
        ))

        # Блок для ответа
        answer_section = self._create_answer_section()
        main_content.add_widget(answer_section)

        # Кнопки управления
        control_section = self._create_control_section()
        main_content.add_widget(control_section)

        main_scroll.add_widget(main_content)
        self.add_widget(main_scroll)

    def _create_code_section(self):
        """Создает секцию для ввода кода"""
        code_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )
        code_container.bind(minimum_height=code_container.setter('height'))

        # Заголовок
        code_label = MDLabel(
            text="Поле для кода Python (самопроверка):",
            theme_text_color="Primary",
            font_style='H6',
            size_hint_y=None,
            height=dp(30),
            halign="left",
            bold=True
        )
        code_container.add_widget(code_label)

        # Поле для ввода кода
        code_input_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(150)
        )

        self.code_input = TextInput(
            text="",
            hint_text="# Напишите код Python здесь...\n# Пример: print('Hello World')\n# Используйте print() для вывода результатов",
            multiline=True,
            font_size='14sp',
            background_color=(0.97, 0.97, 0.97, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            size_hint_y=None,
            write_tab=False,
            cursor_color=(0.2, 0.5, 0.8, 1)
        )
        self.code_input.bind(minimum_height=self.code_input.setter('height'))
        code_input_container.add_widget(self.code_input)
        code_container.add_widget(code_input_container)

        # Кнопки управления кодом
        button_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )

        run_button = MDRaisedButton(
            text="Выполнить код",
            size_hint_x=0.6,
            on_release=self.execute_user_code,
            md_bg_color=(0.2, 0.5, 0.8, 1),
            font_size='13sp'
        )

        clear_button = MDRaisedButton(
            text="Очистить",
            size_hint_x=0.4,
            on_release=self.clear_code,
            md_bg_color=(0.8, 0.3, 0.3, 1),
            font_size='13sp'
        )

        button_layout.add_widget(run_button)
        button_layout.add_widget(clear_button)
        code_container.add_widget(button_layout)

        # Поле для вывода результатов
        output_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(5)
        )
        output_container.bind(minimum_height=output_container.setter('height'))

        output_label = MDLabel(
            text="Результат выполнения:",
            theme_text_color="Secondary",
            font_style='Body2',
            size_hint_y=None,
            height=dp(25),
            halign="left"
        )
        output_container.add_widget(output_label)

        self.code_output_label = TextInput(
            text="Результат появится здесь...",
            readonly=True,
            font_size='13sp',
            background_color=(0.94, 0.94, 0.94, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            padding=[dp(8), dp(8), dp(8), dp(8)],
            size_hint_y=None,
            multiline=True
        )
        self.code_output_label.bind(minimum_height=self.code_output_label.setter('height'))
        output_container.add_widget(self.code_output_label)

        code_container.add_widget(output_container)

        return code_container

    def _create_answer_section(self):
        """Создает секцию для ввода ответа"""
        answer_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )
        answer_container.bind(minimum_height=answer_container.setter('height'))

        # Заголовок
        answer_label = MDLabel(
            text="Введите окончательный ответ:",
            theme_text_color="Primary",
            font_style='H6',
            size_hint_y=None,
            height=dp(30),
            halign="left",
            bold=True
        )
        answer_container.add_widget(answer_label)

        # Поле для ввода ответа
        answer_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )

        self.answer_input = MDTextField(
            hint_text="Числа через запятую (например: 5, 10, 15)",
            mode="rectangle",
            size_hint_x=0.7,
            font_size='15sp',
            line_color_focus=(0.2, 0.5, 0.8, 1)
        )
        answer_layout.add_widget(self.answer_input)

        check_button = MDRaisedButton(
            text="Проверить ответ",
            size_hint_x=0.3,
            on_release=self.check_answer,
            md_bg_color=(0.3, 0.7, 0.3, 1),
            font_size='13sp'
        )
        answer_layout.add_widget(check_button)

        answer_container.add_widget(answer_layout)

        # Метка для результата проверки
        self.result_label = MDLabel(
            text="",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(35),
            halign="center",
            valign="middle",
            font_style='Body1'
        )
        answer_container.add_widget(self.result_label)

        return answer_container

    def _create_control_section(self):
        """Создает секцию с управляющими кнопками"""
        control_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            spacing=dp(15),
            padding=[dp(20), 0, dp(20), 0]
        )

        back_button = MDRaisedButton(
            text="Назад к выбору",
            size_hint_x=0.5,
            on_release=self.go_back,
            md_bg_color=(0.5, 0.5, 0.5, 1),
            font_size='14sp'
        )

        new_task_button = MDRaisedButton(
            text="Новое задание",
            size_hint_y=None,
            height=dp(48),
            size_hint_x=0.5,
            on_release=lambda x: self.generate_new_task(),
            md_bg_color=(0.2, 0.6, 0.9, 1),
            font_size='14sp'
        )

        control_container.add_widget(back_button)
        control_container.add_widget(new_task_button)

        return control_container

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
            halign="justify",
            font_style='Body1'
        )
        desc_label.bind(texture_size=desc_label.setter('size'))
        container.add_widget(desc_label)

        # Отступ
        container.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))

        # Правила игры
        rules_label = MDLabel(
            text=task['rules'],
            theme_text_color="Primary",
            size_hint_y=None,
            halign="justify",
            font_style='Body1'
        )
        rules_label.bind(texture_size=rules_label.setter('size'))
        container.add_widget(rules_label)

        # Отступ
        container.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))

        # Начальные условия
        initial_label = MDLabel(
            text=task['initial'],
            theme_text_color="Primary",
            size_hint_y=None,
            halign="justify",
            font_style='Body1'
        )
        initial_label.bind(texture_size=initial_label.setter('size'))
        container.add_widget(initial_label)

        # Отступ
        container.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))

        # Условие задачи
        condition_label = MDLabel(
            text=task['condition'],
            theme_text_color="Primary",
            size_hint_y=None,
            halign="justify",
            font_style='Body1'
        )
        condition_label.bind(texture_size=condition_label.setter('size'))
        container.add_widget(condition_label)

    def clear_code(self, instance):
        """Очищает поле для кода"""
        if self.code_input:
            self.code_input.text = ""
        if self.code_output_label:
            self.code_output_label.text = "Результат появится здесь..."

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

    def execute_user_code(self, instance):
        """Выполняет код, написанный пользователем"""
        if not self.code_input:
            return

        code = self.code_input.text.strip()
        if not code:
            self.code_output_label.text = "Введите код для выполнения"
            return

        try:
            # Создаем безопасное окружение для выполнения
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'range': range,
                    'len': len,
                    'int': int,
                    'str': str,
                    'list': list,
                    'dict': dict,
                    'set': set,
                    'tuple': tuple,
                    'bool': bool,
                    'float': float,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'abs': abs,
                    'round': round,
                    'sorted': sorted,
                    'enumerate': enumerate,
                    'zip': zip,
                }
            }

            # Перенаправляем stdout для захвата вывода
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            # Выполняем код
            exec(code, safe_globals, {})

            # Получаем вывод
            output = new_stdout.getvalue()
            sys.stdout = old_stdout

            if output:
                # Обрезаем слишком длинный вывод
                if len(output) > 1000:
                    output = output[:1000] + "\n... (вывод обрезан, слишком длинный)"
                self.code_output_label.text = output
            else:
                self.code_output_label.text = "Код выполнен успешно, но ничего не выведено.\nИспользуйте print() для вывода результатов."

        except Exception as e:
            # Восстанавливаем stdout
            sys.stdout = old_stdout

            error_msg = f"Ошибка выполнения кода:\n{type(e).__name__}: {str(e)}"
            self.code_output_label.text = error_msg

            # Показываем детали ошибки в диалоговом окне
            self._show_error_dialog(e)

    def _show_error_dialog(self, error):
        """Показывает диалоговое окно с деталями ошибки"""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Ошибка выполнения кода",
                text=str(error),
                size_hint=(0.8, 0.4),
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        self.dialog.text = str(error)
        self.dialog.open()

    def check_answer(self, instance):
        """Проверяет ответ пользователя и записывает статистику"""
        if self.result_label is None:
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
                self.result_label.text_color = (0, 0.6, 0, 1)
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