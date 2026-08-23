# court2_pygame.py
import os
import pygame
import math

class CourtFail:
    def __init__(self, screen):
        self.screen = screen
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Размеры экрана
        self.screen_width = 420
        self.screen_height = 240
        
        # Масштабирование
        self.scale_x = self.screen_width / 800
        self.scale_y = self.screen_height / 500
        
        # Загрузка изображений
        self.img_man = None
        self.img_basket = None
        self.img_ball = None
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
        self.animation_complete = False
        
        # Цвета
        self.sky_color = (66, 170, 255)
        self.ground_color = (209, 106, 32)

    def load_images(self):
        """Загрузка изображений из папки animation"""
        try:
            man_path = os.path.join(self.base_dir, "man.png")
            basket_path = os.path.join(self.base_dir, "basket.png")
            ball_path = os.path.join(self.base_dir, "ball3.png")
            
            if os.path.exists(man_path):
                img_man = pygame.image.load(man_path)
                man_width = int(700 * self.scale_x)
                man_height = int(900 * self.scale_y)
                self.img_man = pygame.transform.scale(img_man, (man_width, man_height))
            else:
                print(f"⚠️ Файл не найден: {man_path}")
                
            if os.path.exists(basket_path):
                img_basket = pygame.image.load(basket_path)
                basket_width = int(650 * self.scale_x)
                basket_height = int(560 * self.scale_y)
                self.img_basket = pygame.transform.scale(img_basket, (basket_width, basket_height))
            else:
                print(f"⚠️ Файл не найден: {basket_path}")
                
            if os.path.exists(ball_path):
                img_ball = pygame.image.load(ball_path)
                ball_size = int(80 * self.scale_x)
                self.img_ball = pygame.transform.scale(img_ball, (ball_size, ball_size))
            else:
                print(f"⚠️ Файл не найден: {ball_path}")
                
        except Exception as e:
            print(f"Ошибка загрузки изображений промаха: {e}")

    def draw_court(self):
        """Рисование поля с масштабированием"""
        # Небо и земля
        self.screen.fill(self.sky_color)
        pygame.draw.rect(self.screen, self.ground_color, (0, 144, self.screen_width, self.screen_height - 144))
        
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
        
        # Мяч
        if self.img_ball:
            self.ball_x = int(550 * self.scale_x)
            self.ball_y = int(285 * self.scale_y)
            self.target_x = int(710 * self.scale_x)
            self.target_y = int(170 * self.scale_y)
            self.bounce_height = int(290 * self.scale_y)

    def start_animation(self):
        """Запуск анимации промаха"""
        self.is_animating = True
        self.animation_complete = False
        self.falling = False
        self.bouncing = False
        self.fall_speed = 5
        self.draw_court()
        # Начальная позиция мяча
        self.ball_x = int(550 * self.scale_x)
        self.ball_y = int(285 * self.scale_y)

    def stop(self):
        """Остановка анимации"""
        self.is_animating = False

    def update(self):
        """Обновление состояния анимации"""
        if not self.is_animating or not self.img_ball:
            return
        
        # Отскок после удара о кольцо
        if self.bouncing:
            if self.ball_y < self.bounce_height:
                self.ball_y += self.fall_speed
                self.fall_speed += self.gravity
                return
            else:
                self.stop()
                self.animation_complete = True
                return
        
        # Проверка попадания в кольцо (промах)
        dx = abs(self.ball_x - self.target_x)
        dy = abs(self.ball_y - self.target_y)
        
        if dx < 10 and dy < 20:
            self.bouncing = True
            self.fall_speed = -10
            self.ball_y = self.target_y - 10
            return
        
        # Движение к цели
        if self.ball_x < self.target_x:
            self.ball_x += self.step
        if self.ball_x > self.target_x:
            self.ball_x -= self.step
        if self.ball_y > self.target_y:
            self.ball_y -= self.step

    def draw(self):
        """Отрисовка мяча на экране"""
        if self.img_ball and self.is_animating:
            self.screen.blit(self.img_ball, (self.ball_x, self.ball_y))

    def is_finished(self):
        """Проверка завершения анимации"""
        return self.animation_complete


# Пример использования
def main():
    pygame.init()
    screen = pygame.display.set_mode((420, 240))
    pygame.display.set_caption("Court Fail Animation")
    clock = pygame.time.Clock()
    
    court_fail = CourtFail(screen)
    court_fail.start_animation()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    court_fail.start_animation()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        court_fail.update()
        court_fail.draw()
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        
        if court_fail.is_finished():
            # Анимация завершена, можно выйти или перезапустить
            pass
    
    pygame.quit()


if __name__ == "__main__":
    main()