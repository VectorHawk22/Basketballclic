# main.py
import pygame
import json
import os
from datetime import datetime, timedelta
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана для мобильных устройств
INFO = pygame.display.Info()
WIDTH = min(INFO.current_w, 800)
HEIGHT = min(INFO.current_h, 600)
if WIDTH < 400 or HEIGHT < 400:
    WIDTH = 400
    HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Кликер")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 200, 255)
GOLD = (255, 215, 0)
PURPLE = (150, 0, 200)

# Шрифты
try:
    font_large = pygame.font.Font(None, int(WIDTH * 0.08))
    font_medium = pygame.font.Font(None, int(WIDTH * 0.06))
    font_small = pygame.font.Font(None, int(WIDTH * 0.05))
except:
    font_large = pygame.font.SysFont(None, int(WIDTH * 0.08))
    font_medium = pygame.font.SysFont(None, int(WIDTH * 0.06))
    font_small = pygame.font.SysFont(None, int(WIDTH * 0.05))


class ClickerGame:
    def __init__(self):
        self.points = 0
        self.potion_active = False
        self.potion_end_time = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_file = os.path.join(self.base_dir, "save.json")
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

    def save_game(self):
        try:
            data = {
                "points": self.points,
                "potion_active": self.potion_active,
                "potion_end_time": self.potion_end_time
            }
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_game(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.points = data.get("points", 0)
                    self.potion_active = data.get("potion_active", False)
                    self.potion_end_time = data.get("potion_end_time", None)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.points = 0
                self.potion_active = False
                self.potion_end_time = None
        else:
            print("Новый прогресс (файл сохранения не найден)")

    def reset_progress(self):
        """Сброс прогресса"""
        self.points = 0
        self.potion_active = False
        self.potion_end_time = None
        self.save_game()


class Button:
    def __init__(self, x, y, width, height, text, color, text_color=BLACK, border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.border_radius = border_radius
        self.is_pressed = False

    def draw(self, surface):
        # Рисуем кнопку с закругленными углами
        color = self.color
        if self.is_pressed:
            color = tuple(max(0, c - 40) for c in self.color)
        
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2, border_radius=self.border_radius)
        
        # Текст
        text_surf = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True
            self.is_pressed = False
        return False
    
    def handle_touch(self, pos, pressed):
        """Обработка касаний для мобильных устройств"""
        if pressed and self.rect.collidepoint(pos):
            self.is_pressed = True
            return True
        elif not pressed:
            if self.is_pressed and self.rect.collidepoint(pos):
                self.is_pressed = False
                return True
            self.is_pressed = False
        return False


class ClickerApp:
    def __init__(self):
        self.game = ClickerGame()
        self.clicks = 0
        self.click_timer = 0
        self.show_message = ""
        self.message_timer = 0
        self.last_click_time = 0
        self.click_cooldown = 0.1  # 100ms между кликами
        
        # Создаем кнопки
        self.create_buttons()
        
        # Для анимации клика
        self.click_animation = []
        self.animation_timer = 0

    def create_buttons(self):
        button_width = int(WIDTH * 0.35)
        button_height = int(HEIGHT * 0.08)
        spacing = int(HEIGHT * 0.02)
        
        # Большая кнопка клика
        click_size = int(min(WIDTH * 0.4, HEIGHT * 0.25))
        self.click_button = Button(
            WIDTH // 2 - click_size // 2,
            HEIGHT // 2 - click_size // 2 - int(HEIGHT * 0.05),
            click_size, click_size,
            "КЛИК!",
            BLUE
        )
        
        # Кнопка зелья
        self.potion_button = Button(
            WIDTH // 2 - button_width // 2,
            HEIGHT - button_height - int(HEIGHT * 0.15),
            button_width, button_height,
            "🧪 Зелье",
            PURPLE,
            WHITE
        )
        
        # Кнопка сброса
        self.reset_button = Button(
            WIDTH // 2 - button_width // 2,
            HEIGHT - button_height - int(HEIGHT * 0.15) - button_height - spacing,
            button_width, button_height,
            "🔄 Сброс",
            RED,
            WHITE
        )

    def handle_click(self, pos):
        """Обработка клика по экрану"""
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_click_time < self.click_cooldown:
            return False
        
        # Проверяем, не нажата ли кнопка
        if self.click_button.rect.collidepoint(pos) or self.potion_button.rect.collidepoint(pos) or self.reset_button.rect.collidepoint(pos):
            return False
        
        self.last_click_time = current_time
        self.clicks += 1
        self.click_timer = pygame.time.get_ticks()
        
        success, chance = self.game.try_add_point(self.clicks)
        
        if success:
            self.show_message = f"+{2 if self.game.is_potion_active() else 1} очко!"
            self.message_timer = pygame.time.get_ticks()
            # Добавляем анимацию
            self.click_animation.append({
                'pos': pos,
                'time': pygame.time.get_ticks(),
                'text': f"+{2 if self.game.is_potion_active() else 1}!"
            })
        else:
            self.show_message = "Мимо!"
            self.message_timer = pygame.time.get_ticks()
        
        return True

    def update(self):
        """Обновление состояния игры"""
        current_time = pygame.time.get_ticks()
        
        # Очищаем сообщение через 1.5 секунды
        if self.message_timer and current_time - self.message_timer > 1500:
            self.show_message = ""
            self.message_timer = 0
        
        # Очищаем анимацию кликов
        self.click_animation = [anim for anim in self.click_animation 
                               if current_time - anim['time'] < 800]
        
        # Обновляем кнопку зелья
        if self.game.is_potion_active():
            time_left = self.game.get_potion_time_left()
            minutes = time_left // 60
            seconds = time_left % 60
            self.potion_button.text = f"🧪 {minutes:02d}:{seconds:02d}"
        else:
            self.potion_button.text = "🧪 Зелье"

    def draw(self, surface):
        # Заливка фона
        surface.fill(WHITE)
        
        # Рисуем очки
        points_text = font_large.render(f"Очки: {self.game.get_points()}", True, BLACK)
        points_rect = points_text.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.08)))
        surface.blit(points_text, points_rect)
        
        # Индикатор зелья
        if self.game.is_potion_active():
            indicator = font_small.render("⚡ Зелье активно! x2", True, GOLD)
            indicator_rect = indicator.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.15)))
            surface.blit(indicator, indicator_rect)
        
        # Рисуем кнопки
        self.click_button.draw(surface)
        self.potion_button.draw(surface)
        self.reset_button.draw(surface)
        
        # Рисуем сообщение
        if self.show_message:
            msg_color = GREEN if "+" in self.show_message else RED
            msg_text = font_medium.render(self.show_message, True, msg_color)
            msg_rect = msg_text.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.25)))
            surface.blit(msg_text, msg_rect)
        
        # Рисуем анимацию кликов
        current_time = pygame.time.get_ticks()
        for anim in self.click_animation:
            alpha = 255 - (current_time - anim['time']) * 255 // 800
            if alpha > 0:
                text = font_small.render(anim['text'], True, (0, 255, 0))
                text.set_alpha(alpha)
                y_offset = (current_time - anim['time']) // 2
                pos = (anim['pos'][0] - text.get_width() // 2, 
                       anim['pos'][1] - y_offset - 20)
                surface.blit(text, pos)
        
        # Подсказка
        hint_text = font_small.render("Кликните в любое место для игры", True, DARK_GRAY)
        hint_rect = hint_text.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.92)))
        surface.blit(hint_text, hint_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка
                        # Проверяем кнопки
                        if self.potion_button.handle_event(event):
                            if self.game.activate_potion():
                                self.show_message = "Зелье активировано! x2"
                                self.message_timer = pygame.time.get_ticks()
                        
                        elif self.reset_button.handle_event(event):
                            self.game.reset_progress()
                            self.show_message = "Прогресс сброшен!"
                            self.message_timer = pygame.time.get_ticks()
                        
                        elif self.click_button.handle_event(event):
                            # Обрабатываем клик по кнопке
                            self.last_click_time = pygame.time.get_ticks() / 1000.0
                            self.clicks += 1
                            self.click_timer = pygame.time.get_ticks()
                            
                            success, chance = self.game.try_add_point(self.clicks)
                            if success:
                                self.show_message = f"+{2 if self.game.is_potion_active() else 1} очко!"
                                self.message_timer = pygame.time.get_ticks()
                                self.click_animation.append({
                                    'pos': pygame.mouse.get_pos(),
                                    'time': pygame.time.get_ticks(),
                                    'text': f"+{2 if self.game.is_potion_active() else 1}!"
                                })
                            else:
                                self.show_message = "Мимо!"
                                self.message_timer = pygame.time.get_ticks()
                        else:
                            # Клик по пустому месту
                            self.handle_click(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.potion_button.handle_event(event)
                    self.reset_button.handle_event(event)
                    self.click_button.handle_event(event)
                
                elif event.type == pygame.VIDEORESIZE:
                    global WIDTH, HEIGHT
                    WIDTH, HEIGHT = event.w, event.h
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    self.create_buttons()
            
            # Для мобильных устройств - обработка касаний
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                # Проверяем кнопки на касание
                if self.potion_button.rect.collidepoint(pos):
                    if self.game.activate_potion():
                        self.show_message = "Зелье активировано! x2"
                        self.message_timer = pygame.time.get_ticks()
                elif self.reset_button.rect.collidepoint(pos):
                    self.game.reset_progress()
                    self.show_message = "Прогресс сброшен!"
                    self.message_timer = pygame.time.get_ticks()
                elif self.click_button.rect.collidepoint(pos):
                    self.last_click_time = pygame.time.get_ticks() / 1000.0
                    self.clicks += 1
                    self.click_timer = pygame.time.get_ticks()
                    success, chance = self.game.try_add_point(self.clicks)
                    if success:
                        self.show_message = f"+{2 if self.game.is_potion_active() else 1} очко!"
                        self.message_timer = pygame.time.get_ticks()
                        self.click_animation.append({
                            'pos': pos,
                            'time': pygame.time.get_ticks(),
                            'text': f"+{2 if self.game.is_potion_active() else 1}!"
                        })
                    else:
                        self.show_message = "Мимо!"
                        self.message_timer = pygame.time.get_ticks()
                else:
                    self.handle_click(pos)
            
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = ClickerApp()
    app.run()