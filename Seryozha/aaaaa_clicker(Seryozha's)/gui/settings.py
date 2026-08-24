import tkinter as tk
from tkinter import messagebox
import json
import os


class Settings:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.settings_file = os.path.join(self.base_dir, "settings.json")

        self.settings = self.load_settings()
        self.build_ui()

    def load_settings(self):
        """Загрузка настроек из файла, создаёт файл если его нет"""
        default_settings = {
            "sound": True,
            "language": "Русский"
        }

        if not os.path.exists(self.settings_file):
            # Создаём файл с настройками по умолчанию
            try:
                with open(self.settings_file, "w", encoding="utf-8") as file:
                    json.dump(default_settings, file, ensure_ascii=False, indent=4)
                print("✅ Создан файл настроек settings.json")
            except Exception as e:
                print(f"⚠️ Не удалось создать settings.json: {e}")
            return default_settings

        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            default_settings.update(data)
            return default_settings
        except (json.JSONDecodeError, OSError) as e:
            print(f"⚠️ Ошибка загрузки настроек: {e}")
            return default_settings

    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as file:
                json.dump(self.settings, file, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            print(f"⚠️ Ошибка сохранения настроек: {e}")
            return False

    def get_language(self):
        """Получение текущего языка"""
        return self.settings.get("language", "Русский")

    def get_sound(self):
        """Получение состояния звука"""
        return self.settings.get("sound", True)

    def build_ui(self):
        """Построение интерфейса настроек"""
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Заголовок
        title = tk.Label(
            self.parent,
            text="⚙️ Настройки",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(25, 20))

        # Язык
        language_frame = tk.Frame(self.parent)
        language_frame.pack(fill=tk.X, padx=40, pady=10)

        tk.Label(
            language_frame,
            text="🌐 Язык:",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)

        self.language_var = tk.StringVar(value=self.settings.get("language", "Русский"))

        # Доступные языки (из главного окна)
        available_langs = list(self.app.translations.keys())

        self.language_menu = tk.OptionMenu(
            language_frame,
            self.language_var,
            *available_langs,
            command=self.on_language_change
        )
        self.language_menu.config(width=15, font=("Arial", 10))
        self.language_menu.pack(side=tk.RIGHT)

        # Звук
        sound_frame = tk.Frame(self.parent)
        sound_frame.pack(fill=tk.X, padx=40, pady=10)

        tk.Label(
            sound_frame,
            text="🔊 Звук:",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)

        self.sound_var = tk.BooleanVar(value=self.settings.get("sound", True))

        self.sound_check = tk.Checkbutton(
            sound_frame,
            text="Включён",
            variable=self.sound_var,
            command=self.on_sound_toggle,
            font=("Arial", 10)
        )
        self.sound_check.pack(side=tk.RIGHT)

        # Кнопка сохранения
        save_button = tk.Button(
            self.parent,
            text="💾 Сохранить настройки",
            font=("Arial", 11, "bold"),
            bg="lightgreen",
            command=self.save_and_close
        )
        save_button.pack(fill=tk.X, padx=40, pady=(25, 8))

        # Кнопка сброса
        reset_button = tk.Button(
            self.parent,
            text="🗑️ Сбросить прогресс",
            font=("Arial", 11, "bold"),
            bg="lightcoral",
            command=self.reset_progress
        )
        reset_button.pack(fill=tk.X, padx=40, pady=8)

    def on_language_change(self, language):
        """Обработка смены языка"""
        self.settings["language"] = language
        self.app.set_language(language)
        self.save_settings()

    def on_sound_toggle(self):
        """Обработка переключения звука"""
        self.settings["sound"] = self.sound_var.get()
        self.save_settings()

    def save_and_close(self):
        """Сохранение и закрытие настроек"""
        self.settings["sound"] = self.sound_var.get()
        self.settings["language"] = self.language_var.get()

        if self.save_settings():
            messagebox.showinfo("Успех", "Настройки сохранены!")
            self.app.close_settings()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить настройки!")

    def reset_progress(self):
        """Сброс прогресса игры"""
        answer = messagebox.askyesno(
            "Сброс прогресса",
            "Вы уверены, что хотите удалить весь прогресс?\n\n"
            "Это действие нельзя отменить!"
        )

        if not answer:
            return

        try:
            self.app.game.reset_progress()
            self.app.update_ui()
            messagebox.showinfo("Готово", "Прогресс успешно сброшен!")
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось сбросить прогресс:\n{e}"
            )