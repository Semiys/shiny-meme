# player.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED
from inventory import Inventory  # Импорт класса Inventory

class Player(pygame.sprite.Sprite):
    MAX_HEALTH = 100
    MAX_ENERGY = 100

    def __init__(self):
        super().__init__()
        self.speed = PLAYER_SPEED
        self.direction = 'down'  # Начальное направление
        self.walking = False  # Состояние движения
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.health = 100
        self.energy = 100
        self.inventory = Inventory()
        # Инициализация инвентаря для игрока

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
        # Инициализация здоровья и энергии
        self.health = self.MAX_HEALTH
        self.energy = self.MAX_ENERGY

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

    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)  # Предотвращаем отрицательное здоровье
        if self.health == 0:
            self.die()

    def die(self):
        # Здесь может быть код для обработки смерти игрока, например:
        print("Игрок умер!")  # Замените это на реальную логику игры
        # Может быть перезагрузка уровня или показ экрана "Game Over"

    def heal(self, amount):
        self.health = min(self.MAX_HEALTH, self.health + amount)

    def use_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            return True  # Энергия успешно использована
        else:
            print("Не хватает энергии!")  # Замените это на реальную логику игры
            return False  # Действие не может быть выполнено из-за недостатка энергии

    def restore_energy(self, amount):
        self.energy = min(self.MAX_ENERGY, self.energy + amount)  # Предотвращаем энергию выше максимума

    # Метод для добавления предмета в инвентарь
    def add_item_to_inventory(self, item_name, quantity=1):
        self.inventory.add_item(item_name, quantity)

    # Метод для использования предмета из инвентаря
    def use_item(self, item_name):
        return self.inventory.use_item(item_name, self)

    def get_items(self):
        return self.inventory