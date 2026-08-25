import pygame
import platform


def get_font(size, bold=False):
    try:
        if platform.system() == "Windows":
            name = "Microsoft YaHei" if not bold else "Microsoft YaHei Bold"
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
    except Exception:
        pass
    return pygame.font.SysFont("Arial", size, bold=bold)


def strip_emoji(text):
    clean = []
    for ch in text:
        if ord(ch) > 0xFFFF:
            continue
        clean.append(ch)
    return "".join(clean)


def render_text(surface, text, font, color, x, y, max_width=None):
    lines = strip_emoji(text).split("\n")
    y_offset = 0
    for line in lines:
        surf = font.render(line, True, color)
        if max_width and surf.get_width() > max_width:
            words = line.split(" ")
            current = ""
            for word in words:
                test = current + (" " if current else "") + word
                if font.size(test)[0] > max_width and current:
                    surface.blit(font.render(current, True, color), (x, y + y_offset))
                    y_offset += font.get_linesize()
                    current = word
                else:
                    current = test
            if current:
                surface.blit(font.render(current, True, color), (x, y + y_offset))
                y_offset += font.get_linesize()
        else:
            surface.blit(surf, (x, y + y_offset))
            y_offset += font.get_linesize()
    return y_offset


def text_height(font, text):
    lines = strip_emoji(text).split("\n")
    return len(lines) * font.get_linesize()


class Screen:
    def __init__(self, app):
        self.app = app

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass


class Button:
    def __init__(self, rect, text, font_size=14, bg_color=(200, 200, 200),
                 text_color=(0, 0, 0), border_radius=8, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = get_font(font_size, bold=True)
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.callback = callback
        self.hovered = False

    def set_text(self, text):
        self.text = text

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()
                return True
        return False

    def draw(self, surface):
        color = tuple(min(255, c + 30) for c in self.bg_color) if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 1, border_radius=self.border_radius)
        txt = strip_emoji(self.text)
        text_surf = self.font.render(txt, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class Checkbox:
    def __init__(self, rect, text, font_size=12, checked=True, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = get_font(font_size)
        self.checked = checked
        self.callback = callback
        self.box_size = 20
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                if self.callback:
                    self.callback(self.checked)
                return True
        return False

    def draw(self, surface):
        box_y = self.rect.centery - self.box_size // 2
        box_rect = pygame.Rect(self.rect.x, box_y, self.box_size, self.box_size)
        color = (255, 255, 255) if self.hovered else (240, 240, 240)
        pygame.draw.rect(surface, color, box_rect, border_radius=3)
        pygame.draw.rect(surface, (100, 100, 100), box_rect, 2, border_radius=3)
        if self.checked:
            inner = box_rect.inflate(-6, -6)
            pygame.draw.rect(surface, (0, 150, 0), inner, border_radius=2)
        txt = strip_emoji(self.text)
        text_surf = self.font.render(txt, True, (0, 0, 0))
        surface.blit(text_surf, (self.rect.x + self.box_size + 8,
                                 self.rect.centery - text_surf.get_height() // 2))


class Dropdown:
    def __init__(self, rect, options, font_size=13, selected=None, callback=None):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.font = get_font(font_size)
        self.callback = callback
        self.selected = selected or (options[0] if options else "")
        self.open = False
        self.option_height = 30

    def set_selected(self, value):
        self.selected = value

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
                return True
            elif self.open:
                for i, opt in enumerate(self.options):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.option_height,
                                           self.rect.width, self.option_height)
                    if opt_rect.collidepoint(event.pos):
                        self.selected = opt
                        self.open = False
                        if self.callback:
                            self.callback(opt)
                        return True
                self.open = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button != 1:
            self.open = False
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=4)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2, border_radius=4)
        txt = strip_emoji(self.selected)
        text_surf = self.font.render(txt, True, (0, 0, 0))
        surface.blit(text_surf, (self.rect.x + 8, self.rect.centery - text_surf.get_height() // 2))
        ax = self.rect.right - 18
        ay = self.rect.centery
        if self.open:
            pygame.draw.polygon(surface, (0, 0, 0),
                                [(ax, ay + 4), (ax + 8, ay + 4), (ax + 4, ay - 4)])
        else:
            pygame.draw.polygon(surface, (0, 0, 0),
                                [(ax, ay - 4), (ax + 8, ay - 4), (ax + 4, ay + 4)])

        if self.open:
            overlay = pygame.Surface((self.rect.width, len(self.options) * self.option_height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 240))
            surface.blit(overlay, (self.rect.x, self.rect.bottom))
            for i, opt in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.option_height,
                                       self.rect.width, self.option_height)
                if opt_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(surface, (200, 220, 255), opt_rect)
                pygame.draw.rect(surface, (180, 180, 180), opt_rect, 1)
                opt_txt = strip_emoji(opt)
                opt_surf = self.font.render(opt_txt, True, (0, 0, 0))
                surface.blit(opt_surf, (opt_rect.x + 8,
                                        opt_rect.centery - opt_surf.get_height() // 2))


class Dialog:
    def __init__(self):
        self.active = False
        self.title = ""
        self.message = ""
        self.buttons = []
        self.callback = None
        self._btn_rects = []

    def show_info(self, title, message):
        self.title = title
        self.message = message
        self.buttons = [("OK", True)]
        self.callback = None
        self.active = True

    def show_confirm(self, title, message, on_yes):
        self.title = title
        self.message = message
        self.buttons = [("Yes", True), ("No", False)]
        self.callback = on_yes
        self.active = True

    def handle_event(self, event):
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, text, value in self._btn_rects:
                if rect.collidepoint(event.pos):
                    self.active = False
                    if self.callback:
                        self.callback(value)
                    return True
        return True

    def draw(self, surface):
        if not self.active:
            return
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        box = pygame.Rect(100, 150, 400, 190)
        pygame.draw.rect(surface, (255, 255, 255), box, border_radius=10)
        pygame.draw.rect(surface, (100, 100, 100), box, 2, border_radius=10)

        title_font = get_font(18, bold=True)
        render_text(surface, self.title, title_font, (0, 0, 0), box.x + 20, box.y + 15, box.width - 40)

        msg_font = get_font(14)
        render_text(surface, self.message, msg_font, (60, 60, 60), box.x + 20, box.y + 50, box.width - 40)

        self._btn_rects = []
        btn_w = 120
        btn_h = 35
        total_w = len(self.buttons) * btn_w + max(0, len(self.buttons) - 1) * 15
        btn_x = box.centerx - total_w // 2
        btn_y = box.bottom - 50

        btn_font = get_font(14, bold=True)
        for text, value in self.buttons:
            rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            mouse_over = rect.collidepoint(pygame.mouse.get_pos())
            color = (220, 220, 220) if mouse_over else (200, 200, 200)
            pygame.draw.rect(surface, color, rect, border_radius=5)
            pygame.draw.rect(surface, (100, 100, 100), rect, 1, border_radius=5)
            txt = strip_emoji(text)
            txt_surf = btn_font.render(txt, True, (0, 0, 0))
            surface.blit(txt_surf, (rect.centerx - txt_surf.get_width() // 2,
                                    rect.centery - txt_surf.get_height() // 2))
            self._btn_rects.append((rect, text, value))
            btn_x += btn_w + 15
