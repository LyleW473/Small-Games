from pygame.draw import line as pygame_draw_line
from pygame.draw import rect as pygame_draw_rect
from pygame.display import get_surface as pygame_display_get_surface

from pygame.font import SysFont as pygame_font_SysFont
from pygame.time import get_ticks as pygame_time_get_ticks
from pygame.key import get_pressed as pygame_key_get_pressed
from pygame import K_SPACE as pygame_K_SPACE

from snake import Snake
from random import randrange as random_randrange

class Board:

    def __init__(self, board_dimensions, ):

        self.surface = pygame_display_get_surface()
        self.dimensions = board_dimensions
        self.num_cells = 20
        self.cell_dimensions = (self.dimensions[0] / self.num_cells, self.dimensions[1] / self.num_cells)

        self.text_font = pygame_font_SysFont("Bahnschrift", 50)
        self.start_text_size = self.text_font.size("Press Spacebar to start!")

        self.reset_timer = 0

        self.snake = Snake(
                            x = ((self.num_cells / 2) - 1) * self.cell_dimensions[0], 
                            y = ((self.num_cells / 2) - 1) * self.cell_dimensions[1]
                        )
        
        # Boolean that determines whether the snake will extend on the next self.move() call
        self.extend_snake = None
        
        # Generate food
        self.food = self.generate_food()
        
        # Snake does not move until the player starts moving
        self.game_started = False

    def draw_text(self, text, text_colour, font, x, y):
        
        # Render the text as an image without anti-aliasing
        text_image = font.render(text, False, text_colour)
        # Blit the image onto the surface
        self.surface.blit(text_image, (x, y))

    def draw_grid(self):
        
        # Vertical
        for i in range(1, self.num_cells):
            pygame_draw_line(
                            surface = self.surface,
                            color = "BLACK",
                            start_pos = (i * self.cell_dimensions[0], 0),
                            end_pos = (i * self.cell_dimensions[0], self.dimensions[1]),
                            width = 1
                            )
        # Horizontal
        for i in range(1, self.num_cells):
            pygame_draw_line(
                            surface = self.surface,
                            color = "BLACK",
                            start_pos = (0, i * self.cell_dimensions[1]),
                            end_pos = (self.dimensions[0], i * self.cell_dimensions[1]),
                            width = 1
                            )
    
    def reset_game(self):

        self.game_started = False
        self.snake = Snake(
                        x = ((self.num_cells / 2) - 1) * self.cell_dimensions[0], 
                        y = ((self.num_cells / 2) - 1) * self.cell_dimensions[1]
                    )
    
    def generate_food(self):
        x_cell_index = random_randrange(0, self.num_cells)
        y_cell_index = random_randrange(0, self.num_cells)
        
        return (x_cell_index * self.cell_dimensions[0], y_cell_index * self.cell_dimensions[1])

    def run(self):
        
        # Grid
        self.draw_grid()
        
        if self.game_started:

            # Draw the food
            pygame_draw_rect(
                            surface = self.surface, 
                            color = "GREEN",
                            rect = (self.food[0], 
                                    self.food[1], 
                                    self.cell_dimensions[0], 
                                    self.cell_dimensions[1]
                                    ),
                            width = 0
                            )
            
            # Check if the snake collided with food
            if self.snake.check_food_collision(food_coord = self.food) == True:
                self.food = self.generate_food()
                self.extend_snake = True # Extend the snake the next time the snake moves


            # Check if the player wants to change the direction the snake is moving in
            self.snake.change_direction()

            # Check if the snake has collided with the borders of the screen or with itself
            if self.snake.check_collision(screen_width = self.dimensions[0], screen_height = self.dimensions[1]) == True:
                self.reset_game()

            # Check if the player wants to move the snake
            current_time = pygame_time_get_ticks()
            if current_time - self.snake.move_timer > 150:
                
                # Extend the snake
                if self.extend_snake == True:
                    self.snake.extend(cell_size = self.cell_dimensions)
                    self.extend_snake = False

                # Just move the snake
                else:
                    self.snake.move(x = self.cell_dimensions[0], y = self.cell_dimensions[1])

                # Reset next iteration timer
                self.snake.move_timer = current_time
        
        else:
            # Draw the start text
            self.draw_text(
                            text = "Press Spacebar to start!",
                            text_colour = "BLACK",
                            font = self.text_font,
                            x = (self.dimensions[0] // 2) - (self.start_text_size[0] // 2),
                            y = (self.dimensions[1] // 2) - (self.start_text_size[1] // 2)
                            )
            
            # Check if the player started the game
            if pygame_key_get_pressed()[pygame_K_SPACE]:
                self.game_started = True

        # Snake
        self.snake.draw(
                        surface = self.surface, 
                        width = self.cell_dimensions[0], 
                        height = self.cell_dimensions[1]
                        )