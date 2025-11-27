from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivymd.uix.snackbar import Snackbar


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
            height=dp(300),
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
            Clipboard.copy(code)
            # Показываем уведомление о копировании
            Snackbar(
                text=f"Код на {language} скопирован в буфер обмена!",
                duration=2
            ).open()
            print(f"Код на {language} скопирован в буфер обмена")
        except Exception as e:
            print(f"Ошибка копирования: {e}")
            Snackbar(
                text="Ошибка копирования в буфер обмена",
                duration=2
            ).open()


class Theory20Page(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        self.dialog = None

        self.show_theory_content()

    def show_theory_content(self):
        """Показывает содержание теории для задания 20"""
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
            text="Теория: Задание 20 - Выигрышная стратегия 2",
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
            text="Типичное условие задания 20",
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(30),
            halign="center"
        )
        condition_card.add_widget(condition_title)

        condition_text = MDLabel(
            text='''Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежит куча камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может добавить в кучу 1 или 2 камня или увеличить количество камней в куче в 2 раза.

Игра завершается в тот момент, когда количество камней в куче становится не менее 40. Победителем считается игрок, сделавший последний ход.

Найдите два таких значения S, при которых:
1) Петя не может выиграть за один ход;
2) Петя может выиграть своим вторым ходом независимо от того, как будет ходить Ваня.''',
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
                'title': 'Особенности задания 20',
                'content': '''Задание 20 является усложнением задания 19. Здесь требуется найти не одно, а несколько значений S, удовлетворяющих сложным условиям. Часто нужно найти 2 или 3 значения, при которых выполняются определенные стратегические условия.''',
            },
            {
                'title': 'Типичные условия в задании 20',
                'content': '''• "Петя не может выиграть за один ход; Петя может выиграть своим вторым ходом"
• "Ваня может выиграть своим первым ходом независимо от ходов Пети"
• "У Пети есть выигрышная стратегия, причём Петя может выиграть своим первым ходом"
• "Найдите два/три таких значения S, при которых..."''',
            },
            {
                'title': 'Метод решения',
                'content': '''1. Определяем выигрышные позиции за 1 ход (как в задании 19)
2. Находим позиции, из которых можно выиграть за 2 хода
3. Исключаем позиции, из которых можно выиграть за 1 ход
4. Анализируем позиции, удовлетворяющие условиям:
   - Петя не может выиграть за 1 ход
   - Но может выиграть за 2 хода при любой игре Вани
5. Находим все значения S, из которых Петя попадает в такие позиции''',
            },
            {
                'title': 'Анализ примера',
                'content': '''Для условия с S: S+1, S+2, S×2 и target=40:

• Выигрышные за 1 ход: 20-39 (могут достичь 40)
• Петя не может выиграть за 1 ход из позиций <20
• Петя может выиграть за 2 хода из позиций, из которых Ваня не может выиграть за 1 ход
• Находим S=10 и S=18 как решения''',
            },
            {
                'title': 'Стратегия решения для двух значений',
                'content': '''1. Постройте таблицу выигрышных позиций для 1 и 2 ходов
2. Найдите позиции, где:
   - Петя не может выиграть за 1 ход (не попадает в 20-39)
   - Но при любом ходе Вани Петя сможет выиграть следующим ходом
3. Определите S, из которых Петя попадает в такие позиции''',
            },
            {
                'title': 'Важные моменты',
                'content': '''• Внимательно анализируйте условие - кто и когда должен выиграть
• Учитывайте, что соперник будет играть оптимально
• Проверяйте все возможные ответвления в дереве игры
• Для двух куч используйте двумерные таблицы
• Всегда проверяйте крайние случаи''',
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
            text="Ниже представлены готовые решения задачи на различных языках программирования. Вы можете изучать алгоритмы и копировать код для использования.",
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
        return '''# Задание 20: Выигрышная стратегия (продвинутый уровень)
# Условие: Найдите два значения S, при которых Петя не может выиграть за один ход,
# но может выиграть своим вторым ходом независимо от ходов Вани.

def analyze_game(target, moves, multiply):
    """
    Анализирует игру и находит позиции, удовлетворяющие условиям задания 20.
    """
    # Множества позиций
    win_1 = set()  # Выигрыш за 1 ход
    win_2 = set()  # Выигрыш за 2 хода
    not_win_1_but_win_2 = set()  # Не выигрыш за 1 ход, но выигрыш за 2 хода

    # Шаг 1: Находим выигрышные позиции за 1 ход
    for stones in range(target, -1, -1):
        # Проверяем, можно ли выиграть за один ход
        can_win = any(stones + move >= target for move in moves) or stones * multiply >= target
        if can_win and stones < target:
            win_1.add(stones)

    # Шаг 2: Находим позиции для выигрыша за 2 хода
    for stones in range(target, -1, -1):
        if stones in win_1:
            continue  # Пропускаем позиции, где можно выиграть за 1 ход

        # Проверяем, можно ли выиграть за 2 хода
        can_win_in_2 = True
        for move in moves:
            next_pos = stones + move
            if next_pos < target:
                # Проверяем, есть ли ход у Вани, который не ведет к выигрышу Пети
                vanya_has_good_move = False
                for vanya_move in moves:
                    vanya_next = next_pos + vanya_move
                    if vanya_next < target and vanya_next not in win_1:
                        vanya_has_good_move = True
                        break
                    vanya_mult = next_pos * multiply
                    if vanya_mult < target and vanya_mult not in win_1:
                        vanya_has_good_move = True
                        break
                if not vanya_has_good_move:
                    can_win_in_2 = False
                    break

        # Также проверяем для операции умножения
        mult_pos = stones * multiply
        if mult_pos < target:
            vanya_has_good_move = False
            for vanya_move in moves:
                vanya_next = mult_pos + vanya_move
                if vanya_next < target and vanya_next not in win_1:
                    vanya_has_good_move = True
                    break
                vanya_mult = mult_pos * multiply
                if vanya_mult < target and vanya_mult not in win_1:
                    vanya_has_good_move = True
                    break
            if not vanya_has_good_move:
                can_win_in_2 = False

        if can_win_in_2 and stones not in win_1:
            win_2.add(stones)

    # Шаг 3: Находим S, удовлетворяющие условиям
    result_S = []
    for stones in range(1, target):
        if stones not in win_1:  # Петя не может выиграть за 1 ход
            # Проверяем, может ли Петя выиграть за 2 хода при любой игре Вани
            petya_can_win_in_2 = False
            for move in moves:
                next_pos = stones + move
                if next_pos in win_2:
                    petya_can_win_in_2 = True
                    break
            mult_pos = stones * multiply
            if mult_pos in win_2:
                petya_can_win_in_2 = True

            if petya_can_win_in_2:
                result_S.append(stones)

    return result_S[:2]  # Возвращаем первые два значения

# Параметры задачи
target = 40
moves = [1, 2]
multiply = 2

# Находим решения
solutions = analyze_game(target, moves, multiply)
print(f"Найденные значения S: {solutions}")

# Альтернативный упрощенный подход для демонстрации
def simple_solution(target, moves, multiply):
    """
    Упрощенный алгоритм для нахождения решений.
    В реальной задаче требуется более сложный анализ.
    """
    solutions = []

    # Анализируем позиции от 1 до target-1
    for S in range(1, target):
        # Проверяем, что Петя не может выиграть за 1 ход
        can_win_1 = any(S + move >= target for move in moves) or S * multiply >= target
        if can_win_1:
            continue

        # Проверяем, что Петя может выиграть за 2 хода
        can_win_2 = False
        for move in moves:
            next_pos = S + move
            # После хода Пети, Ваня не должен иметь выигрышного хода
            vanya_cannot_win = True
            for vanya_move in moves:
                if next_pos + vanya_move >= target or next_pos * multiply >= target:
                    vanya_cannot_win = False
                    break
            if vanya_cannot_win:
                can_win_2 = True
                break

        if can_win_2:
            solutions.append(S)
            if len(solutions) == 2:
                break

    return solutions

print("Упрощенный алгоритм:")
simple_solutions = simple_solution(target, moves, multiply)
print(f"Значения S: {simple_solutions}")'''

    def get_cpp_code(self):
        """Возвращает код решения на C++"""
        return '''#include <iostream>
#include <vector>
#include <set>
#include <algorithm>

using namespace std;

// Функция для анализа игры и нахождения решений
vector<int> analyzeGame(int target, vector<int> moves, int multiply) {
    set<int> win1;  // Выигрыш за 1 ход
    set<int> win2;  // Выигрыш за 2 хода

    // Находим выигрышные позиции за 1 ход
    for (int stones = target; stones >= 0; stones--) {
        bool canWin = false;

        // Проверяем операции сложения
        for (int move : moves) {
            if (stones + move >= target) {
                canWin = true;
                break;
            }
        }

        // Проверяем операцию умножения
        if (stones * multiply >= target) {
            canWin = true;
        }

        if (canWin && stones < target) {
            win1.insert(stones);
        }
    }

    // Находим позиции для задания 20
    vector<int> result;
    for (int S = 1; S < target; S++) {
        // Условие 1: Петя не может выиграть за 1 ход
        if (win1.find(S) != win1.end()) {
            continue;
        }

        // Условие 2: Петя может выиграть за 2 хода
        bool canWinIn2 = false;

        // Проверяем все возможные ходы Пети
        for (int move : moves) {
            int nextPos = S + move;
            if (nextPos < target) {
                // Проверяем, что Ваня не может помешать
                bool vanyaCanPrevent = false;
                for (int vanyaMove : moves) {
                    int vanyaNext = nextPos + vanyaMove;
                    if (vanyaNext >= target) {
                        vanyaCanPrevent = true;
                        break;
                    }
                    if (nextPos * multiply >= target) {
                        vanyaCanPrevent = true;
                        break;
                    }
                }
                if (!vanyaCanPrevent) {
                    canWinIn2 = true;
                    break;
                }
            }
        }

        # Проверяем операцию умножения
        int multPos = S * multiply;
        if (multPos < target) {
            bool vanyaCanPrevent = false;
            for (int vanyaMove : moves) {
                int vanyaNext = multPos + vanyaMove;
                if (vanyaNext >= target) {
                    vanyaCanPrevent = true;
                    break;
                }
                if (multPos * multiply >= target) {
                    vanyaCanPrevent = true;
                    break;
                }
            }
            if (!vanyaCanPrevent) {
                canWinIn2 = true;
            }
        }

        if (canWinIn2) {
            result.push_back(S);
            if (result.size() == 2) {
                break;
            }
        }
    }

    return result;
}

int main() {
    int target = 40;
    vector<int> moves = {1, 2};
    int multiply = 2;

    vector<int> solutions = analyzeGame(target, moves, multiply);

    cout << "Найденные значения S: ";
    for (int s : solutions) {
        cout << s << " ";
    }
    cout << endl;

    return 0;
}'''

    def get_pascal_code(self):
        """Возвращает код решения на Pascal"""
        return '''program Task20;

const
  MAX_TARGET = 100;

type
  IntArray = array[1..MAX_TARGET] of Integer;
  BoolArray = array[0..MAX_TARGET] of Boolean;

function AnalyzeGame(target: Integer; moves: array of Integer; multiply: Integer): IntArray;
var
  win1: BoolArray;
  win2: BoolArray;
  i, j, k, count: Integer;
  canWin, canWinIn2, vanyaCanPrevent: Boolean;
  result: IntArray;
begin
  // Инициализация
  for i := 0 to MAX_TARGET do
  begin
    win1[i] := False;
    win2[i] := False;
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

  // Находим решения для задания 20
  count := 0;
  for i := 1 to target - 1 do
  begin
    // Условие 1: Петя не может выиграть за 1 ход
    if win1[i] then
      Continue;

    // Условие 2: Петя может выиграть за 2 хода
    canWinIn2 := False;

    // Проверяем ходы сложения
    for j := 0 to Length(moves) - 1 do
    begin
      if i + moves[j] < target then
      begin
        vanyaCanPrevent := False;

        // Проверяем ходы Вани
        for k := 0 to Length(moves) - 1 do
        begin
          if (i + moves[j] + moves[k] >= target) or 
             ((i + moves[j]) * multiply >= target) then
          begin
            vanyaCanPrevent := True;
            Break;
          end;
        end;

        if not vanyaCanPrevent then
        begin
          canWinIn2 := True;
          Break;
        end;
      end;
    end;

    // Проверяем операцию умножения
    if i * multiply < target then
    begin
      vanyaCanPrevent := False;
      for k := 0 to Length(moves) - 1 do
      begin
        if (i * multiply + moves[k] >= target) or 
           (i * multiply * multiply >= target) then
        begin
          vanyaCanPrevent := True;
          Break;
        end;
      end;

      if not vanyaCanPrevent then
        canWinIn2 := True;
    end;

    if canWinIn2 then
    begin
      count := count + 1;
      result[count] := i;
      if count = 2 then
        Break;
    end;
  end;

  // Заполняем остальные элементы нулями
  for i := count + 1 to MAX_TARGET do
    result[i] := 0;

  AnalyzeGame := result;
end;

var
  target, multiply: Integer;
  moves: array[0..1] of Integer;
  solutions: IntArray;
  i: Integer;
begin
  target := 40;
  moves[0] := 1;
  moves[1] := 2;
  multiply := 2;

  solutions := AnalyzeGame(target, moves, multiply);

  Write('Найденные значения S: ');
  i := 1;
  while (solutions[i] <> 0) and (i <= 2) do
  begin
    Write(solutions[i], ' ');
    i := i + 1;
  end;
  Writeln;
end.'''

    def get_java_code(self):
        """Возвращает код решения на Java"""
        return '''import java.util.*;

public class Task20 {

    public static List<Integer> analyzeGame(int target, int[] moves, int multiply) {
        Set<Integer> win1 = new HashSet<>();  // Выигрыш за 1 ход
        List<Integer> solutions = new ArrayList<>();

        // Находим выигрышные позиции за 1 ход
        for (int stones = target; stones >= 0; stones--) {
            boolean canWin = false;

            // Проверяем операции сложения
            for (int move : moves) {
                if (stones + move >= target) {
                    canWin = true;
                    break;
                }
            }

            // Проверяем операцию умножения
            if (stones * multiply >= target) {
                canWin = true;
            }

            if (canWin && stones < target) {
                win1.add(stones);
            }
        }

        // Ищем решения для задания 20
        for (int S = 1; S < target; S++) {
            // Условие 1: Петя не может выиграть за 1 ход
            if (win1.contains(S)) {
                continue;
            }

            // Условие 2: Петя может выиграть за 2 хода
            boolean canWinIn2 = false;

            // Проверяем ходы сложения
            for (int move : moves) {
                int nextPos = S + move;
                if (nextPos < target) {
                    // Проверяем, что Ваня не может выиграть или помешать
                    boolean vanyaCanWin = false;
                    for (int vanyaMove : moves) {
                        if (nextPos + vanyaMove >= target || nextPos * multiply >= target) {
                            vanyaCanWin = true;
                            break;
                        }
                    }
                    if (!vanyaCanWin) {
                        canWinIn2 = true;
                        break;
                    }
                }
            }

            // Проверяем операцию умножения
            int multPos = S * multiply;
            if (multPos < target) {
                boolean vanyaCanWin = false;
                for (int vanyaMove : moves) {
                    if (multPos + vanyaMove >= target || multPos * multiply >= target) {
                        vanyaCanWin = true;
                        break;
                    }
                }
                if (!vanyaCanWin) {
                    canWinIn2 = true;
                }
            }

            if (canWinIn2) {
                solutions.add(S);
                if (solutions.size() == 2) {
                    break;
                }
            }
        }

        return solutions;
    }

    public static void main(String[] args) {
        int target = 40;
        int[] moves = {1, 2};
        int multiply = 2;

        List<Integer> solutions = analyzeGame(target, moves, multiply);

        System.out.print("Найденные значения S: ");
        for (int s : solutions) {
            System.out.print(s + " ");
        }
        System.out.println();
    }
}'''