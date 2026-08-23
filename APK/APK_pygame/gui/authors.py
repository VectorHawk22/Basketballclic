import pygame
from pygame.locals import *


class AuthorsManager:
    def __init__(self, screen, translations, current_lang, game_state):
        self.screen = screen
        self.translations = translations
        self.current_lang = current_lang
        self.game_state = game_state
        self.tr = self.translations[self.current_lang]
        
        # Шрифты
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Цвета
        self.bg_color = (240, 240, 240)
        self.text_color = (0, 0, 0)
        self.title_color = (50, 50, 150)
        
        # Кнопка "Назад"
        self.back_button_rect = pygame.Rect(20, 20, 80, 40)
        self.back_button_color = (200, 70, 70)
        self.back_button_hover = (220, 100, 100)
        self.is_hover_back = False
        
        # Основной фрейм (визуальный контейнер)
        self.authors_frame_rect = pygame.Rect(50, 80, 
                                             self.screen.get_width() - 100, 
                                             self.screen.get_height() - 160)
        
        # Активен ли экран
        self.is_active = False

    def open(self):
        """Открытие экрана авторов"""
        self.tr = self.translations[self.current_lang]
        self.is_active = True
        # Обновляем состояние игры, чтобы остановить игровой процесс
        self.game_state["current_screen"] = "authors"

    def close(self):
        """Закрытие экрана авторов"""
        self.is_active = False
        self.game_state["current_screen"] = "game"

    def update_language(self, new_lang):
        """Обновление языка"""
        self.current_lang = new_lang
        self.tr = self.translations[self.current_lang]

    def handle_event(self, event):
        """Обработка событий"""
        if not self.is_active:
            return False
            
        if event.type == MOUSEMOTION:
            # Проверка наведения на кнопку "Назад"
            if self.back_button_rect.collidepoint(event.pos):
                self.is_hover_back = True
            else:
                self.is_hover_back = False
                
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            # Клик по кнопке "Назад"
            if self.back_button_rect.collidepoint(event.pos):
                self.close()
                return True
                
        return False

    def draw(self):
        """Отрисовка экрана авторов"""
        if not self.is_active:
            return
        
        # Очистка экрана
        self.screen.fill(self.bg_color)
        
        # Рисуем фон фрейма
        pygame.draw.rect(self.screen, (255, 255, 255), self.authors_frame_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.authors_frame_rect, 2)
        
        # Заголовок
        title_text = self.tr.get("btn_authors", "Авторы")
        title_surface = self.font_title.render(title_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 140))
        self.screen.blit(title_surface, title_rect)
        
        # Информация об авторах
        authors_lines = [
            "👨‍💻 Разработчики:",
            "",
            "  • thekosmoss",
            "  • artman",
            "  • amonpys",
            "",
            "🏀 Проект: Basketball Click",
            "📅 2026 © GlitchHunters Team",
            "",
            "🔧 Версия: 1.0.0"
        ]
        
        y_offset = 200
        for line in authors_lines:
            text_surface = self.font_text.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 35
        
        # Кнопка "Назад"
        back_color = self.back_button_hover if self.is_hover_back else self.back_button_color
        pygame.draw.rect(self.screen, back_color, self.back_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (150, 50, 50), self.back_button_rect, 2, border_radius=8)
        
        # Текст кнопки "Назад"
        back_text = self.tr.get("btn_back", "Назад")
        back_surface = self.font_small.render(back_text, True, (255, 255, 255))
        back_rect = back_surface.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_surface, back_rect)
        
        # Обновляем экран
        pygame.display.flip()

    def update(self):
        """Обновление логики (если нужно)"""
        pass

    def is_displayed(self):
        """Проверка, активен ли экран"""
        return self.is_active