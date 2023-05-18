

from pygame.draw import line as pygame_draw_line
from pygame.display import get_surface as pygame_display_get_surface

from pygame.font import SysFont as pygame_font_SysFont
from pygame.time import get_ticks as pygame_time_get_ticks
from pygame.key import get_pressed as pygame_key_get_pressed
from pygame import K_SPACE as pygame_K_SPACE

from snake import Snake

class Board:

    def __init__(self, board_dimensions, ):

        self.surface = pygame_display_get_surface()
        self.dimensions = board_dimensions
        self.num_cells = 20
        self.cell_dimensions = (self.dimensions[0] / self.num_cells, self.dimensions[1] / self.num_cells)

        self.text_font = pygame_font_SysFont("Bahnschrift", 75)
        self.reset_timer = 0

        self.snake = Snake(
                            x = ((self.num_cells / 2) - 1) * self.cell_dimensions[0], 
                            y = ((self.num_cells / 2) - 1) * self.cell_dimensions[1]
                        )
        
        # Snake does not move until the player starts moving
        self.game_started = False


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
    
    def draw_text(self, text, text_colour, font, x, y):
        
        # Render the text as an image without anti-aliasing
        text_image = font.render(text, False, text_colour)
        # Blit the image onto the surface
        self.surface.blit(text_image, (x, y))

    def run(self):
        
        self.draw_grid()

        # Snake
        self.snake.draw(
                        surface = self.surface, 
                        width = self.cell_dimensions[0], 
                        height = self.cell_dimensions[1]
                        )
        
        self.snake.change_direction()

        if self.game_started:
            current_time = pygame_time_get_ticks()
            if current_time - self.snake.move_timer > 200:
                self.snake.move(x = self.cell_dimensions[0], y = self.cell_dimensions[1])
                self.snake.move_timer = current_time

        else:
            if pygame_key_get_pressed()[pygame_K_SPACE]:
                self.game_started = True