"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Position in the grid which we are highlighting
        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        self.highlighted_tile = False #recicle to dragging

        # Drag and drop
        self.drag_origin_x = -1
        self.drag_origin_y = -1
        self.dragged_tile = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000 

        self.possible_matches_count = self.board.count_possible_matches()

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)
        
        # Drawing moving tile
        # I do it this way because I want to draw the moving tile on top of the other tiles.
        if self.highlighted_tile and self.dragged_tile is not None:
            original_x = self.dragged_tile.x
            original_y = self.dragged_tile.y
            
            self.dragged_tile.x = self.drag_offset_x
            self.dragged_tile.y = self.drag_offset_y
            
            self.dragged_tile.render(surface, self.board.x, self.board.y)

            self.dragged_tile.x = original_x
            self.dragged_tile.y = original_y

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Possible Matches: {self.possible_matches_count}",
            settings.FONTS["small"],
            30,
            136,
            (99, 155, 255),
            shadowed=True,
        )
    
    # Validate click on the board
    def get_board_position(self, pos_x: int, pos_y: int):
        pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
        pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
        
        i = (pos_y - self.board.y) // settings.TILE_SIZE
        j = (pos_x - self.board.x) // settings.TILE_SIZE
        
        if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
            return (i, j)
        return None

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        if input_id == "click":
            pos_x, pos_y = input_data.position
            board_pos = self.get_board_position(pos_x, pos_y)

            if input_data.pressed and board_pos is not None:

                i, j = board_pos

                # Check if the player clicked on a power-up
                if self.board.tiles[i][j].power_up > 0 and not self.highlighted_tile:
                    self.active = False
                    power_up_tile = self.board.tiles[i][j]
                    affected_tiles = self.board.activate_power_up(power_up_tile)
                    affected_tiles.append(power_up_tile)
                    self.__remove_affected_tiles(affected_tiles)                    
                    return

                if not self.highlighted_tile:
                    self.highlighted_tile = True
                    self.highlighted_i1 = i
                    self.highlighted_j1 = j
                    self.dragged_tile = self.board.tiles[i][j]

                    self.drag_origin_x = self.dragged_tile.x
                    self.drag_origin_y = self.dragged_tile.y

                    self.drag_offset_x = self.dragged_tile.x
                    self.drag_offset_y = self.dragged_tile.y
                    
                    self.dragged_tile.draw = False

            elif input_data.released and self.highlighted_tile:
                release_pos = self.get_board_position(pos_x, pos_y)

                if release_pos is not None:
                    i, j = release_pos

                    self.highlighted_i2 = i
                    self.highlighted_j2 = j
                    di = abs(self.highlighted_i2 - self.highlighted_i1)
                    dj = abs(self.highlighted_j2 - self.highlighted_j1)

                    if di <= 1 and dj <= 1 and di != dj:
                        self.active = False
                        tile1 = self.board.tiles[self.highlighted_i1][
                            self.highlighted_j1
                        ]
                        tile2 = self.board.tiles[self.highlighted_i2][
                            self.highlighted_j2
                        ]
                        self.dragged_tile.x = self.drag_origin_x
                        self.dragged_tile.y = self.drag_origin_y

                        def arrive():
                            tile1 = self.board.tiles[self.highlighted_i1][
                                self.highlighted_j1
                            ]
                            tile2 = self.board.tiles[self.highlighted_i2][
                                self.highlighted_j2
                            ]
                            (
                                self.board.tiles[tile1.i][tile1.j],
                                self.board.tiles[tile2.i][tile2.j],
                            ) = (
                                self.board.tiles[tile2.i][tile2.j],
                                self.board.tiles[tile1.i][tile1.j],
                            )
                            tile1.i, tile1.j, tile2.i, tile2.j = (
                                tile2.i,
                                tile2.j,
                                tile1.i,
                                tile1.j,
                            )

                            def reverse():
                                # Reverse changes
                                (
                                    self.board.tiles[tile1.i][tile1.j],
                                    self.board.tiles[tile2.i][tile2.j],
                                ) = (
                                    self.board.tiles[tile2.i][tile2.j],
                                    self.board.tiles[tile1.i][tile1.j],
                                )
                                tile1.i, tile1.j, tile2.i, tile2.j = (
                                    tile2.i,
                                    tile2.j,
                                    tile1.i,
                                    tile1.j,
                                )
                                self.active = True
                            
                            matches = self.board.calculate_matches_for([tile1, tile2], self.highlighted_i2, self.highlighted_j2)

                            if matches is None:
                                Timer.tween(
                                    0.25,
                                    [
                                        (tile1, {"x": tile2.x, "y": tile2.y}),
                                        (tile2, {"x": tile1.x, "y": tile1.y}),
                                    ],
                                    on_finish=reverse,
                                )
                            else:
                                self.__calculate_matches([tile1, tile2], self.highlighted_i2, self.highlighted_j2)

                        # Swap tiles
                        Timer.tween(
                            0.25,
                            [
                                (tile1, {"x": tile2.x, "y": tile2.y}),
                                (tile2, {"x": tile1.x, "y": tile1.y}),
                            ],
                            on_finish=arrive,
                        )
                    else:
                        self.dragged_tile.x = self.drag_origin_x
                        self.dragged_tile.y = self.drag_origin_y

                else:
                    self.dragged_tile.x = self.drag_origin_x
                    self.dragged_tile.y = self.drag_origin_y

                self.highlighted_tile = False
                self.drag_origin_x = -1
                self.drag_origin_y = -1
                self.dragged_tile.draw = True
                self.dragged_tile = None

        elif input_id == "mouse_motion" and self.highlighted_tile:
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            
            # Tile center
            origin_mouse_x = self.board.x + self.highlighted_j1 * settings.TILE_SIZE + settings.TILE_SIZE // 2
            origin_mouse_y = self.board.y + self.highlighted_i1 * settings.TILE_SIZE + settings.TILE_SIZE // 2

            delta_x = pos_x - origin_mouse_x
            delta_y = pos_y - origin_mouse_y

            max_offset = settings.TILE_SIZE

            # Limit movement 
            if abs(delta_x) > settings.TILE_SIZE // 4:
                delta_x = max(-max_offset, min(max_offset, delta_x))
                self.drag_offset_x = self.drag_origin_x + delta_x
                self.drag_offset_y = self.drag_origin_y
            elif abs(delta_y) > settings.TILE_SIZE // 4:
                delta_y = max(-max_offset, min(max_offset, delta_y))
                self.drag_offset_x = self.drag_origin_x
                self.drag_offset_y = self.drag_origin_y + delta_y

    def __calculate_matches(self, tiles: List, last_moved_i: int = -1, last_moved_j: int = -1) -> None:
        matches = self.board.calculate_matches_for(tiles, last_moved_i, last_moved_j)

        if matches is None:
            self.possible_matches_count = self.board.count_possible_matches()
            self.active = True
            return

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        for match in matches:
            self.score += len(match) * 50

        self.board.remove_matches(last_moved_i, last_moved_j)

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self.__calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )

    def __remove_affected_tiles(self, tiles: List) -> None:
        for tile in tiles:
            self.board.tiles[tile.i][tile.j] = None
                
        self.score += len(tiles) * 50
                
        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()
                
        falling_tiles = self.board.get_falling_tiles()
                
        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self.__calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )