import pygame as pg


SCREEN_HEIGHT = 640
SCREEN_WIDTH = 640

class Ball(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('pokeball.png')
        self.image = pg.transform.scale(self.image, (30, 30))
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width
        self.rect.y = SCREEN_HEIGHT - self.rect.height
class Player(pg.sprite.Sprite):
    def __init__(self, game, velocity=4):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('eevee2.png')
        self.image = pg.transform.scale(self.image, (30, 30))
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
            return # do nothing

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
                return True
        return False