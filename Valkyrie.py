import pygame
from SETTINGS import *
from LoadLevel import enemies, sprites, group_player
from valkyrie_images import valkyrie_images


class Valkyrie(pygame.sprite.Sprite):
    images = valkyrie_images

    def __init__(self, pos):
        super(Valkyrie, self).__init__(sprites, enemies)

        self.health = 3000
        self.max_health = 3000
        self.kd_bar_show = 100
        self.bar_status_show = False
        self.speed = 2

        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, player_width, player_height)
        self.key = 'front3'
        self.image = Valkyrie.images[self.key]

        self.health_bar = pygame.sprite.Sprite()
        self.draw_health_bar()

        self.kd_self_bar_show = 100
        self.status_self_bar_show = False

        self.hit_amount = 0

    def update(self, dmg_dealer=None, **kwargs):
        if dmg_dealer:
            self.get_hit(dmg_dealer)
        if self.status_self_bar_show:
            if self.status_self_bar_show == self.kd_self_bar_show:
                self.status_self_bar_show = False
                self.health_bar.remove(sprites)
            else:
                self.status_self_bar_show += 1
            self.show_health_bar()
        if self.key == 'front3':
            self.image = pygame.transform.scale(self.image, (tile_width, tile_height))

    def draw_health_bar(self):
        self.health_bar.rect = pygame.Rect(self.rect.x, self.rect.y - (10 * height // 600), player_width, hp_bar_height)
        image = pygame.Surface((player_width, hp_bar_height), pygame.SRCALPHA)
        length_line = player_width * self.health // self.max_health
        pygame.draw.rect(image, red, (0, 0, length_line, hp_bar_height))
        pygame.draw.rect(image, black, (0, 0, player_width, hp_bar_height), 1)
        self.health_bar.image = image

    def show_health_bar(self):
        if not sprites.has(self.health_bar) and self.status_self_bar_show:
            sprites.add(self.health_bar)
        self.draw_health_bar()

    def get_hit(self, dmg_dealer):
        damage_box = dmg_dealer.damage_box
        if pygame.sprite.collide_rect(self, damage_box):
            self.hit_amount += 1
            if self.hit_amount >= 100:
                group_player.update(dmg_dealer=dmg_dealer)
            self.health -= dmg_dealer.damage
            if self.health > 0:
                self.status_self_bar_show = 1
            else:
                self.health = 0
                self.status_self_bar_show = False
                self.kill(), self.health_bar.kill()

    def get_hit_count(self):
        return self.hit_amount
