from task_base import BaseTaskPage
import random


class Task21Page(BaseTaskPage):
    def __init__(self, main_app, **kwargs):
        super().__init__(main_app, "task_21", **kwargs)

    def generate_task(self):
        """Генерирует задание №21 - Сложная выигрышная стратегия"""
        S = random.randint(15, 25)
        P = random.randint(30, 50)

        self.current_task = {
            'description': f'''Два игрока играют в игру. Есть две кучи камней. 
За один ход игрок может:
- добавить 1 камень в одну из куч
- или увеличить количество камней в одной из куч в 2 раза
Победителем считается игрок, первым сделавший суммарное количество камней ≥ {P}.''',
            'question': f'''Найдите все начальные значения куч (в пределах от 1 до {S}), 
при которых первый игрок имеет выигрышную стратегию.''',
            'answer': f"Выигрышные позиции для целевой суммы {P}"
        }