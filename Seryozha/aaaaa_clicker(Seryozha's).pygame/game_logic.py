import json
import os
import hashlib
from datetime import datetime, timedelta
import random

_SECRET = "bK7x2mP9qL4wR8jN"


class ClickerGame:
    def __init__(self):
        self.points = 0
        self.potion_active = False
        self.potion_end_time = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_file = os.path.join(self.base_dir, "save.json")
        self.hash_file = os.path.join(self.base_dir, "save1.json")
        self.load_game()

    def try_add_point(self, clicks):
        """Попытка добавить очко на основе количества кликов"""
        if clicks == 0:
            return False, 0.0

        base_chance = 0.3
        luck_factor = min(clicks * 0.05, 0.7)
        total_chance = min(base_chance + luck_factor, 0.95)
        success = random.random() < total_chance

        if success:
            points_to_add = 2 if self.is_potion_active() else 1
            self.points += points_to_add
            self.save_game()

        return success, total_chance

    def get_points(self):
        return self.points

    def is_potion_active(self):
        if self.potion_active and self.potion_end_time:
            try:
                end_time = datetime.fromisoformat(self.potion_end_time)
                if datetime.now() < end_time:
                    return True
                else:
                    self.potion_active = False
                    self.potion_end_time = None
                    self.save_game()
            except (ValueError, TypeError):
                self.potion_active = False
                self.potion_end_time = None
        return False

    def activate_potion(self):
        if not self.is_potion_active():
            end_time = datetime.now() + timedelta(minutes=10)
            self.potion_active = True
            self.potion_end_time = end_time.isoformat()
            self.save_game()
            return True
        return False

    def get_potion_time_left(self):
        if not self.is_potion_active():
            return 0
        try:
            end_time = datetime.fromisoformat(self.potion_end_time)
            left = (end_time - datetime.now()).total_seconds()
            return max(0, int(left))
        except (ValueError, TypeError):
            return 0

    def _compute_hash(self, data):
        raw = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256((_SECRET + raw).encode("utf-8")).hexdigest()

    def save_game(self):
        try:
            data = {
                "points": self.points,
                "potion_active": self.potion_active,
                "potion_end_time": self.potion_end_time
            }
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            h = self._compute_hash(data)
            with open(self.hash_file, "w", encoding="utf-8") as f:
                json.dump({"hash": h}, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def _verify_hash(self, data):
        if not os.path.exists(self.hash_file):
            return False
        try:
            with open(self.hash_file, "r", encoding="utf-8") as f:
                stored = json.load(f)
            expected = self._compute_hash(data)
            return stored.get("hash") == expected
        except Exception:
            return False

    def load_game(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if self._verify_hash(data):
                    self.points = data.get("points", 0)
                    self.potion_active = data.get("potion_active", False)
                    self.potion_end_time = data.get("potion_end_time", None)
                else:
                    print("Обнаружена модификация save.json! Прогресс сброшен.")
                    self.points = 0
                    self.potion_active = False
                    self.potion_end_time = None
                    self.save_game()
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.points = 0
                self.potion_active = False
                self.potion_end_time = None
        else:
            print("Новый прогресс (файл сохранения не найден)")
            self.save_game()

    def reset_progress(self):
        """Сброс прогресса"""
        self.points = 0
        self.potion_active = False
        self.potion_end_time = None
        self.save_game()