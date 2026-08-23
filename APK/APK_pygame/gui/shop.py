import pygame
import sys

class ShopManager:
    def __init__(self, screen, translations, current_lang, back_callback):
        self.screen = screen
        self.translations = translations
        self.current_lang = current_lang
        self.tr = self.translations[self.current_lang]
        self.back_callback = back_callback

        # Шрифты (для APK лучше использовать системные или встроенные)
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)

        # Цвета
        self.bg_color = (30, 30, 40)
        self.text_color = (220, 220, 220)
        self.gray_color = (160, 160, 160)

        # Кнопка "Назад" (будет создана при открытии)
        self.back_button_rect = None

    def open(self):
        """Открытие магазина (вызывается из основного цикла)"""
        self.tr = self.translations[self.current_lang]
        self.running = True
        self.back_button_rect = pygame.Rect(20, 20, 120, 50)

    def close(self):
        """Закрытие магазина (вызывается по кнопке 'Назад')"""
        self.running = False
        if self.back_callback:
            self.back_callback()

    def update_language(self, new_lang):
        """Обновление языка"""
        self.current_lang = new_lang
        self.tr = self.translations[self.current_lang]

    def handle_events(self, events):
        """Обработка событий (клики по кнопкам)"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                    self.close()

    def draw(self):
        """Отрисовка экрана магазина"""
        self.screen.fill(self.bg_color)

        # Заголовок
        title_surf = self.font_title.render(self.tr.get("btn_shop", "Shop"), True, self.text_color)
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_surf, title_rect)

        # Сообщение "Магазин закрыт"
        closed_text = self.tr.get("shop_closed", "🏪 Shop is temporarily closed")
        closed_surf = self.font_text.render(closed_text, True, self.gray_color)
        closed_rect = closed_surf.get_rect(center=(self.screen.get_width() // 2, 180))
        self.screen.blit(closed_surf, closed_rect)

        # Дополнительный текст
        work_text = self.tr.get("shop_work", "🚧 Under construction\n\nNew items coming soon!")
        lines = work_text.split('\n')
        y_offset = 250
        for line in lines:
            line_surf = self.font_small.render(line, True, self.gray_color)
            line_rect = line_surf.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(line_surf, line_rect)
            y_offset += 40

        # Кнопка "Назад"
        self._draw_back_button()

    def _draw_back_button(self):
        """Отрисовка кнопки возврата"""
        if self.back_button_rect:
            pygame.draw.rect(self.screen, (80, 80, 120), self.back_button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 220), self.back_button_rect, 2, border_radius=10)

            back_text = self.tr.get("back", "Back")
            back_surf = self.font_small.render(back_text, True, (240, 240, 255))
            back_rect = back_surf.get_rect(center=self.back_button_rect.center)
            self.screen.blit(back_surf, back_rect)