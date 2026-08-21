import os
import tkinter as tk
from PIL import Image, ImageTk


class CourtFail:
    def __init__(self, canvas):
        self.canvas = canvas
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Масштабирование
        self.scale_x = 1.0
        self.scale_y = 1.0

        # Загрузка изображений из папки animation
        self.img_man = None
        self.img_basket = None
        self.img_ball = None
        self.ball_obj = None
        self.load_images()

        # Параметры анимации
        self.ball_x = 0
        self.ball_y = 0
        self.target_x = 0
        self.target_y = 0
        self.step = 5
        self.falling = False
        self.bouncing = False
        self.fall_speed = 5
        self.gravity = 0.5
        self.bounce_height = 0
        self.is_animating = False
        self.anim_id = None

    def load_images(self):
        """Загрузка изображений из папки animation"""
        try:
            anim_dir = os.path.join(self.base_dir, "animation")

            man_path = os.path.join(anim_dir, "man.png")
            basket_path = os.path.join(anim_dir, "basket.png")
            ball_path = os.path.join(anim_dir, "ball3.png")

            if os.path.exists(man_path):
                self.img_man = tk.PhotoImage(file=man_path)

            if os.path.exists(basket_path):
                self.img_basket = tk.PhotoImage(file=basket_path)

            if os.path.exists(ball_path):
                img_ball = Image.open(ball_path)
                self.img_ball = ImageTk.PhotoImage(img_ball.resize((40, 30), Image.Resampling.LANCZOS))

        except Exception as e:
            print(f"Ошибка загрузки изображений промаха: {e}")

    def update_scale(self):
        """Обновление масштаба"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 50 and h > 50:
            self.scale_x = w / 800
            self.scale_y = h / 500
            return True
        return False

    def draw_court(self):
        """Рисование поля с масштабированием"""
        self.canvas.delete("all")

        if not self.update_scale():
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Небо и земля
        self.canvas.create_rectangle(0, 0, w, h * 0.6, fill="#42AAFF")
        self.canvas.create_rectangle(0, h * 0.6, w, h, fill="#D16A20")

        # Корзина
        if self.img_basket:
            x = int(450 * self.scale_x)
            y = int(75 * self.scale_y)
            self.canvas.create_image(x, y, image=self.img_basket, anchor=tk.NW)

        # Человек
        if self.img_man:
            x = int(222 * self.scale_x)
            y = int(85 * self.scale_y)
            self.canvas.create_image(x, y, image=self.img_man, anchor=tk.NW)

        # Мяч
        if self.img_ball:
            self.ball_x = int(550 * self.scale_x)
            self.ball_y = int(285 * self.scale_y)
            self.target_x = int(760 * self.scale_x)
            self.target_y = int(190 * self.scale_y)
            self.bounce_height = int(290 * self.scale_y)
            self.ball_obj = self.canvas.create_image(
                self.ball_x, self.ball_y,
                image=self.img_ball
            )

    def start_animation(self):
        """Запуск анимации промаха"""
        self.is_animating = True
        self.falling = False
        self.bouncing = False
        self.fall_speed = 5
        self.draw_court()
        if self.ball_obj:
            self._move_ball()

    def stop(self):
        """Остановка анимации"""
        self.is_animating = False
        if self.anim_id:
            try:
                self.canvas.after_cancel(self.anim_id)
            except:
                pass
            self.anim_id = None

    def _move_ball(self):
        """Движение мяча при промахе"""
        if not self.is_animating or not self.img_ball or not self.ball_obj:
            return

        # Отскок после удара о кольцо
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

        # Проверка попадания в кольцо (промах)
        dx = abs(self.ball_x - self.target_x)
        dy = abs(self.ball_y - self.target_y)

        if dx < 10 and dy < 20:
            self.bouncing = True
            self.fall_speed = -10
            self.ball_y = self.target_y - 10
            self.canvas.coords(self.ball_obj, self.ball_x, self.ball_y)
            self.anim_id = self.canvas.after(50, self._move_ball)
            return

        # Движение к цели
        if self.ball_x < self.target_x:
            self.ball_x += self.step
        if self.ball_x > self.target_x:
            self.ball_x -= self.step
        if self.ball_y > self.target_y:
            self.ball_y -= self.step

        self.canvas.coords(self.ball_obj, self.ball_x, self.ball_y)
        self.anim_id = self.canvas.after(50, self._move_ball)