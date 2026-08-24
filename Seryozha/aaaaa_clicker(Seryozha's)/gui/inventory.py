import tkinter as tk
import os
from PIL import Image, ImageTk


class InventoryManager:
    def __init__(self, parent, game, translations, current_lang):
        self.parent = parent
        self.game = game
        self.translations = translations
        self.current_lang = current_lang
        self.tr = self.translations[self.current_lang]

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Фрейм инвентаря
        self.inventory_frame = tk.Frame(parent.left_frame)

        # Атрибуты для зелья
        self.potion_frame = None
        self.potion_btn = None
        self.potion_timer_label = None
        self.photo = None
        self.empty_photo = None
        self.image_label = None
        self.update_id = None

    def open(self):
        """Открытие инвентаря"""
        self.tr = self.translations[self.current_lang]

        # Скрываем игровой экран
        self.parent.game_frame.pack_forget()
        self.parent.right_frame.grid_remove()

        # Очищаем фрейм
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        self.inventory_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(
            self.inventory_frame,
            text=self.tr["inventory"],
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # Фрейм зелья
        self.potion_frame = tk.Frame(
            self.inventory_frame,
            relief="ridge",
            bd=3,
            bg="lightyellow",
            highlightbackground="gold",
            highlightthickness=2,
            width=250,
            height=170
        )
        self.potion_frame.pack(pady=20, padx=(20, 10), anchor="w")
        self.potion_frame.pack_propagate(False)

        # Верхняя часть с изображением
        top_frame = tk.Frame(self.potion_frame, bg="lightyellow")
        top_frame.place(x=10, y=10, width=230, height=100)

        # Контейнер для изображения
        image_frame = tk.Frame(top_frame, bg="lightyellow", width=80, height=80)
        image_frame.pack(side=tk.LEFT, padx=(0, 10))
        image_frame.pack_propagate(False)

        # Загрузка изображений из папки images
        self.load_images()

        # Отображение зелья
        is_active = self.game.is_potion_active()
        current_img = self.empty_photo if is_active else self.photo

        if current_img:
            self.image_label = tk.Label(
                image_frame,
                image=current_img,
                bg="lightyellow"
            )
            self.image_label.image = current_img
        else:
            self.image_label = tk.Label(
                image_frame,
                text="🧪",
                font=("Arial", 32),
                bg="lightyellow"
            )
        self.image_label.pack(expand=True)

        # Текстовая часть
        text_frame = tk.Frame(top_frame, bg="lightyellow")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            text_frame,
            text=self.tr["potion"],
            bg="lightyellow",
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))

        # Кнопка использования
        self.potion_btn = tk.Button(
            text_frame,
            font=("Arial", 9),
            width=14,
            command=self.use_potion
        )
        self.potion_btn.pack(anchor="w")

        # Таймер
        self.potion_timer_label = tk.Label(
            self.potion_frame,
            text="",
            bg="lightyellow",
            fg="black",
            font=("Arial", 9),
            anchor="w",
            justify="left"
        )
        self.potion_timer_label.place(x=10, y=115, width=230, height=45)

        # Обновление кнопки и таймера
        self.update_button()
        self.update_timer()

        # Показываем кнопку назад
        self.parent._show_back_button(self.close)

        # Запускаем обновление
        self.start_updates()

    def load_images(self):
        """Загрузка изображений зелья из папки images"""
        try:
            images_dir = os.path.join(self.base_dir, "images")

            full_path = os.path.join(images_dir, "potionthatgives2xcoins.png")
            empty_path = os.path.join(images_dir, "emptypotionthatgives2xcoins.png")

            if os.path.exists(full_path):
                img = Image.open(full_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
            else:
                print(f"⚠️ Файл не найден: {full_path}")

            if os.path.exists(empty_path):
                img = Image.open(empty_path).resize((80, 80), Image.Resampling.LANCZOS)
                self.empty_photo = ImageTk.PhotoImage(img)
            else:
                print(f"⚠️ Файл не найден: {empty_path}")

        except Exception as e:
            print(f"⚠️ Ошибка загрузки изображений зелья: {e}")

    def close(self):
        """Закрытие инвентаря"""
        self.stop_updates()
        self.inventory_frame.pack_forget()
        self.parent.game_frame.pack(fill=tk.BOTH, expand=True)
        self.parent.right_frame.grid()
        self.parent._hide_back_button()
        self.parent.update_ui()

    def use_potion(self):
        """Использование зелья"""
        if self.game.activate_potion():
            self.update_button()
            self.update_timer()
            self.update_image()
            self.parent.update_ui()
            self.parent.label_result.config(text="🧪 Эффект x2 активирован!", fg="green")

            # Визуальный эффект
            self.potion_frame.config(bg="lightgreen")
            self.potion_timer_label.config(bg="lightgreen")
            self.parent.root.after(3000, self._reset_colors)
        else:
            self.parent.label_result.config(text="⏳ Эффект уже активен!", fg="orange")

    def _reset_colors(self):
        """Сброс цветов после анимации"""
        if self.potion_frame:
            self.potion_frame.config(bg="lightyellow")
        if self.potion_timer_label:
            self.potion_timer_label.config(bg="lightyellow")

    def update_button(self):
        """Обновление состояния кнопки"""
        tr = self.translations[self.current_lang]
        is_active = self.game.is_potion_active()

        if self.potion_btn:
            if is_active:
                self.potion_btn.config(text=tr["use"], state="disabled")
            else:
                self.potion_btn.config(text=tr["potion_inactive"], state="normal")

    def update_timer(self):
        """Обновление таймера"""
        tr = self.translations[self.current_lang]
        time_left = self.game.get_potion_time_left()

        if self.potion_timer_label:
            if time_left > 0:
                self.potion_timer_label.config(
                    text=tr["potion_active"].format(time_left),
                    bg="lightgreen"
                )
            else:
                self.potion_timer_label.config(text="", bg="lightyellow")

    def update_image(self):
        """Обновление изображения зелья"""
        if not self.image_label:
            return

        is_active = self.game.is_potion_active()
        current_img = self.empty_photo if is_active else self.photo

        if current_img:
            self.image_label.config(image=current_img)
            self.image_label.image = current_img

    def start_updates(self):
        """Запуск периодического обновления"""
        self.update_timer()
        self.update_button()
        self.update_image()
        self.update_id = self.parent.root.after(1000, self.start_updates)

    def stop_updates(self):
        """Остановка обновления"""
        if self.update_id:
            try:
                self.parent.root.after_cancel(self.update_id)
            except:
                pass
            self.update_id = None

    def update_language(self, new_lang):
        """Обновление языка"""
        self.current_lang = new_lang
        self.tr = self.translations[self.current_lang]
        if hasattr(self, 'potion_btn') and self.potion_btn:
            self.update_button()