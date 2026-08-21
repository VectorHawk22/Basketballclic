import json
import os
import pygame

class Settings:
    def __init__(self, app):
        self.app = app
        self.settings_file = "settings.json"
        self.settings = self.load_settings()
        self.language = self.settings.get("language", "Русский")
        self.sound = self.settings.get("sound", True)
        self.music_volume = self.settings.get("music_volume", 0.5)
        self.sfx_volume = self.settings.get("sfx_volume", 0.7)
        
    def load_settings(self):
        default_settings = {
            "sound": True,
            "language": "Русский",
            "music_volume": 0.5,
            "sfx_volume": 0.7
        }
        if not os.path.exists(self.settings_file):
            return default_settings
        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                default_settings.update(data)
                return default_settings
        except:
            return default_settings

    def save_settings(self):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as file:
                json.dump(self.settings, file, ensure_ascii=False, indent=4)
        except:
            pass

    def change_language(self, language):
        self.settings["language"] = language
        self.language = language
        self.save_settings()

    def toggle_sound(self):
        self.settings["sound"] = not self.settings["sound"]
        self.sound = self.settings["sound"]
        self.save_settings()

    def set_music_volume(self, volume):
        self.settings["music_volume"] = max(0, min(1, volume))
        self.music_volume = self.settings["music_volume"]
        self.save_settings()
        
    def set_sfx_volume(self, volume):
        self.settings["sfx_volume"] = max(0, min(1, volume))
        self.sfx_volume = self.settings["sfx_volume"]
        self.save_settings()

    def reset_progress(self):
        self.app.game.points = 0
        self.app.game.save_game()