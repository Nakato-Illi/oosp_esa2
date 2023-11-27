import pygame

from Obstacle import ObstacleType, Obstacle


class RunningGame:
    """
    Initializes the RunningGame instance.
    Sets up the game window, clock, fonts, colors, and game elements.
    """
    def __init__(self):
        pygame.init()
        self.screen_w = 1200
        self.screen_h = 550
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption('Running game')

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.background = self.white
        self.gravity = 0.7
        self.ground = 298
        self.active = False

        self.score = 0
        self.obstacles_speed = 1

        self.player_x = 50
        self.player_y = 600
        self.y_change = 0
        self.x_change = 0
        self.left_move = False
        self.right_move = False

        self.bg = pygame.image.load("image/bg1.jpg")
        self.bg = pygame.transform.scale(self.bg, (self.screen_w, self.screen_h))
        self.play_fig = pygame.image.load("image/player1.png")
        self.obstacles = []
        self.obstacle_sprites = pygame.sprite.Group()
        self.get_obstacles()

    def start_game(self):
        """
        Runs the main game loop.
        Handles events, updates game elements, and renders the game window.
        """
        running = True
        while running:
            self.clock.tick(self.fps)
            self.screen.fill(self.background)
            self.screen.blit(self.bg, (0, 0))

            if not self.active:
                self.show_instructions()

            self.show_score()

            pygame.draw.rect(self.screen, self.black, [0, 370, self.screen_w, 5])

            self.show_player()
            self.show_obstacles()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event)

            self.move_obstacles()
            self.handle_jump()

            pygame.display.flip()

        pygame.quit()

    def show_instructions(self):
        """
        Displays game instructions on the screen.
        """
        instruction_text = self.font.render('Press Space Bar to Play + Restart Game!', True, self.black, self.white)
        self.screen.blit(instruction_text, [40, 50])
        instruction_text2 = self.font.render('move with <- / ->', True, self.black, self.white)
        self.screen.blit(instruction_text2, [40, 100])

    def show_score(self):
        """
        Displays the current score and obstacles speed on the screen.
        """
        score_text = self.font.render(f'Score: {self.score}, Speed: {self.obstacles_speed}', True, self.white,
                                      self.black)
        self.screen.blit(score_text, [850, 50])

    def show_player(self):
        """
        Displays the player character on the screen.
        """
        self.screen.blit(self.play_fig, [self.player_x, self.player_y, 20, 20])

    def show_obstacles(self):
        """
        Displays the obstacles on the screen.
        """
        for ob in self.obstacles:
            self.screen.blit(ob.image, ob.rect)

    def move_obstacles(self):
        """
        Moves the obstacles on the screen.
        """
        for o in self.obstacles:
            o.move()

    def handle_jump(self):
        """
        Handles the jumping (left, right and gravity) action of the player.
        Makes sure player stays inside frame
        """
        if 0 <= self.player_x <= self.screen_w:
            self.player_x += self.x_change
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > self.screen_w:
            self.player_x = self.screen_w

        if self.y_change > 0 or self.player_y < self.ground:
            self.player_y -= self.y_change
            self.y_change -= self.gravity
        if self.player_y > self.ground:
            self.player_y = self.ground
        if self.player_y == self.ground and self.y_change < 0:
            self.y_change = 0

    def get_obstacles(self):
        """
        Creates a new set of obstacles for the game.
        """
        self.obstacles = []
        for t in ObstacleType:
            # Pass the sprite group to the Obstacle constructor
            self.obstacles.append(Obstacle(self, t, self.obstacle_sprites))

    def handle_keydown(self, event):
        """
        Handles keydown events for controlling the player character.
        :param event: The pygame event for a keydown action.
        """
        if not self.active and event.key == pygame.K_SPACE:
            self.get_obstacles()
            self.player_x = 50
            self.score = 0
            self.obstacles_speed = 1
            self.active = True
            self.right_move = False
            self.left_move = False

        if self.active:
            if event.key == pygame.K_SPACE and self.y_change == 0:
                self.y_change = 18
            if event.key == pygame.K_RIGHT:
                self.right_move = True
                self.x_change = 4
            if event.key == pygame.K_LEFT:
                self.left_move = True
                self.x_change = -2
        else:
            self.x_change = 0
            self.y_change = 0

    def handle_keyup(self, event):
        """
        Handles keyup events for controlling the player character.
        :param event: The pygame event for a keyup action.
        """
        if self.active:
            if event.key == pygame.K_RIGHT:
                self.right_move = False
            if event.key == pygame.K_LEFT:
                self.left_move = False
            if not (self.left_move or self.right_move):
                self.x_change = 0
        else:
            self.x_change = 0

    @property
    def player_rect(self):
        """
        Gets the rectangular region occupied by the player character.
        :return: Rect object representing the player's position.
        """
        return self.play_fig.get_rect(x=self.player_x, y=self.player_y)
