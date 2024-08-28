# player.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = PLAYER_SPEED
        self.direction = 'down'  # Начальное направление
        self.walking = False  # Состояние движения

        # Загрузка анимаций
        self.animations = {
            'idle': {
                'down': [pygame.image.load('assets/player/idle/Cyborgsolo_idle1.png').convert_alpha()],
                'up': [pygame.image.load('assets/player/idle/Cyborgsolo_idle2.png').convert_alpha()],
                'left': [pygame.image.load('assets/player/idle/Cyborgsolo_idle3.png').convert_alpha()],
                'right': [pygame.image.load('assets/player/idle/Cyborgsolo_idle4.png').convert_alpha()]
            },
            'walking': {
                'down': [pygame.image.load(f'assets/player/run/Cyborgsolo_run{i}.png').convert_alpha() for i in
                         range(1, 7)],
                'up': [pygame.image.load(f'assets/player/run/Cyborgsolo_run{i}.png').convert_alpha() for i in
                       range(1, 7)],
                'left': [pygame.image.load(f'assets/player/run/Cyborgsolo_run{i}.png').convert_alpha() for i in
                         range(1, 7)],
                'right': [pygame.image.load(f'assets/player/run/Cyborgsolo_run{i}.png').convert_alpha() for i in
                          range(1, 7)]
            }
        }

        # Установка начального изображения как первый элемент списка анимации 'idle' 'down'
        self.image = self.animations['idle']['down'][0]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


        self.current_frame = 0
        self.last_updated = pygame.time.get_ticks()
        self.frame_rate = 100  # Скорость смены кадров в миллисекундах

    def update(self, keys):
        self.walking = False
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = 'left'
            self.walking = True
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'right'
            self.walking = True
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = 'up'
            self.walking = True
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = 'down'
            self.walking = True

        # Анимация движения
        animation_type = 'walking' if self.walking else 'idle'
        animation_frames = self.animations[animation_type][self.direction]

        now = pygame.time.get_ticks()
        if now - self.last_updated > self.frame_rate:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(animation_frames)
            self.image = animation_frames[self.current_frame]