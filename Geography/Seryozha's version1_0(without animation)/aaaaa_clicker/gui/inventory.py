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

        # Скрываем основную игру и правую панель
        self.parent.game_frame.pack_forget()
        self.parent.right_frame.grid_remove()

        # Очищаем инвентарь перед перерисовкой
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        # Показываем инвентарь
        self.inventory_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(self.inventory_frame, text=tr["inventory"], font=("Arial", 16, "bold")).pack(pady=20)

        # === Слот для зелья ===
        # Важно: pack_propagate(False) запрещает фрейму менять размер под содержимое
        self.potion_frame = tk.Frame(
            self.inventory_frame,
            relief="ridge",
            bd=4,
            bg="lightyellow",
            highlightbackground="gold",
            highlightthickness=2,
            width=250,
            height=140
        )
        self.potion_frame.pack(pady=30, padx=(20, 10), anchor="w")
        self.potion_frame.pack_propagate(False)

        # Внутренний контейнер с отступами от рамки
        inner_frame = tk.Frame(self.potion_frame, bg="lightyellow")
        # Используем fill=BOTH, но без expand, чтобы не распирать фрейм насильно,
        # хотя при pack_propagate(False) это не критично
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Левая часть: Картинка ===
        image_frame = tk.Frame(inner_frame, bg="lightyellow", width=80, height=80)
        image_frame.pack(side=tk.LEFT, anchor="nw", padx=(0, 10))
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

            if os.path.exists(empty_path):
                img = Image.open(empty_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.empty_potion_image = ImageTk.PhotoImage(img)

        except Exception as e:
            print(f"❌ Ошибка загрузки изображений: {e}")

        # Определяем текущее изображение
        is_active = self.game.is_potion_active()
        start_img = self.empty_potion_image if is_active else self.photo

        if start_img:
            self.image_label = tk.Label(image_frame, image=start_img, bg="lightyellow")
            self.image_label.image = start_img
            self.image_label.pack(expand=True)  # Центрируем картинку в её квадрате
        else:
            self.image_label = tk.Label(image_frame, text="🧪", font=("Arial", 32), bg="lightyellow")
            self.image_label.pack(expand=True)

        # === Правая часть: Текст и кнопка ===
        text_frame = tk.Frame(inner_frame, bg="lightyellow")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Название зелья
        tk.Label(
            text_frame,
            text=tr["potion"],
            bg="lightyellow",
            font=("Arial", 10, "bold"),
            anchor="w",
            bd=0,  # Убираем рамку
            highlightthickness=0
        ).pack(fill=tk.X, pady=(0, 5))

        # Кнопка использования
        self.potion_btn = tk.Button(
            text_frame,
            text="",
            font=("Arial", 9),
            # width=18 можно убрать, если хотим адаптивности, но оставим для стабильности
            width=18,
            command=self.use_potion
        )
        self.potion_btn.pack(anchor="w", pady=(0, 5))

        # Таймер (ПРОБЛЕМА БЫЛА ЗДЕСЬ)
        # Добавляем height=2, чтобы зарезервировать место под 2 строки текста
        # bd=0 и highlightthickness=0 убирают лишние пиксели рамки
        self.potion_timer_label = tk.Label(
            self.potion_frame,  # Pack-аем прямо в potion_frame, чтобы быть внизу слота
            text="",
            bg="lightyellow",
            font=("Arial", 9),
            justify="left",
            anchor="w",
            height=2,  # <--- ФИКС: Фиксируем высоту в строках
            bd=0,  # <--- ФИКС: Убираем внутреннюю рамку
            highlightthickness=0  # <--- ФИКС: Убираем внешнюю рамку фокуса
        )
        # Размещаем таймер внизу основного фрейма зелья, а не во inner_frame
        # Это гарантирует, что он будет прижат к низу и не съедается padding'ом inner_frame
        self.potion_timer_label.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 5))

        # Обновляем состояние
        self.update_button()
        self.update_timer()

        # Управление кнопками навигации
        # Примечание: убедитесь, что в главном классе btn_back и btn_language управляются корректно
        if hasattr(self.parent, '_show_back_button'):
            self.parent._show_back_button(self.close)
        else:
            # Фоллбэк, если используется старая логика
            self.parent.btn_language.grid_remove()
            self.parent.btn_back.grid()  # Или pack, зависит от вашей реализации в main

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