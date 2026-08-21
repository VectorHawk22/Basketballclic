import tkinter as tk
from court1 import CourtSuccess
from court2 import CourtFail


class TestCourtAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Тест анимации баскетбола")
        self.root.geometry("850x650")
        self.root.resizable(False, False)
        
        # Canvas 800x500
        self.animation_canvas = tk.Canvas(
            root, 
            width=800, 
            height=500, 
            bg="#f0f0f0",
            highlightthickness=2, 
            highlightbackground="gray"
        )
        self.animation_canvas.pack(pady=20)
        
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
            pady=10
        )
        self.btn_success.pack(side=tk.LEFT, padx=10)
        
        self.btn_fail = tk.Button(
            self.button_frame, 
            text="❌ Неудачный бросок", 
            command=self.start_fail,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.btn_fail.pack(side=tk.LEFT, padx=10)
        
        self.btn_stop = tk.Button(
            self.button_frame, 
            text="⏹ Стоп", 
            command=self.stop_animation,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.btn_stop.pack(side=tk.LEFT, padx=10)
        
        # Загружаем начальный фон
        self.court_success.draw_court()
    
    def start_success(self):
        self.stop_animation()
        self.court_success.start_animation()
    
    def start_fail(self):
        self.stop_animation()
        self.court_fail.start_animation()
    
    def stop_animation(self):
        if self.court_success.is_animating:
            self.court_success.stop()
        if self.court_fail.is_animating:
            self.court_fail.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TestCourtAnimation(root)
    root.mainloop()