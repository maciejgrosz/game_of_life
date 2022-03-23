import sys
import pygame
import numpy as np
import config as cg
import random


class Game_of_life:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(cg.BOARD_SIZE)
        self.clear_screen()
        self.init_grids()

    def init_grids(self):
        self.grids = {
            'active': np.zeros((cg.NUM_COLS, cg.NUM_ROWS), dtype=int),
            'new': np.zeros((cg.NUM_COLS, cg.NUM_ROWS), dtype=int)
        }
        self.set_active_grid(True)

    def swap_grids(self):
        self.grids = {'active': self.grids['new'], 'new': self.grids['active']}

    # set active grid to random filled matrix with 0 or 1 with arg. random = True
    # With random = False active grid is filled by zeros
    def set_active_grid(self, r):
        if r:
            for c in range(cg.NUM_COLS):
                for r in range(cg.NUM_ROWS):
                    self.grids['active'][c][r] = np.random.choice([0, 1], p=[0.8, 0.2])

            # Cleaner option but i need to set weightes for spawning alive cells
            # self.grids['active'] = np.random.randint(
            #     2, size=(cg.NUM_COLS, cg.NUM_ROWS))
        else:
            self.grids['active'] = np.zeros(
                (cg.NUM_COLS, cg.NUM_ROWS), dtype=int)

    def clear_screen(self):
        self.screen.fill(cg.DEAD_COLOR)

    def game_update(self):
        # Checks the status of grid
        # updating grid with new_grid and swap it.
        pass

    def draw_grid(self):
        self.clear_screen()
        alive_coords = np.argwhere(self.grids['active'] == 1)
        for coord in alive_coords:
            pygame.draw.rect(self.screen, cg.ALIVE_COLOR, (coord[0] * cg.CELL_SIZE[0] + (
                cg.CELL_SIZE[0]/2), coord[1] * cg.CELL_SIZE[1] + (cg.CELL_SIZE[1]/2), *cg.CELL_SIZE))
        pygame.display.flip()

    def event_handler(self):
        for event in pygame.event.get():
            # if event == keypress 'space' -> pause the game
            # if event == keypress 'r' -> reset the game/grid
            # if event == keypress 'q' -> quit the game
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self) -> None:
        while True:
            self.set_active_grid(True)
            self.event_handler()
            self.game_update()
            self.draw_grid()
