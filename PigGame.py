__author__ = 'XemyL'
# -*- coding: utf-8 -*-

# Surface - на ньому малюється
# Rect - зберігає координати
# var = pygame.get_rect(Surface, corner or side=(x, y))
# Surface.get_size - return tuple(width, height)
# Surface.blit(surface, coords) - on this.blit(draw this, (x, y)

import pygame
from sys import exit

pygame.init()
# pygame.display.init() -2mb ram

class Game:
    def __init__(self):
        self.event_queue = None
        self.window_width = pygame.display.Info().current_w
        self.window_height = pygame.display.Info().current_h

        # Initialize window
        self.playground = pygame.display
        self.playSurface = self.playground.set_mode(size=(self.window_width, self.window_height), flags=pygame.FULLSCREEN, depth=32)
        self.bg = pygame.image.load('sprites/bg.png').convert()
        self.playSurface.blit(self.bg, (0, 0))
        self.playground.set_caption('Pig Game')
        self.clock = pygame.time.Clock()

    def mainloop(self):
        while 1:
            self.clock.tick(60)
            self.playSurface.blit(self.bg, (0, 0))
            level.map_drawing()
            self.event_queue = pygame.event.get()
            self.press_buttons()
            pig.move()

            self.playground.flip()

    # Button binds
    # keys = pygame.key.get_pressed() ???
    def press_buttons(self):
        for click in self.event_queue:
            if click.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif click.type == pygame.KEYDOWN:
                if click.key == pygame.K_F4 and click.mod == pygame.KMOD_LALT:
                    pygame.quit()
                    exit()


class Sprite:
    def __init__(self):
        self.coords = None
        self.speed = None
        self.size = None
        self.on_ground = None

    def move(self):
        pass

    def within_tile_x(self, sprite, speed, tile):
        # if tile[0] <= sprite[2] + self.speed[0] <= tile[2] or tile[0] <= sprite[0] + self.speed[0] <= tile[2]:
        if tile[0] < sprite[2] + speed[0] < tile[2] or tile[0] < sprite[0] + speed[0] < tile[2]:
            return True
        else:
            return False

    def within_tile_y_top(self, sprite, speed, tile):
        if tile[1] < sprite[1] + speed[1] < tile[3]:
            return True
        else:
            return False

    def within_tile_y_bottom(self, sprite, speed, tile):
        if tile[1] < sprite[3] + speed[1] < tile[3]:
            return True
        else:
            return False

    def collision_line_y_top(self, sprite, speed, tile):
        if self.within_tile_y_top(sprite, speed, tile):
            if sprite[0] + speed[0] < tile[2] and sprite[2] + speed[0] > tile[0]:
                return True  # speed[1] = 0
            else:
                return False

    def collision_line_y_bottom(self, sprite, speed, tile):
        if self.within_tile_y_bottom(sprite, speed, tile):
            if sprite[0] + speed[0] < tile[2] and sprite[2] + speed[0] > tile[0]:
                self.on_ground = True
                return True  # speed[1] = 0
            else:
                return False

    def collision_line_x(self, sprite, speed, tile):
        if self.within_tile_x(sprite, speed, tile):
            if tile[1] < sprite[1] < tile[3] or tile[1] < sprite[3] < tile[3] or \
            (sprite[1] < tile[1] and sprite[3] > tile[3]):
                self.speed[0] = 0
                speed[0] = 0
                return True  # speed[0] = 0
            else:
                return False

    def collision_check(self, sprite, speed, tiles):
        for tile in tiles:
            if self.collision_line_x(sprite, speed, tile):
                self.speed[0] = 0
            if self.collision_line_y_top(sprite, speed, tile):
                self.speed[1] = 0
            if self.collision_line_y_bottom(sprite, speed, tile):
                self.speed[1] = 0


class Pig(Sprite):
    def __init__(self):
        super().__init__()
        self.speed = [0, 0]  # speed = [x, y]
        self.gravity = 1
        self.pigSurface = pygame.image.load('sprites/Pig1.0.png').convert_alpha()
        self.pigRect = pygame.Surface.get_rect(self.pigSurface, bottomleft=(300, 600))
        self.size = self.pigSurface.get_size()
        game.playSurface.blit(self.pigSurface, self.pigRect)
        game.playground.flip()

    def move(self):
        self.coords = [self.pigRect[0], self.pigRect[1], self.pigRect[0] + self.size[0], self.pigRect[1] + self.size[1]]
        keys = pygame.key.get_pressed()

        # Increase speed
        if self.within_right_border():
            if keys[pygame.K_RIGHT] and self.speed[0] < 10:
                self.speed[0] += 1
        if self.within_left_border():
            if keys[pygame.K_LEFT] and self.speed[0] > -10:
                self.speed[0] -= 1
        if keys[pygame.K_SPACE] and self.on_ground:
            self.on_ground = False
            self.speed[1] = -15
        # Decrease speed
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            if self.speed[0] > 0:
                self.speed[0] -= 1
            if self.speed[0] < 0:
                self.speed[0] += 1
        if not keys[pygame.K_SPACE] or not self.on_ground:
            self.speed[1] += self.gravity

        self.collision_check(self.coords, self.speed, level.mergedtiles_group)
        self.pigRect.move_ip(self.speed[0], self.speed[1])
        game.playSurface.blit(self.pigSurface, self.pigRect)

    def within_right_border(self):
        if self.pigRect[0] + self.pigRect[2] + self.speed[0] + 1 > game.window_width:
            self.speed[0] = 0
            return False
        return True

    def within_left_border(self):
        if self.pigRect[0] + self.speed[0] < 0:
            self.speed[0] = 0
            return False
        return True


class MapBuilder:
    def __init__(self):
        self.tile_size = 32  # tile = square
        self.tile = pygame.image.load('sprites/ground.png').convert()
        self.x, self.y = 0, 0
        self.map_loading()

    def map_loading(self):
        self.tiles_group = []
        self.mergedtiles_group = []
        self.add_tile = []
        map1 = ['0',
                '0',
                '0',
                '0',
                '0',
                '000000000000000000000000000011111',
                '000000000111111000000000000011111',
                '0',
                '0',
                '0',
                '0',
                '0001100000000000000000000000000000000011',
                '0',
                '0001100000000000000000000000000000000011',
                '0001100000000000000000000000000000000111',
                '00000000000000000000000000000000000001',
                '0000000000000011111100000000000000001',
                '0001100000000000000000000001000000010011',
                '0000001000000000000000000001',
                '0000001000000000000000000001',
                '0000001000000000000000000001011',
                '0001101000000000010000000001000000000011',
                '0001101000000000000000000001000000000011',
                '1111111111111111111111111111111111111111']
        for row in map1:
            self.x = 0
            for tile in row:
                if tile == '0':
                    self.x += self.tile_size
                elif tile == '1':
                    self.add_tile = [self.x, self.y, self.x + self.tile_size, self.y + self.tile_size]
                    self.tiles_group.append(self.add_tile)
                    self.x += self.tile_size
            self.y += self.tile_size
        self.to_merge_tiles_row = []
        self.tiles_group_merging = self.tiles_group[:]
        self.merge_tiles_row(self.tiles_group_merging)

    def map_drawing(self):
        for tile in self.tiles_group:
            self.tileSurface = pygame.Surface.get_rect(self.tile, topleft=(tile[0], tile[1]))
            game.playSurface.blit(self.tile, self.tileSurface)

    def merge_tiles_row(self, tiles):
        if tiles == []:
            self.to_merge_tiles_row.sort(key=lambda tile: tile[0])
            self.merge_tiles_column(self.to_merge_tiles_row)
        else:
            tile = tiles[0]
            while len(tiles) > 1 and tile[2] == tiles[1][0] and tile[1] == tiles[1][1] and \
            tile[3] == tiles[1][3]:
                tile[2], tile[3] = tiles[1][2], tiles[1][3]
                tiles.pop(1)
            self.to_merge_tiles_row.append(tile)
            tiles.pop(0)
            self.merge_tiles_row(tiles)

    def merge_tiles_column(self, tiles):
        if tiles == []:
            return
        else:
            tile = tiles[0]
            while len(tiles) > 1 and tile[0] == tiles[1][0] and tile[2] == tiles[1][2] and \
            tile[3] == tiles[1][1]:
                tile[2], tile[3] = tiles[1][2], tiles[1][3]
                tiles.pop(1)
            self.mergedtiles_group.append(tile)
            tiles.pop(0)
            self.merge_tiles_column(tiles)

game = Game()
level = MapBuilder()
pig = Pig()

# Start
game.mainloop()
