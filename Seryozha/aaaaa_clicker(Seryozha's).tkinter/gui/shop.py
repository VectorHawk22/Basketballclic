import tkinter as tk
import os
from PIL import Image, ImageTk


class ShopManager:
    BALL_ITEMS = [
        {"file": "ball2.png", "name": "Ball 2", "price": 500},
        {"file": "ball3.png", "name": "Ball 3", "price": 500},
        {"file": "ball4.png", "name": "Ball 4", "price": 500},
    ]
    BASKET_ITEMS = [
        {"file": "basket4.png", "name": "Hoop 4", "price": 500},
        {"file": "basket3.png", "name": "Hoop 3", "price": 800},
        {"file": "basket2.png", "name": "Hoop 2", "price": 1000},
    ]

    def __init__(self, parent, game, translations, current_lang):
        self.parent = parent
        self.game = game
        self.translations = translations
        self.current_lang = current_lang
        self.tr = self.translations[self.current_lang]

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.animation_dir = os.path.join(self.base_dir, "animation")

        self.shop_frame = tk.Frame(parent.left_frame)
        self.active_tab = None
        self.tab_buttons = {}
        self.tab_container = None
        self._thumb_refs = []

    def open(self):
        self.tr = self.translations[self.current_lang]

        for widget in self.shop_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.shop_frame,
            text=self.tr["btn_shop"],
            font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))

        tab_bar = tk.Frame(self.shop_frame)
        tab_bar.pack(pady=(0, 5))

        self.tab_buttons = {
            "upgrades": tk.Button(
                tab_bar, text=self.tr["shop_tab_upgrades"],
                font=("Arial", 10, "bold"), width=14,
                command=lambda: self.show_tab("upgrades")
            ),
            "balls": tk.Button(
                tab_bar, text=self.tr["shop_tab_balls"],
                font=("Arial", 10, "bold"), width=14,
                command=lambda: self.show_tab("balls")
            ),
            "baskets": tk.Button(
                tab_bar, text=self.tr["shop_tab_baskets"],
                font=("Arial", 10, "bold"), width=14,
                command=lambda: self.show_tab("baskets")
            ),
        }
        for btn in self.tab_buttons.values():
            btn.pack(side=tk.LEFT, padx=4)

        self.tab_container = tk.Frame(self.shop_frame)
        self.tab_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.show_tab("balls")

        self.shop_frame.pack(fill=tk.BOTH, expand=True)
        self.parent._show_back_button(self.close)

    def show_tab(self, name):
        self.active_tab = name
        self._thumb_refs = []

        for key, btn in self.tab_buttons.items():
            if key == name:
                btn.config(bg="lightblue", relief="solid", bd=2)
            else:
                btn.config(bg="SystemButtonFace", relief="flat", bd=1)

        for widget in self.tab_container.winfo_children():
            widget.destroy()

        if name == "upgrades":
            self.build_upgrades_tab()
        elif name == "balls":
            self.build_balls_tab()
        elif name == "baskets":
            self.build_baskets_tab()

    def build_upgrades_tab(self):
        tk.Label(
            self.tab_container,
            text=self.tr["shop_coming_soon"],
            font=("Arial", 12),
            fg="gray"
        ).pack(pady=40)

    def build_balls_tab(self):
        inv = self.parent.settings.get("inventory_balls", [])
        self._build_item_grid(self.BALL_ITEMS, inv, "ball")

    def build_baskets_tab(self):
        inv = self.parent.settings.get("inventory_baskets", [])
        self._build_item_grid(self.BASKET_ITEMS, inv, "basket")

    def _build_item_grid(self, items, owned, kind):
        canvas = tk.Canvas(self.tab_container, highlightthickness=0, bg="SystemButtonFace")
        scrollbar = tk.Scrollbar(self.tab_container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for item in items:
            self._make_shop_item(inner, item, item["file"] in owned, kind)

    def _make_shop_item(self, parent, item, owned, kind):
        frame = tk.Frame(parent, relief="ridge", bd=1, padx=8, pady=6)
        frame.pack(fill=tk.X, padx=5, pady=4)

        thumb = self._load_thumb(os.path.join(self.animation_dir, item["file"]))
        if thumb:
            img_label = tk.Label(frame, image=thumb)
            img_label.image = thumb
            self._thumb_refs.append(thumb)
        else:
            img_label = tk.Label(frame, text="?", font=("Arial", 20))
        img_label.pack(side=tk.LEFT, padx=(0, 10))

        info = tk.Frame(frame)
        info.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(info, text=item["name"], font=("Arial", 11, "bold"), anchor="w").pack(fill=tk.X)

        if owned:
            tk.Label(
                info, text=self.tr["shop_owned"],
                font=("Arial", 10), fg="green", anchor="w"
            ).pack(fill=tk.X)
        else:
            price_text = self.tr["shop_price"].format(item["price"])
            tk.Label(info, text=price_text, font=("Arial", 10), fg="#b35900", anchor="w").pack(fill=tk.X)
            btn = tk.Button(
                frame, text=self.tr["shop_buy"],
                font=("Arial", 9, "bold"), bg="lightgreen",
                command=lambda i=item, k=kind: self.buy_item(i, k)
            )
            btn.pack(side=tk.RIGHT, padx=5)

    def buy_item(self, item, kind):
        points = self.game.get_points()
        if points < item["price"]:
            self.parent.label_result.config(
                text=self.tr["shop_not_enough"], fg="red"
            )
            return

        self.game.points -= item["price"]
        self.game.save_game()

        inv_key = "inventory_balls" if kind == "ball" else "inventory_baskets"
        inv = self.parent.settings.get(inv_key, [])
        if item["file"] not in inv:
            inv.append(item["file"])
            self.parent.settings[inv_key] = inv

        self.parent.save_settings()
        self.parent.update_ui()

        self.open()

    def _load_thumb(self, path, box=50):
        try:
            if not os.path.exists(path):
                return None
            img = Image.open(path).convert("RGBA")
            mask = img.getchannel("A").point(lambda a: 255 if a > 100 else 0)
            bbox = mask.getbbox()
            if bbox:
                img = img.crop(bbox)
            w, h = img.size
            scale = min(box / float(w), box / float(h))
            size = (max(1, int(w * scale)), max(1, int(h * scale)))
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def close(self):
        self.shop_frame.pack_forget()
        self.parent.show_game()
        self.parent._hide_back_button()
        self.parent.update_ui()

    def update_language(self, new_lang):
        self.current_lang = new_lang
        self.tr = self.translations[self.current_lang]
