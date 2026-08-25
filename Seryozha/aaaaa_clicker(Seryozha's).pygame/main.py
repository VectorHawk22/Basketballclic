import pygame
import sys
import os
import json

from game_logic import ClickerGame
from gui import get_font, strip_emoji, render_text, Dialog
from gui.game import GameScreen
from gui.settings import SettingsScreen
from gui.inventory import InventoryScreen
from gui.shop import ShopScreen
from gui.authors import AuthorsScreen

WIDTH = 600
HEIGHT = 490
BACK_BTN_RECT = (20, 440, 560, 40)

TRANSLATIONS = {
    "Английский": {
        "title": "Clicker", "hit": "Hit! +1 point!", "miss": "Missed :(",
        "points": "Points: {}", "start_challenge": "Click to start!",
        "click_now": "CLICK NOW!", "score_message": "{} clicks in 1 second!",
        "inventory": "Inventory", "potion": "Double Points (10 min)",
        "potion_active": "Active! Time left: {} sec",
        "potion_inactive": "Use: 10 min x2", "use": "Use", "back": "Back",
        "btn_inventory": "Inventory", "btn_shop": "Shop",
        "btn_authors": "Authors", "btn_settings": "Settings",
        "settings_title": "Settings", "language_label": "Language:",
        "sound_label": "Sound:", "sound_on": "On", "sound_off": "Off",
        "save_button": "Save Settings", "reset_button": "Reset Progress",
        "reset_confirm": "Are you sure you want to\ndelete all progress?\n\nThis action cannot be undone!",
        "reset_done": "Progress successfully reset!",
        "reset_error": "Failed to reset progress",
        "tab_potions": "Potions", "tab_skins": "Skins",
        "skins_balls": "Balls", "skins_baskets": "Hoops",
        "save_success": "Settings saved!",
        "save_error": "Failed to save settings!",
        "button_click": "Click!",
        "shop_tab_upgrades": "Upgrades", "shop_tab_balls": "Balls", "shop_tab_baskets": "Hoops",
        "shop_buy": "Buy", "shop_owned": "Owned",
        "shop_price": "{} pts", "shop_not_enough": "Not enough points!",
        "shop_coming_soon": "Coming soon...",
        "dialog_yes": "Yes", "dialog_no": "No",
    },
    "Русский": {
        "title": "Кликер", "hit": "Попал! +1 очко!", "miss": "Промах :(",
        "points": "Очки: {}", "start_challenge": "Нажми, и начни!",
        "click_now": "ЖМИ СЕЙЧАС!", "score_message": "{} кликов за 1 секунду!",
        "inventory": "Инвентарь", "potion": "2x очки (10 мин)",
        "potion_active": "Активно! Осталось: {} сек",
        "potion_inactive": "Использовать: 10 мин x2", "use": "Использовать",
        "back": "Назад", "btn_inventory": "Инвентарь", "btn_shop": "Магазин",
        "btn_authors": "Авторы", "btn_settings": "Настройки",
        "settings_title": "Настройки", "language_label": "Язык:",
        "sound_label": "Звук:", "sound_on": "Включён", "sound_off": "Выключен",
        "save_button": "Сохранить настройки", "reset_button": "Сбросить прогресс",
        "reset_confirm": "Вы уверены, что хотите удалить\nвесь прогресс?\n\nЭто действие нельзя отменить!",
        "reset_done": "Прогресс успешно сброшен!",
        "reset_error": "Не удалось сбросить прогресс",
        "tab_potions": "Зелья", "tab_skins": "Скины",
        "skins_balls": "Мячи", "skins_baskets": "Корзины",
        "save_success": "Настройки сохранены!",
        "save_error": "Не удалось сохранить настройки!",
        "button_click": "Клик!",
        "shop_tab_upgrades": "Улучшения", "shop_tab_balls": "Мячи", "shop_tab_baskets": "Кольца",
        "shop_buy": "Купить", "shop_owned": "Куплено",
        "shop_price": "{} очков", "shop_not_enough": "Недостаточно очков!",
        "shop_coming_soon": "Скоро будет...",
        "dialog_yes": "Да", "dialog_no": "Нет",
    },
    "Французский": {
        "title": "Cliqueur", "hit": "Touche ! +1 point !", "miss": "Rate :(",
        "points": "Points : {}", "start_challenge": "Cliquez pour commencer !",
        "click_now": "CLIQUEZ MAINTENANT !",
        "score_message": "{} clics en 1 seconde !",
        "inventory": "Inventaire", "potion": "Double points (10 min)",
        "potion_active": "Actif ! Temps restant : {} sec",
        "potion_inactive": "Utiliser : 10 min x2", "use": "Utiliser",
        "back": "Retour", "btn_inventory": "Inventaire", "btn_shop": "Magasin",
        "btn_authors": "Auteurs", "btn_settings": "Parametres",
        "settings_title": "Parametres", "language_label": "Langue :",
        "sound_label": "Son :", "sound_on": "Active", "sound_off": "Desactive",
        "save_button": "Enregistrer", "reset_button": "Reinitialiser",
        "reset_confirm": "Etes-vous sur de vouloir supprimer\ntoute la progression ?\n\nCette action est irreversible !",
        "reset_done": "Progression reinitialisee !",
        "reset_error": "Echec de la reinitialisation",
        "tab_potions": "Elixirs", "tab_skins": "Skins",
        "skins_balls": "Ballons", "skins_baskets": "Paniers",
        "save_success": "Parametres enregistres !",
        "save_error": "Echec de l'enregistrement !",
        "button_click": "Cliquez !",
        "shop_tab_upgrades": "Ameliorations", "shop_tab_balls": "Ballons", "shop_tab_baskets": "Paniers",
        "shop_buy": "Acheter", "shop_owned": "Possede",
        "shop_price": "{} pts", "shop_not_enough": "Pas assez de points !",
        "shop_coming_soon": "Bientot disponible...",
        "dialog_yes": "Oui", "dialog_no": "Non",
    },
    "Немецкий": {
        "title": "Klicker", "hit": "Treffer! +1 Punkt!", "miss": "Daneben :(",
        "points": "Punkte: {}", "start_challenge": "Klicke zum Starten!",
        "click_now": "JETZT KLICKEN!",
        "score_message": "{} Klicks in 1 Sekunde!",
        "inventory": "Inventar", "potion": "Doppelte Punkte (10 Min)",
        "potion_active": "Aktiv! Verbleibend: {} Sek",
        "potion_inactive": "Benutzen: 10 Min x2", "use": "Benutzen",
        "back": "Zurueck", "btn_inventory": "Inventar", "btn_shop": "Laden",
        "btn_authors": "Autoren", "btn_settings": "Einstellungen",
        "settings_title": "Einstellungen", "language_label": "Sprache:",
        "sound_label": "Sound:", "sound_on": "Ein", "sound_off": "Aus",
        "save_button": "Einstellungen speichern",
        "reset_button": "Fortschritt zuruecksetzen",
        "reset_confirm": "Sind Sie sicher, dass Sie den\ngesamten Fortschritt loeschen moechten?\n\nDiese Aktion kann nicht rueckgaengig gemacht werden!",
        "reset_done": "Fortschritt erfolgreich zurueckgesetzt!",
        "reset_error": "Fehler beim Zuruecksetzen",
        "tab_potions": "Traenke", "tab_skins": "Skins",
        "skins_balls": "Baelle", "skins_baskets": "Koerbe",
        "save_success": "Einstellungen gespeichert!",
        "save_error": "Fehler beim Speichern!",
        "button_click": "Klick!",
        "shop_tab_upgrades": "Verbesserungen", "shop_tab_balls": "Baelle", "shop_tab_baskets": "Koerbe",
        "shop_buy": "Kaufen", "shop_owned": "Besessen",
        "shop_price": "{} Punkte", "shop_not_enough": "Nicht genug Punkte!",
        "shop_coming_soon": "Demnaechst verfuegbar...",
        "dialog_yes": "Ja", "dialog_no": "Nein",
    },
    "Китайский": {
        "title": "点击器", "hit": "击中！+1 分！", "miss": "未命中 :(",
        "points": "分数: {}", "start_challenge": "点击开始！",
        "click_now": "立即点击！",
        "score_message": "1秒内点击 {} 次！",
        "inventory": "背包", "potion": "双倍积分 (10分钟)",
        "potion_active": "生效中！剩余时间：{} 秒",
        "potion_inactive": "使用：10分钟双倍", "use": "使用",
        "back": "返回", "btn_inventory": "背包", "btn_shop": "商店",
        "btn_authors": "作者", "btn_settings": "设置",
        "settings_title": "设置", "language_label": "语言:",
        "sound_label": "声音:", "sound_on": "开启", "sound_off": "关闭",
        "save_button": "保存设置", "reset_button": "重置进度",
        "reset_confirm": "您确定要删除所有进度吗？\n\n此操作无法撤销！",
        "reset_done": "进度已成功重置！",
        "reset_error": "重置进度失败",
        "tab_potions": "药水", "tab_skins": "皮肤",
        "skins_balls": "球", "skins_baskets": "篮筐",
        "save_success": "设置已保存！",
        "save_error": "保存设置失败！",
        "button_click": "点击！",
        "shop_tab_upgrades": "升级", "shop_tab_balls": "球", "shop_tab_baskets": "篮筐",
        "shop_buy": "购买", "shop_owned": "已拥有",
        "shop_price": "{} 分", "shop_not_enough": "分数不足！",
        "shop_coming_soon": "即将推出...",
        "dialog_yes": "是", "dialog_no": "否",
    },
}


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Basketball Click")

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "animation", "icon.jpg")
        if os.path.exists(icon_path):
            try:
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
            except Exception:
                pass

        self.clock = pygame.time.Clock()
        self.running = True
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.settings = self._load_settings()
        self.game = ClickerGame()
        self.current_lang = self.settings.get("language", "Русский")
        self.translations = TRANSLATIONS

        self.dialog = Dialog()

        self.current_screen = "game"
        self.screens = {
            "game": GameScreen(self),
            "settings": None,
            "inventory": None,
            "shop": ShopScreen(self),
            "authors": AuthorsScreen(self),
        }

        self.back_btn_rect = pygame.Rect(*BACK_BTN_RECT)

        self._set_icon_caption()

    def _set_icon_caption(self):
        tr = self.translations.get(self.current_lang, TRANSLATIONS["Русский"])
        pygame.display.set_caption(strip_emoji(tr["title"]))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on_closing()
                    return

                if self.dialog.active:
                    self.dialog.handle_event(event)
                    continue

                if self.current_screen != "game":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.back_btn_rect.collidepoint(event.pos):
                            self.switch_screen("game")
                            continue

                self.screens[self.current_screen].handle_event(event)

            self.screens[self.current_screen].update()

            self.screen.fill((240, 240, 240))
            self.screens[self.current_screen].draw(self.screen)

            if self.current_screen != "game":
                self._draw_back_button()

            if self.dialog.active:
                self.dialog.draw(self.screen)

            self._draw_glitch_label()

            pygame.display.flip()
            self.clock.tick(60)

    def switch_screen(self, name):
        if name != "game":
            if name == "settings":
                self.screens["settings"] = SettingsScreen(self)
            elif name == "inventory":
                self.screens["inventory"] = InventoryScreen(self)
            elif name == "shop":
                self.screens["shop"] = ShopScreen(self)
        self.current_screen = name

    def set_language(self, lang):
        self.current_lang = lang
        self.settings["language"] = lang
        self.save_settings()
        self._set_icon_caption()
        if "game" in self.screens and self.screens["game"]:
            self.screens["game"].set_language()

    def apply_skins(self):
        if "game" in self.screens and self.screens["game"]:
            self.screens["game"].apply_skins()

    def _draw_back_button(self):
        tr = self.translations.get(self.current_lang, TRANSLATIONS["Русский"])
        mouse_over = self.back_btn_rect.collidepoint(pygame.mouse.get_pos())
        color = (200, 220, 255) if mouse_over else (173, 216, 230)
        pygame.draw.rect(self.screen, color, self.back_btn_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), self.back_btn_rect, 1, border_radius=8)
        font = get_font(14, bold=True)
        txt = strip_emoji(tr["back"])
        txt_surf = font.render(txt, True, (0, 0, 0))
        self.screen.blit(txt_surf, (self.back_btn_rect.centerx - txt_surf.get_width() // 2,
                                    self.back_btn_rect.centery - txt_surf.get_height() // 2))

    def _draw_glitch_label(self):
        font = get_font(10)
        txt = font.render("GlitchHunters", True, (0, 0, 200))
        self.screen.blit(txt, (10, HEIGHT - 25))

    def on_closing(self):
        self.game.save_game()
        self.save_settings()
        self.running = False
        pygame.quit()

    def _load_settings(self):
        settings_file = os.path.join(self.base_dir, "settings.json")
        defaults = {
            "sound": True, "language": "Русский",
            "skin_ball": "ball1.png", "skin_basket": "basket.png",
            "inventory_balls": ["ball1.png"], "inventory_baskets": ["basket.png"]
        }
        if not os.path.exists(settings_file):
            try:
                with open(settings_file, "w", encoding="utf-8") as f:
                    json.dump(defaults, f, ensure_ascii=False, indent=4)
            except Exception:
                pass
            return dict(defaults)
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            defaults.update(data)
            return defaults
        except Exception:
            return dict(defaults)

    def save_settings(self):
        settings_file = os.path.join(self.base_dir, "settings.json")
        try:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception:
            pass


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
