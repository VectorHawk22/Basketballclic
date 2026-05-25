import tkinter as tk
from game_logic import ClickerGame
from datetime import datetime
import os
from PIL import Image, ImageTk  # Для масштабирования изображений


class ClickerGUI:
    def __init__(self, root):
        self.game = ClickerGame()
        self.root = root
        self.root.title("Кликер")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Загружаем игру
        self.game.load_game()

        # Словарь переводов
        self.translations = {
            "Английский": {
                "title": "Clicker",
                "result": "Result: -",
                "hit": "🎯 Hit! +1 point!",
                "miss": "❌ Missed :(",
                "points": "Points: {}",
                "button_click": "Click!",
                "menu_lang": "Select language",
                "btn_inventory": "Inventory",
                "btn_shop": "Shop",
                "btn_authors": "Authors",
                "start_challenge": "Click to start!",
                "click_now": "CLICK NOW!",
                "score_message": "{} clicks in 1 second!",
                "inventory": "Inventory",
                "potion": "🧪 Double Points (10 min)",
                "potion_active": "Active! Time left: {} sec",
                "potion_inactive": "Use: 10 min x2",
                "use": "Use",
                "back": "Back"
            },
            "Русский": {
                "title": "Кликер",
                "result": "Результат: -",
                "hit": "🎯 Попал! +1 очко!",
                "miss": "❌ Промах :(",
                "points": "Очки: {}",
                "button_click": "Клик!",
                "menu_lang": "Язык",
                "btn_inventory": "Инвентарь",
                "btn_shop": "Магазин",
                "btn_authors": "Авторы",
                "start_challenge": "Нажми, и начни!",
                "click_now": "ЖМИ СЕЙЧАС!",
                "score_message": "{} кликов за 1 секунду!",
                "inventory": "Инвентарь",
                "potion": "🧪2x очки (10 мин)",
                "potion_active": "Активно! Осталось: {} сек",
                "potion_inactive": "Использовать: 10 мин",
                "use": "Использовать",
                "back": "Назад"
            },
            "Французский": {
                "title": "Cliqueur",
                "result": "Résultat : -",
                "hit": "🎯 Touché ! +1 point !",
                "miss": "❌ Raté :(",
                "points": "Points : {}",
                "button_click": "Cliquez !",
                "menu_lang": "Choisir la langue",
                "btn_inventory": "Inventaire",
                "btn_shop": "Magasin",
                "btn_authors": "Auteurs",
                "start_challenge": "Cliquez pour commencer !",
                "click_now": "CLIQUEZ MAINTENANT !",
                "score_message": "{} clics en 1 seconde !",
                "inventory": "Inventaire",
                "potion": "🧪 Double points (10 min)",
                "potion_active": "Actif ! Temps restant : {} sec",
                "potion_inactive": "Utiliser : 10 min x2",
                "use": "Utiliser",
                "back": "Retour"
            },
            # --- НОВЫЕ ЯЗЫКИ НИЖЕ ---
            "Немецкий": {
                "title": "Klicker",
                "result": "Ergebnis: -",
                "hit": "🎯 Treffer! +1 Punkt!",
                "miss": "❌ Daneben :(",
                "points": "Punkte: {}",
                "button_click": "Klick!",
                "menu_lang": "Sprache wählen",
                "btn_inventory": "Inventar",
                "btn_shop": "Laden",
                "btn_authors": "Autoren",
                "start_challenge": "Klicke zum Starten!",
                "click_now": "JETZT KLICKEN!",
                "score_message": "{} Klicks in 1 Sekunde!",
                "inventory": "Inventar",
                "potion": "🧪 Doppelte Punkte (10 Min)",
                "potion_active": "Aktiv! Verbleibend: {} Sek",
                "potion_inactive": "Benutzen: 10 Min x2",
                "use": "Benutzen",
                "back": "Zurück"
            },
            "Китайский": {
                "title": "点击器",
                "result": "结果: -",
                "hit": "🎯 击中！+1 分！",
                "miss": "❌ 未命中 :(",
                "points": "分数: {}",
                "button_click": "点击！",
                "menu_lang": "选择语言",
                "btn_inventory": "背包",
                "btn_shop": "商店",
                "btn_authors": "作者",
                "start_challenge": "点击开始！",
                "click_now": "立即点击！",
                "score_message": "1秒内点击 {} 次！",
                "inventory": "背包",
                "potion": "🧪 双倍积分 (10分钟)",
                "potion_active": "生效中！剩余时间：{} 秒",
                "potion_inactive": "使用：10分钟双倍",
                "use": "使用",
                "back": "返回"
            }
        }

        self.current_lang = "Русский"
        tr = self.translations[self.current_lang]

        # Главный фрейм
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая колонка — основной контент
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)

        # Элементы основной игры
        self.game_frame = tk.Frame(left_frame)
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.game_frame, text="").pack(pady=40)

        # Очки
        self.label_points = tk.Label(self.game_frame, text=tr["points"].format(self.game.get_points()),
                                     font=("Arial", 16, "bold"))
        self.label_points.pack(padx=1, pady=1)
        # Атрибуты для изображений зелья
        self.photo = None  # Полная бутылка
        self.empty_photo = None  # Пустая бутылка
        self.image_label = None  # Виджет Label с картинкой

        # Водяной знак
        glitch_label = tk.Label(
            root,
            text="GlitchHunters",
            font=("Georgia", 10),
            fg="blue"
        )
        glitch_label.place(x=10, y=10, anchor="nw")

        # Сообщение
        self.label_result = tk.Label(self.game_frame, text="", font=("Arial", 12))
        self.label_result.pack(pady=10)

        # Кнопка действия
        self.button_click = tk.Button(
            self.game_frame, text=tr["start_challenge"],
            font=("Arial", 14), width=15, height=3, bg="lightblue", command=self.start_challenge
        )
        self.button_click.pack(pady=30)

        # Правая колонка — боковые кнопки
        right_frame = tk.Frame(main_frame, width=120)
        right_frame.grid(row=0, column=1, sticky="ns")
        right_frame.pack_propagate(False)
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(2, weight=1)

        self.btn1 = tk.Button(right_frame, text=tr["btn_inventory"], bg="lightcoral", font=("Arial", 10, "bold"),
                              command=self.open_inventory)
        self.btn1.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(0, 1))

        self.btn2 = tk.Button(right_frame, text=tr["btn_shop"], bg="lightgreen", font=("Arial", 10, "bold"),
                              command=self.open_shop)
        self.btn2.grid(row=1, column=0, sticky="nsew", padx=(0, 5), pady=1)

        self.btn3 = tk.Button(right_frame, text=tr["btn_authors"], bg="lightyellow", font=("Arial", 10, "bold"),
                              command=self.open_authors)
        self.btn3.grid(row=2, column=0, sticky="nsew", padx=(0, 5), pady=(1, 0))

        # Кнопка выбора языка снизу
        bottom_frame = tk.Frame(root, height=60)
        bottom_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=10, pady=10)
        bottom_frame.pack_propagate(False)

        self.btn_language = tk.Button(
            bottom_frame,
            text=tr["menu_lang"],
            font=("Arial", 12),
            bg="lightblue",
            command=self.show_language_menu
        )
        self.btn_language.pack(fill=tk.BOTH, expand=True)

        self.root.title(tr["title"])

        # Переменные для механики
        self.click_count = 0
        self.challenge_active = False

        # Фрейм инвентаря (скрыт по умолчанию)
        self.inventory_frame = tk.Frame(left_frame)
        self.shop_frame = tk.Frame(left_frame)
        self.authors_frame = tk.Frame(left_frame)

        # Слот для зелья (будет в инвентаре)
        self.potion_frame = None
        self.potion_btn = None
        self.potion_timer_label = None

        # Кнопка "Назад" (внизу)
        self.btn_back = tk.Button(
            bottom_frame,
            text=tr["back"],
            font=("Arial", 12),
            bg="lightblue",
            command=self.close_inventory,
            state="normal"
        )

        # Сохраняем правую панель как атрибут
        self.right_frame = right_frame

        # Показываем основную игру
        self.show_game()

        # Обновление таймера
        self.update_potion_display()

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        success, chance = self.game.try_add_point(self.click_count)
        self.update_ui(result=1 if success else 2)
        tr = self.translations[self.current_lang]
        self.button_click.config(text=tr["start_challenge"], command=self.start_challenge)

    def show_message(self, action):
        # Добавляем новые языки в сообщения об ошибках/пустых состояниях
        messages = {
            "Inventory": {
                "Русский": "Инвентарь пуст",
                "Английский": "Inventory is empty",
                "Французский": "L'inventaire est vide",
                "Немецкий": "Inventar ist leer",
                "Китайский": "背包是空的"
            },
            "Shop": {
                "Русский": "Магазин закрыт",
                "Английский": "Shop is closed",
                "Французский": "Le magasin est fermé",
                "Немецкий": "Laden geschlossen",
                "Китайский": "商店已关闭"
            },
            "Authors": {
                "Русский": "Разработчик: Вы",
                "Английский": "Developer: You",
                "Французский": "Développeur : Vous",
                "Немецкий": "Entwickler: Du",
                "Китайский": "开发者：你"
            }
        }

        # Защита от KeyError, если язык есть в основном словаре, но не в сообщениях
        lang_dict = messages.get(action, {})
        msg = lang_dict.get(self.current_lang, messages[action].get("Английский", "Error"))

        self.label_result.config(text=msg, fg="purple")

    def show_language_menu(self):
        if hasattr(self, 'language_menu') and self.language_menu:
            self.language_menu.destroy()
        self.language_menu = tk.Menu(self.root, tearoff=0)
        for lang in self.translations.keys():
            self.language_menu.add_command(label=lang, command=lambda l=lang: self.set_language(l))
        btn_x = self.btn_language.winfo_rootx()
        btn_y = self.btn_language.winfo_rooty() + self.btn_language.winfo_height()
        self.language_menu.post(btn_x, btn_y)

    def set_language(self, lang):
        self.current_lang = lang
        tr = self.translations[lang]
        self.root.title(tr["title"])
        self.btn_language.config(text=tr["menu_lang"])
        self.btn_back.config(text=tr["back"])

        # Логика обновления текста кнопки действия в зависимости от её текущего состояния
        current_text = self.button_click.cget("text")
        if current_text == self.translations["Русский"]["start_challenge"] or \
                current_text == self.translations["Английский"]["start_challenge"] or \
                current_text == self.translations["Французский"]["start_challenge"] or \
                current_text == self.translations["Немецкий"]["start_challenge"] or \
                current_text == self.translations["Китайский"]["start_challenge"]:
            self.button_click.config(text=tr["start_challenge"])
        elif current_text == self.translations["Русский"]["click_now"] or \
                current_text == self.translations["Английский"]["click_now"] or \
                current_text == self.translations["Французский"]["click_now"] or \
                current_text == self.translations["Немецкий"]["click_now"] or \
                current_text == self.translations["Китайский"]["click_now"]:
            self.button_click.config(text=tr["click_now"])
        elif current_text == self.translations["Русский"]["button_click"] or \
                current_text == self.translations["Английский"]["button_click"] or \
                current_text == self.translations["Французский"]["button_click"] or \
                current_text == self.translations["Немецкий"]["button_click"] or \
                current_text == self.translations["Китайский"]["button_click"]:
            self.button_click.config(text=tr["button_click"])

        self.label_points.config(text=tr["points"].format(self.game.get_points()))
        self.btn1.config(text=tr["btn_inventory"])
        self.btn2.config(text=tr["btn_shop"])
        self.btn3.config(text=tr["btn_authors"])

    def update_ui(self, result=None):
        tr = self.translations[self.current_lang]
        self.label_points.config(text=tr["points"].format(self.game.get_points()))
        if result == 1:
            self.label_result.config(text=tr["hit"], fg="green")
        elif result == 2:
            self.label_result.config(text=tr["miss"], fg="red")

    def open_inventory(self):
        tr = self.translations[self.current_lang]

        # Скрываем основную игру и правую панель
        self.game_frame.pack_forget()
        self.right_frame.grid_remove()

        # Очищаем инвентарь перед перерисовкой
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        # Показываем инвентарь
        self.inventory_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(self.inventory_frame, text=tr["inventory"], font=("Arial", 16, "bold")).pack(pady=20)

        # === Слот для зелья ===
        self.potion_frame = tk.Frame(
            self.inventory_frame,
            relief="ridge", bd=4, bg="lightyellow",
            highlightbackground="gold", highlightthickness=2,
            width=250, height=140
        )
        self.potion_frame.pack(pady=30, padx=(20, 10), anchor="w")
        self.potion_frame.pack_propagate(False)

        inner_frame = tk.Frame(self.potion_frame, bg="lightyellow")
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === ЛЕВАЯ ЧАСТЬ — КАРТИНКА ===
        image_frame = tk.Frame(inner_frame, bg="lightyellow", width=100, height=100)
        image_frame.pack(side=tk.LEFT, anchor="w", padx=(0, 10))
        image_frame.pack_propagate(False)

        # Сброс переменных изображений
        self.photo = None
        self.empty_photo = None
        self.image_label = None

        try:
            # Определяем пути. Убедитесь, что папка images лежит рядом с allgui.py
            # Поднимаемся на один уровень вверх из папки gui/ в папку проект/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            full_path = os.path.join(base_dir, "images", "potionthatgives2xcoins.png")
            empty_path = os.path.join(base_dir, "images", "emptypotionthatgives2xcoins.png")

            print(f"🔍 Ищем полную бутылку: {full_path}")
            print(f"🔍 Ищем пустую бутылку: {empty_path}")

            # Загрузка полной
            if os.path.exists(full_path):
                img_full = Image.open(full_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img_full)
            else:
                print("⚠️ Файл полной бутылки НЕ НАЙДЕН!")

            # Загрузка пустой
            if os.path.exists(empty_path):
                img_empty = Image.open(empty_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.empty_photo = ImageTk.PhotoImage(img_empty)
            else:
                print("⚠️ Файл пустой бутылки НЕ НАЙДЕН!")

            # Выбор текущего изображения
            current_img = self.empty_photo if self.game.is_potion_active() else self.photo

            # Если картинок нет вообще, ставим заглушку
            if current_img is None:
                current_img = self.photo if self.photo else self.empty_photo

            # Создание Label
            if current_img:
                self.image_label = tk.Label(image_frame, image=current_img, bg="lightyellow")
                self.image_label.image = current_img  # Сохраняем ссылку!
            else:
                # Если ни одной картинки не загрузилось
                self.image_label = tk.Label(image_frame, text="🧪", font=("Arial", 32), bg="lightyellow")

            self.image_label.pack(side=tk.LEFT, padx=5, pady=5)

        except Exception as e:
            print(f"❌ Критическая ошибка загрузки: {e}")
            # Фоллбэк при ошибке
            self.image_label = tk.Label(image_frame, text="", font=("Arial", 32), bg="lightyellow")
            self.image_label.pack(side=tk.LEFT, padx=5, pady=5)

        # === ПРАВАЯ ЧАСТЬ ===
        text_frame = tk.Frame(inner_frame, bg="lightyellow")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(text_frame, text=tr["potion"], bg="lightyellow", font=("Arial", 10, "bold"), anchor="w").pack(
            fill=tk.X, pady=(0, 5))

        self.potion_btn = tk.Button(text_frame, text="", font=("Arial", 9), width=18, command=self.use_potion)
        self.potion_btn.pack(anchor="w")

        self.potion_timer_label = tk.Label(self.potion_frame, text="", bg="lightyellow", font=("Arial", 9))
        self.potion_timer_label.pack(pady=(5, 0), anchor="w", padx=15)

        # Обновляем UI
        self.update_potion_button()
        self.update_potion_timer_label()

        # Переключение кнопок навигации
        self.btn_language.pack_forget()
        self.btn_back.pack(fill=tk.BOTH, expand=True)

    def close_inventory(self):
        # Скрываем инвентарь
        self.inventory_frame.pack_forget()
        # Показываем основную игру
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        # Возвращаем правую панель
        self.right_frame.grid()
        # Возвращаем кнопку языка
        self.btn_back.pack_forget()
        self.btn_language.pack(fill=tk.BOTH, expand=True)
        # Обновляем UI
        self.update_ui()

    def use_potion(self):
        if self.game.activate_potion():
            self.update_potion_button()
            self.update_potion_timer_label()
            self.update_potion_image()  # ← ДОБАВЛЕНО: меняем картинку
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
                self.potion_timer_label.config(text=tr["potion_active"].format(time_left))
            else:
                self.potion_timer_label.config(text="")

    def update_potion_display(self):
        self.update_ui()

        if self.inventory_frame.winfo_ismapped():
            self.update_potion_timer_label()
            self.update_potion_button()
            self.update_potion_image()  # ← ДОБАВЛЕНО: проверка каждые 1 сек

        self.root.after(1000, self.update_potion_display)

    def show_game(self):
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.inventory_frame.pack_forget()

    def save_game(self):
        self.game.save_game()

    def on_closing(self):
        self.save_game()
        self.root.destroy()

    def open_shop(self):
        tr = self.translations[self.current_lang]

        # 1. Скрываем игру и правую панель
        self.game_frame.pack_forget()
        self.right_frame.grid_remove()  # Скрывает инвентарь, магазин, авторов

        # 2. Скрываем кнопку языка
        self.btn_language.pack_forget()

        # 3. Очищаем магазин от старого содержимого
        for widget in self.shop_frame.winfo_children():
            widget.destroy()

        # 4. Рисуем интерфейс магазина
        tk.Label(self.shop_frame, text=tr["btn_shop"], font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.shop_frame, text="🏪 Магазин временно закрыт", font=("Arial", 12), fg="gray").pack(pady=10)

        # 5. Показываем фрейм магазина
        self.shop_frame.pack(fill=tk.BOTH, expand=True)

        # 6. Настраиваем и показываем кнопку "Назад"
        # Важно: меняем команду кнопки, чтобы она закрывала именно магазин
        self.btn_back.config(command=self.close_shop, text=tr["back"])
        self.btn_back.pack(fill=tk.BOTH, expand=True)

    def close_shop(self):
        # 1. Скрываем магазин
        self.shop_frame.pack_forget()

        # 2. Возвращаем игру
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        # 3. Возвращаем правую панель
        self.right_frame.grid()

        # 4. Скрываем кнопку "Назад"
        self.btn_back.pack_forget()

        # 5. Возвращаем кнопку языка
        self.btn_language.pack(fill=tk.BOTH, expand=True)

        # 6. Возвращаем команду кнопки "Назад" к инвентарю (по умолчанию)
        tr = self.translations[self.current_lang]
        self.btn_back.config(command=self.close_inventory, text=tr["back"])

    def open_authors(self):
        """Открывает экран 'Авторы', скрывая всё остальное"""
        tr = self.translations[self.current_lang]

        # 1. Скрываем игру и правую панель
        self.game_frame.pack_forget()
        self.right_frame.grid_remove()  # Скрывает Инвентарь/Магазин/Авторы

        # 2. Скрываем кнопку языка
        self.btn_language.pack_forget()

        # 3. Очищаем старые виджеты экрана авторов
        for widget in self.authors_frame.winfo_children():
            widget.destroy()

        # 4. Рисуем интерфейс авторов
        tk.Label(self.authors_frame, text=tr["btn_authors"], font=("Arial", 16, "bold")).pack(pady=20)

        authors_text = (
            "🎮 Authors:\n\n"
            "• thekosmoss\n"
            "• artman\n"
            "• Kirill\n\n"
            "🔧 Project: Clicker Basketball\n"
            "📅 2025 GlitchHunters Team"
        )

        tk.Label(
            self.authors_frame,
            text=authors_text,
            font=("Arial", 11),
            justify="center",
            fg="black"
        ).pack(pady=10)

        # 5. Показываем фрейм авторов
        self.authors_frame.pack(fill=tk.BOTH, expand=True)

        # 6. Настраиваем кнопку "Назад" для закрытия экрана авторов
        self.btn_back.config(command=self.close_authors, text=tr["back"])
        self.btn_back.pack(fill=tk.BOTH, expand=True)

    def close_authors(self):
        """Закрывает экран 'Авторы' и возвращает интерфейс игры"""
        # 1. Скрываем экран авторов
        self.authors_frame.pack_forget()

        # 2. Возвращаем игру
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        # 3. Возвращаем правую панель
        self.right_frame.grid()

        # 4. Скрываем кнопку "Назад"
        self.btn_back.pack_forget()

        # 5. Возвращаем кнопку языка
        self.btn_language.pack(fill=tk.BOTH, expand=True)

        # 6. Возвращаем команду кнопки "Назад" к инвентарю (по умолчанию)
        tr = self.translations[self.current_lang]
        self.btn_back.config(command=self.close_inventory, text=tr["back"])

    def update_potion_image(self):
        """Обновляет изображение зелья в зависимости от статуса"""
        # Проверяем, создан ли вообще label и загружены ли картинки
        if not hasattr(self, 'image_label') or self.image_label is None:
            return

        if not self.photo or not self.empty_photo:
            # Если картинки не загрузились, ничего не меняем
            return

        try:
            is_active = self.game.is_potion_active()
            new_img = self.empty_photo if is_active else self.photo

            # Применяем новое изображение
            self.image_label.config(image=new_img)
            self.image_label.image = new_img  # 🔑 ВАЖНО: держим ссылку для GC
        except Exception as e:
            print(f"Ошибка обновления картинки: {e}")