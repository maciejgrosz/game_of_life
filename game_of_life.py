import sys
import pygame
import numpy as np
import config as cg


class Game_of_life:
    def __init__(self) -> None:
        """
        Initialize the grid and screen, set game state
        :param max_fps: Framerate cap to limit game speed
        """
        pygame.init()
        self.screen = pygame.display.set_mode(cg.BOARD_SIZE)
        self.clear_screen()
        self.init_grids()
        self.max_fps = cg.MAX_FPS
        self.paused = False
        self.end = False

    def init_grids(self):
        """
        Initialize active and new grid in dict structure, then randomly fulfilling active grid
        """
        self.grids = {
            "active": np.zeros((cg.NUM_COLS, cg.NUM_ROWS), dtype=int),
            "new": np.zeros((cg.NUM_COLS, cg.NUM_ROWS), dtype=int),
        }
        self.set_grid(True, "active")

    def swap_grids(self):
        """
        Swaps between new and active greed
        """
        self.grids = {"active": self.grids["new"], "new": self.grids["active"]}

    def set_grid(self, r, grid):
        """
        Fill grid with values
        :param r: define if cells are random (probability defined in config.py) or only zeros
        :param grid: The grid that is being filled
        """
        if r:
            for c in range(cg.NUM_COLS):
                for r in range(cg.NUM_ROWS):
                    self.grids[grid][c][r] = np.random.choice(
                        [0, 1], p=[cg.PROB_0, cg.PROB_1]
                    )

        else:
            self.grids[grid] = np.zeros((cg.NUM_COLS, cg.NUM_ROWS), dtype=int)

    def clear_screen(self):
        """
        Fill whole screen with dead color
        """
        self.screen.fill(cg.DEAD_COLOR)

    def get_state_of_cell(self, row_num, col_num):
        """
        Return state dead or alive (0,1) of cell in active grid
        :param row_num: row number of specific cell
        :param col_num: column number of specific cell
        :return: 0 or 1 depending on state of cell. Defaults to 0 (dead)
        """
        try:
            cell_value = self.grids["active"][row_num][col_num]
        except:
            cell_value = 0
        return cell_value

    def check_neighbours(self, row_index, col_index):
        """
        Get the number of alive cell in neighborhood.
        Then based on game logic, determine if it lives, dies, born or survives

        :param row_index: Row number of cell to check
        :param col_index: Column number of cell to check
        :return: The state of cell in next gen (0 - dead, 1 - live)
        """
        alive_num = 0
        for r in range(row_index - 1, row_index + 2):
            for c in range(col_index - 1, col_index + 2):
                if [r, c] != [row_index, col_index]:
                    alive_num += self.get_state_of_cell(r, c)

        if self.grids["active"][row_index][col_index] == 1:  # if its alive
            if alive_num > 3:  # overpopulation
                return 0
            if alive_num < 2:  # underpopulation
                return 0
            if alive_num == 2 or alive_num == 3:
                return 1
        elif self.grids["active"][row_index][col_index] == 0:
            if alive_num == 3:
                return 1

        return self.grids["active"][row_index][col_index]

    def game_update(self):
        """
        Updating active grid, based on game logic.
        """
        self.set_grid(False, "new")
        for r in range(cg.NUM_ROWS - 1):
            for c in range(cg.NUM_COLS - 1):
                next_state = self.check_neighbours(r, c)
                self.grids["new"][r][c] = next_state
        self.swap_grids()

    def draw_grid(self):
        """
        Drawing rectangles on screen based on active grid
        """
        self.clear_screen()
        alive_coords = np.argwhere(self.grids["active"] == 1)
        for coord in alive_coords:
            pygame.draw.rect(
                self.screen,
                cg.ALIVE_COLOR,
                (
                    coord[0] * cg.CELL_SIZE[0] + (cg.CELL_SIZE[0] / 2),
                    coord[1] * cg.CELL_SIZE[1] + (cg.CELL_SIZE[1] / 2),
                    *cg.CELL_SIZE,
                ),
            )
        pygame.display.flip()

    def event_handler(self):
        """
        Handle keypressing
        p - start/stop (pause) the game
        q - quit
        r - reset grid
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                if event.key == pygame.K_q:
                    self.end = True
                if event.key == pygame.K_r:
                    self.set_grid(True, "active")
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self) -> None:
        """
        Start the game
        """
        clock = pygame.time.Clock()
        while True:
            if self.end:
                return

            self.event_handler()

            if not self.paused:
                self.game_update()
                self.draw_grid()

            clock.tick(self.max_fps)


if __name__ == "__main__":
    game = Game_of_life()
    game.run()
