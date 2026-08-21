import tkinter as tk
import os
from PIL import Image, ImageTk


class CourtFail:
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_running = False
        self.anim_dir = os.path.dirname(os.path.abspath(__file__))
        self.images = {}
        self.use_images = False
        self.score = 0

        try:
            # Пути к изображениям (как в court2_my.py)
            man_path = os.path.join(self.anim_dir, "man.png")
            basket_path = os.path.join(self.anim_dir, "basket.png")
            ball_path = os.path.join(self.anim_dir, "ball3.png")

            if os.path.exists(man_path) and os.path.exists(basket_path) and os.path.exists(ball_path):
                man_img = Image.open(man_path).resize((100, 140), Image.Resampling.LANCZOS)
                basket_img = Image.open(basket_path).resize((80, 100), Image.Resampling.LANCZOS)
                ball_img = Image.open(ball_path).resize((50, 40), Image.Resampling.LANCZOS)

                self.images['man'] = ImageTk.PhotoImage(man_img)
                self.images['basket'] = ImageTk.PhotoImage(basket_img)
                self.images['ball'] = ImageTk.PhotoImage(ball_img)
                self.use_images = True
                print("✅ Court2: Картинки загружены")
            else:
                print("⚠️ Court2: Картинки не найдены, используем fallback-графику")
        except Exception as e:
            print(f"❌ Court2 ошибка: {e}")

        # Параметры анимации (как в court2_my.py)
        self.ball_x = 0
        self.ball_y = 0
        self.target_x = 0
        self.target_y = 0
        self.falling = False
        self.bouncing = False
        self.fall_speed = 5
        self.bounce_speed = 10
        self.gravity = 0.5
        self.step = 5
        self.bounce_height = 0
        self.ball_radius = 8

        self.draw_court()

    def draw_court(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 10 or height <= 10:
            return

        self.canvas.delete("all")

        # === ФОН (как в court2_my.py) ===
        self.canvas.create_rectangle(0, 0, width, height * 0.6, fill="#42AAFF", outline="")
        self.floor_y = height * 0.6
        self.canvas.create_rectangle(0, self.floor_y, width, height, fill="#D16A20", outline="")
        self.canvas.create_line(0, self.floor_y, width, self.floor_y, fill="#8B4513", width=2)

        # === СЧЁТ (как в court2_my.py) ===
        self.score_text = self.canvas.create_text(50, 50, text=str(self.score), font=("Arial", 24, "bold"), fill="white")

        # === КОРЗИНА ===
        self.basket_x = width * 0.88  # ~704
        self.basket_y = height * 0.35  # ~175

        if self.use_images and 'basket' in self.images:
            self.basket_item = self.canvas.create_image(self.basket_x, self.basket_y,
                                                        image=self.images['basket'], anchor=tk.CENTER)
        else:
            # fallback-графика
            self.canvas.create_rectangle(
                self.basket_x + 15, self.basket_y - 50,
                self.basket_x + 25, self.basket_y + 30,
                fill="white", outline="gray", width=3
            )
            self.canvas.create_oval(
                self.basket_x - 35, self.basket_y - 15,
                self.basket_x + 5, self.basket_y + 15,
                fill="", outline="orange", width=5
            )
            for i in range(-30, 0, 10):
                self.canvas.create_line(
                    self.basket_x + i, self.basket_y - 10,
                    self.basket_x + i + 5, self.basket_y + 30,
                    fill="white", width=2
                )

        # === ИГРОК ===
        self.man_x = width * 0.18  # ~144
        self.man_y = self.floor_y  # 300

        if self.use_images and 'man' in self.images:
            self.man_item = self.canvas.create_image(self.man_x, self.man_y,
                                                     image=self.images['man'], anchor=tk.S)
        else:
            # fallback-графика
            self.man_item = self.canvas.create_rectangle(
                self.man_x - 30, self.man_y - 120,
                self.man_x + 30, self.man_y - 40,
                fill="#2E5C8A", outline="black", width=3
            )
            self.canvas.create_oval(
                self.man_x - 25, self.man_y - 155,
                self.man_x + 25, self.man_y - 115,
                fill="#FFB0A0", outline="black", width=3
            )
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

        # === МЯЧ (начальная позиция как в court2_my.py) ===
        self.ball_start_x = width * 0.69  # ~550
        self.ball_start_y = height * 0.57  # ~285
        self.ball_x = self.ball_start_x
        self.ball_y = self.ball_start_y
        self.target_x = width * 0.95  # ~760
        self.target_y = height * 0.38  # ~190
        self.bounce_height = height * 0.58  # ~290
        self.bouncing = False
        self.falling = False
        self.fall_speed = 5

        if self.use_images and 'ball' in self.images:
            self.ball_item = self.canvas.create_image(self.ball_x, self.ball_y,
                                                      image=self.images['ball'], anchor=tk.CENTER)
        else:
            self.ball_item = self.canvas.create_oval(
                self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                self.ball_x + self.ball_radius, self.ball_y + self.ball_radius,
                fill="#F77F0F", outline="#333", width=3
            )

    def update_ball_position(self):
        if self.use_images and 'ball' in self.images:
            self.canvas.coords(self.ball_item, self.ball_x, self.ball_y)
        else:
            self.canvas.coords(self.ball_item,
                               self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
                               self.ball_x + self.ball_radius, self.ball_y + self.ball_radius)

    def start_animation(self):
        if self.is_running:
            return
        self.draw_court()
        self.is_running = True
        self.ball_x = self.ball_start_x
        self.ball_y = self.ball_start_y
        self.bouncing = False
        self.falling = False
        self.fall_speed = 5
        self.animate()

    def animate(self):
        if not self.is_running:
            return

        if self.bouncing:
            # Анимация отскока с замедлением (как в court2_my.py)
            if self.ball_y < self.bounce_height:
                self.ball_y += self.fall_speed
                self.fall_speed += self.gravity
                self.update_ball_position()
                self.canvas.after(50, self.animate)
                return
            else:
                # После падения телепортируем мяч обратно
                self.ball_x = self.ball_start_x
                self.ball_y = self.ball_start_y
                self.bouncing = False
                self.falling = False
                self.fall_speed = 5
                self.update_ball_position()
                self.is_running = False
                return

        # Движение к кольцу (как в court2_my.py)
        if abs(self.ball_x - self.target_x) < 5 and self.ball_y < self.target_y + 10:
            # Начинаем отскок с большей скоростью
            self.bouncing = True
            self.fall_speed = -10  # Начальная скорость отскока вверх
            self.ball_y = self.target_y - 10  # Позиция для отскока
            self.update_ball_position()
            self.canvas.after(50, self.animate)
            return

        # Движение к кольцу
        if self.ball_x < self.target_x:
            self.ball_x += self.step
        elif self.ball_x > self.target_x:
            self.ball_x -= self.step
        if self.ball_y > self.target_y:
            self.ball_y -= self.step

        # Обновляем позицию мяча
        self.update_ball_position()
        self.canvas.after(50, self.animate)  # 50ms как в court2_my.py

    def stop(self):
        self.is_running = False