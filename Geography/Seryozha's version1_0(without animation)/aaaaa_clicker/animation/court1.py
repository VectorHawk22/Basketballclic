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
image_man = tk.PhotoImage(file= "man.png")
image_basket = tk.PhotoImage(file="basket.png")
image_ball1 = tk.PhotoImage(file="ball1.png")

# Создаём кольцо
basket = canvas.create_image(450, 75, image=image_basket, anchor= tk.NW)


# Создаём игрока с мячом
man = canvas.create_image(222, 85, image = image_man, anchor = tk.NW)
ball = canvas.create_oval(550-8, 285-8, 550+8, 285+8, fill="#F77F0F")
score = 0
score_text = canvas.create_text(50, 50, text=score)

# Параметры для анимации
ball_x = 550
ball_y = 285
target_x = 730
target_y = 190
falling = False  # Флаг для падения
fall_speed = 5   # Скорость падения
step = 5         # Шаг движения к кольцу

def update_score():
    global score
    canvas.itemconfig(score_text, text=score)

def move_ball():
    global ball_x, ball_y, score, falling
    
    if falling:
        # Анимация падения
        if ball_y < 310:
            ball_y += fall_speed
            canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
            root.after(50, move_ball)  # Запускаем снова через 50мс
            return
        
        # После падения телепортируем мяч обратно
        ball_x = 550
        ball_y = 285
        falling = False
        canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
        return
    
    # Движение к кольцу
    if abs(ball_x - target_x) < 5 and abs(ball_y - target_y) < 5:
        score += 1
        update_score()
        falling = True  # Начинаем падение
        ball_x = target_x  # Ставим мяч в кольцо
        canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
        move_ball()  # Продолжаем анимацию
        return
    
    if ball_x < target_x:
        ball_x += step
    if ball_x > target_x:
        ball_x -= step
    if ball_y > target_y:
        ball_y -= step
    
    canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
    root.after(50, move_ball)  # Запускаем снова через 50мс

# Запускаем анимацию автоматически
move_ball()

root.mainloop()

