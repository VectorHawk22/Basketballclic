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
        self.step = 3
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
            # Картинки в той же папке (animation/)
            man_path = os.path.join(self.base_dir, "man.png")
            basket_path = os.path.join(self.base_dir, "basket.png")
            ball_path = os.path.join(self.base_dir, "ball3.png")

            if os.path.exists(man_path):
                img_man = Image.open(man_path)
                # ЕЩЁ БОЛЬШЕ УВЕЛИЧИВАЕМ человека
                man_width = int(700 * self.scale_x)  # было 500
                man_height = int(900 * self.scale_y)  # было 640
                self.img_man = ImageTk.PhotoImage(img_man.resize((man_width, man_height), Image.Resampling.LANCZOS))
            else:
                print(f"⚠️ Файл не найден: {man_path}")

            if os.path.exists(basket_path):
                img_basket = Image.open(basket_path)
                # ЕЩЁ БОЛЬШЕ УВЕЛИЧИВАЕМ корзину
                basket_width = int(650 * self.scale_x)  # было 450
                basket_height = int(560 * self.scale_y)  # было 390
                self.img_basket = ImageTk.PhotoImage(
                    img_basket.resize((basket_width, basket_height), Image.Resampling.LANCZOS))
            else:
                print(f"⚠️ Файл не найден: {basket_path}")

            if os.path.exists(ball_path):
                img_ball = Image.open(ball_path)
                # НЕМНОГО УВЕЛИЧИВАЕМ мяч
                ball_size = int(80 * self.scale_x)  # было 60
                self.img_ball = ImageTk.PhotoImage(img_ball.resize((ball_size, ball_size), Image.Resampling.LANCZOS))
            else:
                print(f"⚠️ Файл не найден: {ball_path}")

        except Exception as e:
            print(f"Ошибка загрузки изображений промаха: {e}")

    def draw_court(self):
        """Рисование поля с масштабированием"""
        self.canvas.delete("all")

        # Небо и земля
        self.canvas.create_rectangle(0, 0, 420, 144, fill="#42AAFF")
        self.canvas.create_rectangle(0, 144, 420, 240, fill="#D16A20")

        # Корзина - размещаем в финальной точке полета мяча
        if self.img_basket:
            # Корректируем позиционирование для увеличенной корзины
            basket_x = int(710 * self.scale_x) - int(300 * self.scale_x)  # было 200
            basket_y = int(170 * self.scale_y) - int(150 * self.scale_y)  # было 25
            self.canvas.create_image(basket_x, basket_y, image=self.img_basket, anchor=tk.NW)

        # Человек - размещаем ближе к мячу
        if self.img_man:
            # Корректируем позиционирование для увеличенного человека
            man_x = int(500 * self.scale_x) - int(340 * self.scale_x)  # было 230
            man_y = int(200 * self.scale_y) - int(300 * self.scale_y)  # было 200
            self.canvas.create_image(man_x, man_y, image=self.img_man, anchor=tk.NW)

        # Мяч
        if self.img_ball:
            self.ball_x = int(550 * self.scale_x)
            self.ball_y = int(285 * self.scale_y)
            self.target_x = int(710 * self.scale_x)
            self.target_y = int(170 * self.scale_y)
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