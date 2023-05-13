from pygame.draw import rect as pygame_draw_rect
from pygame.key import get_pressed as pygame_key_get_pressed
from pygame import K_a as pygame_K_a
from pygame import K_d as pygame_K_d
from pygame import K_w as pygame_K_w
from pygame import K_s as pygame_K_s

class Snake:
    
    def __init__(self, x, y):

        self.parts = [[x, y], [x + (900 / 20), y], [x + ((900 / 20) * 2), y], [x + ((900 / 20) * 3), y]]

        self.current_direction = "L"

        self.move_timer = 0

    def draw(self, surface, width, height):

        for i in range(len(self.parts)):

            colour = "RED" if i == 0 else "BLUE"
            pygame_draw_rect(
                            surface = surface,
                            color = colour, 
                            rect = (self.parts[i][0], self.parts[i][1], width, height),
                            width = 0
                            )
        
    def move(self, x, y):
        
        # Alter every cell to be the one before it (except the first)
        for i in range(len(self.parts) - 1, 0, -1):
            self.parts[i][0] = self.parts[i - 1][0]
            self.parts[i][1] = self.parts[i - 1][1]

        # Move the first cell in the current direction set
        match self.current_direction:

            case "L":
                self.parts[0][0] -= x
                
            case "R":
                self.parts[0][0] += x

            case "D":
                self.parts[0][1] += y

            case "U":
                self.parts[0][1] -= y
    
    def change_direction(self):

        
        # Note: Extra conditions is so that the snake cannot go into itself (cannot go in the opposite of their current direction)

        if pygame_key_get_pressed()[pygame_K_a] == True and self.current_direction != "R":
            self.current_direction = "L"

        elif pygame_key_get_pressed()[pygame_K_d] == True and self.current_direction != "L":
            self.current_direction = "R"

        elif pygame_key_get_pressed()[pygame_K_w] == True and self.current_direction != "D":
            self.current_direction = "U"

        elif pygame_key_get_pressed()[pygame_K_s] == True and self.current_direction != "U":
            self.current_direction = "D"