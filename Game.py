import pygame as pg
import random
import copy

FPS = 60
SIZE = 20

DEAD = (255, 255, 255)
ALIVE = (0, 0, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

class Player(pg.sprite.Sprite):
    def __init__(self, game, velocity=8):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([30, 30])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.game = game
        self.velocity = velocity

    def update(self):
        keys = pg.key.get_pressed()
        new_x, new_y = self.x, self.y

        if keys[pg.K_w]: new_y -= self.velocity

        if keys[pg.K_a]: new_x -= self.velocity

        if keys[pg.K_s]: new_y += self.velocity

        if keys[pg.K_d]: new_x += self.velocity

        if self.collides_with_black(new_x, new_y):
            return

        if new_x < 0:
            new_x = 0
        if new_y < 0:
            new_y = 0
        if new_x + self.rect.width > SCREEN_WIDTH:
            new_x = SCREEN_WIDTH - self.rect.width
        if new_y + self.rect.height > SCREEN_HEIGHT:
            new_y = SCREEN_HEIGHT - self.rect.height

        self.x, self.y = new_x, new_y
        self.rect.x = self.x
        self.rect.y = self.y

    def collides_with_black(self, x, y):
        new_position = pg.Rect(x, y, 30, 30)
        for cell_rect in self.game.walls:
            if new_position.colliderect(cell_rect):
                print("collision detected")
                return True
        return False
class Game:
    def __init__(self):
        self.board = []

        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                row.append(DEAD)
            self.board.append(row)

        self.prev = copy.deepcopy(self.board)

        self.finished = False
        self.running = False

        self._cells: list[pg.Rect] = self.create_cells()
        self._delay = 250
        self.player = Player(self)
        self.walls = []

        pg.init()
        self._display = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    def loop(self):
        clock = pg.time.Clock()
        self.create_maze()
        self.walls = self.get_walls()
        while not self.finished:
            delta = clock.tick(FPS) / 1000.0 # set fps
            self.walls = self.get_walls()

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
            pg.display.update()
        pg.quit()

    def create_cells(self):
        rects = []
        for i in range(SIZE):
            rects.append([])
            for j in range(SIZE):
                rects[i].append(pg.Rect(i * 32, j*32, 30, 30))
        return rects

    def cell_clicked(self, coords):
        print("Cell at " + str(coords) + " clicked")
        for row in range(SIZE):
            for col in range(SIZE):
                if self._cells[row][col].collidepoint(coords):
                    print("Click mapped to (" + str(row) + ", " + str(col) + ")")
                    return row, col
        return None, None

    # change cell to opposite color when clicked
    def change_color(self, row, col):
        cell = self.board[row][col]
        if cell == DEAD:
            self.board[row][col] = ALIVE
        else:
            self.board[row][col] = DEAD

    def draw_cells(self):
        for i in range(20):
            for j in range(20):
                pg.draw.rect(self._display, self.board[i][j], self._cells[i][j])


    def draw_player(self):
        pg.draw.rect(self._display, )
    
    def start_random(self):
        for i in range(20):
            for j in range(20):
                num = random.randint(0, 1)
                if num == 0:
                    self.board[i][j] = DEAD
                else:
                    self.board[i][j] = ALIVE

    def update(self):
        self.prev = copy.deepcopy(self.board)
        for i in range(SIZE):
            for j in range(SIZE):
                count = self.get_neighbors(i, j)
                cell = self.board[i][j]
                if cell == DEAD and count == 3:
                    self.board[i][j] = ALIVE
                elif (count < 2 or count > 4) and cell == ALIVE:
                    self.board[i][j] = DEAD

    def get_neighbors(self, row, col) -> int:

        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i + row < SIZE and j + col < SIZE and row - i > 0 and col - j > 0:
                    if i == 0 and j == 0:
                        continue
                    neighbor = self.prev[i + row][j + col]
                    if neighbor != DEAD:
                        count += 1
        return count

    def create_maze(self):
        self.start_random()
        for _ in range(100):
            self.update()

    def cell_at_pos(self, x, y):
        col = x // 32
        row = y // 32
        return row, col

    def get_walls(self) -> list[pg.Rect]:
        walls = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == ALIVE:
                    walls.append(self._cells[i][j])
        return walls