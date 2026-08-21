# allgui_kivy.py

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder

# Добавляем путь для импорта ваших модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_logic import ClickerGame
from gui.settings import Settings  # предположим, что Settings тоже адаптирован под Kivy
from animation.court1 import CourtSuccess
from animation.court2 import CourtFail

# --- Языковые переводы (оставляем как есть) ---
TRANSLATIONS = {
    "Английский": {
        "title": "Clicker", "result": "Result: -", "hit": "🎯 Hit! +1 point!", "miss": "❌ Missed :(",
        "points": "Points: {}", "button_click": "Click!", "menu_lang": "Select language",
        "btn_inventory": "Inventory", "btn_shop": "Shop", "btn_authors": "Authors",
        "start_challenge": "Click to start!", "click_now": "CLICK NOW!",
        "score_message": "{} clicks in 1 second!", "inventory": "Inventory",
        "potion": "🧪 Double Points (10 min)", "potion_active": "Active! Time left: {} sec",
        "potion_inactive": "Use: 10 min x2", "use": "Use", "back": "Back", "btn_settings": "Settings"
    },
    "Русский": {
        "title": "Кликер", "result": "Результат: -", "hit": "🎯 Попал! +1 очко!", "miss": "❌ Промах :(",
        "points": "Очки: {}", "button_click": "Клик!", "menu_lang": "Язык",
        "btn_inventory": "Инвентарь", "btn_shop": "Магазин", "btn_authors": "Авторы",
        "start_challenge": "Нажми, и начни!", "click_now": "ЖМИ СЕЙЧАС!",
        "score_message": "{} кликов за 1 секунду!", "inventory": "Инвентарь",
        "potion": "🧪2x очки (10 мин)", "potion_active": "Активно! Осталось: {} сек",
        "potion_inactive": "Использовать: 10 мин", "use": "Использовать", "back": "Назад",
        "btn_settings": "Настройки"
    },
    "Французский": {
        "title": "Cliqueur", "result": "Résultat : -", "hit": "🎯 Touché ! +1 point !", "miss": "❌ Raté :(",
        "points": "Points : {}", "button_click": "Cliquez !", "menu_lang": "Choisir la langue",
        "btn_inventory": "Inventaire", "btn_shop": "Magasin", "btn_authors": "Auteurs",
        "start_challenge": "Cliquez pour commencer !", "click_now": "CLIQUEZ MAINTENANT !",
        "score_message": "{} clics en 1 seconde !", "inventory": "Inventaire",
        "potion": "🧪 Double points (10 min)", "potion_active": "Actif ! Temps restant : {} sec",
        "potion_inactive": "Utiliser : 10 min x2", "use": "Utiliser", "back": "Retour",
        "btn_settings": "Paramètres"
    },
    "Немецкий": {
        "title": "Klicker", "result": "Ergebnis: -", "hit": "🎯 Treffer! +1 Punkt!", "miss": "❌ Daneben :(",
        "points": "Punkte: {}", "button_click": "Klick!", "menu_lang": "Sprache wählen",
        "btn_inventory": "Inventar", "btn_shop": "Laden", "btn_authors": "Autoren",
        "start_challenge": "Klicke zum Starten!", "click_now": "JETZT KLICKEN!",
        "score_message": "{} Klicks in 1 Sekunde!", "inventory": "Inventar",
        "potion": "🧪 Doppelte Punkte (10 Min)", "potion_active": "Aktiv! Verbleibend: {} Sek",
        "potion_inactive": "Benutzen: 10 Min x2", "use": "Benutzen", "back": "Zurück",
        "btn_settings": "Einstellungen"
    },
    "Китайский": {
        "title": "点击器", "result": "结果: -", "hit": "🎯 击中！+1 分！", "miss": "❌ 未命中 :(",
        "points": "分数: {}", "button_click": "点击！", "menu_lang": "选择语言",
        "btn_inventory": "背包", "btn_shop": "商店", "btn_authors": "作者",
        "start_challenge": "点击开始！", "click_now": "立即点击！",
        "score_message": "1秒内点击 {} 次！", "inventory": "背包",
        "potion": "🧪 双倍积分 (10分钟)", "potion_active": "生效中！剩余时间：{} 秒",
        "potion_inactive": "使用：10分钟双倍", "use": "使用", "back": "返回", "btn_settings": "设置"
    }
}

# --- KV-разметка для главного окна (встроенная) ---
KV = '''
<RootWidget>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    BoxLayout:
        id: main_layout
        orientation: 'horizontal'
        spacing: dp(10)

        # Левая панель (основная)
        BoxLayout:
            id: left_panel
            orientation: 'vertical'
            size_hint_x: 0.8
            spacing: dp(5)

            # Контейнер для анимации
            BoxLayout:
                id: anim_container
                size_hint_y: 0.6
                canvas.before:
                    Color:
                        rgba: 0.94, 0.94, 0.94, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size

                # Здесь будет Canvas для анимации (заменяет Tkinter Canvas)
                FloatLayout:
                    id: animation_area
                    size_hint: 1, 1

            # Игровая область (метки, кнопки)
            BoxLayout:
                id: game_frame
                orientation: 'vertical'
                size_hint_y: 0.4
                spacing: dp(5)

                Label:
                    id: label_result
                    text: ''
                    font_size: dp(16)
                    size_hint_y: None
                    height: dp(30)

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(60)
                    spacing: dp(10)

                    Button:
                        id: button_click
                        text: root.tr['start_challenge']
                        font_size: dp(14)
                        size_hint_x: 0.6
                        background_color: 0.68, 0.85, 1, 1  # lightblue
                        on_release: root.start_challenge()

                    Label:
                        id: label_points
                        text: root.tr['points'].format(root.game.get_points())
                        font_size: dp(16)
                        bold: True
                        size_hint_x: 0.4

        # Правая панель (кнопки навигации)
        BoxLayout:
            id: right_panel
            orientation: 'vertical'
            size_hint_x: 0.2
            spacing: dp(5)

            Button:
                text: root.tr['btn_inventory']
                background_color: 1, 0.6, 0.6, 1  # lightcoral
                font_size: dp(12)
                bold: True
                on_release: root.open_inventory()
            Button:
                text: root.tr['btn_shop']
                background_color: 0.6, 1, 0.6, 1  # lightgreen
                font_size: dp(12)
                bold: True
                on_release: root.open_shop()
            Button:
                text: root.tr['btn_authors']
                background_color: 1, 1, 0.6, 1  # lightyellow
                font_size: dp(12)
                bold: True
                on_release: root.open_authors()
            Button:
                id: btn_language
                text: root.tr['menu_lang']
                background_color: 0.68, 0.85, 1, 1  # lightblue
                font_size: dp(12)
                bold: True
                on_release: root.show_language_menu()
            Button:
                text: root.tr['btn_settings']
                background_color: 0.8, 0.8, 0.8, 1  # lightgray
                font_size: dp(12)
                bold: True
                on_release: root.open_settings()

    # Кнопка "Назад" (изначально скрыта)
    Button:
        id: btn_back
        text: root.tr['back']
        font_size: dp(14)
        bold: True
        background_color: 0.68, 0.85, 1, 1
        size_hint_y: None
        height: dp(40)
        opacity: 0
        disabled: True
        on_release: root.close_inventory()  # временно, меняется динамически

    # Подпись GlitchHunters
    Label:
        text: 'GlitchHunters'
        font_size: dp(10)
        color: 0, 0, 1, 1
        size_hint: (None, None)
        size: (dp(100), dp(20))
        pos: (dp(10), dp(10))
'''

class RootWidget(BoxLayout):
    # Будем хранить ссылки на дочерние виджеты для переключения
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = ClickerGame()
        self.game.load_game()

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.current_lang = "Русский"
        self.tr = TRANSLATIONS[self.current_lang]

        # Переменные для игры
        self.click_count = 0
        self.challenge_active = False

        # Переменные для инвентаря и т.д.
        self.inventory_frame = None
        self.shop_frame = None
        self.authors_frame = None
        self.settings_frame = None
        self.settings = None
        self.potion_frame = None
        self.potion_btn = None
        self.potion_timer_label = None
        self.image_label = None

        # Анимация (адаптируем под Kivy)
        self.animation_area = self.ids.animation_area
        self.court_success = CourtSuccess(self.animation_area)  # предположим, что адаптировано
        self.court_fail = CourtFail(self.animation_area)

        # После построения виджетов подключаем обработку закрытия
        Window.bind(on_request_close=self.on_closing)

        # Обновление отображения зелья
        Clock.schedule_interval(self.update_potion_display, 1.0)

    # ---------- Методы, аналогичные оригинальному классу ----------
    def open_inventory(self):
        # Скрываем основную игру
        self.ids.game_frame.clear_widgets()
        self.ids.anim_container.clear_widgets()

        # Убираем правые кнопки (не удаляя их)
        self.ids.right_panel.opacity = 0
        self.ids.right_panel.disabled = True

        # Создаем инвентарь
        if not self.inventory_frame:
            self.inventory_frame = BoxLayout(orientation='vertical', spacing=dp(10))
            # Заполняем инвентарь...
            label = Label(text=self.tr['inventory'], font_size=dp(16), bold=True)
            self.inventory_frame.add_widget(label)

            # Контейнер для зелья
            potion_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150),
                                   padding=dp(10), spacing=dp(5))
            potion_box.canvas.before.add(Color(1, 1, 0.8, 1))
            potion_box.canvas.before.add(Rectangle(pos=potion_box.pos, size=potion_box.size))
            # Внутренний слой для изображения и текста
            top_content = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
            # Картинка
            image_frame = BoxLayout(size_hint_x=0.3)
            # Загружаем изображение
            try:
                img_path = os.path.join(self.base_dir, "images", "potionthatgives2xcoins.png")
                if os.path.exists(img_path):
                    img = Image(source=img_path)
                    img.texture.mag_filter = 'nearest'
                    image_frame.add_widget(img)
                else:
                    image_frame.add_widget(Label(text='🧪', font_size=dp(32)))
            except:
                image_frame.add_widget(Label(text='🧪', font_size=dp(32)))
            top_content.add_widget(image_frame)

            text_frame = BoxLayout(orientation='vertical', size_hint_x=0.7)
            text_frame.add_widget(Label(text=self.tr['potion'], font_size=dp(10), bold=True, halign='left'))
            self.potion_btn = Button(text=self.tr['potion_inactive'], font_size=dp(9), size_hint_y=None, height=dp(30))
            self.potion_btn.bind(on_release=self.use_potion)
            text_frame.add_widget(self.potion_btn)
            top_content.add_widget(text_frame)

            potion_box.add_widget(top_content)

            # Таймер
            self.potion_timer_label = Label(text='', font_size=dp(9), size_hint_y=None, height=dp(40),
                                            color=(0,0,0,1))
            self.potion_timer_label.canvas.before.add(Color(0.6, 0.9, 0.6, 1))
            self.potion_timer_label.canvas.before.add(Rectangle(pos=self.potion_timer_label.pos,
                                                                size=self.potion_timer_label.size))
            potion_box.add_widget(self.potion_timer_label)

            self.inventory_frame.add_widget(potion_box)

        self.add_widget(self.inventory_frame)

        # Показываем кнопку "Назад"
        self.ids.btn_back.opacity = 1
        self.ids.btn_back.disabled = False
        self.ids.btn_back.unbind(on_release)
        self.ids.btn_back.bind(on_release=self.close_inventory)

    def close_inventory(self, *args):
        if self.inventory_frame:
            self.remove_widget(self.inventory_frame)
        self.ids.right_panel.opacity = 1
        self.ids.right_panel.disabled = False
        self.ids.game_frame.clear_widgets()
        # Восстанавливаем игру
        self.show_game()
        self.ids.btn_back.opacity = 0
        self.ids.btn_back.disabled = True
        self.update_ui()

    def open_shop(self):
        # Аналогично, но для магазина
        self.ids.game_frame.clear_widgets()
        self.ids.anim_container.clear_widgets()
        self.ids.right_panel.opacity = 0
        self.ids.right_panel.disabled = True

        if not self.shop_frame:
            self.shop_frame = BoxLayout(orientation='vertical')
            self.shop_frame.add_widget(Label(text=self.tr['btn_shop'], font_size=dp(16), bold=True))
            self.shop_frame.add_widget(Label(text='🏪 Магазин временно закрыт', font_size=dp(12), color=(0.5,0.5,0.5,1)))
        self.add_widget(self.shop_frame)

        self.ids.btn_back.opacity = 1
        self.ids.btn_back.disabled = False
        self.ids.btn_back.unbind(on_release)
        self.ids.btn_back.bind(on_release=self.close_shop)

    def close_shop(self, *args):
        if self.shop_frame:
            self.remove_widget(self.shop_frame)
        self.ids.right_panel.opacity = 1
        self.ids.right_panel.disabled = False
        self.show_game()
        self.ids.btn_back.opacity = 0
        self.ids.btn_back.disabled = True

    def open_authors(self):
        self.ids.game_frame.clear_widgets()
        self.ids.anim_container.clear_widgets()
        self.ids.right_panel.opacity = 0
        self.ids.right_panel.disabled = True

        if not self.authors_frame:
            self.authors_frame = BoxLayout(orientation='vertical')
            self.authors_frame.add_widget(Label(text=self.tr['btn_authors'], font_size=dp(16), bold=True))
            authors_text = "🎮 Authors:\n• thekosmoss\n• artman\n• Kirill\n\n🔧 Project: Clicker Basketball\n📅 2025 GlitchHunters Team"
            self.authors_frame.add_widget(Label(text=authors_text, font_size=dp(11), halign='center'))
        self.add_widget(self.authors_frame)

        self.ids.btn_back.opacity = 1
        self.ids.btn_back.disabled = False
        self.ids.btn_back.unbind(on_release)
        self.ids.btn_back.bind(on_release=self.close_authors)

    def close_authors(self, *args):
        if self.authors_frame:
            self.remove_widget(self.authors_frame)
        self.ids.right_panel.opacity = 1
        self.ids.right_panel.disabled = False
        self.show_game()
        self.ids.btn_back.opacity = 0
        self.ids.btn_back.disabled = True

    def open_settings(self):
        # Аналогично, адаптируем Settings под Kivy
        self.ids.game_frame.clear_widgets()
        self.ids.anim_container.clear_widgets()
        self.ids.right_panel.opacity = 0
        self.ids.right_panel.disabled = True

        if not self.settings_frame:
            self.settings_frame = BoxLayout(orientation='vertical')
            self.settings = Settings(self.settings_frame, self)  # адаптировано
        self.add_widget(self.settings_frame)

        self.ids.btn_back.opacity = 1
        self.ids.btn_back.disabled = False
        self.ids.btn_back.unbind(on_release)
        self.ids.btn_back.bind(on_release=self.close_settings)

    def close_settings(self, *args):
        if self.settings_frame:
            self.remove_widget(self.settings_frame)
        self.ids.right_panel.opacity = 1
        self.ids.right_panel.disabled = False
        self.show_game()
        self.ids.btn_back.opacity = 0
        self.ids.btn_back.disabled = True

    def show_game(self):
        # Восстанавливаем game_frame и anim_container
        # В KV они уже есть, просто снова делаем видимыми
        self.ids.game_frame.clear_widgets()
        self.ids.game_frame.add_widget(self.ids.label_result)
        # Кнопку и лейбл точек нужно пересоздавать? Лучше хранить ссылки.
        # Используем существующие из KV
        self.ids.game_frame.add_widget(self.ids.button_click)  # пока не работает, надо переделать
        # Вместо этого мы просто пересоздадим виджеты или воспользуемся тем, что уже есть

    def start_challenge(self):
        self.tr = TRANSLATIONS[self.current_lang]
        self.ids.button_click.text = self.tr['click_now']
        self.ids.button_click.background_color = (1, 0, 0, 1)
        self.ids.button_click.disabled = False
        self.ids.label_result.text = ''
        self.click_count = 0
        self.challenge_active = True
        self.ids.button_click.unbind(on_release)
        self.ids.button_click.bind(on_release=self.register_click)
        Clock.schedule_once(self.end_challenge, 1.0)

    def register_click(self, instance):
        if self.challenge_active:
            self.click_count += 1

    def end_challenge(self, dt):
        self.challenge_active = False
        self.tr = TRANSLATIONS[self.current_lang]
        self.ids.label_result.text = self.tr['score_message'].format(self.click_count)
        self.ids.label_result.color = (0, 0, 1, 1)
        self.ids.button_click.text = self.tr['button_click']
        self.ids.button_click.background_color = (0.68, 0.85, 1, 1)
        self.ids.button_click.unbind(on_release)
        self.ids.button_click.bind(on_release=self.process_result)

    def process_result(self, instance):
        success, _ = self.game.try_add_point(self.click_count)
        self.court_success.stop()
        self.court_fail.stop()

        if success:
            self.court_success.start_animation()
            self.update_ui(result=1)
        else:
            self.court_fail.start_animation()
            self.update_ui(result=2)

        self.tr = TRANSLATIONS[self.current_lang]
        self.ids.button_click.text = self.tr['start_challenge']
        self.ids.button_click.unbind(on_release)
        self.ids.button_click.bind(on_release=self.start_challenge)

    def show_message(self, action):
        messages = {
            "Inventory": {"Русский": "Инвентарь пуст", "Английский": "Inventory is empty",
                          "Французский": "L'inventaire est vide", "Немецкий": "Inventar ist leer",
                          "Китайский": "背包是空的"},
            "Shop": {"Русский": "Магазин закрыт", "Английский": "Shop is closed", "Французский": "Le magasin est fermé",
                     "Немецкий": "Laden geschlossen", "Китайский": "商店已关闭"},
            "Authors": {"Русский": "Разработчик: Вы", "Английский": "Developer: You",
                        "Французский": "Développeur : Vous", "Немецкий": "Entwickler: Du", "Китайский": "开发者：你"}
        }
        lang_dict = messages.get(action, {})
        msg = lang_dict.get(self.current_lang, messages[action].get("Английский", "Error"))
        self.ids.label_result.text = msg
        self.ids.label_result.color = (0.5, 0, 0.5, 1)

    def show_language_menu(self):
        # В Kivy обычно создают всплывающее окно или DropDown
        # Упростим: создадим кнопки прямо поверх интерфейса (или используем Popup)
        # Здесь для демонстрации просто выводим сообщение
        self.show_message("Menu")  # Временно

    def set_language(self, lang):
        self.current_lang = lang
        self.tr = TRANSLATIONS[lang]
        # Обновляем тексты всех виджетов
        self.ids.btn_language.text = self.tr['menu_lang']
        self.ids.btn_back.text = self.tr['back']
        # и т.д.

    def update_ui(self, result=None):
        self.tr = TRANSLATIONS[self.current_lang]
        self.ids.label_points.text = self.tr['points'].format(self.game.get_points())
        if result == 1:
            self.ids.label_result.text = self.tr['hit']
            self.ids.label_result.color = (0, 1, 0, 1)
        elif result == 2:
            self.ids.label_result.text = self.tr['miss']
            self.ids.label_result.color = (1, 0, 0, 1)

    def use_potion(self, instance):
        if self.game.activate_potion():
            self.update_potion_button()
            self.update_potion_timer_label()
            self.update_potion_image()
            self.update_ui()
            self.ids.label_result.text = "🧪 Эффект x2 активирован!"
            self.ids.label_result.color = (0, 1, 0, 1)
        else:
            self.ids.label_result.text = "Эффект уже активен!"
            self.ids.label_result.color = (1, 0.5, 0, 1)

    def update_potion_button(self):
        self.tr = TRANSLATIONS[self.current_lang]
        if self.potion_btn:
            if self.game.is_potion_active():
                self.potion_btn.text = self.tr['use']
                self.potion_btn.disabled = True
            else:
                self.potion_btn.text = self.tr['potion_inactive']
                self.potion_btn.disabled = False

    def update_potion_timer_label(self):
        self.tr = TRANSLATIONS[self.current_lang]
        time_left = self.game.get_potion_time_left()
        if self.potion_timer_label:
            if time_left > 0:
                self.potion_timer_label.text = self.tr['potion_active'].format(time_left)
                self.potion_timer_label.color = (0,0,0,1)
            else:
                self.potion_timer_label.text = "Не активно"
                self.potion_timer_label.color = (0.5,0.5,0.5,1)

    def update_potion_display(self, dt=None):
        self.update_ui()
        # если инвентарь открыт, обновить
        if self.inventory_frame and self.inventory_frame.parent:
            self.update_potion_timer_label()
            self.update_potion_button()
            self.update_potion_image()

    def update_potion_image(self):
        # обновление картинки зелья
        pass

    def save_game(self):
        self.game.save_game()

    def on_closing(self, *args):
        self.save_game()
        # Остановить приложение
        App.get_running_app().stop()

# --- Класс приложения ---
class ClickerApp(App):
    def build(self):
        Window.size = (600, 450)  # как в оригинале
        return Builder.load_string(KV)

if __name__ == '__main__':
    ClickerApp().run()
