from window_config import *
import pygame

class Player():
    def __init__(self, x, y, vel, width, height, colour):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x, y, width, height)

    def set_name(self, name):
        self.name = name

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x - self.vel < 0:
                self.x = screen_width
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            if self.x + self.vel > screen_width:
                self.x = 0
            self.x += self.vel

        if keys[pygame.K_UP]:
            if self.y - self.vel < 0:
                self.y = screen_height
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            if self.y + self.vel > screen_height:
                self.y = 0
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)