import pygame as pg
import sys
import random
from pygame.locals import *

pg.init()
# Constant values
# width,height -> x,y
screensize = width, height = 640, 720
screen = pg.display.set_mode(screensize)
time_clock = pg.time.Clock()
# directions
right_direction = 'RIGHT'
left_direction = 'LEFT'
up_direction = 'UP'
down_direction = 'DOWN'
# current_direction = right_direction
# center of the screen
# mid_height = 360
# mid_width = 320
pinkColor = pg.Color(255, 182, 193)
blackColor = pg.Color(0, 0, 0)
whiteColor = pg.Color(255, 255, 255)
snake_body = [[320, 360], [300, 360], [280, 360], [260, 360], [240, 360]]
# keyboard listener（to determine if a direction is a valid move)
listener_direction = right_direction


# flag：to see if seed has been eaten


# screen.fill(blackColor)
# create a list of coordinates that contains snake_body's position
# initialize with 5 block of body
# 3 blocks
class Snake:
    is_seeds_alive = 1

    # to create a snake object with default direction and body segments
    def __init__(self, current_direction=right_direction, current_body=snake_body):
        self.current_direction = current_direction
        self.current_body = current_body
        self.snake_head = snake_body[0]

    # method to draw snake
    # read self.current_body variable(which constantly updated by move_x() function
    def draw_snake(self):
        for body_parts in self.current_body:
            pg.draw.rect(screen, pinkColor, pg.Rect(body_parts[0], body_parts[1], 20, 20))

    # method to seed
    def draw_seed(self):
        pass
    
    # method to move snake
    # moving snake body by taking two arguments
    # direction: decide the snake which direction to move
    # seed_postion: tell the snake where the seed is
    def move(self, direction, seed_postion):
        new_body = []
        # setting snake's moving direction, by adding one-block size 20
        # here is checking if it touches its body if True ->call game_over()
        # if False 
        if direction == right_direction:
            new_head = [self.snake_head[0] + 20, self.snake_head[1]]
            if new_head in self.current_body:
                self.game_over()
            self.current_direction = right_direction
        elif direction == left_direction:
            new_head = [self.snake_head[0] - 20, self.snake_head[1]]
            if new_head in self.current_body:
                self.game_over()
            self.current_direction = left_direction
        elif direction == up_direction:
            new_head = [self.snake_head[0], self.snake_head[1] - 20]
            if new_head in self.current_body:
                self.game_over()
            self.current_direction = up_direction
        elif direction == down_direction:
            new_head = [self.snake_head[0], self.snake_head[1] + 20]
            if new_head in self.current_body:
                self.game_over()
            self.current_direction = down_direction
        new_body.append(new_head)
        # assmeble the rest parts of snake's body
        # checking if the snake got the seed
        # True -> set the flag:is_seeds_alive to False
        # False -> pop the last body_parts of its new_body
        for body_parts in self.current_body:
            new_body.append(body_parts)
        if new_head == seed_postion:
            self.is_seeds_alive = 0
        else:
            new_body.pop()
        # update current_body to new_body
        self.current_body = new_body
        # update snake_head tp new_head
        self.snake_head = new_head
        # log current_body to console
        print(self.current_body)
    
    # method to generate a seed coordinates
    # checking if it is a valid coordinates
    def generate_seed_position(self):
        is_valid = 0
        # screen size is set to 640*720
        # 20*20 is one block
        # we divide the whole screen to 20*20 block
        # on each axis, there is maximun value of blocks
        # x range = 32
        # y range = 36
        while not is_valid:
            seeds = []
            x = random.randint(0, 31)
            y = random.randint(0, 35)
            seeds = [x * 20, y * 20]
            # check if the seed is in snake's body
            if seeds not in self.current_body:
                is_valid = 1
        return seeds

    def game_over(self):
        # plan to add some msg when game is over
        # plan to add a restart feature
        sys.exit()


# game's main logic part
# should be done within class Snake, like making a execute() function to carry out the logic part
def main():
    # create a Snake object
    the_snake = Snake()
    # genearte a seeds coordinates
    seeds_position = the_snake.generate_seed_position()
    # state the listener_direction is the global variable 
    # not the one show up in this context
    # since python checking local variable first
    global listener_direction
    while 1:
        listener_direction = the_snake.current_direction
        # listening events on pygame's event line
        # if its quit then game_over
        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()
                # if the event is KEYDOWN(a key pressed)
            elif event.type == pg.KEYDOWN:
                # check the direction of pressed key
                # set listener_direction to the key-pressed direction
                # Note: the 'and not' parts is to check if the intend moving direction is 
                # opposite of snake's current direction
                if event.key == pg.K_UP and not the_snake.current_direction == down_direction:
                    listener_direction = up_direction
                elif event.key == pg.K_DOWN and not the_snake.current_direction == up_direction:
                    listener_direction = down_direction
                elif event.key == pg.K_RIGHT and not the_snake.current_direction == left_direction:
                    listener_direction = right_direction
                elif event.key == pg.K_LEFT and not the_snake.current_direction == right_direction:
                    listener_direction = left_direction
                else:
                    pass
        # set snake moving direction accodring to listener_direction
        # here is double checking if direction is opposite of snake's current_direction
        if listener_direction == right_direction and not the_snake.current_direction == left_direction:
            the_snake.move(right_direction, seeds_position)
        elif listener_direction == left_direction and not the_snake.current_direction == right_direction:
            the_snake.move(left_direction, seeds_position)
        elif listener_direction == up_direction and not the_snake.current_direction == down_direction:
            the_snake.move(up_direction, seeds_position)
        elif listener_direction == down_direction and not the_snake.current_direction == up_direction:
            the_snake.move(down_direction, seeds_position)
        else:
            the_snake.move(the_snake.current_direction, seeds_position)
        # this part is checking if the snake is out of boundaries
        # checking X axis
        if the_snake.snake_head[0] < 0 or the_snake.snake_head[0] > 620:
            the_snake.game_over()
        # checking Y axis
        if the_snake.snake_head[1] < 0 or the_snake.snake_head[1] > 700:
            the_snake.game_over()
        # fill screen with black color
        screen.fill(blackColor)
        # check the seed's flag
        # Flase -> call generate_seeds_position method
        if not the_snake.is_seeds_alive:
            seeds_position = the_snake.generate_seed_position()
            the_snake.is_seeds_alive = 1
        # Draw the seed on screen
        pg.draw.rect(screen, whiteColor, pg.Rect(seeds_position[0], seeds_position[1], 20, 20))
        # Draw snake
        the_snake.draw_snake()
        # 
        pg.display.flip()
        time_clock.tick(5)


if __name__ == '__main__':
    main()
