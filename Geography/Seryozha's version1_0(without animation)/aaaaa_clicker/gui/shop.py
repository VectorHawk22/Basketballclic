import tkinter as tk


class ShopManager:
    def __init__(self, parent, translations, current_lang):
        self.parent = parent
        self.translations = translations
        self.current_lang = current_lang
        self.tr = self.translations[self.current_lang]

        # Фрейм магазина
        self.shop_frame = tk.Frame(parent.left_frame)

        # Сохраняем состояние видимости кнопок
        self.buttons_visible = True

    def open(self):
        """Открывает магазин — скрывает ВСЕ кроме кнопки 'Назад'"""


        # 1. Скрываем основной игровой фрейм
        self.parent.game_frame.pack_forget()

        # 2. Скрываем ПРАВУЮ ПАНЕЛЬ полностью (вместе со всеми кнопками внутри)
        self.parent.right_frame.grid_remove()

        # 3. Скрываем НИЖНЮЮ панель с кнопкой языка
        self.parent.btn_language.pack_forget()

        # 4. Очищаем магазин от предыдущего содержимого
        for widget in self.shop_frame.winfo_children():
            widget.destroy()

        # 5. Создаем интерфейс магазина
        tk.Label(
            self.shop_frame,
            text=self.tr["btn_shop"],
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Label(
            self.shop_frame,
            text="🏪 Магазин временно закрыт",
            font=("Arial", 12),
            fg="gray"
        ).pack(pady=10)

        # 6. Показываем магазин
        self.shop_frame.pack(fill=tk.BOTH, expand=True)

        # 7. Показываем ТОЛЬКО кнопку "Назад"
        self.parent.btn_back.pack(fill=tk.BOTH, expand=True)

        # 8. Обновляем окно, чтобы изменения применились
        self.parent.update_idletasks()

    def close(self):
        """Закрывает магазин и возвращает всё обратно"""

        # 1. Скрываем магазин
        self.shop_frame.pack_forget()

        # 2. Скрываем кнопку "Назад"
        self.parent.btn_back.pack_forget()

        # 3. Возвращаем игровой фрейм
        self.parent.game_frame.pack(fill=tk.BOTH, expand=True)

        # 4. Возвращаем правую панель с кнопками
        self.parent.right_frame.grid()

        # 5. Возвращаем кнопку языка
        self.parent.btn_language.pack(fill=tk.BOTH, expand=True)

        # 6. Обновляем UI
        self.parent.update_ui()
        self.parent.update_idletasks()