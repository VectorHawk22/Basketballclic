import tkinter as tk
from court1 import CourtSuccess
from court2 import CourtFail


class TestCourtAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Тест анимации баскетбола - УВЕЛИЧЕННЫЕ ОБЪЕКТЫ")
        self.root.geometry("850x650")
        self.root.resizable(False, False)
        
        # Информационная панель сверху
        self.info_frame = tk.Frame(root, bg="#f0f0f0", height=40)
        self.info_frame.pack(fill=tk.X, pady=(10, 0))
        self.info_frame.pack_propagate(False)
        
        self.info_label = tk.Label(
            self.info_frame,
            text="📐 Canvas: 420x240 | ОГРОМНЫЕ объекты: человек ~184x216px, корзина ~158x125px, мяч ~32x32px",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#333"
        )
        self.info_label.pack(pady=8)
        
        # Canvas 420x240
        self.canvas_frame = tk.Frame(root, width=420, height=240, bg="white", relief=tk.RAISED, bd=2)
        self.canvas_frame.pack(pady=15)
        self.canvas_frame.pack_propagate(False)
        
        self.animation_canvas = tk.Canvas(
            self.canvas_frame, 
            width=420, 
            height=240, 
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.animation_canvas.pack()
        
        # Создаем экземпляры классов
        self.court_success = CourtSuccess(self.animation_canvas)
        self.court_fail = CourtFail(self.animation_canvas)
        
        # Кнопки
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        self.btn_success = tk.Button(
            self.button_frame, 
            text="🏀 Успешный бросок", 
            command=self.start_success,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            width=18
        )
        self.btn_success.pack(side=tk.LEFT, padx=8)
        
        self.btn_fail = tk.Button(
            self.button_frame, 
            text="❌ Неудачный бросок", 
            command=self.start_fail,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            width=18
        )
        self.btn_fail.pack(side=tk.LEFT, padx=8)
        
        self.btn_stop = tk.Button(
            self.button_frame, 
            text="⏹ Стоп", 
            command=self.stop_animation,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            width=18
        )
        self.btn_stop.pack(side=tk.LEFT, padx=8)
        
        self.btn_reset = tk.Button(
            self.button_frame, 
            text="🔄 Сброс", 
            command=self.reset_canvas,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            width=18
        )
        self.btn_reset.pack(side=tk.LEFT, padx=8)
        
        # Статусная строка
        self.status_frame = tk.Frame(root, bg="#f5f5f5", height=35)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="✅ Готово | Огромные объекты для лучшей видимости!",
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#333"
        )
        self.status_label.pack(pady=8)
        
        # Загружаем начальный фон
        self.court_success.draw_court()
    
    def start_success(self):
        self.stop_animation()
        self.status_label.config(text="🏀 Запущен УСПЕШНЫЙ бросок...", fg="#4CAF50")
        self.court_success.start_animation()
    
    def start_fail(self):
        self.stop_animation()
        self.status_label.config(text="❌ Запущен НЕУДАЧНЫЙ бросок...", fg="#f44336")
        self.court_fail.start_animation()
    
    def stop_animation(self):
        if self.court_success.is_animating:
            self.court_success.stop()
            self.status_label.config(text="⏹ Успешный бросок остановлен", fg="#FF9800")
        if self.court_fail.is_animating:
            self.court_fail.stop()
            self.status_label.config(text="⏹ Неудачный бросок остановлен", fg="#FF9800")
    
    def reset_canvas(self):
        self.stop_animation()
        self.court_success.draw_court()
        self.status_label.config(text="🔄 Canvas сброшен к начальному состоянию", fg="#9E9E9E")


if __name__ == "__main__":
    root = tk.Tk()
    app = TestCourtAnimation(root)
    root.mainloop()