import os
import pygame

class CourtSuccess:
    def __init__(self, screen):
        self.screen = screen
        self.is_running = False
        self.score = 0
        self.images = {}
        self.use_images = False
        
        # Параметры анимации
        self.ball_x = 0
        self.ball_y = 0
        self.target_x = 0
        self.target_y = 0
        self.falling = False
        self.fall_speed = 5
        self.step = 5
        self.ball_radius = 8
        self.anim_timer = 0
        self.frame_delay = 50
        
        # Позиции объектов
        self.basket_x = 0
        self.basket_y = 0
        self.man_x = 0
        self.man_y = 0
        self.ball_start_x = 0
        self.ball_start_y = 0
        self.floor_y = 0
        
        self.load_images()

    def load_images(self):
        """Загрузка изображений"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
            man_path = os.path.join(base_dir, "images", "man.png")
            basket_path = os.path.join(base_dir, "images", "basket.png")
            ball_path = os.path.join(base_dir, "images", "ball3.png")
            
            if os.path.exists(man_path) and os.path.exists(basket_path) and os.path.exists(ball_path):
                self.images['man'] = pygame.image.load(man_path)
                self.images['man'] = pygame.transform.scale(self.images['man'], (100, 140))
                self.images['basket'] = pygame.image.load(basket_path)
                self.images['basket'] = pygame.transform.scale(self.images['basket'], (80, 100))
                self.images['ball'] = pygame.image.load(ball_path)
                self.images['ball'] = pygame.transform.scale(self.images['ball'], (50, 40))
                self.use_images = True
            else:
                print("⚠️ CourtSuccess: Картинки не найдены")
        except Exception as e:
            print(f"❌ CourtSuccess ошибка загрузки: {e}")

    def start_animation(self):
        if self.is_running:
            return
        self.is_running = True
        self.ball_x = self.ball_start_x
        self.ball_y = self.ball_start_y
        self.falling = False
        self.anim_timer = 0

    def update(self, dt):
        """Обновление анимации"""
        if not self.is_running:
            return

        self.anim_timer += dt * 1000
        if self.anim_timer < self.frame_delay:
            return
        self.anim_timer = 0

        if self.falling:
            if self.ball_y < self.floor_y + 10:
                self.ball_y += self.fall_speed
            else:
                self.ball_x = self.ball_start_x
                self.ball_y = self.ball_start_y
                self.falling = False
                self.is_running = False
            return

        if abs(self.ball_x - self.target_x) < 5 and abs(self.ball_y - self.target_y) < 5:
            self.score += 1
            self.falling = True
            self.ball_x = self.target_x
            return

        if self.ball_x < self.target_x:
            self.ball_x += self.step
        elif self.ball_x > self.target_x:
            self.ball_x -= self.step
        if self.ball_y > self.target_y:
            self.ball_y -= self.step

    def draw(self, offset_x=0, offset_y=0):
        """Отрисовка анимации"""
        width, height = self.screen.get_size()
        
        # Фон
        self.floor_y = height * 0.6
        pygame.draw.rect(self.screen, (66, 170, 255), (0, 0, width, self.floor_y))
        pygame.draw.rect(self.screen, (209, 106, 32), (0, self.floor_y, width, height - self.floor_y))
        pygame.draw.line(self.screen, (139, 69, 19), (0, self.floor_y), (width, self.floor_y), 2)

        # Счёт
        font = pygame.font.Font(None, 36)
        score_text = font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (50, 50))

        # Корзина
        self.basket_x = width * 0.88
        self.basket_y = height * 0.35
        self.target_x = self.basket_x
        self.target_y = self.basket_y

        if self.use_images and 'basket' in self.images:
            basket_rect = self.images['basket'].get_rect(center=(self.basket_x, self.basket_y))
            self.screen.blit(self.images['basket'], basket_rect)
        else:
            # Fallback графика
            pygame.draw.rect(self.screen, (255, 255, 255), (self.basket_x + 15, self.basket_y - 50, 10, 80))
            pygame.draw.rect(self.screen, (128, 128, 128), (self.basket_x + 15, self.basket_y - 50, 10, 80), 3)
            pygame.draw.ellipse(self.screen, (255, 165, 0), (self.basket_x - 35, self.basket_y - 15, 40, 30), 5)
            for i in range(-30, 0, 10):
                pygame.draw.line(self.screen, (255, 255, 255), 
                               (self.basket_x + i, self.basket_y - 10),
                               (self.basket_x + i + 5, self.basket_y + 30), 2)

        # Игрок
        self.man_x = width * 0.18
        self.man_y = self.floor_y

        if self.use_images and 'man' in self.images:
            man_rect = self.images['man'].get_rect(center=(self.man_x, self.man_y - 50))
            self.screen.blit(self.images['man'], man_rect)
        else:
            # Fallback графика
            pygame.draw.rect(self.screen, (46, 92, 138), (self.man_x - 30, self.man_y - 120, 60, 80))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.man_x - 30, self.man_y - 120, 60, 80), 3)
            pygame.draw.ellipse(self.screen, (255, 176, 160), (self.man_x - 25, self.man_y - 155, 50, 40))
            pygame.draw.ellipse(self.screen, (0, 0, 0), (self.man_x - 25, self.man_y - 155, 50, 40), 3)
            pygame.draw.line(self.screen, (51, 51, 51), (self.man_x - 20, self.man_y - 40), (self.man_x - 20, self.man_y), 8)
            pygame.draw.line(self.screen, (51, 51, 51), (self.man_x + 20, self.man_y - 40), (self.man_x + 20, self.man_y), 8)
            pygame.draw.line(self.screen, (255, 176, 160), (self.man_x - 30, self.man_y - 90), (self.man_x - 50, self.man_y - 70), 6)
            pygame.draw.line(self.screen, (255, 176, 160), (self.man_x + 30, self.man_y - 90), (self.man_x + 50, self.man_y - 80), 6)

        # Мяч
        self.ball_start_x = width * 0.69
        self.ball_start_y = height * 0.57
        if not self.is_running and not self.falling:
            self.ball_x = self.ball_start_x
            self.ball_y = self.ball_start_y

        if self.use_images and 'ball' in self.images:
            ball_rect = self.images['ball'].get_rect(center=(self.ball_x, self.ball_y))
            self.screen.blit(self.images['ball'], ball_rect)
        else:
            pygame.draw.circle(self.screen, (247, 127, 15), (int(self.ball_x), int(self.ball_y)), self.ball_radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(self.ball_x), int(self.ball_y)), self.ball_radius, 3)

    def stop(self):
        self.is_running = False
        self.score = 0