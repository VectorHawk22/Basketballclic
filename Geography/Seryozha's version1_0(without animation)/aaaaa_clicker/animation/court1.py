import tkinter as tk
import os
from PIL import Image, ImageTk


class CourtSuccess:
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_running = False
        self.anim_dir = os.path.dirname(os.path.abspath(__file__))
        self.images = {}

        try:
            man_path = os.path.join(self.anim_dir, "man.png")
            basket_path = os.path.join(self.anim_dir, "basket.png")
            if os.path.exists(man_path):
                img = Image.open(man_path)
                img = img.resize((120, 120))
                self.images['man'] = ImageTk.PhotoImage(img)
            if os.path.exists(basket_path):
                img = Image.open(basket_path)
                img = img.resize((100, 100))
                self.images['basket'] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"️ Картинки court1: {e}")

        self.draw_court()

    def draw_court(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.delete("all")

        # === ФОН ===
        # Небо
        self.canvas.create_rectangle(0, 0, width, height * 0.6, fill="#42AAFF", outline="")
        # Пол
        self.floor_y = height * 0.6
        self.canvas.create_rectangle(0, self.floor_y, width, height, fill="#D16A20", outline="")
        # Линия пола
        self.canvas.create_line(0, self.floor_y, width, self.floor_y, fill="#8B4513", width=2)

        # === КОРЗИНА (справа) ===
        self.basket_x = width * 0.88
        self.basket_y = height * 0.35
        if 'basket' in self.images:
            self.basket_item = self.canvas.create_image(self.basket_x, self.basket_y,
                                                        image=self.images['basket'], anchor=tk.CENTER)
        else:
            self.basket_item = self.canvas.create_oval(
                self.basket_x - 30, self.basket_y - 30,
                self.basket_x + 30, self.basket_y + 30,
                fill="orange", width=4)
            # Щит
            self.canvas.create_line(
                self.basket_x + 20, self.basket_y - 50,
                self.basket_x + 20, self.basket_y + 10,
                fill="white", width=3)

        # === ИГРОК (стоит на полу, слева) ===
        self.man_x = width * 0.18
        self.man_y = self.floor_y  # На полу!
        if 'man' in self.images:
            self.man_item = self.canvas.create_image(
                self.man_x,
                self.man_y - 40,
                image=self.images['man'],
                anchor=tk.CENTER
            )

        else:
            # Тело
            self.man_item = self.canvas.create_rectangle(
                self.man_x - 22, self.man_y - 90,
                self.man_x + 22, self.man_y - 20,
                fill="#333")
            # Голова
            self.canvas.create_oval(
                self.man_x - 15, self.man_y - 110,
                self.man_x + 15, self.man_y - 80,
                fill="#FFB0A0")
            # Ноги
            self.canvas.create_line(
                self.man_x - 10, self.man_y - 20,
                self.man_x - 10, self.man_y,
                fill="#333", width=4)
            self.canvas.create_line(
                self.man_x + 10, self.man_y - 20,
                self.man_x + 10, self.man_y,
                fill="#333", width=4)

        # === МЯЧ (летит к корзине) ===
        self.ball_radius = 18
        self.ball_start_x = width * 0.45
        self.ball_start_y = height * 0.45
        self.ball = self.canvas.create_oval(
            self.ball_start_x - self.ball_radius, self.ball_start_y - self.ball_radius,
            self.ball_start_x + self.ball_radius, self.ball_start_y + self.ball_radius,
            fill="#F77F0F", outline="#333", width=3)
        # Полоски на мяче
        self.canvas.create_arc(
            self.ball_start_x - self.ball_radius, self.ball_start_y - self.ball_radius,
            self.ball_start_x + self.ball_radius, self.ball_start_y + self.ball_radius,
            start=30, extent=120, outline="#333", width=2, style=tk.ARC)

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
        self.is_running = True
        self.ball_x = self.ball_start_x
        self.ball_y = self.ball_start_y
        self.falling = False
        self.canvas.coords(self.ball,
                           self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                           self.ball_x + self.ball_radius, self.ball_y + self.ball_radius)
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
                return
            else:
                self.is_running = False
                return

        if abs(self.ball_x - self.target_x) < 7 and abs(self.ball_y - self.target_y) < 7:
            self.falling = True
            self.ball_x = self.target_x
            self.canvas.coords(self.ball,
                               self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                               self.ball_x + self.ball_radius, self.ball_y + self.ball_radius)
            self.canvas.after(30, self.animate)
            return

        if self.ball_x < self.target_x:
            self.ball_x += self.step
        if self.ball_x > self.target_x:
            self.ball_x -= self.step
        if self.ball_y > self.target_y:
            self.ball_y -= self.step

        self.canvas.coords(self.ball,
                           self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                           self.ball_x + self.ball_radius, self.ball_y + self.ball_radius)
        self.canvas.after(30, self.animate)

    def stop(self):
        self.is_running = False