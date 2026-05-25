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
        self.photo = None  # Для хранения изображения

    def open(self):
        """Открывает инвентарь"""
        tr = self.translations[self.current_lang]
        # Скрываем основную игру
        self.parent.game_frame.pack_forget()
        # Скрываем правую панель
        self.parent.right_frame.grid_remove()
        # Показываем инвентарь
        self.inventory_frame.pack(fill=tk.BOTH, expand=True)

        # Очищаем
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        # Заголовок
        tk.Label(self.inventory_frame, text=tr["inventory"], font=("Arial", 16, "bold")).pack(pady=20)

        # === Слот для зелья ===
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

        inner_frame = tk.Frame(self.potion_frame, bg="lightyellow")
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Картинка ===
        image_frame = tk.Frame(inner_frame, bg="lightyellow", width=100, height=100)
        image_frame.pack(side=tk.LEFT, anchor="w", padx=(0, 10))
        image_frame.pack_propagate(False)

        # === Загрузка изображений ===
        self.photo = None
        self.empty_potion_image = None

        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            full_path = os.path.join(base_dir, "images", "potionthatgives2xcoins.png")
            empty_path = os.path.join(base_dir, "images", "emptypotionthatgives2xcoins.png")

            # Полная бутылка
            if os.path.exists(full_path):
                img = Image.open(full_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                print("✅ Загружена полная бутылка")
            else:
                print(f"⚠️ Нет файла полной бутылки: {full_path}")

            # Пустая бутылка
            if os.path.exists(empty_path):
                img = Image.open(empty_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.empty_potion_image = ImageTk.PhotoImage(img)
                print("✅ Загружена пустая бутылка")
            else:
                print(f"⚠️ Нет файла пустой бутылки: {empty_path}")

        except Exception as e:
            print(f"❌ Ошибка загрузки изображений: {e}")

        # Определяем стартовое изображение
        start_img = self.empty_potion_image if self.game.is_potion_active() else self.photo
        fallback_text = "" if start_img is None else None

        if start_img:
            self.image_label = tk.Label(image_frame, image=start_img, bg="lightyellow")
            self.image_label.image = start_img  # Критически важно для Tkinter
            self.image_label.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            self.image_label = tk.Label(image_frame, text=fallback_text, font=("Arial", 32), bg="lightyellow")
            self.image_label.pack(side=tk.LEFT, padx=5, pady=5)
        # === Текст и кнопка ===
        text_frame = tk.Frame(inner_frame, bg="lightyellow")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            text_frame,
            text=tr["potion"],
            bg="lightyellow",
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))

        self.potion_btn = tk.Button(
            text_frame,
            text="",
            font=("Arial", 9),
            width=18,
            command=self.use_potion
        )
        self.potion_btn.pack(anchor="w")

        # Таймер
        self.potion_timer_label = tk.Label(
            self.potion_frame,
            text="",
            bg="lightyellow",
            font=("Arial", 9)
        )
        self.potion_timer_label.pack(pady=(5, 0), anchor="w", padx=15)

        # Обновляем состояние
        self.update_button()
        self.update_timer()

        # Переключаем кнопку внизу
        self.parent.btn_language.pack_forget()
        self.parent.btn_back.pack(fill=tk.BOTH, expand=True)
        self.update_button()
    def close(self):
        """Закрывает инвентарь"""
        self.inventory_frame.pack_forget()
        self.parent.game_frame.pack(fill=tk.BOTH, expand=True)
        self.parent.right_frame.grid()
        self.parent.btn_back.pack_forget()
        self.parent.btn_language.pack(fill=tk.BOTH, expand=True)
        self.parent.update_ui()

    def use_potion(self):
        if self.game.activate_potion():
            # Сначала обновляем состояние UI (кнопка + изображение)
            self.update_button()
            self.update_timer()

            # Визуальная обратная связь
            self.parent.update_ui()
            self.parent.label_result.config(text=" Эффект x2 активирован!", fg="green")

            # Мигание рамки
            self.potion_frame.config(bg="lightgreen")
            self.parent.root.after(3000, lambda: self.potion_frame.config(bg="lightyellow"))

            print("🔄 Состояние обновлено. Изображение должно смениться автоматически.")
        else:
            self.parent.label_result.config(text="⏳ Эффект уже активен!", fg="orange")
    def update_button(self):
        tr = self.translations[self.current_lang]
        is_active = self.game.is_potion_active()

        # 1. Обновляем кнопку
        if self.potion_btn:
            if is_active:
                self.potion_btn.config(text=tr["use"], state="disabled")
            else:
                self.potion_btn.config(text=tr["potion_inactive"], state="normal")

        # 2. Обновляем изображение (только если метка существует)
        if self.image_label:
            new_img = self.empty_potion_image if is_active else self.photo

            if new_img:
                self.image_label.config(image=new_img)
                self.image_label.image = new_img  # Держим ссылку, иначе GC удалит картинку
            else:
                # Если нужное изображение не загрузилось, ставим эмодзи
                self.image_label.config(text="🧪" if is_active else "⬜", image="")
                self.image_label.image = None
    def update_timer(self):
        tr = self.translations[self.current_lang]
        time_left = self.game.get_potion_time_left()
        if self.potion_timer_label:
            if time_left > 0:
                self.potion_timer_label.config(text=tr["potion_active"].format(time_left))
            else:
                self.potion_timer_label.config(text="")