import tkinter as tk


class AuthorsManager:
    def __init__(self, parent, translations, current_lang):
        self.parent = parent
        self.translations = translations
        self.current_lang = current_lang
        self.tr = self.translations[self.current_lang]

        # Фрейм "Авторы"
        self.authors_frame = tk.Frame(parent.left_frame)

    def open(self):
        """Открывает экран 'Авторы'"""
        # Скрываем основную игру
        self.parent.game_frame.pack_forget()
        # Скрываем правую панель
        self.parent.right_frame.grid_remove()
        # Показываем экран авторов
        self.authors_frame.pack(fill=tk.BOTH, expand=True)

        # Очищаем
        for widget in self.authors_frame.winfo_children():
            widget.destroy()

        # Заголовок
        tk.Label(self.authors_frame, text=self.tr["btn_authors"], font=("Arial", 16, "bold")).pack(pady=20)

        # Информация об авторах
        authors_text = (
            "🎮 Разработчики:\n\n"
            "• Иван Петров — геймдизайн\n"
            "• Анна Сидорова — графика\n"
            "• Дмитрий Козлов — программирование\n\n"
            "🔧 Проект: Clicker Basketball\n"
            "📅 2025 © GlitchHunters"
        )

        tk.Label(
            self.authors_frame,
            text=authors_text,
            font=("Arial", 11),
            justify="center",
            fg="black"
        ).pack(pady=10)

        # Кнопка "Назад"
        self.parent.btn_language.pack_forget()
        self.parent.btn_back.pack(fill=tk.BOTH, expand=True)

    def close(self):
        """Закрывает экран 'Авторы'"""
        self.authors_frame.pack_forget()
        self.parent.game_frame.pack(fill=tk.BOTH, expand=True)
        self.parent.right_frame.grid()
        self.parent.btn_back.pack_forget()
        self.parent.btn_language.pack(fill=tk.BOTH, expand=True)
        self.parent.update_ui()