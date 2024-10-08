# game.py
import pygame
import pytmx
from settings import *
from player import Player
from camera import Camera
from pytmx.util_pygame import load_pygame
from enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG Game")
        self.clock = pygame.time.Clock()
        screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.player = Player(screen_center)
        self.running = True
        # Загрузка иконок предметов
        self.health_item_image = pygame.image.load('assets/potion/Healthpotion.png').convert_alpha()
        self.energy_item_image = pygame.image.load('assets/titles/Tiles.png').convert_alpha()
        # Загрузка карты
        self.tmx_data = load_pygame('mapdev/Testmap.tmx')
        self.map_surface = self.make_map()
        self.map_rect = self.map_surface.get_rect()

        # Создание предметов для восстановления здоровья
        self.health_items = []
        for i in range(2):
            item = pygame.sprite.Sprite()
            item.image = self.health_item_image
            item.rect = item.image.get_rect(topleft=(i * 300, 300))
            self.health_items.append(item)

        # Создание предметов для восстановления энергии
        self.energy_items = []
        for i in range(2):
            item = pygame.sprite.Sprite()
            item.image = self.energy_item_image
            item.rect = item.image.get_rect(topleft=(i * 400, 300))
            self.energy_items.append(item)
        self.camera = Camera(self.tmx_data.width * self.tmx_data.tilewidth, self.tmx_data.height * self.tmx_data.tileheight)
        self.enemies = pygame.sprite.Group()
        self.load_enemies()
    def camera_update(self, target):
        self.camera.update(target)
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.camera_update(self.player)  # Обновляем камеру с учетом положения игрока

    # В классе Game
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Нажатие клавиши 'h' для использования предмета здоровья
                    self.player.inventory.use_item("health_potion", self.player)
                elif event.key == pygame.K_e:  # Нажатие клавиши 'e' для использования предмета энергии
                    self.player.inventory.use_item("energy_potion", self.player)
                elif event.key == pygame.K_f:  # Нажатие клавиши 'f' для подбора предметов
                    self.check_item_pickup()

    def check_item_pickup(self):
        # Проверка столкновений с предметами здоровья
        for item in self.health_items[:]:  # Создаем копию списка, чтобы избежать ошибок во время итерации
            if self.player.rect.colliderect(item.rect):
                self.player.inventory.pickup_item("health_potion")
                self.health_items.remove(item)  # Удаляем предмет из списка после подбора

        # Проверка столкновений с предметами энергии
        for item in self.energy_items[:]:  # Аналогично создаем копию списка
            if self.player.rect.colliderect(item.rect):
                self.player.inventory.pickup_item("energy_potion")
                self.energy_items.remove(item)  # Удаляем предмет из списка после подбора
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys,self.enemies)
        self.enemies.update()
        self.camera.update(self.player)   # Обновляем камеру с учетом положения игрока


    def draw_health_bar(self, current, max, pos, color):
        # Рисуем полосу здоровья на экране
        bar_length = 100
        bar_height = 10
        fill = (current / max) * bar_length
        outline_rect = pygame.Rect(pos, (bar_length, bar_height))
        fill_rect = pygame.Rect(pos, (fill, bar_height))
        pygame.draw.rect(self.screen, color, fill_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2)

    def draw_inventory(self):
        # Отображение фона инвентаря
        inventory_background = pygame.Rect(10, SCREEN_HEIGHT - 70, 200, 60)
        pygame.draw.rect(self.screen, (50, 50, 50), inventory_background)

        # Отображение иконок предметов инвентаря
        x = 20
        y = SCREEN_HEIGHT - 65  # Отступ сверху для иконок
        for item_name, quantity in self.player.inventory.get_items():
            # Получаем изображение иконки для предмета
            item_image = self.player.inventory.item_images[item_name]
            # Отрисовка иконки предмета
            self.screen.blit(item_image, (x, y))
            # Отрисовка количества предмета
            font = pygame.font.Font(None, 24)
            text_surface = font.render(str(quantity), True, (255, 255, 255))
            self.screen.blit(text_surface, (x + item_image.get_width() + 5, y))
            # Сдвигаем x для отображения следующего предмета
            x += item_image.get_width() + 40  # Дополнительный отступ между иконками

    def make_map(self):
        """Создает Pygame Surface для всей карты."""
        temp_surface = pygame.Surface((self.tmx_data.width * self.tmx_data.tilewidth,
                                       self.tmx_data.height * self.tmx_data.tileheight))
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        temp_surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
        return temp_surface

    def draw_debug(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (255, 0, 0), self.camera.apply_rect(enemy.rect), 1)
        pygame.draw.rect(self.screen, (0, 255, 0), self.camera.apply_rect(self.player.rect), 1)
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map_surface, self.camera.apply_rect(self.map_rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        for item in self.health_items:
            self.screen.blit(item.image, self.camera.apply(item))
        for item in self.energy_items:
            self.screen.blit(item.image, self.camera.apply(item))
        # В методе draw класса Game
        for enemy in self.enemies:
            self.screen.blit(enemy.image, self.camera.apply(enemy))

        self.draw_inventory()
        self.draw_health_bar(self.player.health, self.player.MAX_HEALTH, (20, 20), (255, 0, 0))
        self.draw_health_bar(self.player.energy, self.player.MAX_ENERGY, (20, 40), (0, 0, 255))
        self.draw_debug()  # Рисуем отладочную информацию
        pygame.display.flip()

    def load_enemies(self):
        print("Загрузка врагов...")
        enemy_images = {
            'idle': pygame.image.load('assets/player/idle/idle_left0.png').convert_alpha(),
        }
        for obj in self.tmx_data.objects:
            if obj.typesd == 'enemy':  # Исправление здесь: должно быть 'type', а не 'typesd'
                print(f"Загрузка врага на позиции: ({obj.x}, {obj.y})")
                enemy = Enemy((obj.x, obj.y), enemy_images, self.player)
                self.enemies.add(enemy)
    def quit(self):
        pygame.quit()