import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, images, player):
        super().__init__()
        self.images = images
        self.image = images['idle']
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)  # Вектор позиции врага
        self.player = player
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 2  # Скорость врага
        self.normal_speed = self.speed  # Нормальная скорость врага
        self.slowed_speed = self.speed / 10  # Замедленная скорость врага
        self.state = "patrolling"
        self.patrol_points = [pygame.math.Vector2(pos), pygame.math.Vector2(pos[0] + 100, pos[1])]
        self.current_patrol_point = 0
        self.health = 100  # Начальное здоровье врага
        self.slowed_timer = 0  # Таймер для замедления
        self.slowed_duration = 2000000  # Длительность замедления в миллисекундаx

    def update(self):
        self.update_slowed_state()
        self.change_state()
        self.move()
        self.rect.center = self.position  # Обновляем rect в соответствии с позицией

    def update_slowed_state(self):
        # Проверяем, истек ли таймер замедления
        if self.slowed_timer > 0:
            self.slowed_timer -= pygame.time.get_ticks()
            if self.slowed_timer <= 0:
                self.speed = self.normal_speed  # Восстанавливаем нормальную скорость

    def change_state(self):
        distance_to_player = self.player.position - self.position
        if distance_to_player.length_squared() < 200 ** 2:  # Уменьшенное значение для тестирования
            self.state = "chasing"
        else:
            self.state = "patrolling"
        print(f"Enemy state: {self.state}")

    def move(self):
        if self.state == "patrolling":
            self.patrol()
        elif self.state == "chasing":
            self.chase()

    def patrol(self):
        target = self.patrol_points[self.current_patrol_point]
        self.move_towards(target)
        # Проверяем, находится ли враг достаточно близко к точке патрулирования
        if self.position.distance_to(target) < self.speed:
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def chase(self):
        self.move_towards(self.player.position, stop_distance=50)  # stop_distance можно настроить

    def move_towards(self, target, stop_distance=0):
        direction = target - self.position
        if direction.length() > stop_distance:  # Останавливаемся на расстоянии stop_distance от цели
            direction = direction.normalize()
            self.velocity = direction * self.speed
        else:
            self.velocity = pygame.math.Vector2(0, 0)
        self.position += self.velocity
        self.rect.center = self.position

    def take_damage(self, amount, attacker):
        self.health -= amount
        if self.health <= 0:
            self.die()
        else:
            self.knockback(attacker)
            self.slow_down()  # Замедляем врага

    def knockback(self, attacker):
        # Определите вектор отталкивания в зависимости от позиций атакующего и врага
        knockback_direction = pygame.math.Vector2(self.position.x - attacker.position.x,
                                                  self.position.y - attacker.position.y)
        if knockback_direction.length() > 0:  # Проверка, чтобы избежать деления на ноль
            # Нормализуйте вектор (для получения вектора единичной длины)
            knockback_direction = knockback_direction.normalize()
        else:
            # Если вектор равен нулю (атакующий в той же позиции, что и враг), просто используем случайное направление
            knockback_direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        # Умножьте вектор на силу отталкивания
        knockback_force = 50  # Это значение можно настроить
        knockback_vector = knockback_direction * knockback_force

        # Примените вектор отталкивания к текущему положению врага
        self.position += knockback_vector
        self.rect.center = self.position  # Обновляем rect в соответствии с новой позицией

    def slow_down(self):
        self.speed = self.slowed_speed  # Устанавливаем замедленную скорость
        self.slowed_timer = pygame.time.get_ticks() + self.slowed_duration  # Устанавливаем таймер замедления

    def die(self):
        # Удалите врага из всех групп спрайтов
        self.kill()