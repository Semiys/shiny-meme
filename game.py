# game.py
import pygame
from settings import *
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cyberpunk RPG Game")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.running = True
        # Создание предметов для восстановления здоровья
        self.health_items = [pygame.sprite.Sprite() for _ in range(2)]
        for i, item in enumerate(self.health_items):
            item.image = pygame.Surface((30, 30))
            item.image.fill((0, 0, 255))
            item.rect = item.image.get_rect(topleft=(i * 300, 300))
            # Создание предметов для восстановления энергии
        self.energy_items = [pygame.sprite.Sprite() for _ in range(2)]
        for i, item in enumerate(self.energy_items):
            item.image = pygame.Surface((30, 30))
            item.image.fill((255, 255, 0))
            item.rect = item.image.get_rect(topleft=(i * 400, 300))
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Нажатие клавиши 'h' для использования предмета здоровья
                    self.player.use_item("health_potion")
                elif event.key == pygame.K_e:  # Нажатие клавиши 'e' для использования предмета энергии
                    self.player.use_item("energy_potion")
                elif event.key == pygame.K_f:  # Нажатие клавиши 'f' для подбора предметов
                    self.check_item_pickup()

    def check_item_pickup(self):
        # Проверка столкновений с предметами здоровья
        for item in self.health_items[:]:  # Создаем копию списка, чтобы избежать ошибок во время итерации
            if self.player.rect.colliderect(item.rect):
                self.player.inventory.pickup_item("health_potion", lambda: self.health_items.remove(item))

        # Проверка столкновений с предметами энергии
        for item in self.energy_items[:]:  # Аналогично создаем копию списка
            if self.player.rect.colliderect(item.rect):
                self.player.inventory.pickup_item("energy_potion", lambda: self.energy_items.remove(item))
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)


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

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_inventory()  # Вызов метода отрисовки инвентаря
        # Отображение предметов здоровья
        for item in self.health_items:
            self.screen.blit(item.image, item.rect.topleft)

        # Отображение предметов энергии
        for item in self.energy_items:
            self.screen.blit(item.image, item.rect.topleft)

        # Отображение полос здоровья и энергии
        self.draw_health_bar(self.player.health, self.player.MAX_HEALTH, (20, 20), (255, 0, 0))
        self.draw_health_bar(self.player.energy, self.player.MAX_ENERGY, (20, 40), (0, 0, 255))
        pygame.display.flip()

    def quit(self):
        pygame.quit()