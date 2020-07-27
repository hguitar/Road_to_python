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
# keyboard listener（to store a direction)
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

    # function to draw snake
    # read self.current_body variable(which constantly updated by move_x() function
    def draw_snake(self):
        for body_parts in self.current_body:
            pg.draw.rect(screen, pinkColor, pg.Rect(body_parts[0], body_parts[1], 20, 20))

    # function to seed
    def draw_seed(self):
        pass

    # moving snake body using separated function
    # needs to pass current
    # using if to judge if its trying to move opposite direction
    def move(self, direction, seed_postion):
        new_body = []
        # 设置蛇头的错误代码：new_head = [self.snake_head[0] + 20, self.snake_head[1]
        # 设置蛇头行进方向，并按照新方向更新本地方向变量
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
        # 计划加入判定，如果此位置有食物，则不pop
        for body_parts in self.current_body:
            new_body.append(body_parts)
        if new_head == seed_postion:
            self.is_seeds_alive = 0
        else:
            new_body.pop()
        # 更新现在蛇头的方向
        # 更新snake类的current_body值
        self.current_body = new_body
        # 更新蛇头位置
        self.snake_head = new_head
        print(self.current_body)

    def generate_seed_position(self):
        is_valid = 0
        # 整个屏幕大小为640*720
        # 且以20*20像素为一格
        # x range = 32
        # y range = 36
        while not is_valid:
            seeds = []
            x = random.randint(0, 31)
            y = random.randint(0, 35)
            seeds = [x * 20, y * 20]
            if seeds not in self.current_body:
                is_valid = 1
        return seeds

    def game_over(self):
        # 加入文字提示，snake挂了
        # 然后计划实现类似暂停的hold和resume的功能
        sys.exit()


# 游戏主要逻辑
def main():
    # 创建Snake
    the_snake = Snake()
    # 生成一个初始种子
    seeds_position = the_snake.generate_seed_position()
    global listener_direction
    while 1:
        listener_direction = the_snake.current_direction
        # 窗口无响应是因为没有任何注册在窗口上的事件
        # 为当前窗口增加事件
        # 利用pygame注册事件，其返回值是一个列表，
        # 存放当前注册时获取的所有事件
        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()
                # 如果事件为按键
            elif event.type == pg.KEYDOWN:
                # 判断按键方向，并且不是现在的反方向，则方向改变
                # 在没有加入and not前，按键之后，画面卡顿，因为即使按了反方向
                # listener的方向还是被改变了
                if event.key == pg.K_UP:  # and not listener_direction == down_direction:
                    listener_direction = up_direction
                elif event.key == pg.K_DOWN:  # and not listener_direction == up_direction:
                    listener_direction = down_direction
                elif event.key == pg.K_RIGHT:  # and not listener_direction == left_direction:
                    listener_direction = right_direction
                elif event.key == pg.K_LEFT:  # and not listener_direction == right_direction:
                    listener_direction = left_direction
                else:
                    pass
        # BUG：假设方向向右，快速按右下左，蛇身会立即转向左
        # 第一次尝试修改方式，将and not从判断按键部分挪动到move部分来判断是否移动了反方向
        # 第一次修改方：问题解决，但是操作手感变迟钝。(手感迟钝在snake_game整个demo中也存在）
        # 根据判断的方向，决定移动方向
        # else中，如果没有新的方向，则按照原来默认方向前进
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
        # 边界在实际像素基础上减去了20
        # 判断是否超出边界:X轴
        if the_snake.snake_head[0] < 0 or the_snake.snake_head[0] > 620:
            the_snake.game_over()
        # 判断是否超出边界:Y轴
        if the_snake.snake_head[1] < 0 or the_snake.snake_head[1] > 700:
            the_snake.game_over()
        # 判断是否碰到身体，放在move中去处理了
        # 顺序很重要，先绘制黑色画布，再绘制方块，再更新画面(已包装到draw() function中）
        # 得到蛇向右移动一次的身体段坐标
        # 待替换为监听键盘方向决定移动方向
        # the_snake.move_down()
        # 使用新身体坐标段，绘制身体
        # 绘制
        screen.fill(blackColor)
        # 检查种子是否被吃
        if not the_snake.is_seeds_alive:
            seeds_position = the_snake.generate_seed_position()
            the_snake.is_seeds_alive = 1
        # 画seeds
        pg.draw.rect(screen, whiteColor, pg.Rect(seeds_position[0], seeds_position[1], 20, 20))
        the_snake.draw_snake()
        pg.display.flip()
        time_clock.tick(5)


if __name__ == '__main__':
    main()
