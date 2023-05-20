from pygame.draw import rect as pygame_draw_rect
from pygame.key import get_pressed as pygame_key_get_pressed
from pygame import K_a as pygame_K_a
from pygame import K_d as pygame_K_d
from pygame import K_w as pygame_K_w
from pygame import K_s as pygame_K_s

from random import choice as random_choice

class Snake:
    
    def __init__(self, x, y):

        self.current_direction =  random_choice(("L", "R", "U", "D"))

        self.parts = [[x, y]]
        
        self.occupied_cells = set((x, y))

        self.move_timer = 0

        self.keys_released = True # Ensures that the player cannot hold onto a key

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

        # Used so that food can be generated in cells that the snake is not "occupying"
        self.occupied_cells = set((coord[0], coord[1]) for coord in self.parts)
    
    def change_direction(self):
        
        # Note: Extra conditions is so that the snake cannot go into itself (cannot go in the opposite of their current direction)

        a_pressed = pygame_key_get_pressed()[pygame_K_a]
        d_pressed = pygame_key_get_pressed()[pygame_K_d]
        w_pressed = pygame_key_get_pressed()[pygame_K_w]
        s_pressed = pygame_key_get_pressed()[pygame_K_s]

        if a_pressed == True and self.current_direction != "R" and self.keys_released:
                self.current_direction = "L"
                self.keys_released = False

        elif d_pressed == True and self.current_direction != "L" and self.keys_released:
                self.current_direction = "R"
                self.keys_released = False

        elif w_pressed == True and self.current_direction != "D" and self.keys_released:
                self.current_direction = "U"
                self.keys_released = False

        elif s_pressed == True and self.current_direction != "U" and self.keys_released:
                self.current_direction = "D"
                self.keys_released = False

        elif a_pressed == False and d_pressed == False and w_pressed == False and s_pressed == False:
            self.keys_released = True

    def check_collision(self, screen_width, screen_height):
        
        # Left, screen_width, Top, screen_height
        if self.parts[0][0] < 0 or self.parts[0][0] >= screen_width or self.parts[0][1] < 0 or self.parts[0][1] >= screen_height:
            return True
        
        # Collision with other parts
        for i in range(1, len(self.parts)):
            if self.parts[0] == self.parts[i]:
                return True

        return False
    
    def check_food_collision(self, food_coord):
        return True if self.parts[0][0] == food_coord[0] and self.parts[0][1] == food_coord[1] else False
    
    def extend(self, cell_size):
        
        last_segment = self.parts[-1][:]
        self.move(x = cell_size[0], y = cell_size[1])
        self.parts.append(last_segment)