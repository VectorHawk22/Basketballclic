import tkinter as tk
import os
from PIL import Image, ImageTk


class InventoryManager:
    def __init__(self, parent, game, translations, current_lang):
        self.parent = parent  # ClickerGUI
        self.game = game
        self.translations = translations
        self.current_lang = current_lang
        self.tr = self.translations[self.current_lang]

        # Фрейм инвентаря
        self.inventory_frame = tk.Frame(parent.left_frame)

        # Атрибуты для слота зелья
        self.potion_frame = None
        self.potion_btn = None
        self.potion_timer_label = None
        self.photo = None
        self.empty_potion_image = None
        self.image_label = None

    def open(self):
        """Открывает инвентарь"""
        tr = self.translations[self.current_lang]
        print("🔍 ОТКРЫВАЕМ ИНВЕНТАРЬ")

        self.parent.game_frame.pack_forget()
        self.parent.right_frame.grid_remove()

        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        self.inventory_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.inventory_frame, text=tr["inventory"], font=("Arial", 16, "bold")).pack(pady=20)

        # УВЕЛИЧИВАЕМ ФРЕЙМ
        self.potion_frame = tk.Frame(
            self.inventory_frame,
            relief="ridge",
            bd=4,
            bg="lightyellow",
            highlightbackground="gold",
            highlightthickness=2,
            width=250,
            height=180  # МАКСИМАЛЬНАЯ ВЫСОТА
        )
        self.potion_frame.pack(pady=30, padx=(20, 10), anchor="w")
        self.potion_frame.pack_propagate(False)
        print(f"✅ potion_frame создан: height=180")

        # ВЕРХНЯЯ ЧАСТЬ
        top_frame = tk.Frame(self.potion_frame, bg="RED")  # КРАСНЫЙ для отладки
        top_frame.place(x=10, y=10, width=230, height=100)

        image_frame = tk.Frame(top_frame, bg="lightyellow", width=80, height=80)
        image_frame.pack(side=tk.LEFT, padx=(0, 10))
        image_frame.pack_propagate(False)

        # Загрузка изображений
        self.photo = None
        self.empty_potion_image = None

        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            full_path = os.path.join(base_dir, "images", "potionthatgives2xcoins.png")
            empty_path = os.path.join(base_dir, "images", "emptypotionthatgives2xcoins.png")

            if os.path.exists(full_path):
                img = Image.open(full_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                print("✅ Загружена полная бутылка")

            if os.path.exists(empty_path):
                img = Image.open(empty_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.empty_potion_image = ImageTk.PhotoImage(img)
                print("✅ Загружена пустая бутылка")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

        is_active = self.game.is_potion_active()
        start_img = self.empty_potion_image if is_active else self.photo

        if start_img:
            self.image_label = tk.Label(image_frame, image=start_img, bg="lightyellow")
            self.image_label.image = start_img
            self.image_label.pack(expand=True)
        else:
            self.image_label = tk.Label(image_frame, text="🧪", font=("Arial", 32), bg="lightyellow")
            self.image_label.pack(expand=True)

        text_frame = tk.Frame(top_frame, bg="lightyellow")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            text_frame,
            text=tr["potion"],
            bg="lightyellow",
            fg="BLACK",  # ЧЁРНЫЙ ТЕКСТ
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))

        self.potion_btn = tk.Button(
            text_frame,
            text="",
            font=("Arial", 9),
            width=14,
            command=self.use_potion
        )
        self.potion_btn.pack(anchor="w")

        # === ТАЙМЕР - СОЗДАЕМ ЗАНОВО КАЖДЫЙ РАЗ ===
        # УНИЧТОЖАЕМ СТАРЫЙ ЕСЛИ ЕСТЬ
        if hasattr(self, 'potion_timer_label') and self.potion_timer_label is not None:
            try:
                self.potion_timer_label.destroy()
                print("🗑️ Уничтожен старый таймер")
            except:
                pass

        # СОЗДАЕМ НОВЫЙ
        self.potion_timer_label = tk.Label(
            self.potion_frame,
            text="ТЕСТ ТАЙМЕРА",  # ЯВНЫЙ ТЕКСТ для проверки
            bg="CYAN",  # ГОЛУБОЙ ФОН для видимости
            fg="BLACK",
            font=("Arial", 10, "bold"),
            anchor="w",
            justify="left",
            relief="solid",  # РАМКА для видимости
            bd=1
        )
        self.potion_timer_label.place(x=10, y=120, width=230, height=50)
        print("✅ Создан НОВЫЙ таймер с текстом 'ТЕСТ ТАЙМЕРА'")

        self.update_button()
        self.update_timer()

        if hasattr(self.parent, '_show_back_button'):
            self.parent._show_back_button(self.close)
        else:
            self.parent.btn_language.grid_remove()
            self.parent.btn_back.grid()
    def close(self):
        """Закрывает инвентарь"""
        self.inventory_frame.pack_forget()
        self.parent.game_frame.pack(fill=tk.BOTH, expand=True)
        self.parent.right_frame.grid()

        if hasattr(self.parent, '_hide_back_button'):
            self.parent._hide_back_button()
        else:
            self.parent.btn_back.grid_remove()
            self.parent.btn_language.grid()

        self.parent.update_ui()

    def use_potion(self):
        if self.game.activate_potion():
            self.update_button()
            self.update_timer()
            self.parent.update_ui()
            self.parent.label_result.config(text="🧪 Эффект x2 активирован!", fg="green")

            # Мигание рамки
            self.potion_frame.config(bg="lightgreen")
            # Меняем цвет фона таймера тоже, чтобы не было контрастного белого пятна
            self.potion_timer_label.config(bg="lightgreen")

            self.parent.root.after(3000, lambda: self._reset_potion_visuals())
        else:
            self.parent.label_result.config(text="⏳ Эффект уже активен!", fg="orange")

    def _reset_potion_visuals(self):
        """Возвращает цвета после анимации"""
        if self.potion_frame:
            self.potion_frame.config(bg="lightyellow")
        if self.potion_timer_label:
            self.potion_timer_label.config(bg="lightyellow")

    def update_button(self):
        tr = self.translations[self.current_lang]
        is_active = self.game.is_potion_active()

        if self.potion_btn:
            if is_active:
                self.potion_btn.config(text=tr["use"], state="disabled")
            else:
                self.potion_btn.config(text=tr["potion_inactive"], state="normal")

        if self.image_label:
            new_img = self.empty_potion_image if is_active else self.photo
            if new_img:
                self.image_label.config(image=new_img)
                self.image_label.image = new_img
            else:
                self.image_label.config(text="🧪" if is_active else "", image="")

    def update_timer(self):
        tr = self.translations[self.current_lang]
        time_left = self.game.get_potion_time_left()
        if self.potion_timer_label:
            if time_left > 0:
                # Форматируем текст, чтобы он точно влезал
                timer_text = tr["potion_active"].format(time_left)
                self.potion_timer_label.config(text=timer_text)
            else:
                # Важно оставлять пробел или пустую строку, но высота фиксирована
                self.potion_timer_label.config(text="")