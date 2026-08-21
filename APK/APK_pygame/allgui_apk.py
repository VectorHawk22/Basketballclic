import os
import sys
import pygame

from game_logic import ClickerGame
from settings import Settings
from court1 import CourtSuccess
from court2 import CourtFail

# ==================== ПЕРЕВОДЫ ====================
TRANSLATIONS = {
    "Английский": {
        "title": "Clicker", "result": "Result: -", "hit": "🎯 Hit! +1 point!", "miss": "❌ Missed :(",
        "points": "Points: {}", "button_click": "Click!", "menu_lang": "Select language",
        "btn_inventory": "Inventory", "btn_shop": "Shop", "btn_authors": "Authors",
        "start_challenge": "Click to start!", "click_now": "CLICK NOW!",
        "score_message": "{} clicks in 1 second!", "inventory": "Inventory",
        "potion": "🧪 Double Points (10 min)", "potion_active": "Active! Time left: {} sec",
        "potion_inactive": "Use: 10 min x2", "use": "Use", "back": "Back", "btn_settings": "Settings"
    },
    "Русский": {
        "title": "Кликер", "result": "Результат: -", "hit": "🎯 Попал! +1 очко!", "miss": "❌ Промах :(",
        "points": "Очки: {}", "button_click": "Клик!", "menu_lang": "Язык",
        "btn_inventory": "Инвентарь", "btn_shop": "Магазин", "btn_authors": "Авторы",
        "start_challenge": "Нажми, и начни!", "click_now": "ЖМИ СЕЙЧАС!",
        "score_message": "{} кликов за 1 секунду!", "inventory": "Инвентарь",
        "potion": "🧪2x очки (10 мин)", "potion_active": "Активно! Осталось: {} сек",
        "potion_inactive": "Использовать: 10 мин", "use": "Использовать", "back": "Назад",
        "btn_settings": "Настройки"
    },
    "Французский": {
        "title": "Cliqueur", "result": "Résultat : -", "hit": "🎯 Touché ! +1 point !", "miss": "❌ Raté :(",
        "points": "Points : {}", "button_click": "Cliquez !", "menu_lang": "Choisir la langue",
        "btn_inventory": "Inventaire", "btn_shop": "Magasin", "btn_authors": "Auteurs",
        "start_challenge": "Cliquez pour commencer !", "click_now": "CLIQUEZ MAINTENANT !",
        "score_message": "{} clics en 1 seconde !", "inventory": "Inventaire",
        "potion": "🧪 Double points (10 min)", "potion_active": "Actif ! Temps restant : {} sec",
        "potion_inactive": "Utiliser : 10 min x2", "use": "Utiliser", "back": "Retour",
        "btn_settings": "Paramètres"
    },
    "Немецкий": {
        "title": "Klicker", "result": "Ergebnis: -", "hit": "🎯 Treffer! +1 Punkt!", "miss": "❌ Daneben :(",
        "points": "Punkte: {}", "button_click": "Klick!", "menu_lang": "Sprache wählen",
        "btn_inventory": "Inventar", "btn_shop": "Laden", "btn_authors": "Autoren",
        "start_challenge": "Klicke zum Starten!", "click_now": "JETZT KLICKEN!",
        "score_message": "{} Klicks in 1 Sekunde!", "inventory": "Inventar",
        "potion": "🧪 Doppelte Punkte (10 Min)", "potion_active": "Aktiv! Verbleibend: {} Sek",
        "potion_inactive": "Benutzen: 10 Min x2", "use": "Benutzen", "back": "Zurück",
        "btn_settings": "Einstellungen"
    },
    "Китайский": {
        "title": "点击器", "result": "结果: -", "hit": "🎯 击中！+1 分！", "miss": "❌ 未命中 :(",
        "points": "分数: {}", "button_click": "点击！", "menu_lang": "选择语言",
        "btn_inventory": "背包", "btn_shop": "商店", "btn_authors": "作者",
        "start_challenge": "点击开始！", "click_now": "立即点击！",
        "score_message": "1秒内点击 {} 次！", "inventory": "背包",
        "potion": "🧪 双倍积分 (10分钟)", "potion_active": "生效中！剩余时间：{} 秒",
        "potion_inactive": "使用：10分钟双倍", "use": "使用", "back": "返回", "btn_settings": "设置"
    }
}

LANGUAGES = list(TRANSLATIONS.keys())

# ==================== КОНСТАНТЫ ====================
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_CORAL = (240, 128, 128)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 153)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
DARK_ORANGE = (209, 106, 32)
DARK_BLUE = (66, 170, 255)
BROWN = (139, 69, 19)


# ==================== КЛАСС КНОПКИ ====================
class Button:
    """Класс кнопки для Pygame"""
    def __init__(self, x, y, width, height, text, color=LIGHT_BLUE, text_color=BLACK, font_size=16):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font_size = font_size
        self.is_hovered = False
        self.is_pressed = False
        self.visible = True
        self.enabled = True
        self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        if not self.visible:
            return
        
        color = self.color
        if not self.enabled:
            color = tuple(min(c + 80, 255) for c in self.color)
        elif self.is_hovered:
            color = tuple(min(c + 30, 255) for c in self.color)
        if self.is_pressed and self.enabled:
            color = tuple(max(c - 30, 0) for c in self.color)
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Текст
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if not self.visible or not self.enabled:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.rect.collidepoint(event.pos):
                    return True
        return False


# ==================== ГЛАВНЫЙ GUI КЛАСС ====================
class AllGUI:
    """Главный GUI-класс, объединяющий всю логику интерфейса"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Clicker Basketball")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Инициализация
        self.game = ClickerGame()
        self.settings = Settings(self)
        self.court_success = CourtSuccess(self.screen)
        self.court_fail = CourtFail(self.screen)
        
        # Состояние
        self.current_screen = "main"  # main, inventory, shop, authors, settings, language
        self.current_lang = self.settings.language
        self.tr = TRANSLATIONS[self.current_lang]
        self.challenge_active = False
        self.click_count = 0
        self.challenge_timer = 0
        self.result_message = ""
        self.result_color = BLACK
        self.show_result_timer = 0
        self.potion_use_btn = None
        
        # Создание кнопок
        self.create_buttons()
        
        # Таймер обновления
        self.update_timer = 0
        
        # Таймер для завершения испытания
        self.challenge_end_timer = None
        
        print("✅ AllGUI инициализирован!")

    def create_buttons(self):
        """Создание кнопок интерфейса"""
        width, height = self.screen.get_size()
        
        # Главная кнопка
        self.click_button = Button(
            width * 0.15, height * 0.6, width * 0.5, height * 0.15,
            self.tr['start_challenge'], LIGHT_BLUE, BLACK, 14
        )
        
        # Кнопки правой панели
        btn_width = width * 0.15
        btn_height = height * 0.07
        btn_x = width * 0.82
        btn_y_start = height * 0.05
        
        self.inventory_btn = Button(
            btn_x, btn_y_start, btn_width, btn_height,
            self.tr['btn_inventory'], LIGHT_CORAL, BLACK, 12
        )
        self.shop_btn = Button(
            btn_x, btn_y_start + btn_height + 5, btn_width, btn_height,
            self.tr['btn_shop'], LIGHT_GREEN, BLACK, 12
        )
        self.authors_btn = Button(
            btn_x, btn_y_start + 2 * (btn_height + 5), btn_width, btn_height,
            self.tr['btn_authors'], LIGHT_YELLOW, BLACK, 12
        )
        self.language_btn = Button(
            btn_x, btn_y_start + 3 * (btn_height + 5), btn_width, btn_height,
            self.tr['menu_lang'], LIGHT_BLUE, BLACK, 12
        )
        self.settings_btn = Button(
            btn_x, btn_y_start + 4 * (btn_height + 5), btn_width, btn_height,
            self.tr['btn_settings'], LIGHT_GRAY, BLACK, 12
        )
        
        # Кнопка "Назад"
        self.back_btn = Button(
            width * 0.1, height * 0.92, width * 0.2, height * 0.06,
            self.tr['back'], LIGHT_BLUE, BLACK, 14
        )
        self.back_btn.visible = False
        
        # Кнопки для выбора языка
        self.lang_buttons = []
        lang_y = height * 0.25
        for i, lang in enumerate(LANGUAGES):
            btn = Button(
                width * 0.25, lang_y + i * 40, width * 0.5, 35,
                lang, LIGHT_BLUE, BLACK, 14
            )
            self.lang_buttons.append((lang, btn))

    def update_buttons_text(self):
        """Обновление текста кнопок при смене языка"""
        self.click_button.text = self.tr['start_challenge']
        self.inventory_btn.text = self.tr['btn_inventory']
        self.shop_btn.text = self.tr['btn_shop']
        self.authors_btn.text = self.tr['btn_authors']
        self.language_btn.text = self.tr['menu_lang']
        self.settings_btn.text = self.tr['btn_settings']
        self.back_btn.text = self.tr['back']

    def run(self):
        """Главный цикл"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            # Обновление таймеров
            self.update_timer += dt
            if self.update_timer >= 1.0:
                self.update_timer = 0
                self.update_potion_display()
            
            # Обновление анимаций
            self.court_success.update(dt)
            self.court_fail.update(dt)
            
            # Проверка завершения испытания
            if self.challenge_active and self.challenge_end_timer is not None:
                self.challenge_end_timer -= dt
                if self.challenge_end_timer <= 0:
                    self.end_challenge()
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)
            
            # Отрисовка
            self.draw()
            pygame.display.flip()
        
        self.game.save_game()
        pygame.quit()

    def handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_back()
        
        # Обработка в зависимости от экрана
        if self.current_screen == "main":
            self.handle_main_events(event)
        elif self.current_screen == "inventory":
            self.handle_inventory_events(event)
        elif self.current_screen == "shop":
            self.handle_shop_events(event)
        elif self.current_screen == "authors":
            self.handle_authors_events(event)
        elif self.current_screen == "settings":
            self.handle_settings_events(event)
        elif self.current_screen == "language":
            self.handle_language_events(event)
        
        # Кнопка "Назад"
        if self.back_btn.visible:
            if self.back_btn.handle_event(event):
                self.go_back()

    def handle_main_events(self, event):
        """Обработка событий на главном экране"""
        if self.click_button.handle_event(event):
            if not self.challenge_active:
                self.start_challenge()
            else:
                self.click_count += 1
        
        if self.inventory_btn.handle_event(event):
            self.open_inventory()
        if self.shop_btn.handle_event(event):
            self.open_shop()
        if self.authors_btn.handle_event(event):
            self.open_authors()
        if self.language_btn.handle_event(event):
            self.open_language_menu()
        if self.settings_btn.handle_event(event):
            self.open_settings()

    def handle_inventory_events(self, event):
        """Обработка событий в инвентаре"""
        if self.potion_use_btn and self.potion_use_btn.handle_event(event):
            self.use_potion()

    def handle_shop_events(self, event):
        pass

    def handle_authors_events(self, event):
        pass

    def handle_settings_events(self, event):
        pass

    def handle_language_events(self, event):
        """Обработка выбора языка"""
        for lang, btn in self.lang_buttons:
            if btn.handle_event(event):
                self.set_language(lang)
                self.current_screen = "main"
                self.back_btn.visible = False

    def go_back(self):
        """Возврат на главный экран"""
        self.current_screen = "main"
        self.back_btn.visible = False
        self.show_result_timer = 0

    def draw(self):
        """Отрисовка всех элементов"""
        self.screen.fill(WHITE)
        
        if self.current_screen == "main":
            self.draw_main()
        elif self.current_screen == "inventory":
            self.draw_inventory()
        elif self.current_screen == "shop":
            self.draw_shop()
        elif self.current_screen == "authors":
            self.draw_authors()
        elif self.current_screen == "settings":
            self.draw_settings()
        elif self.current_screen == "language":
            self.draw_language_menu()
        
        # Кнопка "Назад"
        if self.back_btn.visible:
            self.back_btn.draw(self.screen)
        
        # GlitchHunters
        font = pygame.font.Font(None, 14)
        text = font.render("GlitchHunters", True, (0, 0, 255))
        self.screen.blit(text, (10, self.screen.get_height() - 25))

    def draw_main(self):
        """Отрисовка главного экрана"""
        width, height = self.screen.get_size()
        
        # Заголовок
        font = pygame.font.Font(None, 28)
        title = font.render(self.tr['title'], True, BLACK)
        self.screen.blit(title, (width // 2 - title.get_width() // 2, 5))
        
        # Анимационная область
        anim_rect = pygame.Rect(10, 30, width * 0.78, height * 0.55)
        pygame.draw.rect(self.screen, (240, 240, 240), anim_rect)
        pygame.draw.rect(self.screen, BLACK, anim_rect, 1)
        
        # Создаем временную поверхность для анимации
        anim_surface = pygame.Surface((anim_rect.width, anim_rect.height))
        old_screen = self.screen
        self.screen = anim_surface
        
        # Отрисовываем анимацию на временной поверхности
        self.court_success.draw()
        self.court_fail.draw()
        
        # Возвращаем основную поверхность и копируем анимацию
        self.screen = old_screen
        self.screen.blit(anim_surface, (anim_rect.x, anim_rect.y))
        
        # Игровая область
        game_y = anim_rect.bottom + 5
        
        # Результат
        if self.result_message:
            font = pygame.font.Font(None, 20)
            text = font.render(self.result_message, True, self.result_color)
            self.screen.blit(text, (10, game_y))
            self.show_result_timer += 1
            if self.show_result_timer > 120:
                self.result_message = ""
                self.show_result_timer = 0
        
        # Кнопка клика
        self.click_button.rect.y = game_y + 25
        self.click_button.draw(self.screen)
        
        # Очки
        font = pygame.font.Font(None, 20)
        points_text = font.render(self.tr['points'].format(self.game.get_points()), True, BLACK)
        self.screen.blit(points_text, (self.click_button.rect.right + 10, game_y + 30))
        
        # Правая панель
        right_x = width * 0.82
        for btn in [self.inventory_btn, self.shop_btn, self.authors_btn, 
                    self.language_btn, self.settings_btn]:
            btn.rect.x = right_x
            btn.draw(self.screen)

    def draw_inventory(self):
        """Отрисовка инвентаря"""
        width, height = self.screen.get_size()
        
        # Заголовок
        font = pygame.font.Font(None, 28)
        title = font.render(self.tr['inventory'], True, BLACK)
        self.screen.blit(title, (width // 2 - title.get_width() // 2, 30))
        
        # Контейнер зелья
        potion_rect = pygame.Rect(width * 0.1, 80, width * 0.8, 150)
        pygame.draw.rect(self.screen, (255, 255, 200), potion_rect)
        pygame.draw.rect(self.screen, BLACK, potion_rect, 2)
        
        # Картинка зелья
        font_big = pygame.font.Font(None, 48)
        potion_icon = font_big.render("🧪", True, BLACK)
        self.screen.blit(potion_icon, (potion_rect.x + 20, potion_rect.y + 20))
        
        # Текст зелья
        font = pygame.font.Font(None, 16)
        potion_text = font.render(self.tr['potion'], True, BLACK)
        self.screen.blit(potion_text, (potion_rect.x + 80, potion_rect.y + 30))
        
        # Кнопка использования
        is_active = self.game.is_potion_active()
        btn_text = self.tr['use'] if is_active else self.tr['potion_inactive']
        btn_enabled = not is_active
        
        if not self.potion_use_btn:
            self.potion_use_btn = Button(
                potion_rect.x + 80, potion_rect.y + 60,
                150, 30, btn_text, LIGHT_GREEN if btn_enabled else LIGHT_GRAY, BLACK, 12
            )
        else:
            self.potion_use_btn.text = btn_text
            self.potion_use_btn.color = LIGHT_GREEN if btn_enabled else LIGHT_GRAY
            self.potion_use_btn.rect.x = potion_rect.x + 80
            self.potion_use_btn.rect.y = potion_rect.y + 60
            self.potion_use_btn.enabled = btn_enabled
        
        self.potion_use_btn.draw(self.screen)
        
        # Таймер зелья
        if is_active:
            time_left = self.game.get_potion_time_left()
            timer_text = self.tr['potion_active'].format(time_left)
            timer_color = BLACK
        else:
            timer_text = "Не активно"
            timer_color = (128, 128, 128)
        
        font = pygame.font.Font(None, 14)
        timer_surface = font.render(timer_text, True, timer_color)
        timer_rect = pygame.Rect(potion_rect.x + 80, potion_rect.y + 100, 200, 30)
        pygame.draw.rect(self.screen, (150, 230, 150), timer_rect)
        pygame.draw.rect(self.screen, BLACK, timer_rect, 1)
        self.screen.blit(timer_surface, (timer_rect.x + 10, timer_rect.y + 5))

    def draw_shop(self):
        """Отрисовка магазина"""
        width, height = self.screen.get_size()
        
        font = pygame.font.Font(None, 28)
        title = font.render(self.tr['btn_shop'], True, BLACK)
        self.screen.blit(title, (width // 2 - title.get_width() // 2, 30))
        
        font = pygame.font.Font(None, 20)
        closed_text = font.render("🏪 Магазин временно закрыт", True, (128, 128, 128))
        self.screen.blit(closed_text, (width // 2 - closed_text.get_width() // 2, height // 2))

    def draw_authors(self):
        """Отрисовка информации об авторах"""
        width, height = self.screen.get_size()
        
        font = pygame.font.Font(None, 28)
        title = font.render(self.tr['btn_authors'], True, BLACK)
        self.screen.blit(title, (width // 2 - title.get_width() // 2, 30))
        
        authors_text = [
            "🎮 Authors:",
            "• thekosmoss",
            "• artman",
            "• Kirill",
            "",
            "🔧 Project: Clicker Basketball",
            "📅 2025 GlitchHunters Team"
        ]
        
        font = pygame.font.Font(None, 18)
        y = 80
        for line in authors_text:
            text = font.render(line, True, BLACK)
            self.screen.blit(text, (width // 2 - text.get_width() // 2, y))
            y += 25

    def draw_settings(self):
        """Отрисовка настроек"""
        width, height = self.screen.get_size()
        
        font = pygame.font.Font(None, 28)
        title = font.render("Настройки", True, BLACK)
        self.screen.blit(title, (width // 2 - title.get_width() // 2, 30))
        
        # Язык
        font = pygame.font.Font(None, 20)
        lang_text = font.render(f"Язык: {self.current_lang}", True, BLACK)
        self.screen.blit(lang_text, (width * 0.2, 100))
        
        # Звук
        sound_text = font.render(f"Звук: {'Включён' if self.settings.sound else 'Выключен'}", True, BLACK)
        self.screen.blit(sound_text, (width * 0.2, 150))

    def draw_language_menu(self):
        """Отрисовка меню выбора языка"""
        width, height = self.screen.get_size()
        
        font = pygame.font.Font(None, 28)
        title = font.render(self.tr['menu_lang'], True, BLACK)
        self.screen.blit(title, (width // 2 - title.get_width() // 2, 30))
        
        for lang, btn in self.lang_buttons:
            btn.draw(self.screen)

    def start_challenge(self):
        """Начало испытания"""
        self.tr = TRANSLATIONS[self.current_lang]
        self.click_button.text = self.tr['click_now']
        self.click_button.color = RED
        self.click_count = 0
        self.challenge_active = True
        self.result_message = ""
        self.challenge_end_timer = 1.0  # 1 секунда

    def end_challenge(self):
        """Завершение испытания"""
        self.challenge_active = False
        self.challenge_end_timer = None
        self.tr = TRANSLATIONS[self.current_lang]
        self.result_message = self.tr['score_message'].format(self.click_count)
        self.result_color = BLUE
        self.click_button.text = self.tr['button_click']
        self.click_button.color = LIGHT_BLUE
        self.show_result_timer = 0
        self.process_result()

    def process_result(self):
        """Обработка результата"""
        success, _ = self.game.try_add_point(self.click_count)
        self.court_success.stop()
        self.court_fail.stop()

        if success:
            self.court_success.start_animation()
            self.result_message = self.tr['hit']
            self.result_color = GREEN
        else:
            self.court_fail.start_animation()
            self.result_message = self.tr['miss']
            self.result_color = RED

        self.tr = TRANSLATIONS[self.current_lang]
        self.click_button.text = self.tr['start_challenge']
        self.click_button.color = LIGHT_BLUE

    def open_inventory(self):
        """Открытие инвентаря"""
        self.current_screen = "inventory"
        self.back_btn.visible = True
        self.potion_use_btn = None

    def open_shop(self):
        """Открытие магазина"""
        self.current_screen = "shop"
        self.back_btn.visible = True

    def open_authors(self):
        """Открытие информации об авторах"""
        self.current_screen = "authors"
        self.back_btn.visible = True

    def open_settings(self):
        """Открытие настроек"""
        self.current_screen = "settings"
        self.back_btn.visible = True

    def open_language_menu(self):
        """Открытие меню выбора языка"""
        self.current_screen = "language"
        self.back_btn.visible = True

    def set_language(self, lang):
        """Установка языка"""
        self.current_lang = lang
        self.tr = TRANSLATIONS[lang]
        self.settings.change_language(lang)
        self.update_buttons_text()

    def use_potion(self):
        """Использование зелья"""
        if self.game.activate_potion():
            self.update_potion_display()
            self.result_message = "🧪 Эффект x2 активирован!"
            self.result_color = GREEN
        else:
            self.result_message = "Эффект уже активен!"
            self.result_color = ORANGE

    def update_potion_display(self):
        """Обновление отображения зелья"""
        self.potion_use_btn = None

    def update_ui(self):
        """Обновление UI"""
        pass


# ==================== ТОЧКА ВХОДА ====================
def main():
    """Точка входа"""
    gui = AllGUI()
    gui.run()


if __name__ == "__main__":
    main()