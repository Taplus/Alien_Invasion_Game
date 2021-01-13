import sys
import pygame
from  setting import Settings

def run_game():
    ai_settings = Settings()#创建一个实例
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")

    #设置背景色
    bg_color = (ai_settings.bg_color)#灰色
    #开始游戏的主循环
    while True:

        #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #用背景色填充屏幕
        screen.fill(bg_color)

        #让最近绘制的屏幕可见
        pygame.display.flip()

run_game()