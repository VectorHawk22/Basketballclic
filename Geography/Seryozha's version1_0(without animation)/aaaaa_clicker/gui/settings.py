#Версия Сергея
import tkinter as tk
from tkinter import messagebox
import json
import os


class Settings:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.settings_file = os.path.join(
            self.app.base_dir,
            "settings.json"
        )

        self.settings = self.load_settings()

        self.build_ui()

    # ================= SETTINGS FILE =================

    def load_settings(self):
        default_settings = {
            "sound": True,
            "language": self.app.current_lang
        }

        if not os.path.exists(self.settings_file):
            return default_settings

        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            default_settings.update(data)
            return default_settings

        except (json.JSONDecodeError, OSError):
            return default_settings

    def save_settings(self):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as file:
                json.dump(
                    self.settings,
                    file,
                    ensure_ascii=False,
                    indent=4
                )
        except OSError as e:
            print(f"Ошибка сохранения настроек: {e}")

    # ================= UI =================

    def build_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.parent,
            text="Настройки",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(25, 20))

        # ---------- LANGUAGE ----------

        language_frame = tk.Frame(self.parent)
        language_frame.pack(fill=tk.X, padx=40, pady=10)

        tk.Label(
            language_frame,
            text="Язык:",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)

        self.language_var = tk.StringVar(
            value=self.settings.get(
                "language",
                self.app.current_lang
            )
        )

        self.language_menu = tk.OptionMenu(
            language_frame,
            self.language_var,
            *self.app.translations.keys(),
            command=self.change_language
        )

        self.language_menu.config(
            width=15,
            font=("Arial", 10)
        )

        self.language_menu.pack(side=tk.RIGHT)

        # ---------- SOUND ----------

        sound_frame = tk.Frame(self.parent)
        sound_frame.pack(fill=tk.X, padx=40, pady=10)

        tk.Label(
            sound_frame,
            text="Звук:",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)

        self.sound_var = tk.BooleanVar(
            value=self.settings.get("sound", True)
        )

        self.sound_check = tk.Checkbutton(
            sound_frame,
            text="Включён",
            variable=self.sound_var,
            command=self.toggle_sound,
            font=("Arial", 10)
        )

        self.sound_check.pack(side=tk.RIGHT)

        # ---------- SAVE ----------

        save_button = tk.Button(
            self.parent,
            text="💾 Сохранить настройки",
            font=("Arial", 11, "bold"),
            bg="lightgreen",
            command=self.save_and_close
        )

        save_button.pack(
            fill=tk.X,
            padx=40,
            pady=(25, 8)
        )

        # ---------- RESET ----------

        reset_button = tk.Button(
            self.parent,
            text="🗑️ Сбросить прогресс",
            font=("Arial", 11, "bold"),
            bg="lightcoral",
            command=self.reset_progress
        )

        reset_button.pack(
            fill=tk.X,
            padx=40,
            pady=8
        )

    # ================= ACTIONS =================

    def change_language(self, language):
        self.settings["language"] = language
        self.app.set_language(language)

    def toggle_sound(self):
        self.settings["sound"] = self.sound_var.get()

    def save_and_close(self):
        self.settings["sound"] = self.sound_var.get()
        self.settings["language"] = self.language_var.get()

        self.save_settings()

        messagebox.showinfo(
            "Настройки",
            "Настройки сохранены!"
        )

    def reset_progress(self):
        answer = messagebox.askyesno(
            "Сброс прогресса",
            "Вы уверены, что хотите удалить весь прогресс?"
        )

        if not answer:
            return

        try:
            self.app.game.points = 0

            if hasattr(self.app.game, "inventory"):
                self.app.game.inventory = {}

            self.app.game.save_game()
            self.app.update_ui()

            messagebox.showinfo(
                "Готово",
                "Прогресс успешно сброшен!"
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось сбросить прогресс:\n{e}"
            )