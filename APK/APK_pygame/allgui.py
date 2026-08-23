# main.py
import pygame
import sys
import os
import json
from game_logic import ClickerGame
from gui.settings import Settings
from gui.inventory import InventoryManager
from gui.shop import ShopManager
from gui.authors import AuthorsManager

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHTBLUE = (173, 216, 230)
LIGHTCORAL = (240, 128, 128)
LIGHTGREEN = (144, 238, 144)
LIGHTYELLOW = (255, 255, 224)
LIGHTGRAY = (211, 211, 211)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGRAY = (100, 100, 100)


class ClickerGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Кликер")
        self.clock = pygame.time.Clock()
        self.running = True

        # Определяем корневую папку проекта
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Загружаем настройки
        self.settings = self.load_settings()

        # Инициализация игры
        self.game = ClickerGame()

        # Устанавливаем язык из настроек
        self.current_lang = self.settings.get("language", "Русский")

        # Менеджеры экранов
        self.inventory_manager = None
        self.shop_manager = None
        self.authors_manager = None
        self.settings_manager = None

        # Текущий экран
        self.current_screen = "game"  # game, inventory, shop, authors, settings

        # Шрифты
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)
        self.font_bold = pygame.font.Font(None, 32)

        self.translations = {
            "Английский": {
                "title": "Clicker", "result": "Result: -", "hit": "Hit! +1 point!", "miss": "Missed :(",
                "points": "Points: {}", "button_click": "Click!", "menu_lang": "Select language",
                "btn_inventory": "Inventory", "btn_shop": "Shop", "btn_authors": "Authors",
                "start_challenge": "Click to start!", "click_now": "CLICK NOW!",
                "score_message": "{} clicks in 1 second!", "inventory": "Inventory",
                "potion": "Double Points (10 min)", "potion_active": "Active! Time left: {} sec",
                "potion_inactive": "Use: 10 min x2", "use": "Use", "back": "Back", "btn_settings": "Settings"
            },
            "Русский": {
                "title": "Кликер", "result": "Результат: -", "hit": "Попал! +1 очко!", "miss": "Промах :(",
                "points": "Очки: {}", "button_click": "Клик!", "menu_lang": "Язык",
                "btn_inventory": "Инвентарь", "btn_shop": "Магазин", "btn_authors": "Авторы",
                "start_challenge": "Нажми, и начни!", "click_now": "ЖМИ СЕЙЧАС!",
                "score_message": "{} кликов за 1 секунду!", "inventory": "Инвентарь",
                "potion": "2x очки (10 мин)", "potion_active": "Активно! Осталось: {} сек",
                "potion_inactive": "Использовать: 10 мин", "use": "Использовать", "back": "Назад",
                "btn_settings": "Настройки"
            },
            "Французский": {
                "title": "Cliqueur", "result": "Résultat : -", "hit": "Touché ! +1 point !", "miss": "Raté :(",
                "points": "Points : {}", "button_click": "Cliquez !", "menu_lang": "Choisir la langue",
                "btn_inventory": "Inventaire", "btn_shop": "Magasin", "btn_authors": "Auteurs",
                "start_challenge": "Cliquez pour commencer !", "click_now": "CLIQUEZ MAINTENANT !",
                "score_message": "{} clics en 1 seconde !", "inventory": "Inventaire",
                "potion": "Double points (10 min)", "potion_active": "Actif ! Temps restant : {} sec",
                "potion_inactive": "Utiliser : 10 min x2", "use": "Utiliser", "back": "Retour",
                "btn_settings": "Paramètres"
            },
            "Немецкий": {
                "title": "Klicker", "result": "Ergebnis: -", "hit": "Treffer! +1 Punkt!", "miss": "Daneben :(",
                "points": "Punkte: {}", "button_click": "Klick!", "menu_lang": "Sprache wählen",
                "btn_inventory": "Inventar", "btn_shop": "Laden", "btn_authors": "Autoren",
                "start_challenge": "Klicke zum Starten!", "click_now": "JETZT KLICKEN!",
                "score_message": "{} Klicks in 1 Sekunde!", "inventory": "Inventar",
                "potion": "Doppelte Punkte (10 Min)", "potion_active": "Aktiv! Verbleibend: {} Sek",
                "potion_inactive": "Benutzen: 10 Min x2", "use": "Benutzen", "back": "Zurück",
                "btn_settings": "Einstellungen"
            },
            "Китайский": {
                "title": "点击器", "result": "结果: -", "hit": "击中！+1 分！", "miss": "未命中 :(",
                "points": "分数: {}", "button_click": "点击！", "menu_lang": "选择语言",
                "btn_inventory": "背包", "btn_shop": "商店", "btn_authors": "作者",
                "start_challenge": "点击开始！", "click_now": "立即点击！",
                "score_message": "1秒内点击 {} 次！", "inventory": "背包",
                "potion": "双倍积分 (10分钟)", "potion_active": "生效中！剩余时间：{} 秒",
                "potion_inactive": "使用：10分钟双倍", "use": "使用", "back": "返回", "btn_settings": "设置"
            }
        }

        # Кнопки
        self.buttons = {}
        self.language_menu_open = False
        self.language_options = list(self.translations.keys())

        # Игровые переменные
        self.click_count = 0
        self.challenge_active = False
        self.challenge_ended = False
        self.last_click_time = 0
        self.result_text = ""
        self.result_color = BLACK
        self.animation_frame = 0
        self.animation_active = False
        self.animation_type = None  # "success" or "fail"

        # Таймер для анимации
        self.animation_timer = 0

        self.init_ui()

    def load_settings(self):
        """Загрузка настроек из файла settings.json"""
        settings_file = os.path.join(self.base_dir, "settings.json")
        default_settings = {"sound": True, "language": "Русский"}

        if not os.path.exists(settings_file):
            try:
                with open(settings_file, "w", encoding="utf-8") as f:
                    json.dump(default_settings, f, ensure_ascii=False, indent=4)
                print("Создан settings.json с настройками по умолчанию")
            except Exception as e:
                print(f"Не удалось создать settings.json: {e}")
            return default_settings

        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            default_settings.update(data)
            return default_settings
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            return default_settings

    def save_settings(self):
        """Сохранение настроек"""
        settings_file = os.path.join(self.base_dir, "settings.json")
        try:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def init_ui(self):
        tr = self.translations[self.current_lang]

        # Кнопки правой панели
        button_configs = [
            ("inventory", tr["btn_inventory"], LIGHTCORAL, self.open_inventory, 50),
            ("shop", tr["btn_shop"], LIGHTGREEN, self.open_shop, 110),
            ("authors", tr["btn_authors"], LIGHTYELLOW, self.open_authors, 170),
            ("language", tr["menu_lang"], LIGHTBLUE, self.toggle_language_menu, 230),
            ("settings", tr["btn_settings"], LIGHTGRAY, self.open_settings, 290)
        ]

        for name, text, color, command, y in button_configs:
            self.buttons[name] = {
                "rect": pygame.Rect(450, y, 130, 45),
                "text": text,
                "color": color,
                "command": command,
                "hover": False
            }

        # Кнопка "Назад"
        self.buttons["back"] = {
            "rect": pygame.Rect(10, WINDOW_HEIGHT - 50, 100, 40),
            "text": tr["back"],
            "color": LIGHTBLUE,
            "command": self.go_back,
            "hover": False,
            "visible": False
        }

        # Кнопка "Клик"
        self.buttons["click"] = {
            "rect": pygame.Rect(150, 370, 180, 60),
            "text": tr["start_challenge"],
            "color": LIGHTBLUE,
            "command": self.start_challenge,
            "hover": False
        }

        # Метки для отображения
        self.labels = {
            "points": {"text": tr["points"].format(self.game.get_points()), "pos": (350, 395), "color": BLACK, "size": "large"},
            "result": {"text": "", "pos": (240, 330), "color": BLACK, "size": "medium"},
            "title": {"text": tr["title"], "pos": (WINDOW_WIDTH // 2, 20), "color": BLACK, "size": "title"}
        }

        # Анимационная область
        self.anim_rect = pygame.Rect(20, 50, 400, 250)

        # Нижний текст
        self.glitch_text = "GlitchHunters"
        self.glitch_pos = (10, WINDOW_HEIGHT - 15)

    def draw_button(self, button, mouse_pos):
        """Отрисовка кнопки"""
        rect = button["rect"]
        color = button["color"]
        if rect.collidepoint(mouse_pos):
            color = tuple(min(c + 30, 255) for c in color)
            button["hover"] = True
        else:
            button["hover"] = False

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, DARKGRAY, rect, 2, border_radius=8)

        # Текст кнопки
        text_surface = self.font_small.render(button["text"], True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_labels(self):
        """Отрисовка меток"""
        for key, label in self.labels.items():
            if key == "title":
                font = self.font_large
            elif label.get("size") == "large":
                font = self.font_bold
            else:
                font = self.font_medium

            text_surface = font.render(label["text"], True, label["color"])
            text_rect = text_surface.get_rect(center=label["pos"])
            self.screen.blit(text_surface, text_rect)

    def draw_animation_area(self):
        """Отрисовка области анимации"""
        pygame.draw.rect(self.screen, GRAY, self.anim_rect, 2)
        self.screen.fill((240, 240, 240), self.anim_rect.inflate(-10, -10))

        # Простая анимация
        if self.animation_active:
            if self.animation_type == "success":
                # Рисуем галочку или конфетти
                for i in range(5):
                    x = self.anim_rect.x + 50 + i * 70 + (self.animation_frame * 3) % 50
                    y = self.anim_rect.y + 50 + (self.animation_frame * 2) % 100
                    pygame.draw.circle(self.screen, GREEN, (x, y), 10)
            elif self.animation_type == "fail":
                # Рисуем крестик
                center = self.anim_rect.center
                size = 30 + (self.animation_frame % 10)
                pygame.draw.line(self.screen, RED, (center[0] - size, center[1] - size), 
                                (center[0] + size, center[1] + size), 4)
                pygame.draw.line(self.screen, RED, (center[0] + size, center[1] - size),
                                (center[0] - size, center[1] + size), 4)

    def draw_language_menu(self, mouse_pos):
        """Отрисовка меню выбора языка"""
        menu_width = 150
        menu_height = len(self.language_options) * 35
        menu_x = 450
        menu_y = 275

        # Фон меню
        pygame.draw.rect(self.screen, WHITE, (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(self.screen, BLACK, (menu_x, menu_y, menu_width, menu_height), 2)

        for i, lang in enumerate(self.language_options):
            y = menu_y + i * 35
            rect = pygame.Rect(menu_x, y, menu_width, 35)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, LIGHTBLUE, rect)

            text_surface = self.font_small.render(lang, True, BLACK)
            text_rect = text_surface.get_rect(center=(menu_x + menu_width // 2, y + 17))
            self.screen.blit(text_surface, text_rect)

    def handle_language_click(self, mouse_pos):
        """Обработка клика по меню языка"""
        menu_x = 450
        menu_y = 275
        for i, lang in enumerate(self.language_options):
            rect = pygame.Rect(menu_x, menu_y + i * 35, 150, 35)
            if rect.collidepoint(mouse_pos):
                self.set_language(lang)
                self.language_menu_open = False
                return True
        return False

    def toggle_language_menu(self):
        """Переключение меню языка"""
        self.language_menu_open = not self.language_menu_open

    def set_language(self, lang):
        """Установка языка"""
        self.current_lang = lang
        self.settings["language"] = lang
        self.save_settings()

        tr = self.translations[lang]
        pygame.display.set_caption(tr["title"])

        # Обновляем тексты кнопок
        self.buttons["inventory"]["text"] = tr["btn_inventory"]
        self.buttons["shop"]["text"] = tr["btn_shop"]
        self.buttons["authors"]["text"] = tr["btn_authors"]
        self.buttons["language"]["text"] = tr["menu_lang"]
        self.buttons["settings"]["text"] = tr["btn_settings"]
        self.buttons["back"]["text"] = tr["back"]

        # Обновляем текст кнопки клика
        current_text = self.buttons["click"]["text"]
        if any(x in current_text for x in ["start", "начни", "commencer", "Starten", "开始"]):
            self.buttons["click"]["text"] = tr["start_challenge"]
        elif any(x in current_text for x in ["now", "сейчас", "maintenant", "jetzt", "立即"]):
            self.buttons["click"]["text"] = tr["click_now"]
        else:
            self.buttons["click"]["text"] = tr["button_click"]

        # Обновляем метки
        self.labels["points"]["text"] = tr["points"].format(self.game.get_points())
        self.labels["title"]["text"] = tr["title"]

        # Обновляем менеджеры
        if self.inventory_manager:
            self.inventory_manager.update_language(lang)
        if self.shop_manager:
            self.shop_manager.update_language(lang)
        if self.authors_manager:
            self.authors_manager.update_language(lang)

    def start_challenge(self):
        """Начало испытания"""
        tr = self.translations[self.current_lang]
        self.buttons["click"]["text"] = tr["click_now"]
        self.buttons["click"]["color"] = RED
        self.labels["result"]["text"] = ""
        self.click_count = 0
        self.challenge_active = True
        self.challenge_ended = False
        self.buttons["click"]["command"] = self.register_click
        self.last_click_time = pygame.time.get_ticks()

    def register_click(self):
        """Регистрация клика"""
        if self.challenge_active:
            self.click_count += 1

    def end_challenge(self):
        """Завершение испытания"""
        self.challenge_active = False
        self.challenge_ended = True
        tr = self.translations[self.current_lang]
        self.labels["result"]["text"] = tr["score_message"].format(self.click_count)
        self.labels["result"]["color"] = BLUE
        self.buttons["click"]["text"] = tr["button_click"]
        self.buttons["click"]["color"] = LIGHTBLUE
        self.buttons["click"]["command"] = self.process_result

    def process_result(self):
        """Обработка результата"""
        success, _ = self.game.try_add_point(self.click_count)

        if success:
            self.animation_active = True
            self.animation_type = "success"
            self.animation_timer = pygame.time.get_ticks()
            self.labels["result"]["text"] = self.translations[self.current_lang]["hit"]
            self.labels["result"]["color"] = GREEN
        else:
            self.animation_active = True
            self.animation_type = "fail"
            self.animation_timer = pygame.time.get_ticks()
            self.labels["result"]["text"] = self.translations[self.current_lang]["miss"]
            self.labels["result"]["color"] = RED

        self.update_ui()
        tr = self.translations[self.current_lang]
        self.buttons["click"]["text"] = tr["start_challenge"]
        self.buttons["click"]["command"] = self.start_challenge
        self.challenge_ended = False

    def update_ui(self):
        """Обновление UI"""
        tr = self.translations[self.current_lang]
        self.labels["points"]["text"] = tr["points"].format(self.game.get_points())

    def open_inventory(self):
        """Открытие инвентаря"""
        if self.inventory_manager is None:
            self.inventory_manager = InventoryManager(
                self, self.game, self.translations, self.current_lang
            )
        self.current_screen = "inventory"
        self.buttons["back"]["visible"] = True
        self.inventory_manager.open()

    def open_shop(self):
        """Открытие магазина"""
        if self.shop_manager is None:
            self.shop_manager = ShopManager(self, self.translations, self.current_lang)
        self.current_screen = "shop"
        self.buttons["back"]["visible"] = True
        self.shop_manager.open()

    def open_authors(self):
        """Открытие авторов"""
        if self.authors_manager is None:
            self.authors_manager = AuthorsManager(self, self.translations, self.current_lang)
        self.current_screen = "authors"
        self.buttons["back"]["visible"] = True
        self.authors_manager.open()

    def open_settings(self):
        """Открытие настроек"""
        if self.settings_manager is None:
            self.settings_manager = Settings(self, self.translations, self.current_lang)
        self.current_screen = "settings"
        self.buttons["back"]["visible"] = True
        self.settings_manager.open()

    def go_back(self):
        """Возврат на главный экран"""
        self.current_screen = "game"
        self.buttons["back"]["visible"] = False

        # Закрываем менеджеры
        if self.inventory_manager:
            self.inventory_manager.close()
        if self.shop_manager:
            self.shop_manager.close()
        if self.authors_manager:
            self.authors_manager.close()
        if self.settings_manager:
            self.settings_manager.close()

    def handle_click(self, mouse_pos):
        """Обработка клика мыши"""
        # Проверяем клик по меню языка
        if self.language_menu_open:
            if self.handle_language_click(mouse_pos):
                return
            # Если клик вне меню - закрываем
            menu_rect = pygame.Rect(450, 275, 150, len(self.language_options) * 35)
            if not menu_rect.collidepoint(mouse_pos):
                self.language_menu_open = False

        # Проверяем клик по кнопкам
        for key, button in self.buttons.items():
            if key == "back" and not button["visible"]:
                continue
            if button["rect"].collidepoint(mouse_pos):
                if button["command"]:
                    button["command"]()
                return

        # Клик по анимационной области для старта
        if self.current_screen == "game" and self.anim_rect.collidepoint(mouse_pos):
            if not self.challenge_active and not self.challenge_ended:
                self.start_challenge()

    def run(self):
        """Главный цикл игры"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            current_time = pygame.time.get_ticks()

            # Проверка таймера для испытания
            if self.challenge_active:
                if current_time - self.last_click_time > 1000:
                    self.end_challenge()

            # Проверка таймера для анимации
            if self.animation_active:
                if current_time - self.animation_timer > 500:
                    self.animation_active = False
                    self.animation_type = None
                else:
                    self.animation_frame = (self.animation_frame + 1) % 100

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка
                        self.handle_click(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_screen != "game":
                            self.go_back()
                        else:
                            self.running = False

            # Отрисовка
            self.screen.fill(WHITE)

            # Отрисовка анимации
            self.draw_animation_area()

            # Отрисовка игрового экрана или других экранов
            if self.current_screen == "game":
                # Отрисовка игровых элементов
                self.draw_labels()

                # Кнопка клика
                self.draw_button(self.buttons["click"], mouse_pos)

                # Кнопки правой панели
                for key in ["inventory", "shop", "authors", "language", "settings"]:
                    self.draw_button(self.buttons[key], mouse_pos)

                # Меню языка
                if self.language_menu_open:
                    self.draw_language_menu(mouse_pos)

            elif self.current_screen == "inventory":
                if self.inventory_manager:
                    self.inventory_manager.draw(self.screen)
            elif self.current_screen == "shop":
                if self.shop_manager:
                    self.shop_manager.draw(self.screen)
            elif self.current_screen == "authors":
                if self.authors_manager:
                    self.authors_manager.draw(self.screen)
            elif self.current_screen == "settings":
                if self.settings_manager:
                    self.settings_manager.draw(self.screen)

            # Кнопка "Назад"
            if self.buttons["back"]["visible"]:
                self.draw_button(self.buttons["back"], mouse_pos)

            # Нижний текст
            text_surface = self.font_small.render(self.glitch_text, True, BLUE)
            self.screen.blit(text_surface, self.glitch_pos)

            pygame.display.flip()
            self.clock.tick(FPS)

        # Сохранение при выходе
        self.game.save_game()
        self.save_settings()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = ClickerGUI()
    game.run()