import os
import tkinter as tk
from PIL import Image, ImageTk


class CourtFail:
    def __init__(self, canvas):
        self.canvas = canvas
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Масштабирование под canvas 420x240
        self.scale_x = 420 / 800
        self.scale_y = 240 / 500

        try:
            self.img_man = tk.PhotoImage(file=os.path.join(self.base_dir, "man.png"))
            self.img_basket = tk.PhotoImage(file=os.path.join(self.base_dir, "basket.png"))
            img_ball = Image.open(os.path.join(self.base_dir, "ball3.png"))
            self.img_ball = ImageTk.PhotoImage(img_ball.resize((26, 19), Image.Resampling.LANCZOS))
        except Exception as e:
            print(f"Ошибка загрузки картинок промаха: {e}")
            self.img_man = self.img_basket = self.img_ball = None

        # Масштабированные координаты
        self.ball_x = int(550 * self.scale_x)
        self.ball_y = int(285 * self.scale_y)
        self.target_x = int(760 * self.scale_x)
        self.target_y = int(190 * self.scale_y)
        self.step = 3
        self.falling = False
        self.bouncing = False
        self.fall_speed = 5
        self.gravity = 0.5
        self.bounce_height = int(290 * self.scale_y)
        self.is_animating = False
        self.anim_id = None

    def draw_court(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 420, 144, fill="#42AAFF")
        self.canvas.create_rectangle(0, 144, 420, 240, fill="#D16A20")
        if self.img_basket:
            self.canvas.create_image(int(450 * self.scale_x), int(75 * self.scale_y),
                                     image=self.img_basket, anchor=tk.NW)
        if self.img_man:
            self.canvas.create_image(int(222 * self.scale_x), int(85 * self.scale_y),
                                     image=self.img_man, anchor=tk.NW)
        if self.img_ball:
            self.ball_obj = self.canvas.create_image(self.ball_x, self.ball_y, image=self.img_ball)

    def start_animation(self):
        self.draw_court()
        self.ball_x = int(550 * self.scale_x)
        self.ball_y = int(285 * self.scale_y)
        self.falling = False
        self.bouncing = False
        self.is_animating = True
        self._move_ball()

    def stop(self):
        self.is_animating = False
        if self.anim_id:
            self.canvas.after_cancel(self.anim_id)

    def _move_ball(self):
        if not self.is_animating or not self.img_ball:
            return

        if self.bouncing:
            if self.ball_y < self.bounce_height:
                self.ball_y += self.fall_speed
                self.fall_speed += self.gravity
                self.canvas.coords(self.ball_obj, self.ball_x, self.ball_y)
                self.anim_id = self.canvas.after(50, self._move_ball)
                return
            else:
                self.stop()
                return

        # Проверка попадания в корзину (промах - мяч пролетает мимо)
        if abs(self.ball_x - self.target_x) < 5 and self.ball_y < self.target_y + 10:
            self.bouncing = True
            self.fall_speed = -10
            self.ball_y = self.target_y - 10
            self.canvas.coords(self.ball_obj, self.ball_x, self.ball_y)
            self.anim_id = self.canvas.after(50, self._move_ball)
            return

        if self.ball_x < self.target_x: self.ball_x += self.step
        if self.ball_x > self.target_x: self.ball_x -= self.step
        if self.ball_y > self.target_y: self.ball_y -= self.step

        self.canvas.coords(self.ball_obj, self.ball_x, self.ball_y)
        self.anim_id = self.canvas.after(50, self._move_ball)