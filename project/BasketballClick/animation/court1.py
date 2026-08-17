import os
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.image import Image as CoreImage


class CourtSuccess:
    """Анимация успешного броска - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    
    def __init__(self, canvas_widget):
        self.canvas = canvas_widget
        self.animating = False
        self.ball = None
        self.ball_x = 0
        self.ball_y = 0
        self.target_x = 0
        self.target_y = 0
        self.falling = False
        self.fall_speed = 5
        self.step = 5
        self.animation_trigger = None
        self.animation_complete = False
        self.images = {}
        self.image_objects = []
        self.man_rect = None
        self.basket_rect = None
        self.ball_size_w = 0
        self.ball_size_h = 0
        
        # Загрузка изображений
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.load_images()
        
        # Подписываемся на изменение размера
        self.canvas.bind(size=self.on_size)
    
    def on_size(self, *args):
        """Перерисовка при изменении размера"""
        self.draw_court()
    
    def load_images(self):
        """Загрузка изображений"""
        try:
            man_path = os.path.join(self.base_dir, "animation", "man.png")
            basket_path = os.path.join(self.base_dir, "animation", "basket.png")
            ball_path = os.path.join(self.base_dir, "animation", "ball3.png")
            
            if os.path.exists(man_path):
                self.images['man'] = CoreImage(man_path).texture
                print(f"✅ Загружен man.png")
            else:
                print(f"❌ Файл не найден: {man_path}")
                
            if os.path.exists(basket_path):
                self.images['basket'] = CoreImage(basket_path).texture
                print(f"✅ Загружен basket.png")
            else:
                print(f"❌ Файл не найден: {basket_path}")
                
            if os.path.exists(ball_path):
                self.images['ball'] = CoreImage(ball_path).texture
                print(f"✅ Загружен ball3.png")
            else:
                print(f"❌ Файл не найден: {ball_path}")
                
        except Exception as e:
            print(f"❌ Ошибка загрузки изображений: {e}")
    
    def draw_court(self):
        """Рисует баскетбольную площадку - ОПУЩЕННАЯ ВЕРСИЯ"""
        canvas = self.canvas
        canvas.canvas.clear()
        
        w = canvas.width
        h = canvas.height
        
        if w < 10 or h < 10:
            Clock.schedule_once(lambda dt: self.draw_court(), 0.1)
            return
        
        self.image_objects = []
        self.man_rect = None
        self.basket_rect = None
        
        # === ОПУСКАЕМ НИЖЕ (сдвиг 100 пикселей вместо 200) ===
        offset_y = 100  # МЕНЬШЕ СДВИГ
        
        # === НЕБО И КОРТ - ПОЛНОЦЕННЫЕ ===
        sky_height = h * 0.55
        ground_height = h * 0.45
        
        with canvas.canvas:
            # НЕБО
            Color(0.26, 0.67, 1, 1)
            Rectangle(pos=(0, offset_y + ground_height), size=(w, sky_height))
            
            # КОРТ/ПОЛ
            Color(0.82, 0.41, 0.13, 1)
            Rectangle(pos=(0, offset_y), size=(w, ground_height))
            
            # === КОЛЬЦО - УВЕЛИЧЕННОЕ ===
            basket_x = w * 0.72
            basket_y = offset_y + ground_height * 0.5
            
            if 'basket' in self.images:
                tex = self.images['basket']
                size_w = w * 0.4  # УВЕЛИЧЕНО
                size_h = h * 0.4   # УВЕЛИЧЕНО
                self.basket_rect = Rectangle(
                    pos=(basket_x - size_w/2, basket_y - size_h/2),
                    size=(size_w, size_h),
                    texture=tex
                )
                self.image_objects.append(self.basket_rect)
            else:
                Color(1, 0.84, 0, 1)
                basket_size = w * 0.25
                Rectangle(pos=(basket_x - basket_size/2, basket_y), 
                         size=(basket_size, basket_size * 0.15))
                Rectangle(pos=(basket_x - basket_size/2, basket_y), 
                         size=(basket_size * 0.06, basket_size * 0.4))
                Rectangle(pos=(basket_x + basket_size/2 - basket_size * 0.06, basket_y), 
                         size=(basket_size * 0.06, basket_size * 0.4))
            
            # === ИГРОК - УВЕЛИЧЕННЫЙ ===
            man_x = w * 0.2
            man_y = offset_y + ground_height * 0.35
            
            if 'man' in self.images:
                tex = self.images['man']
                size_w = w * 0.3   # УВЕЛИЧЕНО
                size_h = h * 0.4   # УВЕЛИЧЕНО
                self.man_rect = Rectangle(
                    pos=(man_x - size_w/2, man_y - size_h/2),
                    size=(size_w, size_h),
                    texture=tex
                )
                self.image_objects.append(self.man_rect)
                man_size_w = size_w
                man_size_h = size_h
            else:
                Color(0.2, 0.6, 1, 1)
                player_size = w * 0.15
                Ellipse(pos=(man_x - player_size/2, man_y), 
                       size=(player_size, player_size * 1.2))
                Color(1, 0.8, 0.6, 1)
                Ellipse(pos=(man_x - player_size * 0.4, man_y + player_size * 0.8), 
                       size=(player_size * 0.7, player_size * 0.6))
                man_size_w = w * 0.15
                man_size_h = h * 0.18
            
            # === РАЗМЕР МЯЧА ===
            self.ball_size_w = w * 0.08
            self.ball_size_h = h * 0.07
            
            # === МЯЧ - СПРАВА ОТ ИГРОКА (на уровне рук) ===
            self.ball_x = man_x + man_size_w * 0.5
            self.ball_y = man_y + man_size_h * 0.2
            
            self.target_x = w * 0.76
            self.target_y = offset_y + ground_height * 0.6
            self.step = w * 0.025
            self.fall_speed = h * 0.025
            
            # === СОЗДАЕМ МЯЧ ===
            self.create_ball()
    
    def create_ball(self):
        """Создает мяч"""
        w = self.canvas.width
        h = self.canvas.height
        
        if w < 10 or h < 10:
            return
        
        # УДАЛЯЕМ СТАРЫЙ МЯЧ
        if self.ball:
            try:
                if hasattr(self.canvas, 'canvas') and self.canvas.canvas:
                    instructions = self.canvas.canvas.get_group('ball')
                    for inst in instructions:
                        self.canvas.canvas.remove(inst)
            except:
                pass
            self.ball = None
        
        if 'ball' in self.images:
            tex = self.images['ball']
            size_w = self.ball_size_w
            size_h = self.ball_size_h
            self.ball = Rectangle(
                pos=(self.ball_x - size_w/2, self.ball_y - size_h/2),
                size=(size_w, size_h),
                texture=tex,
                group='ball'
            )
            print(f"Мяч создан на {self.ball_x},{self.ball_y} размер {size_w}x{size_h}")
        else:
            ball_size = w * 0.04
            self.ball = Ellipse(
                pos=(self.ball_x - ball_size/2, self.ball_y - ball_size/2),
                size=(ball_size, ball_size),
                group='ball'
            )
    
    def start_animation(self):
        """Запускает анимацию"""
        if self.animating:
            return
        
        self.animating = True
        self.animation_complete = False
        
        w = self.canvas.width
        h = self.canvas.height
        if w < 10 or h < 10:
            self.animating = False
            return
        
        offset_y = 100
        ground_height = h * 0.45
        
        man_x = w * 0.2
        man_y = offset_y + ground_height * 0.35
        man_size_w = w * 0.3
        man_size_h = h * 0.4
        
        self.ball_size_w = w * 0.08
        self.ball_size_h = h * 0.07
        
        self.ball_x = man_x + man_size_w * 0.5
        self.ball_y = man_y + man_size_h * 0.2
        self.target_x = w * 0.76
        self.target_y = offset_y + ground_height * 0.6
        self.falling = False
        self.fall_speed = h * 0.025
        self.step = w * 0.025
        
        if self.animation_trigger:
            self.animation_trigger.cancel()
            self.animation_trigger = None
        
        self.animation_trigger = Clock.schedule_interval(self.move_ball, 0.03)
    
    def move_ball(self, dt):
        """Движение мяча"""
        if not self.animating:
            return False
        
        try:
            if self.falling:
                if self.ball_y > self.canvas.height * 0.05:
                    self.ball_y -= self.fall_speed
                    self.update_ball_position()
                    return True
                
                # Возвращаем мяч к игроку
                w = self.canvas.width
                h = self.canvas.height
                offset_y = 100
                ground_height = h * 0.45
                man_x = w * 0.2
                man_y = offset_y + ground_height * 0.35
                man_size_w = w * 0.3
                man_size_h = h * 0.4
                self.ball_x = man_x + man_size_w * 0.5
                self.ball_y = man_y + man_size_h * 0.2
                self.falling = False
                self.update_ball_position()
                self.stop_animation()
                return False
            
            # Движение к кольцу
            dx = self.target_x - self.ball_x
            dy = self.target_y - self.ball_y
            dist = (dx*dx + dy*dy) ** 0.5
            
            if dist < 10:
                self.ball_x = self.target_x
                self.ball_y = self.target_y
                self.falling = True
                self.update_ball_position()
                return True
            
            if dist > 0:
                speed = self.step * 1.5
                self.ball_x += (dx / dist) * speed
                self.ball_y += (dy / dist) * speed
            
            self.update_ball_position()
            return True
            
        except Exception as e:
            print(f"Ошибка в анимации: {e}")
            self.stop_animation()
            return False
    
    def update_ball_position(self):
        """Обновляет позицию мяча"""
        if self.ball is None:
            return
        
        try:
            if hasattr(self.canvas, 'canvas') and self.canvas.canvas:
                instructions = self.canvas.canvas.get_group('ball')
                for inst in instructions:
                    self.canvas.canvas.remove(inst)
            
            w = self.canvas.width
            h = self.canvas.height
            if w < 10 or h < 10:
                return
            
            with self.canvas.canvas:
                if 'ball' in self.images:
                    tex = self.images['ball']
                    size_w = self.ball_size_w
                    size_h = self.ball_size_h
                    self.ball = Rectangle(
                        pos=(self.ball_x - size_w/2, self.ball_y - size_h/2),
                        size=(size_w, size_h),
                        texture=tex,
                        group='ball'
                    )
                else:
                    ball_size = w * 0.04
                    self.ball = Ellipse(
                        pos=(self.ball_x - ball_size/2, self.ball_y - ball_size/2),
                        size=(ball_size, ball_size),
                        group='ball'
                    )
        except Exception as e:
            print(f"Ошибка обновления мяча: {e}")
    
    def stop_animation(self):
        """Останавливает анимацию"""
        self.animating = False
        self.animation_complete = True
        if self.animation_trigger:
            self.animation_trigger.cancel()
            self.animation_trigger = None
        
        w = self.canvas.width
        h = self.canvas.height
        if w > 10 and h > 10:
            offset_y = 100
            ground_height = h * 0.45
            man_x = w * 0.2
            man_y = offset_y + ground_height * 0.35
            man_size_w = w * 0.3
            man_size_h = h * 0.4
            self.ball_x = man_x + man_size_w * 0.5
            self.ball_y = man_y + man_size_h * 0.2
            self.update_ball_position()
    
    def stop(self):
        """Внешний останов анимации"""
        self.stop_animation()