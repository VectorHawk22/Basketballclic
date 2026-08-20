import json
import os
from datetime import datetime, timedelta

class ClickerGame:
    def __init__(self):
        self.points = 0
        self.potion_active = False
        self.potion_end_time = None  # timestamp в формате ISO
        self.load_game()

    def try_add_point(self, clicks):
        base_chance = 0.3
        luck_factor = min(clicks * 0.05, 0.7)
        total_chance = base_chance + luck_factor
        import random
        success = random.random() < total_chance
        if success:
            # Если зелье активно — +2 очка, иначе +1
            points_to_add = 2 if self.is_potion_active() else 1
            self.points += points_to_add
        return success, total_chance

    def get_points(self):
        return self.points

    def is_potion_active(self):
        if self.potion_active and self.potion_end_time:
            end_time = datetime.fromisoformat(self.potion_end_time)
            if datetime.now() < end_time:
                return True
            else:
                self.potion_active = False
                self.potion_end_time = None
        return False

    def activate_potion(self):
        if not self.is_potion_active():
            end_time = datetime.now() + timedelta(minutes=10)
            self.potion_active = True
            self.potion_end_time = end_time.isoformat()
            return True
        return False

    def get_potion_time_left(self):
        if not self.is_potion_active():
            return 0
        end_time = datetime.fromisoformat(self.potion_end_time)
        left = (end_time - datetime.now()).total_seconds()
        return max(0, int(left))

    def save_game(self):
        data = {
            "points": self.points,
            "potion_active": self.potion_active,
            "potion_end_time": self.potion_end_time
        }
        with open("save.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_game(self):
        if os.path.exists("save.json"):
            try:
                with open("save.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.points = data.get("points", 0)
                    self.potion_active = data.get("potion_active", False)
                    self.potion_end_time = data.get("potion_end_time", None)
            except Exception as e:
                print("Ошибка загрузки:", e)
        else:
            print("Новый прогресс (файл сохранения не найден)")