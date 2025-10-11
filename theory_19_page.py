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
            height=dp(250),
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


class Theory19Page(MDBoxLayout):
    def __init__(self, main_app, **kwargs):
        super().__init__(**kwargs)
        self.main_app = main_app
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(20)
        self.dialog = None

        self.show_theory_content()

    def show_theory_content(self):
        """Показывает содержание теории для задания 19"""
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
            text="Теория: Задание 19 - Выигрышная стратегия 1",
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
            text="Условие задачи",
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(30),
            halign="center"
        )
        condition_card.add_widget(condition_title)

        condition_text = MDLabel(
            text='''Два игрока, Петя и Ваня, играют в следующую игру. Перед игроками лежит куча камней. Игроки ходят по очереди, первый ход делает Петя. За один ход игрок может добавить 1 или 2 камня. Игра завершается в тот момент, когда количество камней в куче становится не менее 30. Победителем считается игрок, сделавший последний ход, то есть первым получивший кучу, в которой будет 30 или больше камней.

Известно, что Ваня выиграл своим первым ходом после неудачного первого хода Пети. Укажите минимальное значение S (начальное количество камней), когда такая ситуация возможна.''',
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
                'title': 'Метод решения',
                'content': '''1. Определяем конечные позиции (≥30 камней)
2. Находим позиции, из которых можно выиграть за 1 ход (27, 28, 29 камней)
3. Анализируем, из каких позиций Петя мог попасть в эти проигрышные для себя позиции
4. Находим минимальное S, удовлетворяющее условию''',
                'interactive': False
            },
            {
                'title': 'Анализ решения',
                'content': '''• Ваня выиграл первым ходом после хода Пети было 27, 28 или 29 камней
• Петя мог прийти в эти позиции из S = 26, 27, 28 (если +1), 25, 26, 27 (если +2)
• Минимальное S = 25''',
                'interactive': False
            },
            {
                'title': 'Советы по решению',
                'content': '''• Внимательно читайте условие - какие ходы разрешены
• Определите условие окончания игры
• Используйте обратный анализ - от конца к началу
• Проверяйте все возможные ходы
• Для сложных случаев стройте дерево игры''',
                'interactive': False
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
        return '''# Задание 19: Выигрышная стратегия
# Условие: Ваня выиграл первым ходом после неудачного хода Пети

def find_min_S(target, moves):
    """
    Находит минимальное S, при котором Ваня выиграет первым ходом
    после любого хода Пети.
    """
    # Множество выигрышных позиций
    win_positions = set()

    # Обратный анализ от целевого значения к 0
    for stones in range(target, -1, -1):
        # Проверяем, можно ли выиграть за один ход
        can_win = any(stones + move >= target for move in moves)

        if can_win:
            win_positions.add(stones)
        else:
            # Проверяем, все ли возможные ходы ведут в выигрышные позиции
            all_moves_win = all((stones + move) in win_positions for move in moves)
            if all_moves_win:
                win_positions.add(stones)

    # Ищем минимальное S, из которого Петя попадает в проигрышную позицию
    min_S = float('inf')
    for stones in range(target):
        # Если текущая позиция проигрышная для Пети
        if stones not in win_positions:
            # Проверяем, из каких позиций Петя мог сюда попасть
            for move in moves:
                prev_stones = stones - move
                if prev_stones >= 0 and prev_stones not in win_positions:
                    min_S = min(min_S, prev_stones)

    return min_S if min_S != float('inf') else -1

# Параметры из условия задачи
target = 30  # Конечное количество камней
moves = [1, 2]  # Возможные ходы

# Находим решение
result = find_min_S(target, moves)
print(f"Минимальное S: {result}")  # Ответ: 25'''

    def get_cpp_code(self):
        """Возвращает код решения на C++"""
        return '''#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <climits>

using namespace std;

// Функция для нахождения минимального S
int findMinS(int target, vector<int> moves) {
    set<int> winPositions;

    // Обратный анализ от target до 0
    for (int stones = target; stones >= 0; stones--) {
        bool canWin = false;

        // Проверяем, можно ли выиграть за один ход
        for (int move : moves) {
            if (stones + move >= target) {
                canWin = true;
                break;
            }
        }

        if (canWin) {
            winPositions.insert(stones);
        } else {
            // Проверяем, все ли ходы ведут в выигрышные позиции
            bool allMovesWin = true;
            for (int move : moves) {
                if (winPositions.find(stones + move) == winPositions.end()) {
                    allMovesWin = false;
                    break;
                }
            }
            if (allMovesWin) {
                winPositions.insert(stones);
            }
        }
    }

    // Поиск минимального S
    int minS = INT_MAX;
    for (int stones = 0; stones < target; stones++) {
        if (winPositions.find(stones) == winPositions.end()) {
            for (int move : moves) {
                int prevStones = stones - move;
                if (prevStones >= 0 && winPositions.find(prevStones) == winPositions.end()) {
                    minS = min(minS, prevStones);
                }
            }
        }
    }

    return (minS != INT_MAX) ? minS : -1;
}

int main() {
    int target = 30;
    vector<int> moves = {1, 2};

    int result = findMinS(target, moves);
    cout << "Минимальное S: " << result << endl;  // Ответ: 25

    return 0;
}'''

    def get_pascal_code(self):
        """Возвращает код решения на Pascal"""
        return '''program Task19;

const
  MAX_TARGET = 100;

type
  BoolArray = array[0..MAX_TARGET] of Boolean;

function FindMinS(target: Integer; moves: array of Integer): Integer;
var
  winPositions: BoolArray;
  i, j, minS, moveCount: Integer;
  canWin, allMovesWin: Boolean;
begin
  moveCount := Length(moves);

  // Инициализация массива выигрышных позиций
  for i := 0 to MAX_TARGET do
    winPositions[i] := False;

  // Обратный анализ от target до 0
  for i := target downto 0 do
  begin
    canWin := False;

    // Проверка возможности выигрыша за один ход
    for j := 0 to moveCount - 1 do
    begin
      if i + moves[j] >= target then
      begin
        canWin := True;
        Break;
      end;
    end;

    if canWin then
      winPositions[i] := True
    else
    begin
      // Проверяем, все ли ходы ведут в выигрышные позиции
      allMovesWin := True;
      for j := 0 to moveCount - 1 do
      begin
        if not winPositions[i + moves[j]] then
        begin
          allMovesWin := False;
          Break;
        end;
      end;
      winPositions[i] := allMovesWin;
    end;
  end;

  // Поиск минимального S
  minS := MAX_TARGET;
  for i := 0 to target - 1 do
  begin
    if not winPositions[i] then
    begin
      for j := 0 to moveCount - 1 do
      begin
        if (i - moves[j] >= 0) and not winPositions[i - moves[j]] then
        begin
          if i - moves[j] < minS then
            minS := i - moves[j];
        end;
      end;
    end;
  end;

  if minS = MAX_TARGET then
    Result := -1
  else
    Result := minS;
end;

var
  target: Integer;
  moves: array[0..1] of Integer;
  result: Integer;
begin
  target := 30;
  moves[0] := 1;
  moves[1] := 2;

  result := FindMinS(target, moves);
  Writeln('Минимальное S: ', result);  // Ответ: 25
end.'''

    def get_java_code(self):
        """Возвращает код решения на Java"""
        return '''import java.util.*;

public class Task19 {

    public static int findMinS(int target, int[] moves) {
        Set<Integer> winPositions = new HashSet<>();

        // Обратный анализ от target до 0
        for (int stones = target; stones >= 0; stones--) {
            boolean canWin = false;

            // Проверяем выигрыш за один ход
            for (int move : moves) {
                if (stones + move >= target) {
                    canWin = true;
                    break;
                }
            }

            if (canWin) {
                winPositions.add(stones);
            } else {
                // Проверяем, все ли ходы ведут к выигрышу
                boolean allMovesWin = true;
                for (int move : moves) {
                    if (!winPositions.contains(stones + move)) {
                        allMovesWin = false;
                        break;
                    }
                }
                if (allMovesWin) {
                    winPositions.add(stones);
                }
            }
        }

        // Поиск минимального S
        int minS = Integer.MAX_VALUE;
        for (int stones = 0; stones < target; stones++) {
            if (!winPositions.contains(stones)) {
                for (int move : moves) {
                    int prevStones = stones - move;
                    if (prevStones >= 0 && !winPositions.contains(prevStones)) {
                        minS = Math.min(minS, prevStones);
                    }
                }
            }
        }

        return minS != Integer.MAX_VALUE ? minS : -1;
    }

    public static void main(String[] args) {
        int target = 30;
        int[] moves = {1, 2};

        int result = findMinS(target, moves);
        System.out.println("Минимальное S: " + result);  // Ответ: 25
    }
}'''