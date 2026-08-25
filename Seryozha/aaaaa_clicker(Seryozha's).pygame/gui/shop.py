import pygame
from gui import Screen, get_font, strip_emoji, render_text


class ShopScreen(Screen):
    def __init__(self, app):
        super().__init__(app)

    def draw(self, surface):
        tr = self.app.translations[self.app.current_lang]
        font_title = get_font(20, bold=True)
        font_msg = get_font(16)
        font_detail = get_font(13)

        render_text(surface, tr["btn_shop"], font_title, (0, 0, 0), 40, 30, 520)
        render_text(surface, "Shop temporarily closed", font_msg, (120, 120, 120), 40, 100, 520)
        render_text(surface, "Under construction,\nnew items coming soon!", font_detail, (140, 140, 140), 40, 160, 520)
