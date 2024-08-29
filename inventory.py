# inventory.py
import pygame


class Inventory:
    def __init__(self):
        self.items = {}  # Словарь для хранения предметов и их количества
        self.item_images = {
            'health_potion': pygame.image.load('assets/titles/Tiles.png').convert_alpha(),
            'energy_potion': pygame.image.load('assets/titles/Tiles.png').convert_alpha()
            # Добавьте другие предметы и их иконки здесь
        }
    def add_item(self, item_name, quantity=1):
        self.items[item_name] = self.items.get(item_name, 0) + quantity

    def remove_item(self, item_name, quantity=1):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] <= 0:
                del self.items[item_name]
            return True
        return False

    def use_item(self, item_name, player):
        if self.remove_item(item_name):
            if item_name == "health_potion":
                player.heal(20)
            elif item_name == "energy_potion":
                player.restore_energy(20)
            # Добавьте здесь другие предметы и их эффекты
            return True
        else:
            print(f"No {item_name} left in inventory!")
            return False

    def pickup_item(self, item_name):
        self.add_item(item_name)



    def get_items(self):
        return self.items.items()