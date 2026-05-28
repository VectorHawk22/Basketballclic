import tkinter as tk
import os
from PIL import Image, ImageTk


class CourtSuccess:
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_running = False
        self.anim_dir = os.path.dirname(os.path.abspath(__file__))
        self.images = {}
        self.use_images = False

        try:
            man_path = os.path.join(self.anim_dir, "man.png")
            basket_path = os.path.join(self.anim_dir, "basket.png")

            if os.path.exists(man_path) and os.path.exists(basket_path):
                man_img = Image.open(man_path).resize((100, 140), Image.Resampling.LANCZOS)
                basket_img = Image.open(basket_path).resize((80, 100), Image.Resampling.LANCZOS)

                self.images['man'] = ImageTk.PhotoImage(man_img)
                self.images['basket'] = ImageTk.PhotoImage(basket_img)
                self.use_images = True
                print("✅ Картинки загружены")
            else:
                print("⚠️ Картинки не найдены, используем БОЛЬШУЮ fallback-графику")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

        self.draw_court()

    def draw_court(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 10 or height <= 10:
            return

        self.canvas.delete("all")

        # === ФОН ===
        self.canvas.create_rectangle(0, 0, width, height * 0.6, fill="#42AAFF", outline="")
        self.floor_y = height * 0.6
        self.canvas.create_rectangle(0, self.floor_y, width, height, fill="#D16A20", outline="")
        self.canvas.create_line(0, self.floor_y, width, self.floor_y, fill="#8B4513", width=2)

        # === КОРЗИНА (БОЛЬШАЯ) ===
        self.basket_x = width * 0.88
        self.basket_y = height * 0.35

        if self.use_images and 'basket' in self.images:
            self.basket_item = self.canvas.create_image(self.basket_x, self.basket_y,
                                                        image=self.images['basket'], anchor=tk.CENTER)
        else:
            # Щит - БОЛЬШОЙ
            self.canvas.create_rectangle(
                self.basket_x + 15, self.basket_y - 50,
                self.basket_x + 25, self.basket_y + 30,
                fill="white", outline="gray", width=3
            )
            # Кольцо - БОЛЬШОЕ
            self.canvas.create_oval(
                self.basket_x - 35, self.basket_y - 15,
                self.basket_x + 5, self.basket_y + 15,
                fill="", outline="orange", width=5
            )
            # Сетка
            for i in range(-30, 0, 10):
                self.canvas.create_line(
                    self.basket_x + i, self.basket_y - 10,
                    self.basket_x + i + 5, self.basket_y + 30,
                    fill="white", width=2
                )

        # === ИГРОК (ОЧЕНЬ БОЛЬШОЙ) ===
        self.man_x = width * 0.18
        self.man_y = self.floor_y

        if self.use_images and 'man' in self.images:
            self.man_item = self.canvas.create_image(self.man_x, self.man_y - 50,
                                                     image=self.images['man'], anchor=tk.CENTER)
        else:
            # Тело - ШИРОКОЕ и ВЫСОКОЕ
            self.man_item = self.canvas.create_rectangle(
                self.man_x - 30, self.man_y - 120,
                self.man_x + 30, self.man_y - 40,
                fill="#2E5C8A", outline="black", width=3
            )
            # Голова - БОЛЬШАЯ
            self.canvas.create_oval(
                self.man_x - 25, self.man_y - 155,
                self.man_x + 25, self.man_y - 115,
                fill="#FFB0A0", outline="black", width=3
            )
            # Ноги - ТОЛСТЫЕ
            self.canvas.create_line(
                self.man_x - 20, self.man_y - 40,
                self.man_x - 20, self.man_y,
                fill="#1a1a1a", width=8
            )
            self.canvas.create_line(
                self.man_x + 20, self.man_y - 40,
                self.man_x + 20, self.man_y,
                fill="#1a1a1a", width=8
            )
            # Руки
            self.canvas.create_line(
                self.man_x - 30, self.man_y - 90,
                self.man_x - 50, self.man_y - 70,
                fill="#FFB0A0", width=6
            )
            self.canvas.create_line(
                self.man_x + 30, self.man_y - 90,
                self.man_x + 50, self.man_y - 80,
                fill="#FFB0A0", width=6
            )

        # === МЯЧ ===
        self.ball_radius = 22
        self.ball_start_x = width * 0.45
        self.ball_start_y = height * 0.45
        self.ball = self.canvas.create_oval(
            self.ball_start_x - self.ball_radius, self.ball_start_y - self.ball_radius,
            self.ball_start_x + self.ball_radius, self.ball_start_y + self.ball_radius,
            fill="#F77F0F", outline="#333", width=3
        )
        self.canvas.create_arc(
            self.ball_start_x - self.ball_radius, self.ball_start_y - self.ball_radius,
            self.ball_start_x + self.ball_radius, self.ball_start_y + self.ball_radius,
            start=30, extent=120, outline="#333", width=2, style=tk.ARC
        )

        self.ball_x = self.ball_start_x
        self.ball_y = self.ball_start_y
        self.target_x = self.basket_x
        self.target_y = self.basket_y
        self.falling = False
        self.fall_speed = 7
        self.step = 7

    def start_animation(self):
        if self.is_running:
            return
        self.draw_court()
        self.is_running = True
        self.ball_x = self.ball_start_x
        self.ball_y = self.ball_start_y
        self.falling = False
        self.animate()

    def animate(self):
        if not self.is_running:
            return
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.target_x = width * 0.88
        self.target_y = height * 0.35

        if self.falling:
            if self.ball_y < height * 0.7:
                self.ball_y += self.fall_speed
                self.canvas.coords(self.ball,
                                   self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                                   self.ball_x + self.ball_radius, self.ball_y + self.ball_radius)
                self.canvas.after(30, self.animate)
            else:
                self.is_running = False
            return

        if abs(self.ball_x - self.target_x) < 7 and abs(self.ball_y - self.target_y) < 7:
            self.falling = True
            self.ball_x = self.target_x
            self.canvas.after(30, self.animate)
            return

        if self.ball_x < self.target_x:
            self.ball_x += self.step
        elif self.ball_x > self.target_x:
            self.ball_x -= self.step
        if self.ball_y > self.target_y: self.ball_y -= self.step

        self.canvas.coords(self.ball,
                           self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                           self.ball_x + self.ball_radius, self.ball_y + self.ball_radius)
        self.canvas.after(30, self.animate)

    def stop(self):
        self.is_running = False