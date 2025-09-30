from task_base import BaseTaskPage
from kivymd.uix.label import MDLabel
import random


class Task19Page(BaseTaskPage):
    def __init__(self, main_app, **kwargs):
        super().__init__(main_app, "task_19", **kwargs)

    def generate_task(self):
        """Генерирует задание №19 - Выигрышная стратегия с одной кучей"""
        S = random.randint(10, 30)  # начальное количество камней
        moves = [1, 2, 3]  # возможные ходы

        self.current_task = {
            'description': f'''Два игрока играют в игру с одной кучей камней. 
За один ход игрок может добавить в кучу {moves[0]}, {moves[1]} или {moves[2]} камня.
Игра завершается, когда количество камней в куче становится не менее {S + 10}. 
Победителем считается игрок, сделавший последний ход.''',
            'question': f'''При каких значениях S первый игрок может гарантированно выиграть 
независимо от ходов второго игрока? (Начальное количество камней: {S})''',
            'answer': f"Правильный ответ для S={S} будет сгенерирован алгоритмом"
        }