import tkinter as tk
from game_logic import ClickerGame
from datetime import datetime
import os
from PIL import Image, ImageTk
from gui.settings import Settings


class ClickerGUI:
    def __init__(self, root):
        self.game = ClickerGame()
        self.root = root
        self.root.title("Кликер")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.game.load_game()

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

        self.current_lang = "Русский"
        self.settings_frame = None
        self.settings = None
        tr = self.translations[self.current_lang]

        # Главный фрейм
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая колонка
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)

        self.game_frame = tk.Frame(self.left_frame)
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.game_frame, text="").pack(pady=(250, 0))
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

        # === ВОДЯНОЙ ЗНАК (сохраняем как self.glitch_label для управления) ===
        self.glitch_label = tk.Label(root, text="GlitchHunters", font=("Georgia", 10), fg="blue")
        self.glitch_label.place(x=10, rely=1.0, y=-10, anchor="sw")

        # Правая колонка
        self.right_frame = tk.Frame(self.main_frame, width=140)
        self.right_frame.grid(row=0, column=1, sticky="ns")
        self.right_frame.pack_propagate(False)
        self.right_frame.columnconfigure(0, weight=1)
        for i in range(5):
            self.right_frame.rowconfigure(i, weight=1)

        self.btn1 = tk.Button(self.right_frame, text=tr["btn_inventory"], bg="lightcoral", font=("Arial", 10, "bold"),
                              command=self.open_inventory)
        self.btn1.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=1)

        self.btn2 = tk.Button(self.right_frame, text=tr["btn_shop"], bg="lightgreen", font=("Arial", 10, "bold"),
                              command=self.open_shop)
        self.btn2.grid(row=1, column=0, sticky="nsew", padx=(0, 5), pady=1)

        self.btn3 = tk.Button(self.right_frame, text=tr["btn_authors"], bg="lightyellow", font=("Arial", 10, "bold"),
                              command=self.open_authors)
        self.btn3.grid(row=2, column=0, sticky="nsew", padx=(0, 5), pady=1)

        self.btn_language = tk.Button(self.right_frame, text=tr["menu_lang"], bg="lightblue",
                                      font=("Arial", 10, "bold"), command=self.show_language_menu)
        self.btn_language.grid(row=3, column=0, sticky="nsew", padx=(0, 5), pady=1)

        self.btn_settings = tk.Button(self.right_frame, text=tr["btn_settings"], font=("Arial", 10, "bold"),
                                      bg="lightgray", command=self.open_settings)
        self.btn_settings.grid(row=4, column=0, sticky="nsew", padx=(0, 5), pady=1)

        # === КНОПКА НАЗАД (ВНИЗУ ГЛАВНОГО ОКНА, НА ВСЮ ШИРИНУ) ===
        self.btn_back = tk.Button(
            self.root,
            text=tr["back"],
            font=("Arial", 12, "bold"),
            bg="lightblue",
            height=2,
            anchor="center",
            command=self.close_inventory
        )
        self.btn_back.pack_forget()  # Изначально скрыта

        self.root.title(tr["title"])
        self.click_count = 0
        self.challenge_active = False

        self.inventory_frame = tk.Frame(self.left_frame)
        self.shop_frame = tk.Frame(self.left_frame)
        self.authors_frame = tk.Frame(self.left_frame)

        self.potion_frame = None
        self.potion_btn = None
        self.potion_timer_label = None
        self.photo = None
        self.empty_photo = None
        self.image_label = None

        self.show_game()
        self.update_potion_display()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ================= УПРАВЛЕНИЕ КНОПКОЙ НАЗАД И ВОДЯНЫМ ЗНАКОМ =================
    def _show_back_button(self, command_func):
        """Показывает кнопку внизу на всю ширину и поднимает водяной знак"""
        tr = self.translations[self.current_lang]
        self.btn_back.config(text=tr["back"], command=command_func)
        if not self.btn_back.winfo_ismapped():
            self.btn_back.pack(side=tk.BOTTOM, fill=tk.X)
        # Поднимаем надпись, чтобы она не перекрывалась кнопкой
        self.glitch_label.place_configure(y=-45)

    def _hide_back_button(self):
        """Скрывает кнопку назад и возвращает водяной знак на место"""
        if self.btn_back.winfo_ismapped():
            self.btn_back.pack_forget()
        # Возвращаем надпись в исходную позицию
        self.glitch_label.place_configure(y=-10)

    # ================= НАВИГАЦИЯ =================
    def open_inventory(self):
        tr = self.translations[self.current_lang]
        self.game_frame.pack_forget()
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid_remove()

        for widget in self.inventory_frame.winfo_children():
            widget.destroy()
        self.inventory_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.inventory_frame, text=tr["inventory"], font=("Arial", 16, "bold")).pack(pady=20)

        # === УВЕЛИЧЕННЫЙ ФРЕЙМ ЗЕЛЬЯ ===
        self.potion_frame = tk.Frame(
            self.inventory_frame,
            relief="ridge",
            bd=4,
            bg="lightyellow",
            highlightbackground="gold",
            highlightthickness=2,
            width=250,
            height=170  # УВЕЛИЧИЛИ ВЫСОТУ
        )
        self.potion_frame.pack(pady=30, padx=(20, 10), anchor="w")
        self.potion_frame.pack_propagate(False)

        # Верхняя часть (картинка + кнопка)
        top_content = tk.Frame(self.potion_frame, bg="lightyellow")
        top_content.place(x=10, y=10, width=230, height=100)

        # Картинка
        image_frame = tk.Frame(top_content, bg="lightyellow", width=80, height=80)
        image_frame.pack(side=tk.LEFT, padx=(0, 10))
        image_frame.pack_propagate(False)

        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(base_dir, "images", "potionthatgives2xcoins.png")
            empty_path = os.path.join(base_dir, "images", "emptypotionthatgives2xcoins.png")

            if os.path.exists(full_path):
                self.photo = ImageTk.PhotoImage(Image.open(full_path).resize((80, 80), Image.Resampling.LANCZOS))
            if os.path.exists(empty_path):
                self.empty_photo = ImageTk.PhotoImage(Image.open(empty_path).resize((80, 80), Image.Resampling.LANCZOS))

            current_img = self.empty_photo if self.game.is_potion_active() else self.photo
            if not current_img:
                current_img = self.photo

            if current_img:
                self.image_label = tk.Label(image_frame, image=current_img, bg="lightyellow")
                self.image_label.image = current_img
            else:
                self.image_label = tk.Label(image_frame, text="🧪", font=("Arial", 32), bg="lightyellow")
            self.image_label.pack(expand=True)

        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.image_label = tk.Label(image_frame, text="🧪", font=("Arial", 32), bg="lightyellow")
            self.image_label.pack(expand=True)

        # Текст и кнопка
        text_frame = tk.Frame(top_content, bg="lightyellow")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(text_frame, text=tr["potion"], bg="lightyellow", font=("Arial", 9, "bold"), anchor="w").pack(
            fill=tk.X, pady=(0, 3))

        self.potion_btn = tk.Button(text_frame, text="", font=("Arial", 8), width=14, command=self.use_potion)
        self.potion_btn.pack(anchor="w")

        # === ТАЙМЕР - ИСПОЛЬЗУЕМ place ДЛЯ ТОЧНОГО ПОЗИЦИОНИРОВАНИЯ ===
        # Уничтожаем старый если есть
        if hasattr(self, 'potion_timer_label') and self.potion_timer_label:
            try:
                self.potion_timer_label.destroy()
            except:
                pass

        # Создаем новый с явными параметрами
        self.potion_timer_label = tk.Label(
            self.potion_frame,
            text="",  # Будет заполнен update_potion_timer_label
            bg="LIGHTGREEN",  # ЯРКИЙ ФОН для видимости
            fg="BLACK",
            font=("Arial", 8),
            anchor="w",
            justify="left",
            relief="solid",
            bd=1,
            wraplength=220
        )
        # Размещаем внизу фрейма зелья
        self.potion_timer_label.place(x=10, y=115, width=230, height=45)

        self.update_potion_button()
        self.update_potion_timer_label()
        self._show_back_button(self.close_inventory)
    def close_inventory(self):
        self.inventory_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid()
        self._hide_back_button()
        self.update_ui()

    def open_shop(self):
        tr = self.translations[self.current_lang]
        self.game_frame.pack_forget()
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid_remove()
        for widget in self.shop_frame.winfo_children():
            widget.destroy()
        tk.Label(self.shop_frame, text=tr["btn_shop"], font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.shop_frame, text="🏪 Магазин временно закрыт", font=("Arial", 12), fg="gray").pack(pady=10)
        self.shop_frame.pack(fill=tk.BOTH, expand=True)
        self._show_back_button(self.close_shop)

    def close_shop(self):
        self.shop_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid()
        self._hide_back_button()

    def open_authors(self):
        tr = self.translations[self.current_lang]
        self.game_frame.pack_forget()
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid_remove()
        for widget in self.authors_frame.winfo_children():
            widget.destroy()
        tk.Label(self.authors_frame, text=tr["btn_authors"], font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.authors_frame,
                 text="🎮 Authors:\n• thekosmoss\n• artman\n• Kirill\n\n🔧 Project: Clicker Basketball\n📅 2025 GlitchHunters Team",
                 font=("Arial", 11), justify="center", fg="black").pack(pady=10)
        self.authors_frame.pack(fill=tk.BOTH, expand=True)
        self._show_back_button(self.close_authors)

    def close_authors(self):
        self.authors_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid()
        self._hide_back_button()

    def open_settings(self):
        self.hide_all_screens()
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid_remove()

        if self.settings_frame is None:
            self.settings_frame = tk.Frame(self.left_frame)
            self.settings = Settings(self.settings_frame, self)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)
        self._show_back_button(self.close_settings)

    def close_settings(self):
        if self.settings_frame:
            self.settings_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        for btn in [self.btn1, self.btn2, self.btn3, self.btn_language, self.btn_settings]:
            btn.grid()
        self._hide_back_button()

    def hide_all_screens(self):
        self.game_frame.pack_forget()
        self.inventory_frame.pack_forget()
        self.shop_frame.pack_forget()
        self.authors_frame.pack_forget()
        if self.settings_frame:
            self.settings_frame.pack_forget()

    # ================= ИГРОВАЯ ЛОГИКА И UI =================
    def start_challenge(self):
        tr = self.translations[self.current_lang]
        self.button_click.config(text=tr["click_now"], bg="red", state="normal")
        self.label_result.config(text="", fg="black")
        self.click_count = 0
        self.challenge_active = True
        self.button_click.config(command=self.register_click)
        self.root.after(1000, self.end_challenge)

    def register_click(self):
        if self.challenge_active: self.click_count += 1

    def end_challenge(self):
        self.challenge_active = False
        self.button_click.config(command=self.process_result)
        tr = self.translations[self.current_lang]
        self.label_result.config(text=tr["score_message"].format(self.click_count), fg="blue")
        self.button_click.config(text=tr["button_click"], bg="lightblue")

    def process_result(self):
        success, _ = self.game.try_add_point(self.click_count)
        self.update_ui(result=1 if success else 2)
        tr = self.translations[self.current_lang]
        self.button_click.config(text=tr["start_challenge"], command=self.start_challenge)

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
        self.label_result.config(text=msg, fg="purple")

    def show_language_menu(self):
        if hasattr(self, 'language_menu') and self.language_menu: self.language_menu.destroy()
        self.language_menu = tk.Menu(self.root, tearoff=0)
        for lang in self.translations.keys():
            self.language_menu.add_command(label=lang, command=lambda l=lang: self.set_language(l))
        self.language_menu.post(self.btn_language.winfo_rootx(),
                                self.btn_language.winfo_rooty() + self.btn_language.winfo_height())

    def set_language(self, lang):
        self.current_lang = lang
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

    def update_ui(self, result=None):
        tr = self.translations[self.current_lang]
        self.label_points.config(text=tr["points"].format(self.game.get_points()))
        if result == 1:
            self.label_result.config(text=tr["hit"], fg="green")
        elif result == 2:
            self.label_result.config(text=tr["miss"], fg="red")

    def use_potion(self):
        if self.game.activate_potion():
            self.update_potion_button()
            self.update_potion_timer_label()
            self.update_potion_image()
            self.update_ui()
            self.label_result.config(text="🧪 Эффект x2 активирован!", fg="green")
            self.potion_frame.config(bg="lightgreen")
            self.root.after(3000, lambda: self.potion_frame.config(bg="lightyellow"))
        else:
            self.label_result.config(text="⏳ Эффект уже активен!", fg="orange")

    def update_potion_button(self):
        tr = self.translations[self.current_lang]
        if hasattr(self, 'potion_btn') and self.potion_btn:
            if self.game.is_potion_active():
                self.potion_btn.config(text=tr["use"], state="disabled")
            else:
                self.potion_btn.config(text=tr["potion_inactive"], state="normal")

    def update_potion_timer_label(self):
        tr = self.translations[self.current_lang]
        time_left = self.game.get_potion_time_left()

        if hasattr(self, 'potion_timer_label') and self.potion_timer_label:
            if time_left > 0:
                timer_text = tr["potion_active"].format(time_left)
                self.potion_timer_label.config(
                    text=timer_text,
                    bg="LIGHTGREEN",  # Яркий фон когда активно
                    fg="BLACK"
                )
            else:
                # Показываем текст когда не активно
                self.potion_timer_label.config(
                    text="Не активно",  # Или tr["potion_inactive"]
                    bg="LIGHTGRAY",  # Серый фон
                    fg="BLACK"
                )

    def update_potion_display(self):
        self.update_ui()
        if hasattr(self, 'inventory_frame') and self.inventory_frame.winfo_ismapped():
            self.update_potion_timer_label()
            self.update_potion_button()
            self.update_potion_image()
        self.root.after(1000, self.update_potion_display)

    def update_potion_image(self):
        if not hasattr(self, 'image_label') or not self.image_label or not self.photo or not self.empty_photo: return
        try:
            new_img = self.empty_photo if self.game.is_potion_active() else self.photo
            self.image_label.config(image=new_img)
            self.image_label.image = new_img
        except Exception as e:
            print(f"Ошибка картинки: {e}")

    def show_game(self):
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.inventory_frame.pack_forget()

    def save_game(self):
        self.game.save_game()

    def on_closing(self):
        self.save_game(); self.root.destroy()