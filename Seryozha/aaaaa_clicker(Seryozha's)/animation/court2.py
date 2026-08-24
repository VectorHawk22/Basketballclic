import os
import tkinter as tk
from PIL import Image, ImageTk


class CourtFail:
    def __init__(self, canvas):
        self.canvas = canvas
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Масштабирование под canvas
        self.scale_x = 420 / 800
        self.scale_y = 240 / 500

        # Загрузка изображений
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
        self.step = 3
        self.falling = False
        self.bouncing = False
        self.fall_speed = 5
        self.gravity = 0.5
        self.bounce_height = 0
        self.is_animating = False
        self.anim_id = None

    def load_images(self):
        """Загрузка изображений"""
        try:
            man_path = os.path.join(self.base_dir, "man.png")
            basket_path = os.path.join(self.base_dir, "basket.png")
            ball_path = os.path.join(self.base_dir, "ball3.png")

            if os.path.exists(man_path):
                img_man = Image.open(man_path)
                man_width = int(350 * self.scale_x)
                man_height = int(480 * self.scale_y)
                self.img_man = ImageTk.PhotoImage(img_man.resize((man_width, man_height), Image.Resampling.LANCZOS))
            else:
                print(f"⚠️ Файл не найден: {man_path}")

            if os.path.exists(basket_path):
                img_basket = Image.open(basket_path)
                basket_width = int(550 * self.scale_x)
                basket_height = int(470 * self.scale_y)
                self.img_basket = ImageTk.PhotoImage(
                    img_basket.resize((basket_width, basket_height), Image.Resampling.LANCZOS))
            else:
                print(f"⚠️ Файл не найден: {basket_path}")

            if os.path.exists(ball_path):
                img_ball = Image.open(ball_path)
                ball_size = int(70 * self.scale_x)
                self.img_ball = ImageTk.PhotoImage(img_ball.resize((ball_size, ball_size), Image.Resampling.LANCZOS))
            else:
                print(f"⚠️ Файл не найден: {ball_path}")

        except Exception as e:
            print(f"Ошибка загрузки изображений промаха: {e}")

    def draw_court(self):
        """Рисование поля"""
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10:
            canvas_width = 420
        if canvas_height < 10:
            canvas_height = 200

        # Небо 65%
        sky_height = int(canvas_height * 0.65)

        self.canvas.create_rectangle(0, 0, canvas_width, sky_height, fill="#42AAFF")
        self.canvas.create_rectangle(0, sky_height, canvas_width, canvas_height, fill="#D16A20")

        man_w = int(350 * self.scale_x)
        man_h = int(480 * self.scale_y)
        basket_w = int(550 * self.scale_x)
        basket_h = int(470 * self.scale_y)

        # Корзина (anchor=SW)
        basket_x = int(canvas_width * 0.70)
        self.canvas.create_image(basket_x, sky_height, image=self.img_basket, anchor=tk.SW)

        # Человек (anchor=SW)
        man_x = int(canvas_width * 0.06)
        self.canvas.create_image(man_x, sky_height, image=self.img_man, anchor=tk.SW)

        # Мяч в руках
        ball_x = man_x + int(man_w * 0.5)
        ball_y = sky_height - int(man_h * 0.5)
        self.ball_x = ball_x
        self.ball_y = ball_y

        self.target_x = basket_x + int(basket_w * 0.35)
        self.target_y = sky_height - int(basket_h * 0.55)
        self.bounce_height = sky_height - 100

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

        canvas_height = self.canvas.winfo_height()
        if canvas_height < 10:
            canvas_height = 200
        ground_y = canvas_height - 10

        # Отскок после удара о кольцо
        if self.bouncing:
            if self.ball_y < ground_y:
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