import sys
import pygame
from  setting import Settings
from ship import Ship
from alien import Alien
import game_function as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    
    ai_settings = Settings()#创建一个实例
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))

    programIcon = pygame.image.load("image\icon.bmp")
    pygame.display.set_icon(programIcon)
    pygame.display.set_caption("外星人入侵")

    #创建一艘飞船
    ship = Ship(ai_settings , screen)
    
    #创建一个用于存储子弹的编组
    bullets = Group()

    #创建一个外星人
    #alien = Alien(ai_settings,screen)

    #创建外星人群
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #创建一个用于存储游戏信息的实例
    stats = GameStats(ai_settings)

    #创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)

    # 创建play按钮
    play_button = Button(ai_settings,screen,'Play')

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
        
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()
