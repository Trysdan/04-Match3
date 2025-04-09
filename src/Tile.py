"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Tile.
"""

import pygame

import settings


class Tile:
    def __init__(self, i: int, j: int, color: int, variety: int) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.color = color
        self.variety = variety
        self.draw = True
        self.power_up = 0 # 0: normal, 1: macht4, 2macht5
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        self.alpha_surface.blit(
            settings.TEXTURES["tiles"],
            (0, 0),
            settings.FRAMES["tiles"][self.color][self.variety],
        )
        pygame.draw.rect(
            self.alpha_surface,
            (34, 32, 52, 200),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )
        surface.blit(self.alpha_surface, (self.x + 2 + offset_x, self.y + 2 + offset_y))
        surface.blit(
            settings.TEXTURES["tiles"],
            (self.x + offset_x, self.y + offset_y),
            settings.FRAMES["tiles"][self.color][self.variety],
        )

        if self.power_up > 0:
            if self.power_up == 1:
                # Draw a cross overlay
                pygame.draw.line(
                    surface,
                    (255, 255, 255, 180),
                    (self.x + offset_x + 4, self.y + offset_y + settings.TILE_SIZE // 2),
                    (self.x + offset_x + settings.TILE_SIZE - 4, self.y + offset_y + settings.TILE_SIZE // 2),
                    2
                )
                pygame.draw.line(
                    surface,
                    (255, 255, 255, 180),
                    (self.x + offset_x + settings.TILE_SIZE // 2, self.y + offset_y + 4),
                    (self.x + offset_x + settings.TILE_SIZE // 2, self.y + offset_y + settings.TILE_SIZE - 4),
                    2
                )
            elif self.power_up == 2:
                # Draw a circle overlay
                pygame.draw.circle(
                    surface,
                    (255, 255, 255, 180),
                    (self.x + offset_x + settings.TILE_SIZE // 2, self.y + offset_y + settings.TILE_SIZE // 2),
                    settings.TILE_SIZE // 3,
                    2
                )