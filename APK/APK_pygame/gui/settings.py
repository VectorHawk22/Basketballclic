# settings.py
import pygame
import json
import os
from pygame.locals import *


class Settings:
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app
        self.running = False
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.LIGHT_GREEN = (144, 238, 144)
        self.LIGHT_CORAL = (240, 128, 128)
        self.BLUE = (70, 130, 180)
        
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
        # Доступные языки (из главного окна)
        available_langs = list(self.app.translations.keys())
        current_lang_index = available_langs.index(self.settings.get("language", "Русский")) if self.settings.get("language", "Русский") in available_langs else 0
        
        # Создаем кнопки и элементы UI
        self.ui_elements = {
            "buttons": [],
            "checkboxes": [],
            "dropdown": {
                "options": available_langs,
                "current_index": current_lang_index,
                "rect": pygame.Rect(0, 0, 150, 35),
                "expanded": False
            }
        }
        
        # Заголовок
        self.title_rect = pygame.Rect(0, 30, self.screen.get_width(), 50)
        
        # Язык
        self.lang_label_rect = pygame.Rect(40, 110, 100, 30)
        self.lang_dropdown_rect = pygame.Rect(180, 110, 150, 35)
        self.ui_elements["dropdown"]["rect"] = self.lang_dropdown_rect
        
        # Звук
        self.sound_label_rect = pygame.Rect(40, 170, 100, 30)
        self.sound_check_rect = pygame.Rect(180, 170, 150, 30)
        self.sound_text = "Включён" if self.settings.get("sound", True) else "Выключен"
        
        # Кнопка сохранения
        self.save_btn_rect = pygame.Rect(40, 250, 300, 50)
        
        # Кнопка сброса
        self.reset_btn_rect = pygame.Rect(40, 320, 300, 50)
        
        # Кнопка назад/закрыть (крестик)
        self.close_btn_rect = pygame.Rect(self.screen.get_width() - 50, 10, 40, 40)

    def draw_dropdown(self):
        """Отрисовка выпадающего списка"""
        dropdown = self.ui_elements["dropdown"]
        rect = dropdown["rect"]
        
        # Основная кнопка
        pygame.draw.rect(self.screen, self.WHITE, rect, border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, rect, 2, border_radius=5)
        
        # Текущий выбранный язык
        font = pygame.font.Font(None, 28)
        text = font.render(dropdown["options"][dropdown["current_index"]], True, self.BLACK)
        text_rect = text.get_rect(midleft=(rect.x + 10, rect.centery))
        self.screen.blit(text, text_rect)
        
        # Стрелка вниз
        arrow_points = [
            (rect.right - 20, rect.centery - 5),
            (rect.right - 10, rect.centery - 5),
            (rect.right - 15, rect.centery + 5)
        ]
        pygame.draw.polygon(self.screen, self.BLACK, arrow_points)
        
        # Если раскрыт, показываем варианты
        if dropdown["expanded"]:
            y_offset = rect.height
            for i, option in enumerate(dropdown["options"]):
                option_rect = pygame.Rect(rect.x, rect.y + y_offset, rect.width, rect.height)
                
                # Подсветка при наведении
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, self.BLUE, option_rect, border_radius=3)
                else:
                    pygame.draw.rect(self.screen, self.WHITE, option_rect, border_radius=3)
                pygame.draw.rect(self.screen, self.BLACK, option_rect, 1, border_radius=3)
                
                text = font.render(option, True, self.BLACK)
                text_rect = text.get_rect(midleft=(option_rect.x + 10, option_rect.centery))
                self.screen.blit(text, text_rect)
                
                y_offset += rect.height

    def handle_events(self, events):
        """Обработка событий"""
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Проверка клика по кнопке закрытия
                if self.close_btn_rect.collidepoint(mouse_pos):
                    self.close_settings()
                    return
                
                # Проверка клика по выпадающему списку
                if self.lang_dropdown_rect.collidepoint(mouse_pos):
                    self.ui_elements["dropdown"]["expanded"] = not self.ui_elements["dropdown"]["expanded"]
                    return
                
                # Проверка клика по пунктам выпадающего списка
                if self.ui_elements["dropdown"]["expanded"]:
                    dropdown = self.ui_elements["dropdown"]
                    y_offset = dropdown["rect"].height
                    for i in range(len(dropdown["options"])):
                        option_rect = pygame.Rect(
                            dropdown["rect"].x,
                            dropdown["rect"].y + y_offset,
                            dropdown["rect"].width,
                            dropdown["rect"].height
                        )
                        if option_rect.collidepoint(mouse_pos):
                            dropdown["current_index"] = i
                            dropdown["expanded"] = False
                            self.settings["language"] = dropdown["options"][i]
                            self.app.set_language(self.settings["language"])
                            self.save_settings()
                            return
                        y_offset += dropdown["rect"].height
                
                # Проверка клика по чекбоксу звука
                if self.sound_check_rect.collidepoint(mouse_pos):
                    self.settings["sound"] = not self.settings["sound"]
                    self.sound_text = "Включён" if self.settings["sound"] else "Выключен"
                    self.save_settings()
                    # Обновляем звук в главном приложении
                    if hasattr(self.app, 'toggle_sound'):
                        self.app.toggle_sound()
                    return
                
                # Проверка клика по кнопке сохранения
                if self.save_btn_rect.collidepoint(mouse_pos):
                    self.save_and_close()
                    return
                
                # Проверка клика по кнопке сброса
                if self.reset_btn_rect.collidepoint(mouse_pos):
                    self.reset_progress()
                    return
                
                # Если клик вне выпадающего списка - закрываем его
                if self.ui_elements["dropdown"]["expanded"]:
                    dropdown = self.ui_elements["dropdown"]
                    expanded_rect = pygame.Rect(
                        dropdown["rect"].x,
                        dropdown["rect"].y,
                        dropdown["rect"].width,
                        dropdown["rect"].height * len(dropdown["options"])
                    )
                    if not expanded_rect.collidepoint(mouse_pos):
                        dropdown["expanded"] = False

    def render(self):
        """Отрисовка окна настроек"""
        # Фон
        self.screen.fill((240, 240, 240))
        
        font_title = pygame.font.Font(None, 48)
        font_label = pygame.font.Font(None, 32)
        font_button = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 28)
        
        # Заголовок
        title = font_title.render("⚙️ Настройки", True, self.BLACK)
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 55))
        self.screen.blit(title, title_rect)
        
        # Язык
        lang_label = font_label.render("🌐 Язык:", True, self.BLACK)
        self.screen.blit(lang_label, (self.lang_label_rect.x, self.lang_label_rect.y))
        
        # Выпадающий список
        self.draw_dropdown()
        
        # Звук
        sound_label = font_label.render("🔊 Звук:", True, self.BLACK)
        self.screen.blit(sound_label, (self.sound_label_rect.x, self.sound_label_rect.y))
        
        # Чекбокс звука
        checkbox_rect = pygame.Rect(self.sound_check_rect.x, self.sound_check_rect.y, 25, 25)
        pygame.draw.rect(self.screen, self.WHITE, checkbox_rect, border_radius=3)
        pygame.draw.rect(self.screen, self.BLACK, checkbox_rect, 2, border_radius=3)
        
        if self.settings["sound"]:
            # Галочка
            pygame.draw.line(self.screen, self.BLACK, 
                           (checkbox_rect.x + 5, checkbox_rect.centery),
                           (checkbox_rect.x + 10, checkbox_rect.bottom - 5), 3)
            pygame.draw.line(self.screen, self.BLACK,
                           (checkbox_rect.x + 10, checkbox_rect.bottom - 5),
                           (checkbox_rect.right - 5, checkbox_rect.y + 5), 3)
        
        sound_text = font_small.render(self.sound_text, True, self.BLACK)
        self.screen.blit(sound_text, (self.sound_check_rect.x + 35, self.sound_check_rect.y))
        
        # Кнопка сохранения
        pygame.draw.rect(self.screen, self.LIGHT_GREEN, self.save_btn_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, self.save_btn_rect, 2, border_radius=10)
        save_text = font_button.render("💾 Сохранить настройки", True, self.BLACK)
        save_rect = save_text.get_rect(center=self.save_btn_rect.center)
        self.screen.blit(save_text, save_rect)
        
        # Кнопка сброса
        pygame.draw.rect(self.screen, self.LIGHT_CORAL, self.reset_btn_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, self.reset_btn_rect, 2, border_radius=10)
        reset_text = font_button.render("🗑️ Сбросить прогресс", True, self.BLACK)
        reset_rect = reset_text.get_rect(center=self.reset_btn_rect.center)
        self.screen.blit(reset_text, reset_rect)
        
        # Кнопка закрытия (крестик)
        pygame.draw.rect(self.screen, (255, 100, 100), self.close_btn_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, self.close_btn_rect, 2, border_radius=5)
        close_text = font_small.render("✕", True, self.BLACK)
        close_rect = close_text.get_rect(center=self.close_btn_rect.center)
        self.screen.blit(close_text, close_rect)

    def save_and_close(self):
        """Сохранение и закрытие настроек"""
        if self.save_settings():
            print("Настройки сохранены!")
            self.close_settings()
        else:
            print("Ошибка сохранения настроек!")

    def close_settings(self):
        """Закрытие окна настроек"""
        self.running = False
        if self.app:
            self.app.settings_open = False

    def reset_progress(self):
        """Сброс прогресса игры"""
        # Диалог подтверждения (упрощенный вариант)
        if self.app.game:
            self.app.game.reset_progress()
            self.app.update_ui()
            print("Прогресс успешно сброшен!")

    def run(self):
        """Запуск окна настроек"""
        self.running = True
        clock = pygame.time.Clock()
        
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    self.running = False
                    return
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.close_settings()
                        return
            
            self.handle_events(events)
            self.render()
            pygame.display.flip()
            clock.tick(60)