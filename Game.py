import pygame as pg
import random
import copy
import maze
import player
import sys 

FPS = 60
SIZE = 20

DEAD = (255, 255, 255)
ALIVE = (0, 0, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

class Game:
    def __init__(self):
        self.maze = maze.Maze()
        self.board = self.maze.get_maze()

        self.finished = False
        self.running = False

        self._cells: list[pg.Rect] = self.create_cells()
        self._delay = 250
        self.player = player.Player(self)
        self.walls = []
        self.ball = player.Ball(self)


        pg.init()
        self._display = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    def loop(self):
        clock = pg.time.Clock()
        while not self.finished:
            self.walls = self.get_walls() # to get changes based on clicked cells
            if self.check_win():
                self.game_over() # spawns end game window

            delta = clock.tick(FPS) / 1000.0 # set fps

            for event in pg.event.get():
                # if the user hits the X
                if event.type == pg.QUIT:
                    self.finished = True

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    coords = pg.mouse.get_pos()

                    row, col = self.cell_clicked(coords) 
                    if row is not None:
                        self.change_color(row, col)

            self.player.update()

            if self.running:
                pg.time.wait(self._delay)
            
            self._display.fill((255, 255, 255))
            self.draw_cells()
            self._display.blit(self.player.image, self.player.rect) # draw player
            self._display.blit(self.ball.image, self.ball.rect) # draw ball
            pg.display.update()
        pg.quit()

    # returns a list of pg.Rects that represent the maze
    def create_cells(self):
        rects = []
        for i in range(SIZE):
            rects.append([])
            for j in range(SIZE):
                rects[i].append(pg.Rect(i * 32, j*32, 30, 30))
        return rects

    # returns the row and column where the click occurred, otherwise returns None
    def cell_clicked(self, coords):
        for row in range(SIZE):
            for col in range(SIZE):
                if self._cells[row][col].collidepoint(coords):
                    return row, col
        return None, None

    # change cell to opposite color when clicked
    def change_color(self, row, col):
        cell = self.board[row][col]
        if cell == DEAD:
            self.board[row][col] = ALIVE
        else:
            self.board[row][col] = DEAD

    # draw the actual rectangles on the screen
    def draw_cells(self):
        for i in range(20):
            for j in range(20):
               pg.draw.rect(self._display, self.board[i][j], self._cells[i][j])

    # returns a list of the 'wall' rects
    def get_walls(self) -> list[pg.Rect]:
        walls = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == ALIVE:
                    walls.append(self._cells[i][j])
        return walls

    # returns true if the player collides with the ball, triggers game over in loop()
    def check_win(self):
        return self.ball.rect.colliderect(self.player.rect)

    '''
    creates a new window that allows the user to either exit (closes all window),
    or start a new game with a new maze
    '''
    def game_over(self):
        pg.init()
        game_over_display = pg.display.set_mode((300, 100))
        pg.display.set_caption("Game Over")
        font = pg.font.Font(None, 36)
        text = font.render("You won!", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = game_over_display.get_rect().centerx
        text_rect.centery = game_over_display.get_rect().centery - 30
        game_over_display.blit(text, text_rect)

        font = pg.font.Font(None, 20)
        exit_text = font.render("Exit", True, (0, 0, 0))
        new_game_text = font.render("New Game", True, (0, 0, 0))

        exit_button = pg.Rect(50, 50, 75, 30)
        new_game_button = pg.Rect(150, 50, 75, 30)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        pg.quit()
                        sys.exit()
                    elif new_game_button.collidepoint(event.pos):
                        pg.quit()
                        game = Game()
                        game.loop()
                        sys.exit()

            pg.draw.rect(game_over_display, (255, 255, 255), exit_button)
            pg.draw.rect(game_over_display, (255, 255, 255), new_game_button)
            exit_text_rect = exit_text.get_rect()
            exit_text_rect.center = (exit_button.x + exit_button.width // 2, exit_button.y + exit_button.height // 2)
            game_over_display.blit(exit_text, exit_text_rect)
            
            new_game_text_rect = new_game_text.get_rect()
            new_game_text_rect.center = (new_game_button.x + new_game_button.width // 2, new_game_button.y + new_game_button.height // 2)
            game_over_display.blit(new_game_text, new_game_text_rect)
            pg.display.update()
