from enum import Enum

import pygame
import random


class ObstacleType(Enum):
    """
    Enum defining different types of obstacles.
    Each obstacle type is associated with an image file, initial x and y coordinates.
    """
    Dino = ("image/dino.png", 300, 300)
    Ghost = ("image/ghost.png", 870, 330)
    Mouth = ("image/mund.png", 550, 320)


class Obstacle(pygame.sprite.Sprite):
    """
    Initializes an obstacle instance.
    :param parent: The parent RunningGame instance.
    :param ob_type: The type of the obstacle (from ObstacleType).
    :param all_sprites: The sprite group containing all sprites.
    """
    def __init__(self, parent, ob_type: ObstacleType, all_sprites):
        super().__init__(all_sprites)
        self.parent = parent
        self.type = ob_type
        self.image_org = pygame.image.load(ob_type.value[0])
        self.image = self.image_org
        x = ob_type.value[1]
        y = ob_type.value[2]
        self.rect = self.image.get_rect(x=x, y=y)
        self.dir_y = 1
        self.dir_x = 1
        self.opacities = [255, 50, 200, 1, 10, 0, 100]
        self.size = 60
        self.size_change = 1

    def update(self):
        """
        Updates the obstacle's position and behavior based on its type.
        Handles movement, size changes, and transparency for different obstacle types.
        """
        if self.type is ObstacleType.Dino:
            if self.rect.y > self.parent.screen_h - 250 or self.rect.y < 120:
                self.dir_y *= -1
            self.rect.y += self.dir_y
        if self.type is ObstacleType.Ghost:
            if random.randint(1, 100) < 15:
                self.image.set_alpha(self.opacities[random.randint(0, len(self.opacities)-1)])
        if self.type is ObstacleType.Mouth:
            if self.size <= 20 or self.size >= 100:
                self.size_change *= -1
            self.size += self.size_change
            y_tmp = self.image.get_size()[1] + self.size_change
            y_scale = y_tmp if y_tmp >= 0 else 0
            self.image = pygame.transform.scale(self.image_org, (self.size, y_scale))
            self.rect.y += -self.size_change

            self.rect = self.image.get_rect(x=self.rect.x, y=self.rect.y)

        self.rect.x -= self.parent.obstacles_speed
        if self.rect.x < -20:
            self.rect.x = random.randint(self.parent.screen_w - 100, self.parent.screen_w + 200)
            self.parent.score += 1
            if self.parent.score % 3 == 0:
                self.parent.obstacles_speed += 1

        if self.parent.player_rect.colliderect(self.rect):
            self.parent.active = False
            self.parent.x_change = 0
            self.parent.y_change = 0

    def move(self):
        """
        Moves the obstacle.
        Calls the update method if the game is active.
        """
        if self.parent.active:
            self.update()
