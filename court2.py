import tkinter as tk
from random import *

width = 800
height = 500
root = tk.Tk()
root.title("Basketball court")

canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

# Создаём корт и элементы
canvas.create_rectangle(0, 0, 800, 300, fill="#42AAFF")
canvas.create_rectangle(0, 300, 800, 500, fill="#D16A20")

# Создаю переменные для отображения картинок
image_man = tk.PhotoImage(file= "/home/ivan/animation/man.png")
image_basket = tk.PhotoImage(file="/home/ivan/animation/basket.png")
image_ball1 = tk.PhotoImage(file="/home/ivan/animation/ball1.png")

# Создаём кольцо
basket = canvas.create_image(435, 75, image=image_basket, anchor= tk.NW)


# Создаём игрока с мячом
man = canvas.create_image(222, 85, image = image_man, anchor = tk.NW)
ball = canvas.create_oval(550-8, 285-8, 550+8, 285+8, fill="#F77F0F")
score = 0
score_text = canvas.create_text(50, 50, text=score)
# Параметры для анимации
ball_x = 550
ball_y = 285
target_x = 710
target_y = 185
falling = False  # Флаг для падения
fall_speed = 5   # Начальная скорость падения
step = 5         # Шаг движения к кольцу
bounce_height = 290  # Высота отскока
bouncing = False  # Флаг отскока
bounce_speed = 10    # Скорость отскока
gravity = 0.5        # Сила гравитации

def move_ball():
    global ball_x, ball_y, falling, bouncing, fall_speed, bounce_speed
    
    if bouncing:
        # Анимация отскока с замедлением
        if ball_y < bounce_height:
            ball_y += fall_speed
            fall_speed += gravity  # Добавляем гравитацию
            canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
            root.after(50, move_ball)
            return
        
        # После падения телепортируем мяч обратно
        ball_x = 550
        ball_y = 285
        bouncing = False
        falling = False
        fall_speed = 5  # Восстанавливаем начальную скорость
        canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
        return
    
    # Движение к кольцу
    if abs(ball_x - target_x) < 5 and ball_y < target_y + 10:
            # Начинаем отскок с большей скоростью
            bouncing = True
            fall_speed = -10  # Начальная скорость отскока вверх
            ball_y = target_y - 10  # Позиция для отскока
            canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
            move_ball()
            return
        
        # Движение к кольцу
    if ball_x < target_x:
        ball_x += step
    if ball_x > target_x:
        ball_x -= step
    if ball_y > target_y:
        ball_y -= step
        
        # Обновляем позицию мяча на холсте
    canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
        
        # Запускаем анимацию снова через 50 мс
    root.after(50, move_ball)

# Запускаем анимацию автоматически
move_ball()

# Запускаем главное окно
root.mainloop()
