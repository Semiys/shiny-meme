# player.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED
from inventory import Inventory  # Импорт класса Inventory


def load_and_scale_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)
class Player(pygame.sprite.Sprite):
    MAX_HEALTH = 100
    MAX_ENERGY = 100

    def __init__(self,pos):
        super().__init__()
        self.position = pygame.math.Vector2(pos)
        self.speed = PLAYER_SPEED
        self.direction = 'down'  # Начальное направление
        self.walking = False  # Состояние движения
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        self.inventory = Inventory()
        # Инициализация инвентаря для игрока


        frame_size = (64, 64)

        self.animations = {
            'idle': {
                'down': [load_and_scale_image(f'assets/player/idle/idle_right{i}.png', frame_size) for i in
                         range(0, 11)],
                'up': [load_and_scale_image(f'assets/player/idle/idle_left{i}.png', frame_size) for i in range(0, 11)],
                'left': [load_and_scale_image(f'assets/player/idle/idle_left{i}.png', frame_size) for i in
                         range(0, 11)],
                'right': [load_and_scale_image(f'assets/player/idle/idle_right{i}.png', frame_size) for i in
                          range(0, 11)]
            },
            'walking': {
                'down': [load_and_scale_image(f'assets/player/walk/walk_right{i}.png', frame_size) for i in
                         range(0, 13)],
                'up': [load_and_scale_image(f'assets/player/walk/walk_left{i}.png', frame_size) for i in range(0, 13)],
                'left': [load_and_scale_image(f'assets/player/walk/walk_left{i}.png', frame_size) for i in
                         range(0, 13)],
                'right': [load_and_scale_image(f'assets/player/walk/walk_right{i}.png', frame_size) for i in
                          range(0, 13)]
            },
            'attacking': {
                'down': [load_and_scale_image(f'assets/player/attack/attacking_right{i}.png', frame_size) for i in
                         range(0, 18)],
                'up': [load_and_scale_image(f'assets/player/attack/attacking_left{i}.png', frame_size) for i in
                       range(0, 18)],
                'left': [load_and_scale_image(f'assets/player/attack/attacking_left{i}.png', frame_size) for i in
                         range(0, 18)],
                'right': [load_and_scale_image(f'assets/player/attack/attacking_right{i}.png', frame_size) for i in
                          range(0, 18)]
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
        self.attacking = False  # Новое состояние для атаки

    def update(self, keys):
        self.walking = False

        # Переменные для движения
        move_x, move_y = 0, 0

        # Проверка на атаку
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.current_frame = 0


        # Определение типа анимации
        if self.attacking:
            animation_type = 'attacking'
            # Устанавливаем продолжительность анимации атаки, например, равной длине списка кадров анимации
            if self.current_frame == len(self.animations[animation_type][self.direction]) - 1:
                self.attacking = False  # Завершаем анимацию атаки
        else:
            if keys[pygame.K_a]:
                move_x -= self.speed
                self.direction = 'left'
            if keys[pygame.K_d]:
                move_x += self.speed
                self.direction = 'right'
            if keys[pygame.K_w]:
                move_y -= self.speed
                if not keys[pygame.K_a] and not keys[pygame.K_d]:  # Если не двигаемся по горизонтали
                    self.direction = 'up'
            if keys[pygame.K_s]:
                move_y += self.speed
                if not keys[pygame.K_a] and not keys[pygame.K_d]:  # Если не двигаемся по горизонтали
                    self.direction = 'down'

            # Обновляем позицию игрока
            self.rect.x += move_x
            self.rect.y += move_y
            self.position = pygame.math.Vector2(self.rect.center)  # Обновляем вектор позиции игрока

            # Установка флага ходьбы, если персонаж переместился
            self.walking = move_x != 0 or move_y != 0

            # Определяем тип анимации на основе движения
            animation_type = 'walking' if self.walking else 'idle'

        # Получение кадров анимации
        animation_frames = self.animations[animation_type][self.direction]

        now = pygame.time.get_ticks()
        if now - self.last_updated > self.frame_rate:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(animation_frames)
            self.image = animation_frames[self.current_frame]

            # Если анимация атаки закончилась, вернуть размер изображения к исходному
            if not self.attacking:
                original_size = (64, 64)  # Установите исходный размер персонажа
                self.image = pygame.transform.scale(self.image, original_size)
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                # Масштабирование изображения во время атаки
                attack_size = (114, 76)  # Установите нужный размер для анимации атаки
                self.image = pygame.transform.scale(self.image, attack_size)
                self.rect = self.image.get_rect(center=self.rect.center)


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