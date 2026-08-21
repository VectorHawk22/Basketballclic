import tkinter as tk
import os
import sys
from PIL import Image, ImageTk

# Добавляем корень проекта в пути импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_logic import ClickerGame
from gui.settings import Settings      # ← gui. потому что settings.py в той же папке gui/
from gui.inventory import InventoryManager
from gui.shop import ShopManager
from gui.authors import AuthorsManager
from animation.court1 import CourtSuccess
from animation.court2 import CourtFail


class ClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Кликер")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Определяем корневую папку проекта
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Загружаем настройки
        self.settings = self.load_settings()

        # Инициализация игры
        self.game = ClickerGame()

        # Устанавливаем язык из настроек
        self.current_lang = self.settings.get("language", "Русский")

        # Менеджеры экранов
        self.inventory_manager = None
        self.shop_manager = None
        self.authors_manager = None
        self.settings_manager = None
        self.settings_frame = None
        self.language_menu = None

        self.translations = {
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
                "potion": "🧪 2x очки (10 мин)", "potion_active": "Активно! Осталось: {} сек",
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

        tr = self.translations[self.current_lang]

        # === ОСНОВНОЙ ЛЕЙАУТ ===
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame, width=440, height=430)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.left_frame.grid_propagate(False)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)

        # === АНИМАЦИЯ ===
        self.anim_container = tk.Frame(self.left_frame, height=280, bg="#f0f0f0")
        self.anim_container.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))
        self.anim_container.pack_propagate(False)

        self.animation_canvas = tk.Canvas(self.anim_container, width=420, height=240, bg="#f0f0f0",
                                          highlightthickness=1, highlightbackground="gray")
        self.animation_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Инициализация классов анимации
        self.court_success = CourtSuccess(self.animation_canvas)
        self.court_fail = CourtFail(self.animation_canvas)
        self.root.after(150, self.redraw_animation)

        # === ИГРОВОЙ ЭКРАН ===
        self.game_frame = tk.Frame(self.left_frame)
        tk.Label(self.game_frame, text="").pack(pady=(20, 0))
        self.label_result = tk.Label(self.game_frame, text="", font=("Arial", 12))
        self.label_result.pack(pady=20)

        bottom_row = tk.Frame(self.game_frame)
        bottom_row.pack(side=tk.BOTTOM, anchor="s", pady=(0, 5))

        self.button_click = tk.Button(bottom_row, text=tr["start_challenge"], font=("Arial", 14), width=18, height=2,
                                      bg="lightblue", command=self.start_challenge)
        self.button_click.pack(side=tk.LEFT, padx=20)

        self.label_points = tk.Label(bottom_row, text=tr["points"].format(self.game.get_points()),
                                     font=("Arial", 16, "bold"))
        self.label_points.pack(side=tk.LEFT, padx=20)

        # === ПРАВАЯ ПАНЕЛЬ ===
        self.right_frame = tk.Frame(self.main_frame, width=140)
        self.right_frame.grid(row=0, column=1, sticky="ns")
        self.right_frame.pack_propagate(False)

        self.btn1 = tk.Button(self.right_frame, text=tr["btn_inventory"], bg="lightcoral", font=("Arial", 10, "bold"),
                              command=self.open_inventory)
        self.btn1.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        self.btn2 = tk.Button(self.right_frame, text=tr["btn_shop"], bg="lightgreen", font=("Arial", 10, "bold"),
                              command=self.open_shop)
        self.btn2.grid(row=1, column=0, sticky="nsew", padx=(0, 5), pady=5)

        self.btn3 = tk.Button(self.right_frame, text=tr["btn_authors"], bg="lightyellow", font=("Arial", 10, "bold"),
                              command=self.open_authors)
        self.btn3.grid(row=2, column=0, sticky="nsew", padx=(0, 5), pady=5)

        self.btn_language = tk.Button(self.right_frame, text=tr["menu_lang"], bg="lightblue",
                                      font=("Arial", 10, "bold"), command=self.show_language_menu)
        self.btn_language.grid(row=3, column=0, sticky="nsew", padx=(0, 5), pady=5)

        self.btn_settings = tk.Button(self.right_frame, text=tr["btn_settings"], font=("Arial", 10, "bold"),
                                      bg="lightgray", command=self.open_settings)
        self.btn_settings.grid(row=4, column=0, sticky="nsew", padx=(0, 5), pady=5)

        # === КНОПКА НАЗАД ===
        self.btn_back = tk.Button(self.root, text=tr["back"], font=("Arial", 12, "bold"), bg="lightblue", height=2,
                                  anchor="center")
        self.btn_back.pack_forget()

        # === НИЖНИЙ ТЕКСТ ===
        self.glitch_label = tk.Label(root, text="GlitchHunters", font=("Georgia", 10), fg="blue")
        self.glitch_label.place(x=10, rely=1.0, y=-10, anchor="sw")

        # === ПЕРЕМЕННЫЕ ДЛЯ ИГРЫ ===
        self.click_count = 0
        self.challenge_active = False

        # Показываем игровой экран
        self.show_game()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):
        """Загрузка настроек из файла settings.json"""
        settings_file = os.path.join(self.base_dir, "settings.json")
        default_settings = {"sound": True, "language": "Русский"}

        if not os.path.exists(settings_file):
            # Создаём файл с настройками по умолчанию
            try:
                import json
                with open(settings_file, "w", encoding="utf-8") as f:
                    json.dump(default_settings, f, ensure_ascii=False, indent=4)
                print("✅ Создан settings.json с настройками по умолчанию")
            except Exception as e:
                print(f"⚠️ Не удалось создать settings.json: {e}")
            return default_settings

        try:
            import json
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            default_settings.update(data)
            return default_settings
        except Exception as e:
            print(f"⚠️ Ошибка загрузки настроек: {e}")
            return default_settings

    def save_settings(self):
        """Сохранение настроек"""
        settings_file = os.path.join(self.base_dir, "settings.json")
        try:
            import json
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ Ошибка сохранения настроек: {e}")

    # ================= UI HELPERS =================
    def _show_back_button(self, command_func):
        tr = self.translations[self.current_lang]
        self.btn_back.config(text=tr["back"], command=command_func)
        if not self.btn_back.winfo_ismapped():
            self.btn_back.pack(side=tk.BOTTOM, fill=tk.X)
        self.glitch_label.place_configure(y=-45)

    def _hide_back_button(self):
        if self.btn_back.winfo_ismapped():
            self.btn_back.pack_forget()
        self.glitch_label.place_configure(y=-10)

    def hide_all_screens(self):
        self.game_frame.pack_forget()
        if self.inventory_manager:
            self.inventory_manager.inventory_frame.pack_forget()
        if self.shop_manager:
            self.shop_manager.shop_frame.pack_forget()
        if self.authors_manager:
            self.authors_manager.authors_frame.pack_forget()
        if self.settings_frame:
            self.settings_frame.pack_forget()

    # ================= NAVIGATION =================
    def open_inventory(self):
        if self.inventory_manager is None:
            self.inventory_manager = InventoryManager(
                self, self.game, self.translations, self.current_lang
            )
        self.inventory_manager.open()

    def open_shop(self):
        if self.shop_manager is None:
            self.shop_manager = ShopManager(self, self.translations, self.current_lang)
        self.shop_manager.open()

    def open_authors(self):
        if self.authors_manager is None:
            self.authors_manager = AuthorsManager(self, self.translations, self.current_lang)
        self.authors_manager.open()

    def open_settings(self):
        if self.settings_frame is None:
            self.settings_frame = tk.Frame(self.left_frame)
            self.settings_manager = Settings(self.settings_frame, self)

        # Скрываем игровой экран
        self.game_frame.pack_forget()
        self.anim_container.pack_forget()

        # Скрываем правую панель
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid_remove()

        self.settings_frame.pack(fill=tk.BOTH, expand=True)
        self._show_back_button(self.close_settings)

    def close_settings(self):
        if self.settings_frame:
            self.settings_frame.pack_forget()
        self.show_game()
        self.anim_container.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid()
        self._hide_back_button()

    # ================= GAME LOGIC =================
    def start_challenge(self):
        tr = self.translations[self.current_lang]
        self.button_click.config(text=tr["click_now"], bg="red", state="normal")
        self.label_result.config(text="", fg="black")
        self.click_count = 0
        self.challenge_active = True
        self.button_click.config(command=self.register_click)
        self.root.after(1000, self.end_challenge)

    def register_click(self):
        if self.challenge_active:
            self.click_count += 1

    def end_challenge(self):
        self.challenge_active = False
        self.button_click.config(command=self.process_result)
        tr = self.translations[self.current_lang]
        self.label_result.config(text=tr["score_message"].format(self.click_count), fg="blue")
        self.button_click.config(text=tr["button_click"], bg="lightblue")

    def process_result(self):
        success, _ = self.game.try_add_point(self.click_count)
        self.court_success.stop()
        self.court_fail.stop()

        if success:
            self.court_success.start_animation()
            self.update_ui(result=1)
        else:
            self.court_fail.start_animation()
            self.update_ui(result=2)

        tr = self.translations[self.current_lang]
        self.button_click.config(text=tr["start_challenge"], command=self.start_challenge)

    # ================= UI & LANGUAGE =================
    def show_language_menu(self):
        if hasattr(self, 'language_menu') and self.language_menu:
            self.language_menu.destroy()
        self.language_menu = tk.Menu(self.root, tearoff=0)
        for lang in self.translations.keys():
            self.language_menu.add_command(
                label=lang,
                command=lambda l=lang: self.set_language(l)
            )
        self.language_menu.post(
            self.btn_language.winfo_rootx(),
            self.btn_language.winfo_rooty() + self.btn_language.winfo_height()
        )

    def set_language(self, lang):
        self.current_lang = lang
        self.settings["language"] = lang
        self.save_settings()

        tr = self.translations[lang]
        self.root.title(tr["title"])
        self.btn_language.config(text=tr["menu_lang"])
        self.btn_back.config(text=tr["back"])

        current = self.button_click.cget("text")
        if any(x in current for x in ["start", "начни", "commencer", "Starten", "开始"]):
            self.button_click.config(text=tr["start_challenge"])
        elif any(x in current for x in ["now", "сейчас", "maintenant", "jetzt", "立即"]):
            self.button_click.config(text=tr["click_now"])
        else:
            self.button_click.config(text=tr["button_click"])

        self.label_points.config(text=tr["points"].format(self.game.get_points()))
        self.btn1.config(text=tr["btn_inventory"])
        self.btn2.config(text=tr["btn_shop"])
        self.btn3.config(text=tr["btn_authors"])
        self.btn_settings.config(text=tr["btn_settings"])

        # Обновляем язык в менеджерах
        if self.inventory_manager:
            self.inventory_manager.update_language(lang)
        if self.shop_manager:
            self.shop_manager.update_language(lang)
        if self.authors_manager:
            self.authors_manager.update_language(lang)

    def update_ui(self, result=None):
        tr = self.translations[self.current_lang]
        self.label_points.config(text=tr["points"].format(self.game.get_points()))
        if result == 1:
            self.label_result.config(text=tr["hit"], fg="green")
        elif result == 2:
            self.label_result.config(text=tr["miss"], fg="red")

    # ================= LIFECYCLE =================
    def show_game(self):
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        if self.inventory_manager:
            self.inventory_manager.inventory_frame.pack_forget()
        if self.shop_manager:
            self.shop_manager.shop_frame.pack_forget()
        if self.authors_manager:
            self.authors_manager.authors_frame.pack_forget()
        if self.settings_frame:
            self.settings_frame.pack_forget()
        self.update_ui()

    def on_closing(self):
        self.game.save_game()
        self.save_settings()
        self.root.destroy()

    def redraw_animation(self):
        w = self.animation_canvas.winfo_width()
        h = self.animation_canvas.winfo_height()
        if w > 50 and h > 50:
            self.animation_canvas.delete("all")
            self.court_success.draw_court()
        else:
            self.root.after(100, self.redraw_animation)