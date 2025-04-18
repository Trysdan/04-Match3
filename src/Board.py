"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Board.
"""

from typing import List, Optional, Tuple, Any, Dict, Set

import pygame

import random

import settings
from src.Tile import Tile


class Board:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.matches: List[List[Tile]] = []
        self.tiles: List[List[Tile]] = []
        self.__initialize_tiles()

    def render(self, surface: pygame.Surface) -> None:
        for row in self.tiles:
            for tile in row:
                # Adjustment not to draw twice the tile that I move
                if tile.draw:
                    tile.render(surface, self.x, self.y)

    def __is_match_generated(self, i: int, j: int, color: int) -> bool:
        if (
            i >= 2
            and self.tiles[i - 1][j].color == color
            and self.tiles[i - 2][j].color == color
        ):
            return True

        return (
            j >= 2
            and self.tiles[i][j - 1].color == color
            and self.tiles[i][j - 2].color == color
        )

    def __initialize_tiles(self) -> None:
        self.tiles = [
            [None for _ in range(settings.BOARD_WIDTH)]
            for _ in range(settings.BOARD_HEIGHT)
        ]
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                color = random.randint(0, settings.NUM_COLORS - 1)
                while self.__is_match_generated(i, j, color):
                    color = random.randint(0, settings.NUM_COLORS - 1)

                self.tiles[i][j] = Tile(
                    i, j, color, random.randint(0, settings.NUM_VARIETIES - 1)
                )

    def __calculate_match_rec(self, tile: Tile) -> Set[Tile]:
        if tile in self.in_stack:
            return []

        self.in_stack.add(tile)

        color_to_match = tile.color

        ## Check horizontal match
        h_match: List[Tile] = []

        # Check left
        if tile.j > 0:
            left = max(0, tile.j - 2)
            for j in range(tile.j - 1, left - 1, -1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        # Check right
        if tile.j < settings.BOARD_WIDTH - 1:
            right = min(settings.BOARD_WIDTH - 1, tile.j + 2)
            for j in range(tile.j + 1, right + 1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        ## Check vertical match
        v_match: List[Tile] = []

        # Check top
        if tile.i > 0:
            top = max(0, tile.i - 2)
            for i in range(tile.i - 1, top - 1, -1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        # Check bottom
        if tile.i < settings.BOARD_HEIGHT - 1:
            bottom = min(settings.BOARD_HEIGHT - 1, tile.i + 2)
            for i in range(tile.i + 1, bottom + 1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        match: List[Tile] = []

        if len(h_match) >= 2:
            for t in h_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(v_match) >= 2:
            for t in v_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(match) > 0:
            if tile not in self.in_match:
                self.in_match.add(tile)
                match.append(tile)

        for t in match:
            match += self.__calculate_match_rec(t)

        self.in_stack.remove(tile)
        return match

    def calculate_matches_for(
        self, new_tiles: List[Tile], last_moved_i: int = -1, last_moved_j: int = -1
    ) -> Optional[List[List[Tile]]]:
        self.in_match: Set[Tile] = set()
        self.in_stack: Set[Tile] = set()

        self.matches = []
        match_sizes = []

        for tile in new_tiles:
            if tile in self.in_match:
                continue
            match = self.__calculate_match_rec(tile)
            if len(match) > 0:
                self.matches.append(match)
                match_sizes.append(len(match))

        delattr(self, "in_match")
        delattr(self, "in_stack")

        if last_moved_i >= 0 and last_moved_j >= 0 and match_sizes:
            for i, match in enumerate(self.matches):
                if i < len(match_sizes) and match_sizes[i] >= 4:
                    for tile in match:
                        if tile.i == last_moved_i and tile.j == last_moved_j:
                            match_color = tile.color
                            match.remove(tile)
                            power_up_type = 1 if match_sizes[i] == 4 else 2
                            tile.power_up = power_up_type
                            break

        return self.matches if len(self.matches) > 0 else None

    def remove_matches(self, last_moved_i: int = -1, last_moved_j: int = -1) -> List[Tuple[int, int, int]]:
        power_ups_to_create = []
    
        for match in self.matches:
            if len(match) >= 4 and last_moved_i >= 0 and last_moved_j >= 0:
                for tile in match:
                    if tile.i == last_moved_i and tile.j == last_moved_j:
                        power_up_type = 1 if len(match) == 4 else 2
                        power_ups_to_create.append((tile.i, tile.j, tile.color, power_up_type))
                        break
                    
            for tile in match:
                if any(tile.i == i and tile.j == j for i, j, _, _ in power_ups_to_create):
                    continue
                self.tiles[tile.i][tile.j] = None
    
        # Create power-ups
        for i, j, color, power_up_type in power_ups_to_create:
            self.tiles[i][j] = Tile(i, j, color, random.randint(0, settings.NUM_VARIETIES - 1))
            self.tiles[i][j].power_up = power_up_type
    
        self.matches = []
        return power_ups_to_create

    def get_falling_tiles(self) -> Tuple[Any, Dict[str, Any]]:
        # List of tweens to create
        tweens: Tuple[Tile, Dict[str, Any]] = []

        # for each column, go up tile by tile until we hit a space
        for j in range(settings.BOARD_WIDTH):
            space = False
            space_i = -1
            i = settings.BOARD_HEIGHT - 1

            while i >= 0:
                tile = self.tiles[i][j]

                # if our previous tile was a space
                if space:
                    # if the current tile is not a space
                    if tile is not None:
                        self.tiles[space_i][j] = tile
                        tile.i = space_i

                        # set its prior position to None
                        self.tiles[i][j] = None

                        tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))
                        space = False
                        i = space_i
                        space_i = -1
                elif tile is None:
                    space = True

                    if space_i == -1:
                        space_i = i

                i -= 1

        # create a replacement tiles at the top of the screen
        for j in range(settings.BOARD_WIDTH):
            for i in range(settings.BOARD_HEIGHT):
                tile = self.tiles[i][j]

                if tile is None:
                    tile = Tile(
                        i,
                        j,
                        random.randint(0, settings.NUM_COLORS - 1),
                        random.randint(0, settings.NUM_VARIETIES - 1),
                    )
                    tile.y -= settings.TILE_SIZE
                    self.tiles[i][j] = tile
                    tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))

        return tweens

    def count_possible_matches(self) -> int:
        def swap(i1, j1, i2, j2):
            self.tiles[i1][j1], self.tiles[i2][j2] = self.tiles[i2][j2], self.tiles[i1][j1]
        
        # Lightweight quick-check for potential matches
        def has_match():
            for i in range(settings.BOARD_HEIGHT):
                count = 1
                for j in range(1, settings.BOARD_WIDTH):
                    if self.tiles[i][j].color == self.tiles[i][j - 1].color:
                        count += 1
                        if count >= 3:
                            return True
                    else:
                        count = 1

            for j in range(settings.BOARD_WIDTH):
                count = 1
                for i in range(1, settings.BOARD_HEIGHT):
                    if self.tiles[i][j].color == self.tiles[i - 1][j].color:
                        count += 1
                        if count >= 3:
                            return True
                    else:
                        count = 1
            return False

        match_count = 0

        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                if j < settings.BOARD_WIDTH - 1:
                    swap(i, j, i, j + 1)
                    if has_match():
                        match_count += 1
                    swap(i, j, i, j + 1)

                if i < settings.BOARD_HEIGHT - 1:
                    swap(i, j, i + 1, j)
                    if has_match():
                        match_count += 1
                    swap(i, j, i + 1, j)

        if match_count == 0:
            self.recreate_board()
            match_count = self.count_possible_matches()

        return match_count

    def recreate_board(self) -> None:
        self.__initialize_tiles()

    def create_power_up(self, tile: Tile, match_size: int) -> None:
        tile.power_up = 1 if match_size == 4 else 2
        tile.variety = random.randint(0, settings.NUM_VARIETIES - 1)

    def activate_power_up(self, tile: Tile) -> List[Tile]:
        affected_tiles = []
   
        if tile.power_up == 1:
            for j in range(settings.BOARD_WIDTH):
                if j != tile.j and self.tiles[tile.i][j] is not None:
                    affected_tiles.append(self.tiles[tile.i][j])
       
            for i in range(settings.BOARD_HEIGHT):
                if i != tile.i and self.tiles[i][tile.j] is not None:
                    affected_tiles.append(self.tiles[i][tile.j])

        elif tile.power_up == 2:
            for i in range(settings.BOARD_HEIGHT):
                for j in range(settings.BOARD_WIDTH):
                    if self.tiles[i][j] is not None and self.tiles[i][j].color == tile.color:
                        if i != tile.i or j != tile.j:
                            affected_tiles.append(self.tiles[i][j])
   
        return affected_tiles