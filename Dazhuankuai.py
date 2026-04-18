import pygame
import sys
import random
import os
import color_me as color

# 初始化游戏参数
pygame.init()
width,height=800,600
clock=pygame.time.Clock()
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Brick Breaker 打砖块")
# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
paddle_w=100
paddle_h=13
paddle_s=8
ball_r=12
ball_sx=4
ball_sy=-4
ball_dx = ball_sx
ball_dy = ball_sy
score=0
brick_rows=5
brick_cols=10
brick_gap=5
brick_w=(width-(brick_cols+1)*brick_gap)//brick_cols
brick_h=20
bricks=[]
brick_colors=[]
brick_palette=[color.red, color.orange, color.yellow, color.green, color.cyan, color.blue, color.pink]
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x=brick_gap+(brick_w+brick_gap)*col
        brick_y=brick_gap+(brick_h+brick_gap)*row
        bricks.append(pygame.Rect(brick_x,brick_y,brick_w,brick_h))
        brick_colors.append(random.choice(brick_palette))
font=pygame.font.Font(None,36)
start_time = pygame.time.get_ticks()
paddle=pygame.Rect(width//2-paddle_w//2,height-35,paddle_w,paddle_h)
ball=pygame.Rect(width//2-ball_r,height//2-ball_r,ball_r*2,ball_r*2)
# 加载底板图片
paddle_image = pygame.image.load(os.path.join(script_dir, '底板.png'))
paddle_image = pygame.transform.scale(paddle_image, (paddle_w, paddle_h))

# 绘制游戏元素的函数
def draw():
    screen.fill(color.black)
    screen.blit(paddle_image, paddle)
    pygame.draw.ellipse(screen,color.white,ball)
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    time_text = font.render(f"Time: {current_time:.2f}", True, color.white)
    score_text = font.render(f"Score: {score}", True, color.white)
    screen.blit(score_text, (660, 570))
    screen.blit(time_text, (10, 570))
    for index, brick in enumerate(bricks):
        pygame.draw.rect(screen, brick_colors[index], brick)
    pygame.display.update()

# 移动桨的函数
def move_paddle(keys):
    if keys[pygame.K_LEFT] and paddle.left>0:
        paddle.x-=paddle_s
    if keys[pygame.K_RIGHT] and paddle.right<width:
        paddle.x+=paddle_s

# 移动球并处理碰撞的函数
def move_ball():
    global ball_dx,ball_dy
    ball.x+=ball_dx
    ball.y+=ball_dy
    if ball.left<=0 or ball.right>=width:
        ball_dx=-ball_dx
    if ball.top<=0:
        ball_dy=-ball_dy
    if ball.colliderect(paddle) and ball_dy > 0:
        ball_dy = -ball_dy
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_brick = bricks.pop(hit_index)
        brick_colors.pop(hit_index)
        ball_dy = -ball_dy
        global score
        score += 10

# 主游戏循环
running=True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(80)
    keys=pygame.key.get_pressed()
    move_paddle(keys)
    move_ball()
    # 检查失败条件
    if ball.bottom >= height:
        end_time = pygame.time.get_ticks()
        screen.fill(color.black)
        lose_text = font.render("Game Over!", True, color.red)
        screen.blit(lose_text, (width//2 - lose_text.get_width()//2, height//2 - 100))
        final_score_text = font.render(f"Score: {score}", True, color.white)
        screen.blit(final_score_text, (width//2 - final_score_text.get_width()//2, height//2 - 50))
        elapsed = (end_time - start_time) / 1000
        final_time_text = font.render(f"Time: {elapsed:.2f} seconds", True, color.white)
        screen.blit(final_time_text, (width//2 - final_time_text.get_width()//2, height//2))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    running = False
        continue
    # 检查胜利条件
    if not bricks:
        end_time = pygame.time.get_ticks()
        screen.fill(color.black)
        win_text = font.render("You Win!", True, color.green)
        screen.blit(win_text, (width//2 - win_text.get_width()//2, height//2 - 100))
        final_score_text = font.render(f"Score: {score}", True, color.white)
        screen.blit(final_score_text, (width//2 - final_score_text.get_width()//2, height//2 - 50))
        elapsed = (end_time - start_time) / 1000
        final_time_text = font.render(f"Time: {elapsed:.2f} seconds", True, color.white)
        screen.blit(final_time_text, (width//2 - final_time_text.get_width()//2, height//2))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False
                    running = False
        continue
    draw()

pygame.quit()
sys.exit()
