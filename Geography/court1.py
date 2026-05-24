import tkinter as tk
from random import *

width = 800
height = 500
root = tk.Tk()
root.title("Basketball court")

canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()


# Создаём сам корт
canvas.create_rectangle(0, 0, 800, 300, fill = "#42AAFF")
canvas.create_rectangle(0, 300, 800, 500, fill="#D16A20")

# Создаю кольцо для мяча
canvas.create_line(780, 350, 780, 150, width=5, fill="#000000")
canvas.create_line(775, 225, 775, 150, width=5, fill="#000000")
canvas.create_line(750, 195, 775, 195, width=4, fill='#000000')
# Делаем челевечка и мяч в руках
canvas.create_line(505,340,505,310, width=6, fill="#FFD6B0")
canvas.create_line(525,340,525,310, width=6, fill="#FFD6B0")
canvas.create_line(505,325,505,310, width=6, fill="#000000")
canvas.create_line(525,325,525,310, width=6, fill="#000000")
canvas.create_rectangle(502,280,530,310, fill="#FF0000")
canvas.create_line(516,275,516,280, width=5, fill= "#FFD6B0")
canvas.create_oval(516-10,265-10,516+10,265+10, fill="#FFD6B0")
canvas.create_line(530,295,545,290, width=5, fill="#FFD6B0")

ball = canvas.create_oval(550-8,285-8,550+8,285+8, fill="#F77F0F")
score = 0
score_text = canvas.create_text(50,50, text=score)

# Параметры для анимации
ball_x = 550
ball_y = 285
target_x = 760
target_y = 190
step = 5  # шаг анимации

    

def update_score():
    global score
    canvas.itemconfig(score_text, text=score)

def move_ball():
    global ball_x, ball_y, score
    
    # Проверяем, достиг ли мяч цели
    if abs(ball_x - target_x) < 5 and abs(ball_y - target_y) < 5:
        score += 1
        update_score()
        ball_x = 550
        ball_y = 285
        
    else:
        # Перемещаем мяч к цели
        if ball_x < target_x:
            ball_x += step
        if ball_x > target_x:
            ball_x -= step
        if ball_y > target_y:
            ball_y -= step
        
        # Обновляем позицию мяча на холсте
        canvas.coords(ball, ball_x-8, ball_y-8, ball_x+8, ball_y+8)
        
    

def throw(event):
    move_ball()

canvas.bind_all("<space>", throw)

root.mainloop()


