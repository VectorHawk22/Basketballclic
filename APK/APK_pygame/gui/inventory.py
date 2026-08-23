# inventory.py
import pygame
import os
from pygame.locals import *


class InventoryManager:
    def __init__(self, game, translations, current_lang, screen_width, screen_height):
        self.game = game
        self.translations = translations
        self.current_lang = current_lang
        self.tr = self.translations[self.current_lang]
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Состояние
        self.is_open = False
        self.visible = False
        self.update_timer = 0
        self.animation_timer = 0
        self.animation_color = None

        # Шрифты
        self.title_font = None
        self.label_font = None
        self.button_font = None
        self.timer_font = None

        # UI элементы (прямоугольники и кнопки)
        self.potion_rect = None
        self.potion_btn_rect = None
        self.back_btn_rect = None

        # Изображения
        self.potion_image = None
        self.empty_potion_image = None
        self.potion_display_image = None

        # Тексты кнопок
        self.potion_btn_text = ""
        self.timer_text = ""

        self.load_fonts()
        self.load_images()

    def load_fonts(self):
        """Загрузка шрифтов"""
        try:
            self.title_font = pygame.font.Font(None, 36)
            self.label_font = pygame.font.Font(None, 28)
            self.button_font = pygame.font.Font(None, 24)
            self.timer_font = pygame.font.Font(None, 22)
        except:
            self.title_font = pygame.font.SysFont("Arial", 36)
            self.label_font = pygame.font.SysFont("Arial", 28)
            self.button_font = pygame.font.SysFont("Arial", 24)
            self.timer_font = pygame.font.SysFont("Arial", 22)

    def load_images(self):
        """Загрузка изображений зелья"""
        try:
            images_dir = os.path.join(self.base_dir, "images")

            full_path = os.path.join(images_dir, "potionthatgives2xcoins.png")
            empty_path = os.path.join(images_dir, "emptypotionthatgives2xcoins.png")

            if os.path.exists(full_path):
                img = pygame.image.load(full_path)
                self.potion_image = pygame.transform.scale(img, (80, 80))
            else:
                print(f"⚠️ Файл не найден: {full_path}")

            if os.path.exists(empty_path):
                img = pygame.image.load(empty_path)
                self.empty_potion_image = pygame.transform.scale(img, (80, 80))
            else:
                print(f"⚠️ Файл не найден: {empty_path}")

        except Exception as e:
            print(f"⚠️ Ошибка загрузки изображений зелья: {e}")

    def open(self):
        """Открытие инвентаря"""
        self.tr = self.translations[self.current_lang]
        self.is_open = True
        self.visible = True
        self.update_timer = 0
        self.animation_color = None
        self.update_button_state()
        self.update_timer_text()

    def close(self):
        """Закрытие инвентаря"""
        self.is_open = False
        self.visible = False
        self.game.update_ui()

    def handle_event(self, event):
        """Обработка событий"""
        if not self.is_open:
            return False

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            # Кнопка назад
            if self.back_btn_rect and self.back_btn_rect.collidepoint(mouse_pos):
                self.close()
                return True

            # Кнопка использования зелья
            if self.potion_btn_rect and self.potion_btn_rect.collidepoint(mouse_pos):
                self.use_potion()
                return True

        return False

    def update(self, dt):
        """Обновление состояния"""
        if not self.is_open:
            return

        self.update_timer += dt

        # Обновление каждую секунду
        if self.update_timer >= 1.0:
            self.update_timer = 0
            self.update_button_state()
            self.update_timer_text()

        # Сброс анимации
        if self.animation_timer > 0:
            self.animation_timer -= dt
            if self.animation_timer <= 0:
                self.animation_color = None

    def use_potion(self):
        """Использование зелья"""
        if self.game.activate_potion():
            self.update_button_state()
            self.update_timer_text()
            self.game.update_ui()

            # Визуальный эффект
            self.animation_color = (144, 238, 144)  # lightgreen
            self.animation_timer = 3.0
        else:
            # Сообщение об ошибке через game
            self.game.show_message("⏳ Эффект уже активен!", (255, 165, 0))

    def update_button_state(self):
        """Обновление состояния кнопки"""
        tr = self.translations[self.current_lang]
        is_active = self.game.is_potion_active()

        if is_active:
            self.potion_btn_text = tr["use"]
        else:
            self.potion_btn_text = tr["potion_inactive"]

    def update_timer_text(self):
        """Обновление текста таймера"""
        tr = self.translations[self.current_lang]
        time_left = self.game.get_potion_time_left()

        if time_left > 0:
            self.timer_text = tr["potion_active"].format(time_left)
        else:
            self.timer_text = ""

    def get_current_image(self):
        """Получение текущего изображения зелья"""
        is_active = self.game.is_potion_active()
        if is_active and self.empty_potion_image:
            return self.empty_potion_image
        return self.potion_image

    def draw(self, screen):
        """Отрисовка инвентаря"""
        if not self.is_open:
            return

        # Затемнённый фон
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Основной фон
        bg_rect = pygame.Rect(
            self.screen_width // 2 - 200,
            self.screen_height // 2 - 200,
            400,
            400
        )
        bg_color = self.animation_color if self.animation_color else (255, 255, 224)  # lightyellow
        pygame.draw.rect(screen, bg_color, bg_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 215, 0), bg_rect, 3, border_radius=10)

        # Заголовок
        title_surf = self.title_font.render(self.tr["inventory"], True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, bg_rect.y + 30))
        screen.blit(title_surf, title_rect)

        # Фрейм зелья
        potion_frame = pygame.Rect(
            bg_rect.x + 30,
            bg_rect.y + 70,
            bg_rect.width - 60,
            170
        )
        frame_color = self.animation_color if self.animation_color else (255, 255, 224)
        pygame.draw.rect(screen, frame_color, potion_frame, border_radius=5)
        pygame.draw.rect(screen, (255, 215, 0), potion_frame, 2, border_radius=5)

        # Изображение зелья
        img = self.get_current_image()
        if img:
            img_rect = img.get_rect(topleft=(potion_frame.x + 15, potion_frame.y + 20))
            screen.blit(img, img_rect)

        # Текст "Зелье"
        label_surf = self.label_font.render(self.tr["potion"], True, (0, 0, 0))
        label_rect = label_surf.get_rect(topleft=(potion_frame.x + 110, potion_frame.y + 20))
        screen.blit(label_surf, label_rect)

        # Кнопка использования
        btn_x = potion_frame.x + 110
        btn_y = potion_frame.y + 60
        btn_width = 160
        btn_height = 35
        self.potion_btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)

        is_active = self.game.is_potion_active()
        btn_color = (200, 200, 200) if is_active else (100, 200, 100)
        pygame.draw.rect(screen, btn_color, self.potion_btn_rect, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), self.potion_btn_rect, 2, border_radius=5)

        btn_text = self.button_font.render(self.potion_btn_text, True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect(center=self.potion_btn_rect.center)
        screen.blit(btn_text, btn_text_rect)

        # Таймер
        if self.timer_text:
            timer_surf = self.timer_font.render(self.timer_text, True, (0, 0, 0))
            timer_rect = timer_surf.get_rect(topleft=(potion_frame.x + 15, potion_frame.y + 120))
            screen.blit(timer_surf, timer_rect)

        # Кнопка назад
        back_btn_w = 120
        back_btn_h = 40
        back_x = self.screen_width // 2 - back_btn_w // 2
        back_y = bg_rect.y + bg_rect.height - 60
        self.back_btn_rect = pygame.Rect(back_x, back_y, back_btn_w, back_btn_h)

        pygame.draw.rect(screen, (200, 200, 200), self.back_btn_rect, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), self.back_btn_rect, 2, border_radius=5)

        back_text = self.button_font.render("← " + self.tr.get("back", "Назад"), True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=self.back_btn_rect.center)
        screen.blit(back_text, back_text_rect)

    def update_language(self, new_lang):
        """Обновление языка"""
        self.current_lang = new_lang
        self.tr = self.translations[self.current_lang]
        self.update_button_state()
        self.update_timer_text()