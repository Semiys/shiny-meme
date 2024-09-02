import pygame

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
        self.state = "patrolling"
        self.patrol_points = [pygame.math.Vector2(pos), pygame.math.Vector2(pos[0] + 100, pos[1])]
        self.current_patrol_point = 0

    def update(self):
        self.change_state()
        self.move()
        self.rect.center = self.position  # Обновляем rect в соответствии с позицией

    def change_state(self):
        distance_to_player = self.player.position - self.position
        if distance_to_player.length_squared() < 100 ** 2:  # Уменьшенное значение для тестирования
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