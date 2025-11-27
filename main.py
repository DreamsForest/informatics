from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

# Импортируем классы страниц
from statistics_main_page import StatisticsMainPage
from statistics_19_page import Statistics19Page  # ← обновлённая версия с kivy_garden.graph
from statistics_20_page import Statistics20Page
from statistics_21_page import Statistics21Page
from statistics_total_page import StatisticsTotalPage
from select_task_page import SelectTaskPage
from theory_page import TheoryPage
from theory_19_page import Theory19Page
from theory_20_page import Theory20Page
from theory_21_page import Theory21Page
from task_19_page import Task19Page
from task_20_page import Task20Page
from task_21_page import Task21Page


class MainApp(MDApp):
    def build(self):
        try:
            self.root_layout = AnchorLayout()
            self.main_container = BoxLayout(orientation='vertical')
            self.root_layout.add_widget(self.main_container)

            # Верхняя панель
            self.toolbar = MDTopAppBar(
                title="Главная страница",
                left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
                elevation=10,
                md_bg_color=(0.2, 0.6, 0.8, 1),
                size_hint_y=None,
                height=dp(56)
            )

            # Контент
            self.main_content = BoxLayout(orientation='vertical', size_hint_y=1)
            self.show_main_page()

            self.main_container.add_widget(self.toolbar)
            self.main_container.add_widget(self.main_content)
            self.create_navigation_drawer()

            return self.root_layout

        except Exception as e:
            from kivy.uix.label import Label
            import traceback
            error_msg = f"Ошибка запуска: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return Label(text=error_msg)

    # -----------------------------
    # Основные страницы приложения
    # -----------------------------
    def show_main_page(self):
        self.main_content.clear_widgets()
        self.toolbar.title = "Главная страница"

        scroll_view = ScrollView(do_scroll_x=False)
        content_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )
        content_layout.height = dp(120) * 3 + dp(20) * 4

        # === Блок Теория ===
        info_block1 = self.create_block(
            title="Теория",
            subtitle="Изучите теоретические материалы перед выполнением заданий",
            color=(0.9, 0.95, 1, 1),
            callback=lambda: self.show_theory_page()
        )
        content_layout.add_widget(info_block1)

        # === Блок Задания ===
        info_block2 = self.create_block(
            title="Задания",
            subtitle="Практикуйтесь на заданиях разного уровня сложности",
            color=(0.95, 0.98, 0.95, 1),
            callback=lambda: self.show_select_task_page()
        )
        content_layout.add_widget(info_block2)

        # === Блок Статистика ===
        info_block3 = self.create_block(
            title="Статистика",
            subtitle="Просмотрите результаты выполнения заданий",
            color=(1, 0.95, 0.95, 1),
            callback=lambda: self.show_statistics_main_page()
        )
        content_layout.add_widget(info_block3)

        scroll_view.add_widget(content_layout)
        self.main_content.add_widget(scroll_view)

    def create_block(self, title, subtitle, color, callback):
        """Создаёт карточку блока с обработкой клика."""
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(10),
            md_bg_color=color,
            radius=[dp(15)],
            elevation=3
        )
        card.add_widget(MDLabel(
            text=title,
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint_y=None,
            height=dp(40)
        ))
        card.add_widget(MDLabel(
            text=subtitle,
            halign='center',
            theme_text_color='Secondary',
            font_style='Body2',
            size_hint_y=None,
            height=dp(60)
        ))
        card.bind(on_touch_down=lambda instance, touch: callback() if instance.collide_point(*touch.pos) else None)
        return card

    # --- Навигация ---
    def show_select_task_page(self):
        self.main_content.clear_widgets()
        self.toolbar.title = "Выбрать задание"
        self.main_content.add_widget(SelectTaskPage(main_app=self))

    def show_theory_page(self):
        self.main_content.clear_widgets()
        self.toolbar.title = "Ознакомление с теорией"
        self.main_content.add_widget(TheoryPage(main_app=self))

    def show_statistics_main_page(self):
        self.main_content.clear_widgets()
        self.toolbar.title = "Статистика"
        self.main_content.add_widget(StatisticsMainPage(main_app=self))

    def show_statistics_detail_page(self, stats_type):
        """Открывает конкретную страницу статистики"""
        self.main_content.clear_widgets()
        if stats_type == "statistics_19":
            self.toolbar.title = "Статистика: Задание 19"
            self.main_content.add_widget(Statistics19Page(main_app=self))
        elif stats_type == "statistics_20":
            self.toolbar.title = "Статистика: Задание 20"
            self.main_content.add_widget(Statistics20Page(main_app=self))
        elif stats_type == "statistics_21":
            self.toolbar.title = "Статистика: Задание 21"
            self.main_content.add_widget(Statistics21Page(main_app=self))
        elif stats_type == "statistics_total":
            self.toolbar.title = "Общая статистика"
            self.main_content.add_widget(StatisticsTotalPage(main_app=self))

    def show_task_page(self, task_type):
        self.main_content.clear_widgets()
        if task_type == "task_19":
            self.toolbar.title = "Задание №19"
            self.main_content.add_widget(Task19Page(main_app=self))
        elif task_type == "task_20":
            self.toolbar.title = "Задание №20"
            self.main_content.add_widget(Task20Page(main_app=self))
        elif task_type == "task_21":
            self.toolbar.title = "Задание №21"
            self.main_content.add_widget(Task21Page(main_app=self))

    # --- Меню ---
    def create_navigation_drawer(self):
        self.nav_drawer = MDNavigationDrawer(size_hint=(0.8, 1), elevation=20, radius=(0, 16, 16, 0))
        drawer_content = BoxLayout(orientation='vertical')
        header = MDLabel(text="Меню", halign='center', font_style='H4', size_hint_y=None, height=dp(60))
        drawer_content.add_widget(header)

        scroll = ScrollView()
        menu_list = MDList()
        for item in ["Главная", "Выбрать задание", "Ознакомление с теорией", "Статистика"]:
            list_item = OneLineListItem(
                text=item,
                on_release=lambda x, item=item: self.menu_item_clicked(item)
            )
            menu_list.add_widget(list_item)
        scroll.add_widget(menu_list)
        drawer_content.add_widget(scroll)

        footer = BoxLayout(size_hint_y=None, height=dp(60))
        footer.add_widget(MDRaisedButton(
            text="Закрыть",
            size_hint=(None, None),
            size=(dp(120), dp(48)),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.nav_drawer.set_state("close")
        ))
        drawer_content.add_widget(footer)

        self.nav_drawer.add_widget(drawer_content)
        self.root_layout.add_widget(self.nav_drawer)
        self.nav_drawer.set_state("close")

    def toggle_nav_drawer(self):
        self.nav_drawer.set_state('close' if self.nav_drawer.state == 'open' else 'open')

    def menu_item_clicked(self, item):
        self.nav_drawer.set_state('close')
        if item == "Главная":
            self.show_main_page()
        elif item == "Выбрать задание":
            self.show_select_task_page()
        elif item == "Ознакомление с теорией":
            self.show_theory_page()
        elif item == "Статистика":
            self.show_statistics_main_page()

    # --- Работа со статистикой ---
    def update_statistics(self, task_type, is_correct):
        try:
            from kivy.storage.jsonstore import JsonStore
            store = JsonStore('user_statistics.json')

            default_stats = {
                "task_19": {"correct": 0, "incorrect": 0, "total": 0},
                "task_20": {"correct": 0, "incorrect": 0, "total": 0},
                "task_21": {"correct": 0, "incorrect": 0, "total": 0}
            }

            stats = store.get('statistics') if store.exists('statistics') else default_stats
            if task_type in stats:
                if is_correct:
                    stats[task_type]["correct"] += 1
                else:
                    stats[task_type]["incorrect"] += 1
                stats[task_type]["total"] += 1
                store.put('statistics', **stats)
        except Exception as e:
            print(f"Ошибка обновления статистики: {e}")

    def get_statistics(self):
        try:
            from kivy.storage.jsonstore import JsonStore
            store = JsonStore('user_statistics.json')
            if store.exists('statistics'):
                return store.get('statistics')
            else:
                return {
                    "task_19": {"correct": 0, "incorrect": 0, "total": 0},
                    "task_20": {"correct": 0, "incorrect": 0, "total": 0},
                    "task_21": {"correct": 0, "incorrect": 0, "total": 0}
                }
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
            return {
                "task_19": {"correct": 0, "incorrect": 0, "total": 0},
                "task_20": {"correct": 0, "incorrect": 0, "total": 0},
                "task_21": {"correct": 0, "incorrect": 0, "total": 0}
            }


if __name__ == '__main__':
    MainApp().run()
