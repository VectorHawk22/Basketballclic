# main.py
import pygame
import os
import sys

# Инициализация Pygame
pygame.init()

# Константы для экрана
SCREEN_WIDTH = 420
SCREEN_HEIGHT = 240
FPS = 20

# Цвета
SKY_COLOR = (66, 170, 255)
GROUND_COLOR = (209, 106, 32)

class CourtSuccess:
    def __init__(self):
        # Настройка экрана
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Court Success")
        self.clock = pygame.time.Clock()
        
        # Путь к папке с изображениями
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Масштабирование под экран 420x240
        self.scale_x = SCREEN_WIDTH / 800
        self.scale_y = SCREEN_HEIGHT / 500
        
        # Загрузка изображений
        self.img_man = None
        self.img_basket = None
        self.img_ball = None
        self.load_images()
        
        # Координаты и состояние анимации
        self.ball_x = 0
        self.ball_y = 0
        self.target_x = 0
        self.target_y = 0
        self.step = 3
        self.falling = False
        self.is_animating = False
        self.ball_rect = None
        
        # Начальная отрисовка
        self.draw_court()
    
    def load_images(self):
        """Загрузка изображений из папки animation"""
        try:
            # Картинки в папке animation/
            man_path = os.path.join(self.base_dir, "animation", "man.png")
            basket_path = os.path.join(self.base_dir, "animation", "basket.png")
            ball_path = os.path.join(self.base_dir, "animation", "ball3.png")
            
            # Альтернативный путь (если изображения в той же папке)
            if not os.path.exists(man_path):
                man_path = os.path.join(self.base_dir, "man.png")
            if not os.path.exists(basket_path):
                basket_path = os.path.join(self.base_dir, "basket.png")
            if not os.path.exists(ball_path):
                ball_path = os.path.join(self.base_dir, "ball3.png")
            
            # Загрузка человека
            if os.path.exists(man_path):
                img_man = pygame.image.load(man_path).convert_alpha()
                man_width = int(700 * self.scale_x)
                man_height = int(900 * self.scale_y)
                self.img_man = pygame.transform.scale(img_man, (man_width, man_height))
            else:
                print(f"⚠️ Файл не найден: {man_path}")
                # Создаем заглушку
                self.img_man = self._create_placeholder((50, 80), (255, 0, 0))
            
            # Загрузка корзины
            if os.path.exists(basket_path):
                img_basket = pygame.image.load(basket_path).convert_alpha()
                basket_width = int(650 * self.scale_x)
                basket_height = int(560 * self.scale_y)
                self.img_basket = pygame.transform.scale(img_basket, (basket_width, basket_height))
            else:
                print(f"⚠️ Файл не найден: {basket_path}")
                self.img_basket = self._create_placeholder((60, 50), (0, 255, 0))
            
            # Загрузка мяча
            if os.path.exists(ball_path):
                img_ball = pygame.image.load(ball_path).convert_alpha()
                ball_size = int(80 * self.scale_x)
                self.img_ball = pygame.transform.scale(img_ball, (ball_size, ball_size))
            else:
                print(f"⚠️ Файл не найден: {ball_path}")
                self.img_ball = self._create_placeholder((30, 30), (255, 200, 0))
                
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")
            # Создаем заглушки
            self.img_man = self._create_placeholder((50, 80), (255, 0, 0))
            self.img_basket = self._create_placeholder((60, 50), (0, 255, 0))
            self.img_ball = self._create_placeholder((30, 30), (255, 200, 0))
    
    def _create_placeholder(self, size, color):
        """Создание заглушки для отсутствующих изображений"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        return surf
    
    def draw_court(self):
        """Рисование поля с масштабированием"""
        # Небо и земля
        self.screen.fill(SKY_COLOR)
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, 144, SCREEN_WIDTH, SCREEN_HEIGHT - 144))
        
        # Корзина
        if self.img_basket:
            basket_x = int(710 * self.scale_x) - int(300 * self.scale_x)
            basket_y = int(170 * self.scale_y) - int(150 * self.scale_y)
            self.screen.blit(self.img_basket, (basket_x, basket_y))
        
        # Человек
        if self.img_man:
            man_x = int(500 * self.scale_x) - int(340 * self.scale_x)
            man_y = int(200 * self.scale_y) - int(300 * self.scale_y)
            self.screen.blit(self.img_man, (man_x, man_y))
        
        # Мяч (начальная позиция)
        if self.img_ball:
            self.ball_x = int(550 * self.scale_x)
            self.ball_y = int(285 * self.scale_y)
            self.target_x = int(710 * self.scale_x)
            self.target_y = int(170 * self.scale_y)
            
            # Сохраняем прямоугольник мяча для обновления
            ball_rect = self.img_ball.get_rect()
            ball_rect.center = (self.ball_x, self.ball_y)
            self.ball_rect = ball_rect
            
            self.screen.blit(self.img_ball, ball_rect)
    
    def start_animation(self):
        """Запуск анимации"""
        self.is_animating = True
        self.falling = False
        self.draw_court()
        # Обновляем позицию мяча в прямоугольнике
        if self.ball_rect:
            self.ball_rect.center = (self.ball_x, self.ball_y)
    
    def stop(self):
        """Остановка анимации"""
        self.is_animating = False
    
    def update(self):
        """Обновление состояния анимации"""
        if not self.is_animating or self.img_ball is None:
            return
        
        # Падение вниз после попадания
        if self.falling:
            if self.ball_y < int(310 * self.scale_y):
                self.ball_y += 3
                if self.ball_rect:
                    self.ball_rect.center = (self.ball_x, self.ball_y)
                return
            else:
                self.stop()
                return
        
        # Проверка достижения цели
        dx = abs(self.ball_x - self.target_x)
        dy = abs(self.ball_y - self.target_y)
        
        if dx < 5 and dy < 5:
            self.falling = True
            self.ball_x = self.target_x
            self.ball_y = self.target_y
            if self.ball_rect:
                self.ball_rect.center = (self.ball_x, self.ball_y)
            return
        
        # Движение к цели
        if self.ball_x < self.target_x:
            self.ball_x += self.step
        if self.ball_x > self.target_x:
            self.ball_x -= self.step
        if self.ball_y > self.target_y:
            self.ball_y -= self.step
        
        # Обновляем позицию мяча
        if self.ball_rect:
            self.ball_rect.center = (self.ball_x, self.ball_y)
    
    def render(self):
        """Отрисовка всех элементов"""
        # Перерисовываем фон и статичные элементы
        self.screen.fill(SKY_COLOR)
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, 144, SCREEN_WIDTH, SCREEN_HEIGHT - 144))
        
        # Корзина
        if self.img_basket:
            basket_x = int(710 * self.scale_x) - int(300 * self.scale_x)
            basket_y = int(170 * self.scale_y) - int(150 * self.scale_y)
            self.screen.blit(self.img_basket, (basket_x, basket_y))
        
        # Человек
        if self.img_man:
            man_x = int(500 * self.scale_x) - int(340 * self.scale_x)
            man_y = int(200 * self.scale_y) - int(300 * self.scale_y)
            self.screen.blit(self.img_man, (man_x, man_y))
        
        # Мяч (обновленная позиция)
        if self.img_ball and self.ball_rect:
            self.screen.blit(self.img_ball, self.ball_rect)
    
    def run(self):
        """Основной игровой цикл"""
        running = True
        animation_started = False
        
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not animation_started:
                        self.start_animation()
                        animation_started = True
                    elif event.key == pygame.K_r:
                        # Сброс анимации
                        animation_started = False
                        self.stop()
                        self.draw_court()
            
            # Обновление анимации
            if self.is_animating:
                self.update()
                self.render()
            else:
                # Если анимация не активна, просто рисуем статичную сцену
                if not animation_started:
                    self.render()
            
            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CourtSuccess()
    game.run()