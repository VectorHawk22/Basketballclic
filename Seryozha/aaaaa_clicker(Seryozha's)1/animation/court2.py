import os
import tkinter as tk
from PIL import Image, ImageTk


class CourtFail:
    def __init__(self, canvas):
        self.canvas = canvas
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Загрузка изображений (обрезаются до видимого содержимого)
        self.img_man = None
        self.img_basket = None
        self.img_ball = None
        self.ball_obj = None
        self._pil_man = None
        self._pil_basket = None
        self._pil_ball = None
        self._prepared_size = None
        self.load_images()

        # Размеры объектов (пересчитываются в prepare_images)
        self.man_w = 0
        self.man_h = 0
        self.basket_w = 0
        self.basket_h = 0

        # Параметры анимации
        self.ball_x = 0
        self.ball_y = 0
        self.target_x = 0
        self.target_y = 0
        self.step = 3
        self.ball_r = 8
        self.falling = False
        self.bouncing = False
        self.fall_speed = 5
        self.gravity = 0.5
        self.bounce_height = 0
        self.is_animating = False
        self.anim_id = None

    def _load_cropped(self, filename):
        """Загрузка изображения с обрезкой прозрачных полей"""
        path = os.path.join(self.base_dir, filename)
        if not os.path.exists(path):
            print(f"⚠️ Файл не найден: {path}")
            return None
        try:
            img = Image.open(path).convert("RGBA")
            mask = img.getchannel("A").point(lambda a: 255 if a > 100 else 0)
            bbox = mask.getbbox()
            if bbox:
                img = img.crop(bbox)
            return img
        except Exception as e:
            print(f"Ошибка загрузки {filename}: {e}")
            return None

    def load_images(self):
        """Загрузка изображений"""
        try:
            self._pil_man = self._load_cropped("man.png")
            self._pil_basket = self._load_cropped("basket.png")
            self._pil_ball = self._load_cropped("ball3.png")
        except Exception as e:
            print(f"Ошибка загрузки изображений промаха: {e}")

    @staticmethod
    def _fit_height(pil_img, target_h):
        """Размер с сохранением пропорций по высоте"""
        w, h = pil_img.size
        return (max(1, int(w * target_h / h)), max(1, int(target_h)))

    def prepare_images(self, canvas_width, canvas_height):
        """Подготовка PhotoImage под размер canvas (с кэшем)"""
        key = (canvas_width, canvas_height)
        if self._prepared_size == key and self.img_man and self.img_basket and self.img_ball:
            return

        sky_height = int(canvas_height * 0.65)

        # Мальчик заметно ниже кольца, мяч маленький
        man_target_h = max(16, int(sky_height * 0.60))
        basket_target_h = max(24, int(sky_height * 0.95))
        ball_target = max(10, int(man_target_h * 0.16))

        if self._pil_man:
            size = self._fit_height(self._pil_man, man_target_h)
            self.man_w, self.man_h = size
            self.img_man = ImageTk.PhotoImage(
                self._pil_man.resize(size, Image.Resampling.LANCZOS))

        if self._pil_basket:
            size = self._fit_height(self._pil_basket, basket_target_h)
            self.basket_w, self.basket_h = size
            self.img_basket = ImageTk.PhotoImage(
                self._pil_basket.resize(size, Image.Resampling.LANCZOS))

        if self._pil_ball:
            size = self._fit_height(self._pil_ball, ball_target)
            self.img_ball = ImageTk.PhotoImage(
                self._pil_ball.resize(size, Image.Resampling.LANCZOS))
            self.ball_r = max(5, size[0] // 2)

        self._prepared_size = key

    def draw_court(self):
        """Рисование поля"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10:
            canvas_width = 420
        if canvas_height < 10:
            canvas_height = 200

        self.canvas.delete("all")

        # Небо 65%
        sky_height = int(canvas_height * 0.65)

        self.canvas.create_rectangle(0, 0, canvas_width, sky_height, fill="#42AAFF")
        self.canvas.create_rectangle(0, sky_height, canvas_width, canvas_height, fill="#D16A20")

        # Масштабируем спрайты под реальный размер canvas
        self.prepare_images(canvas_width, canvas_height)

        # Корзина (у правого края, anchor=SE)
        basket_right_x = int(canvas_width * 0.97)
        if self.img_basket:
            self.canvas.create_image(basket_right_x, sky_height, image=self.img_basket, anchor=tk.SE)
        basket_left_x = basket_right_x - self.basket_w

        # Человек (anchor=SW)
        man_x = int(canvas_width * 0.06)
        if self.img_man:
            self.canvas.create_image(man_x, sky_height, image=self.img_man, anchor=tk.SW)

        # Мяч в руках (руки вытянуты вперёд на уровне ~65% роста)
        self.ball_x = man_x + int(self.man_w * 0.8)
        self.ball_y = sky_height - int(self.man_h * 0.65)

        # ЦЕЛЬ - кольцо (перекладина: ~22% ширины, ~20% высоты картинки корзины)
        self.target_x = basket_left_x + int(self.basket_w * 0.22)
        self.target_y = (sky_height - self.basket_h) + int(self.basket_h * 0.20)
        self.bounce_height = sky_height - int(self.man_h * 0.5)

        if self.img_ball:
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
            # Параметры полёта: дуга (Безье) с контрольной точкой над кольцом,
            # чтобы мяч опускался в него сверху
            self.arc_start_x = self.ball_x
            self.arc_start_y = self.ball_y
            dist = abs(self.target_x - self.ball_x)
            self.ctrl_x = self.target_x - max(30, int(dist * 0.12))
            self.ctrl_y = self.ball_r + 2
            steps = max(1, dist // self.step)
            self.t_progress = 0.0
            self.t_speed = 1.0 / steps
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

        sky_height = int(self.canvas.winfo_height() * 0.65)
        # Земля - линия поля; мяч останавливается, когда касается её нижним краем
        ground_y = sky_height - self.ball_r

        # Отскок после удара о кольцо
        if self.bouncing:
            if self.ball_y < ground_y:
                self.ball_y += self.fall_speed
                self.fall_speed += self.gravity
                # не вылетать за верх canvas
                if self.ball_y < self.ball_r:
                    self.ball_y = self.ball_r
                    self.fall_speed = 0
                if self.ball_y > ground_y:
                    self.ball_y = ground_y
                self.canvas.coords(self.ball_obj, self.ball_x, self.ball_y)
                self.anim_id = self.canvas.after(50, self._move_ball)
                return
            else:
                self.stop()
                return

        # Полёт по дуге (квадратичная Безье) - мяч приходит в кольцо сверху
        self.t_progress = min(1.0, self.t_progress + self.t_speed)
        t = self.t_progress
        mt = 1.0 - t
        self.ball_x = int(mt * mt * self.arc_start_x + 2 * mt * t * self.ctrl_x + t * t * self.target_x)
        self.ball_y = int(mt * mt * self.arc_start_y + 2 * mt * t * self.ctrl_y + t * t * self.target_y)

        if t >= 1.0:
            # Мяч долетел до кольца - отскок (промах)
            self.bouncing = True
            self.fall_speed = -8

        self.canvas.coords(self.ball_obj, self.ball_x, self.ball_y)
        self.anim_id = self.canvas.after(50, self._move_ball)