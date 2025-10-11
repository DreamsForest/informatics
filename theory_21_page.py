from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
import pyperclip


class SyntaxHighlighter:
    """Простой синтаксический высоклайтер для разных языков"""

    @staticmethod
    def highlight_python(code):
        """Подсветка Python кода"""
        # Ключевые слова Python
        keywords = ['def', 'return', 'if', 'else', 'elif', 'for', 'while', 'in', 'and', 'or', 'not', 'True', 'False',
                    'None']
        # Типы данных
        types = ['int', 'float', 'str', 'list', 'dict', 'set', 'tuple']

        lines = code.split('\n')
        highlighted = []

        for line in lines:
            if line.strip().startswith('#'):
                # Комментарии - зеленый
                highlighted.append(f"[color=228B22]{line}[/color]")
            else:
                highlighted_line = line
                # Ключевые слова - синий
                for keyword in keywords:
                    highlighted_line = highlighted_line.replace(f" {keyword} ", f" [color=87CEEB]{keyword}[/color] ")
                    highlighted_line = highlighted_line.replace(f" {keyword}(", f" [color=87CEEB]{keyword}[/color](")
                # Типы - фиолетовый
                for type_word in types:
                    highlighted_line = highlighted_line.replace(f" {type_word} ",
                                                                f" [color=DDA0DD]{type_word}[/color] ")
                # Строки - красный
                if '\"' in line or "'" in line:
                    parts = highlighted_line.split('"')
                    if len(parts) > 1:
                        for i in range(1, len(parts), 2):
                            parts[i] = f'[color=FF6B6B]"{parts[i]}"[/color]'
                        highlighted_line = '"'.join(parts)

                # Числа - оранжевый
                words = highlighted_line.split()
                for i, word in enumerate(words):
                    if word.isdigit() or (word.replace('.', '').isdigit() and '.' in word):
                        words[i] = f'[color=FFA500]{word}[/color]'
                highlighted_line = ' '.join(words)

                highlighted.append(highlighted_line)

        return '\n'.join(highlighted)

    @staticmethod
    def highlight_cpp(code):
        """Подсветка C++ кода"""
        keywords = ['include', 'using', 'namespace', 'int', 'bool', 'void', 'return', 'if', 'else', 'for', 'while',
                    'true', 'false']

        lines = code.split('\n')
        highlighted = []

        for line in lines:
            if line.strip().startswith('//'):
                highlighted.append(f"[color=228B22]{line}[/color]")
            else:
                highlighted_line = line
                for keyword in keywords:
                    highlighted_line = highlighted_line.replace(f" {keyword} ", f" [color=87CEEB]{keyword}[/color] ")
                    highlighted_line = highlighted_line.replace(f" {keyword}(", f" [color=87CEEB]{keyword}[/color](")
                    highlighted_line = highlighted_line.replace(f" {keyword}<", f" [color=87CEEB]{keyword}[/color]<")
                    highlighted_line = highlighted_line.replace(f" {keyword};", f" [color=87CEEB]{keyword}[/color];")

                # Директивы препроцессора - фиолетовый
                if line.strip().startswith('#'):
                    highlighted_line = f"[color=DDA0DD]{line}[/color]"

                highlighted.append(highlighted_line)

        return '\n'.join(highlighted)

    @staticmethod
    def highlight_java(code):
        """Подсветка Java кода"""
        keywords = ['public', 'class', 'static', 'void', 'int', 'boolean', 'return', 'if', 'else', 'for', 'while',
                    'true', 'false']

        lines = code.split('\n')
        highlighted = []

        for line in lines:
            if line.strip().startswith('//'):
                highlighted.append(f"[color=228B22]{line}[/color]")
            else:
                highlighted_line = line
                for keyword in keywords:
                    highlighted_line = highlighted_line.replace(f" {keyword} ", f" [color=87CEEB]{keyword}[/color] ")
                    highlighted_line = highlighted_line.replace(f" {keyword}(", f" [color=87CEEB]{keyword}[/color](")

                highlighted.append(highlighted_line)

        return '\n'.join(highlighted)

    @staticmethod
    def highlight_pascal(code):
        """Подсветка Pascal кода"""
        keywords = ['program', 'const', 'type', 'var', 'function', 'procedure', 'begin', 'end', 'if', 'then', 'else',
                    'for', 'to', 'do', 'while', 'array', 'of', 'integer', 'boolean']

        lines = code.split('\n')
        highlighted = []

        for line in lines:
            if line.strip().startswith('//') or line.strip().startswith('{'):
                highlighted.append(f"[color=228B22]{line}[/color]")
            else:
                highlighted_line = line
                for keyword in keywords:
                    highlighted_line = highlighted_line.replace(f" {keyword} ", f" [color=87CEEB]{keyword}[/color] ")
                    highlighted_line = highlighted_line.replace(f" {keyword}(", f" [color=87CEEB]{keyword}[/color](")
                    highlighted_line = highlighted_line.replace(f" {keyword};", f" [color=87CEEB]{keyword}[/color];")

                highlighted.append(highlighted_line)

        return '\n'.join(highlighted)


class CodeCard(MDCard):
    """Карточка с кодом на определенном языке программирования"""

    def __init__(self, language, code, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        self.size_hint_y = None
        self.md_bg_color = (0.1, 0.1, 0.2, 1)  # Темный фон для кода
        self.radius = [dp(10)]
        self.elevation = 2

        # Заголовок с названием языка
        title = MDLabel(
            text=f"Язык: {language}",
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),  # Белый текст
            font_style='H6',
            size_hint_y=None,
            height=dp(30),
            halign="center"
        )
        self.add_widget(title)

        # Контейнер для кода с прокруткой
        code_scroll = ScrollView(
            size_hint_y=None,
            height=dp(350),
            do_scroll_x=False,
            bar_color=(0.5, 0.5, 0.7, 1)
        )

        # Подсветка кода в зависимости от языка
        highlighted_code = code
        if language == "Python":
            highlighted_code = SyntaxHighlighter.highlight_python(code)
        elif language == "C++":
            highlighted_code = SyntaxHighlighter.highlight_cpp(code)
        elif language == "Java":
            highlighted_code = SyntaxHighlighter.highlight_java(code)
        elif language == "Pascal":
            highlighted_code = SyntaxHighlighter.highlight_pascal(code)

        # Поле для отображения кода
        code_label = MDLabel(
            text=highlighted_code,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),  # Белый текст для кода
            size_hint_y=None,
            halign="left",
            valign="top",
            markup=True  # Включаем разметку для цветов
        )
        code_label.bind(texture_size=code_label.setter('size'))

        code_scroll.add_widget(code_label)

        # Кнопка копирования
        copy_button = MDFlatButton(
            text="Копировать код",
            theme_text_color='Custom',
            text_color=(0.8, 0.8, 1, 1),
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.copy_code(code, language)
        )

        self.add_widget(code_scroll)
        self.add_widget(copy_button)

        # Устанавливаем высоту карточки
        self.bind(minimum_height=self.setter('height'))

    def copy_code(self, code, language):
        """Копирует код в буфер обмена"""
        try:
            pyperclip.copy(code)
            # Можно добавить уведомление о копировании
            print(f"Код на {language} скопирован в буфер обмена")
        except Exception as e:
            print(f"Ошибка копирования: {e}")


class Theory21Page(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        self.dialog = None

        self.show_theory_content()

    def show_theory_content(self):
        """Показывает содержание теории для задания 21"""
        self.clear_widgets()

        # Создаем ScrollView для контента
        scroll_view = ScrollView(do_scroll_x=False)

        # Основной контейнер для контента
        content_container = MDBoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(15),
            size_hint_y=None
        )
        content_container.bind(minimum_height=content_container.setter('height'))

        # Заголовок
        title_label = MDLabel(
            text="Теория: Задание 21 - выигрышная стратегия 3",
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40),
            halign="center"
        )
        content_container.add_widget(title_label)

        # Условие задачи
        condition_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 0.95, 0.9, 1),
            radius=[dp(10)],
            elevation=2
        )
        condition_card.bind(minimum_height=condition_card.setter('height'))

        condition_title = MDLabel(
            text="Типичное условие задания 21",
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(30),
            halign="center"
        )
        condition_card.add_widget(condition_title)

        condition_text = MDLabel(
            text='''Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежит куча камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может добавить в кучу 1 или 2 камня или увеличить количество камней в куче в 2 раза.

Игра завершается в тот момент, когда количество камней в куче становится не менее 50. Победителем считается игрок, сделавший последний ход.

Найдите минимальное значение S, при котором одновременно выполняются два условия:
1) У Вани есть выигрышная стратегия, позволяющая ему выиграть первым или вторым ходом при любой игре Пети;
2) У Вани нет стратегии, которая позволит ему гарантированно выиграть первым ходом.''',
            theme_text_color='Secondary',
            size_hint_y=None,
            halign="justify"
        )
        condition_text.bind(texture_size=condition_text.setter('size'))
        condition_card.add_widget(condition_text)

        content_container.add_widget(condition_card)

        # Основной контент теории
        theory_content = [
            {
                'title': 'Особенности задания 21',
                'content': '''Задание 21 - самое сложное в этой группе. Оно требует глубокого анализа игрового дерева на 3-4 хода вперед и работы со сложными комбинированными условиями. Часто требуется найти значение S, удовлетворяющее нескольким противоречивым условиям одновременно.''',
            },
            {
                'title': 'Типичные условия в задании 21',
                'content': '''• "У Вани есть выигрышная стратегия, позволяющая выиграть первым или вторым ходом"
• "У Вани нет стратегии, которая позволит выиграть первым ходом"
• "У Пети есть выигрышная стратегия, но он не может выиграть первым ходом"
• "Найдите минимальное значение S, при котором выполняются два условия"''',
            },
            {
                'title': 'Метод решения',
                'content': '''1. Определяем выигрышные позиции за 1 ход
2. Находим позиции для выигрыша за 2 хода
3. Анализируем позиции для выигрыша за 3 хода
4. Ищем S, удовлетворяющие сложным условиям:
   - Игрок может выиграть за 1 ИЛИ 2 хода
   - Но НЕ может выиграть гарантированно за 1 ход
5. Проверяем минимальность найденного S''',
            },
            {
                'title': 'Анализ двойных условий',
                'content': '''Для условия "Ваня может выиграть за 1 или 2 хода, но не может гарантированно за 1 ход":
• Ваня может выиграть за 1 ход только при неудачной игре Пети
• Ваня всегда выигрывает за 2 хода при любой игре Пети
• Находим S, где у Вани есть "запасной" вариант на 2 хода''',
            },
            {
                'title': 'Стратегия для сложных условий',
                'content': '''1. Постройте полное дерево игры на 3 хода вперед
2. Помечайте позиции:
   - В1: Ваня выигрывает за 1 ход
   - В2: Ваня выигрывает за 2 хода
   - П1: Петя выигрывает за 1 ход
   - П2: Петя выигрывает за 2 хода
3. Ищите S, где есть В2, но нет гарантированного В1''',
            },
            {
                'title': 'Работа с двумя кучами',
                'content': '''Для задач с двумя кучами:
• Используйте двумерные таблицы
• Анализируйте сумму камней и отдельные кучи
• Учитывайте, что ходы можно делать в разные кучи
• Сложность возрастает экспоненциально''',
            },
            {
                'title': 'Важные моменты',
                'content': '''• Внимательно анализируйте формулировки "при любой игре" и "гарантированно"
• Проверяйте все возможные ветвления дерева игры
• Для двух куч используйте системный перебор
• Всегда проверяйте минимальность найденного решения
• Учитывайте, что соперник играет оптимально''',
            }
        ]

        for section in theory_content:
            # Создаем карточку для каждого раздела
            card = MDCard(
                orientation='vertical',
                size_hint_y=None,
                padding=dp(15),
                spacing=dp(10),
                md_bg_color=(0.95, 0.95, 1, 1),
                radius=[dp(10)],
                elevation=1
            )
            card.bind(minimum_height=card.setter('height'))

            # Заголовок раздела
            title = MDLabel(
                text=section['title'],
                theme_text_color='Primary',
                font_style='H6',
                size_hint_y=None,
                height=dp(30),
                halign="left"
            )
            card.add_widget(title)

            # Содержание раздела
            content = MDLabel(
                text=section['content'],
                theme_text_color='Secondary',
                size_hint_y=None,
                halign="left"
            )
            content.bind(texture_size=content.setter('size'))
            card.add_widget(content)

            content_container.add_widget(card)

        # Блок с готовыми решениями на разных языках
        solutions_title_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=(0.9, 0.95, 0.9, 1),
            radius=[dp(10)],
            elevation=1
        )
        solutions_title_card.bind(minimum_height=solutions_title_card.setter('height'))

        solutions_title = MDLabel(
            text="Готовые решения на разных языках программирования",
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40),
            halign="center"
        )
        solutions_title_card.add_widget(solutions_title)

        solutions_description = MDLabel(
            text="Ниже представлены готовые решения сложной задачи на различных языках программирования. Вы можете изучать алгоритмы и копировать код для использования.",
            theme_text_color='Secondary',
            size_hint_y=None,
            halign="center"
        )
        solutions_description.bind(texture_size=solutions_description.setter('size'))
        solutions_title_card.add_widget(solutions_description)

        content_container.add_widget(solutions_title_card)

        # Добавляем карточки с кодом для каждого языка
        languages = [
            ("Python", self.get_python_code()),
            ("C++", self.get_cpp_code()),
            ("Pascal", self.get_pascal_code()),
            ("Java", self.get_java_code())
        ]

        for language, code in languages:
            code_card = CodeCard(language=language, code=code)
            content_container.add_widget(code_card)

        # Кнопка возврата
        back_button = MDRaisedButton(
            text="Назад к теории",
            size_hint_y=None,
            height=dp(50),
            on_release=lambda x: self.main_app.show_theory_page()
        )
        content_container.add_widget(back_button)

        scroll_view.add_widget(content_container)
        self.add_widget(scroll_view)

    def get_python_code(self):
        """Возвращает код решения на Python"""
        return '''# Задание 21: Сложная выигрышная стратегия
# Условие: Найдите минимальное S, при котором Ваня может выиграть 
# за 1 или 2 хода, но не может гарантированно выиграть за 1 ход.

def analyze_complex_game(target, moves, multiply):
    """
    Анализирует сложную игру для задания 21.
    Находит S, удовлетворяющее двойному условию.
    """
    # Множества позиций для сложного анализа
    win_1 = set()      # Выигрыш за 1 ход
    win_2 = set()      # Выигрыш за 2 хода  
    win_1_or_2 = set() # Выигрыш за 1 ИЛИ 2 хода
    complex_win = set() # Сложные позиции для задания 21

    # Шаг 1: Находим выигрышные позиции за 1 ход
    for stones in range(target, -1, -1):
        can_win = any(stones + move >= target for move in moves) or stones * multiply >= target
        if can_win and stones < target:
            win_1.add(stones)

    # Шаг 2: Находим выигрышные позиции за 2 хода
    for stones in range(target, -1, -1):
        if stones in win_1:
            continue

        # Проверяем, можно ли выиграть за 2 хода
        can_win_in_2 = False
        for move in moves:
            next_pos = stones + move
            if next_pos < target:
                # Проверяем, что у Вани есть выигрышный ответ на любой ход Пети
                vanya_can_win = True
                for petya_move in moves:
                    petya_next = next_pos + petya_move
                    if petya_next < target and petya_next not in win_1:
                        # Проверяем умножение
                        petya_mult = next_pos * multiply
                        if petya_mult < target and petya_mult not in win_1:
                            vanya_can_win = False
                            break
                if vanya_can_win:
                    can_win_in_2 = True
                    break

        # Проверяем операцию умножения
        mult_pos = stones * multiply
        if mult_pos < target:
            vanya_can_win = True
            for petya_move in moves:
                petya_next = mult_pos + petya_move
                if petya_next < target and petya_next not in win_1:
                    petya_mult = mult_pos * multiply
                    if petya_mult < target and petya_mult not in win_1:
                        vanya_can_win = False
                        break
            if vanya_can_win:
                can_win_in_2 = True

        if can_win_in_2:
            win_2.add(stones)

    # Шаг 3: Находим позиции для сложного условия задания 21
    for stones in range(1, target):
        # Условие 1: Ваня может выиграть за 1 ИЛИ 2 хода
        can_win_1_or_2 = stones in win_1 or stones in win_2

        # Условие 2: Ваня НЕ может гарантированно выиграть за 1 ход
        # Это значит, что есть хотя бы один ход Пети, после которого Ваня не выигрывает за 1 ход
        cannot_win_guaranteed_1 = False
        if stones in win_1:
            # Проверяем, есть ли ход Пети, который не ведет к немедленному выигрышу Вани
            for petya_move in moves:
                petya_pos = stones + petya_move
                if petya_pos < target and petya_pos not in win_1:
                    cannot_win_guaranteed_1 = True
                    break
            petya_mult = stones * multiply
            if petya_mult < target and petya_mult not in win_1:
                cannot_win_guaranteed_1 = True
        else:
            cannot_win_guaranteed_1 = True

        if can_win_1_or_2 and cannot_win_guaranteed_1:
            complex_win.add(stones)

    # Находим минимальное S
    return min(complex_win) if complex_win else -1

# Параметры задачи
target = 50
moves = [1, 2]
multiply = 2

# Находим решение
solution = analyze_complex_game(target, moves, multiply)
print(f"Минимальное S, удовлетворяющее условиям: {solution}")

# Альтернативный подход с полным деревом игры
def build_game_tree(target, moves, multiply, max_depth=4):
    """
    Строит дерево игры для глубокого анализа.
    """
    # Словарь для хранения информации о позициях
    game_tree = {}

    # Заполняем дерево от конечных позиций
    for stones in range(target * 2, -1, -1):
        if stones >= target:
            game_tree[stones] = {'win_in': 0, 'can_win': True}
        else:
            # Анализируем все возможные ходы
            next_positions = []
            for move in moves:
                next_positions.append(stones + move)
            next_positions.append(stones * multiply)

            # Находим минимальное количество ходов до победы
            min_win_moves = float('inf')
            can_win = False

            for next_pos in next_positions:
                if next_pos in game_tree and game_tree[next_pos]['can_win']:
                    can_win = True
                    min_win_moves = min(min_win_moves, game_tree[next_pos]['win_in'] + 1)

            game_tree[stones] = {
                'win_in': min_win_moves if can_win else float('inf'),
                'can_win': can_win
            }

    return game_tree

def find_complex_solution(game_tree, target):
    """
    Находит решение для задания 21 по построенному дереву игры.
    """
    solutions = []

    for S in range(1, target):
        if not game_tree[S]['can_win']:
            continue

        win_in = game_tree[S]['win_in']

        # Проверяем сложные условия
        # Ваня может выиграть за 1 или 2 хода
        can_win_1_or_2 = win_in in [1, 2]

        # Но не может гарантированно выиграть за 1 ход
        # (должен быть хотя бы один вариант, где выигрыш за 2 хода)
        cannot_guarantee_1 = True

        if can_win_1_or_2 and cannot_guarantee_1:
            solutions.append(S)

    return min(solutions) if solutions else -1

print("\\nАльтернативный подход с деревом игры:")
game_tree = build_game_tree(target, moves, multiply)
complex_solution = find_complex_solution(game_tree, target)
print(f"Решение: {complex_solution}")'''

    def get_cpp_code(self):
        """Возвращает код решения на C++"""
        return '''#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <map>
#include <climits>

using namespace std;

// Функция для анализа сложной игры задания 21
int analyzeComplexGame(int target, vector<int> moves, int multiply) {
    set<int> win1;  // Выигрыш за 1 ход
    set<int> win2;  // Выигрыш за 2 хода
    set<int> complexWin; // Позиции для задания 21

    // Находим выигрышные позиции за 1 ход
    for (int stones = target; stones >= 0; stones--) {
        bool canWin = false;

        for (int move : moves) {
            if (stones + move >= target) {
                canWin = true;
                break;
            }
        }

        if (stones * multiply >= target) {
            canWin = true;
        }

        if (canWin && stones < target) {
            win1.insert(stones);
        }
    }

    // Находим выигрышные позиции за 2 хода
    for (int stones = target; stones >= 0; stones--) {
        if (win1.find(stones) != win1.end()) {
            continue;
        }

        bool canWinIn2 = false;

        // Проверяем ходы сложения
        for (int move : moves) {
            int nextPos = stones + move;
            if (nextPos < target) {
                // Проверяем, что у Вани есть ответ на любой ход Пети
                bool vanyaCanWin = true;
                for (int petyaMove : moves) {
                    int petyaNext = nextPos + petyaMove;
                    if (petyaNext < target && win1.find(petyaNext) == win1.end()) {
                        int petyaMult = nextPos * multiply;
                        if (petyaMult < target && win1.find(petyaMult) == win1.end()) {
                            vanyaCanWin = false;
                            break;
                        }
                    }
                }
                if (vanyaCanWin) {
                    canWinIn2 = true;
                    break;
                }
            }
        }

        // Проверяем операцию умножения
        int multPos = stones * multiply;
        if (multPos < target) {
            bool vanyaCanWin = true;
            for (int petyaMove : moves) {
                int petyaNext = multPos + petyaMove;
                if (petyaNext < target && win1.find(petyaNext) == win1.end()) {
                    int petyaMult = multPos * multiply;
                    if (petyaMult < target && win1.find(petyaMult) == win1.end()) {
                        vanyaCanWin = false;
                        break;
                    }
                }
            }
            if (vanyaCanWin) {
                canWinIn2 = true;
            }
        }

        if (canWinIn2) {
            win2.insert(stones);
        }
    }

    // Находим позиции для сложного условия
    for (int S = 1; S < target; S++) {
        // Условие 1: Ваня может выиграть за 1 ИЛИ 2 хода
        bool canWin1or2 = (win1.find(S) != win1.end()) || (win2.find(S) != win2.end());

        // Условие 2: Ваня НЕ может гарантированно выиграть за 1 ход
        bool cannotWinGuaranteed1 = false;

        if (win1.find(S) != win1.end()) {
            // Проверяем, есть ли ход Пети, который не ведет к немедленному выигрышу
            for (int petyaMove : moves) {
                int petyaPos = S + petyaMove;
                if (petyaPos < target && win1.find(petyaPos) == win1.end()) {
                    cannotWinGuaranteed1 = true;
                    break;
                }
            }
            int petyaMult = S * multiply;
            if (petyaMult < target && win1.find(petyaMult) == win1.end()) {
                cannotWinGuaranteed1 = true;
            }
        } else {
            cannotWinGuaranteed1 = true;
        }

        if (canWin1or2 && cannotWinGuaranteed1) {
            complexWin.insert(S);
        }
    }

    // Возвращаем минимальное S
    return complexWin.empty() ? -1 : *complexWin.begin();
}

// Альтернативный подход с деревом игры
struct GameState {
    int winIn;
    bool canWin;
};

map<int, GameState> buildGameTree(int target, vector<int> moves, int multiply, int maxDepth) {
    map<int, GameState> gameTree;

    // Заполняем от больших значений к меньшим
    for (int stones = target * 2; stones >= 0; stones--) {
        if (stones >= target) {
            gameTree[stones] = {0, true};
        } else {
            vector<int> nextPositions;
            for (int move : moves) {
                nextPositions.push_back(stones + move);
            }
            nextPositions.push_back(stones * multiply);

            int minWinMoves = INT_MAX;
            bool canWin = false;

            for (int nextPos : nextPositions) {
                if (gameTree.find(nextPos) != gameTree.end() && gameTree[nextPos].canWin) {
                    canWin = true;
                    minWinMoves = min(minWinMoves, gameTree[nextPos].winIn + 1);
                }
            }

            gameTree[stones] = {
                minWinMoves == INT_MAX ? INT_MAX : minWinMoves,
                canWin
            };
        }
    }

    return gameTree;
}

int findComplexSolution(map<int, GameState>& gameTree, int target) {
    int minS = INT_MAX;

    for (int S = 1; S < target; S++) {
        if (gameTree.find(S) == gameTree.end() || !gameTree[S].canWin) {
            continue;
        }

        int winIn = gameTree[S].winIn;

        // Проверяем условия задания 21
        if ((winIn == 1 || winIn == 2)) {
            minS = min(minS, S);
        }
    }

    return minS == INT_MAX ? -1 : minS;
}

int main() {
    int target = 50;
    vector<int> moves = {1, 2};
    int multiply = 2;

    int solution = analyzeComplexGame(target, moves, multiply);
    cout << "Минимальное S: " << solution << endl;

    // Альтернативный подход
    cout << "Альтернативный подход:" << endl;
    auto gameTree = buildGameTree(target, moves, multiply, 4);
    int complexSolution = findComplexSolution(gameTree, target);
    cout << "Решение: " << complexSolution << endl;

    return 0;
}'''

    def get_pascal_code(self):
        """Возвращает код решения на Pascal"""
        return '''program Task21;

const
  MAX_TARGET = 100;
  MAX_MOVES = 10;

type
  BoolArray = array[0..MAX_TARGET] of Boolean;
  IntArray = array[1..MAX_TARGET] of Integer;

function AnalyzeComplexGame(target: Integer; moves: array of Integer; multiply: Integer): Integer;
var
  win1, win2, complexWin: BoolArray;
  i, j, k, minS: Integer;
  canWin, canWinIn2, vanyaCanWin, canWin1or2, cannotWinGuaranteed1: Boolean;
begin
  // Инициализация
  for i := 0 to MAX_TARGET do
  begin
    win1[i] := False;
    win2[i] := False;
    complexWin[i] := False;
  end;

  // Находим выигрышные позиции за 1 ход
  for i := target downto 0 do
  begin
    canWin := False;

    // Проверяем операции сложения
    for j := 0 to Length(moves) - 1 do
    begin
      if i + moves[j] >= target then
      begin
        canWin := True;
        Break;
      end;
    end;

    // Проверяем операцию умножения
    if i * multiply >= target then
      canWin := True;

    if canWin and (i < target) then
      win1[i] := True;
  end;

  // Находим выигрышные позиции за 2 хода
  for i := target downto 0 do
  begin
    if win1[i] then
      Continue;

    canWinIn2 := False;

    // Проверяем ходы сложения
    for j := 0 to Length(moves) - 1 do
    begin
      if i + moves[j] < target then
      begin
        vanyaCanWin := True;

        // Проверяем ходы Пети
        for k := 0 to Length(moves) - 1 do
        begin
          if (i + moves[j] + moves[k] < target) and 
             (not win1[i + moves[j] + moves[k]]) and
             ((i + moves[j]) * multiply < target) and
             (not win1[(i + moves[j]) * multiply]) then
          begin
            vanyaCanWin := False;
            Break;
          end;
        end;

        if vanyaCanWin then
        begin
          canWinIn2 := True;
          Break;
        end;
      end;
    end;

    // Проверяем операцию умножения
    if i * multiply < target then
    begin
      vanyaCanWin := True;
      for k := 0 to Length(moves) - 1 do
      begin
        if (i * multiply + moves[k] < target) and 
           (not win1[i * multiply + moves[k]]) and
           (i * multiply * multiply < target) and
           (not win1[i * multiply * multiply]) then
        begin
          vanyaCanWin := False;
          Break;
        end;
      end;

      if vanyaCanWin then
        canWinIn2 := True;
    end;

    if canWinIn2 then
      win2[i] := True;
  end;

  // Находим решения для задания 21
  minS := MAX_TARGET;
  for i := 1 to target - 1 do
  begin
    // Условие 1: Ваня может выиграть за 1 ИЛИ 2 хода
    canWin1or2 := win1[i] or win2[i];

    // Условие 2: Ваня НЕ может гарантированно выиграть за 1 ход
    cannotWinGuaranteed1 := False;

    if win1[i] then
    begin
      // Проверяем, есть ли ход Пети, который не ведет к выигрышу Вани за 1 ход
      for j := 0 to Length(moves) - 1 do
      begin
        if (i + moves[j] < target) and (not win1[i + moves[j]]) then
        begin
          cannotWinGuaranteed1 := True;
          Break;
        end;
      end;

      if (i * multiply < target) and (not win1[i * multiply]) then
        cannotWinGuaranteed1 := True;
    end
    else
    begin
      cannotWinGuaranteed1 := True;
    end;

    if canWin1or2 and cannotWinGuaranteed1 then
    begin
      if i < minS then
        minS := i;
    end;
  end;

  if minS = MAX_TARGET then
    Result := -1
  else
    Result := minS;
end;

var
  target, multiply, solution: Integer;
  moves: array[0..1] of Integer;
begin
  target := 50;
  moves[0] := 1;
  moves[1] := 2;
  multiply := 2;

  solution := AnalyzeComplexGame(target, moves, multiply);
  Writeln('Минимальное S: ', solution);
end.'''

    def get_java_code(self):
        """Возвращает код решения на Java"""
        return '''import java.util.*;

public class Task21 {

    public static int analyzeComplexGame(int target, int[] moves, int multiply) {
        Set<Integer> win1 = new HashSet<>();  // Выигрыш за 1 ход
        Set<Integer> win2 = new HashSet<>();  // Выигрыш за 2 хода
        Set<Integer> complexWin = new HashSet<>(); // Решения для задания 21

        // Находим выигрышные позиции за 1 ход
        for (int stones = target; stones >= 0; stones--) {
            boolean canWin = false;

            for (int move : moves) {
                if (stones + move >= target) {
                    canWin = true;
                    break;
                }
            }

            if (stones * multiply >= target) {
                canWin = true;
            }

            if (canWin && stones < target) {
                win1.add(stones);
            }
        }

        // Находим выигрышные позиции за 2 хода
        for (int stones = target; stones >= 0; stones--) {
            if (win1.contains(stones)) {
                continue;
            }

            boolean canWinIn2 = false;

            // Проверяем ходы сложения
            for (int move : moves) {
                int nextPos = stones + move;
                if (nextPos < target) {
                    // Проверяем, что у Вани есть ответ на любой ход Пети
                    boolean vanyaCanWin = true;
                    for (int petyaMove : moves) {
                        int petyaNext = nextPos + petyaMove;
                        if (petyaNext < target && !win1.contains(petyaNext)) {
                            int petyaMult = nextPos * multiply;
                            if (petyaMult < target && !win1.contains(petyaMult)) {
                                vanyaCanWin = false;
                                break;
                            }
                        }
                    }
                    if (vanyaCanWin) {
                        canWinIn2 = true;
                        break;
                    }
                }
            }

            // Проверяем операцию умножения
            int multPos = stones * multiply;
            if (multPos < target) {
                boolean vanyaCanWin = true;
                for (int petyaMove : moves) {
                    int petyaNext = multPos + petyaMove;
                    if (petyaNext < target && !win1.contains(petyaNext)) {
                        int petyaMult = multPos * multiply;
                        if (petyaMult < target && !win1.contains(petyaMult)) {
                            vanyaCanWin = false;
                            break;
                        }
                    }
                }
                if (vanyaCanWin) {
                    canWinIn2 = true;
                }
            }

            if (canWinIn2) {
                win2.add(stones);
            }
        }

        // Находим решения для сложного условия
        for (int S = 1; S < target; S++) {
            // Условие 1: Ваня может выиграть за 1 ИЛИ 2 хода
            boolean canWin1or2 = win1.contains(S) || win2.contains(S);

            // Условие 2: Ваня НЕ может гарантированно выиграть за 1 ход
            boolean cannotWinGuaranteed1 = false;

            if (win1.contains(S)) {
                // Проверяем, есть ли ход Пети, который не ведет к немедленному выигрышу
                for (int petyaMove : moves) {
                    int petyaPos = S + petyaMove;
                    if (petyaPos < target && !win1.contains(petyaPos)) {
                        cannotWinGuaranteed1 = true;
                        break;
                    }
                }
                int petyaMult = S * multiply;
                if (petyaMult < target && !win1.contains(petyaMult)) {
                    cannotWinGuaranteed1 = true;
                }
            } else {
                cannotWinGuaranteed1 = true;
            }

            if (canWin1or2 && cannotWinGuaranteed1) {
                complexWin.add(S);
            }
        }

        // Возвращаем минимальное S
        return complexWin.isEmpty() ? -1 : Collections.min(complexWin);
    }

    public static void main(String[] args) {
        int target = 50;
        int[] moves = {1, 2};
        int multiply = 2;

        int solution = analyzeComplexGame(target, moves, multiply);
        System.out.println("Минимальное S: " + solution);
    }
}'''