# Alien_invasion-Game
- 用 Python 编写的外星人入侵小游戏
- 来源 《Python编程 从入门到实践》项目1 外星人入侵
----

## 操作方法
- 按左右键移动飞船
- 按空格键射击
- 按Q键退出
----
## 附上代码

- 主程序

  ```python
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
  
  ```

----

- 飞船类:设置飞船的相关参数

  ```python
  import pygame
  from pygame.sprite import Sprite
  
  class Ship(Sprite):
      def __init__(self,ai_settings,screen):
          '''初始化飞船并设置其初始位置'''
  
          super(Ship,self).__init__()
          # Sprite.__init__(self)
          self.screen = screen
  
          self.ai_settings = ai_settings
  
          # 加载飞船图像并获得其外接矩形
          self.image = pygame.image.load("image\ship.bmp")
          self.rect = self.image.get_rect()
          self.screen_rect = screen.get_rect()
  
          # 将每艘飞船放在屏幕底部中央
          self.rect.centerx = self.screen_rect.centerx
          self.rect.bottom = self.screen_rect.bottom
  
          #在飞船属性center中存储小数
          self.center = float(self.rect.centerx)
  
          # 移动标志
          self.moving_right = False
          self.moving_left = False
  
      def update(self):
          '''根据移动标志调整飞船的位置'''
          #更新飞船的center值，而不是rect
          if self.moving_right and self.rect.right < self.screen_rect.right:
              self.rect.centerx += self.ai_settings.ship_speed_factor
  
          if self.moving_left and self.rect.left > 0:
              self.rect.centerx -= self.ai_settings.ship_speed_factor
  
      def blitme(self):
          '''在指定位置绘制飞船'''
          self.screen.blit(self.image,self.rect)
  
      def center_ship(self):
          '''让飞船在屏幕居中'''
          self.center = self.screen_rect.centerx
  ```

  

----

- 外星人类

  ```python
  import pygame
  from pygame.sprite import Sprite
  
  class Alien(Sprite):
      '''表示单个外星人的类'''
  
      def __init__(self,ai_settings,screen):
          '''初始化外星人并设置其起始位置'''
          Sprite.__init__(self)
          self.screen = screen
          self.ai_settings = ai_settings
  
          # 加载外星人图像，并设置其rect属性
          self.image = pygame.image.load("image\\alien.bmp")
          self.rect =self.image.get_rect()
  
          # 每个外星人最初都在屏幕左上角附近
          self.rect.x = self.rect.width
          self.rect.y = self.rect.height
  
          # 存储外星人的准确位置
          self.x = float(self.rect.x)
  
      def blitme(self):
          '''在指定位置上绘制外星人'''
          self.screen.blit(self.image,self.rect)
  
      def check_edges(self):
          '''如果外星人位于屏幕边缘，就返回True'''
          screen_rect = self.screen.get_rect()
          if self.rect.right >= screen_rect.right:
              return True
          elif self.rect.left <= 0:
              return True
  
      def update(self):
          '''向右移动外星人'''
          self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
          self.rect.x = self.x
  
  ```

  

----

- 游戏运行函数

  ```python
  import sys
  import pygame
  from bullet import Bullet
  from alien import Alien
  from time import sleep
  
  def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
      '''响应按键和鼠标事件'''
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              sys.exit()
  
          elif event.type == pygame.KEYDOWN:
              check_keydown_events(event, ai_settings, screen, ship, bullets)
  
          elif event.type == pygame.KEYUP:
              check_keyup_events(event,ship)
  
          elif event.type == pygame.MOUSEBUTTONDOWN:
              mouse_x,mouse_y = pygame.mouse.get_pos()
              check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
  
  def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
      '''在玩家单击play按钮时开始新游戏'''
      button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
      if button_clicked and not stats.game_active:
          # 重置游戏设置
          ai_settings.initialize_dynamic_settings()
  
          # 隐藏光标
          pygame.mouse.set_visible(False)
          # 重置游戏统计信息
          stats.rest_stats()
          stats.game_active = True
  
          # 重置记分牌图像
          sb.prep_score()
          sb.prep_high_score()
          sb.prep_level()
          sb.prep_ships()
  
          # 清空外星人列表和子弹列表 
          aliens.empty()
          bullets.empty()
  
          # 创建一群新的外星人，并让飞船居中
          create_fleet(ai_settings,screen,ship,aliens)
          ship.center_ship()
  
  def check_keydown_events(event, ai_settings, screen, ship, bullets):
      if event.key == pygame.K_RIGHT:
          ship.moving_right = True
      elif event.key == pygame.K_LEFT:
          ship.moving_left = True
      elif event.key == pygame.K_SPACE:
          fire_bullet(ai_settings,screen,ship,bullets)
      elif event.key == pygame.K_q:
          sys.exit()
  
  def check_keyup_events(event,ship):
      if event.key == pygame.K_RIGHT:
          ship.moving_right = False
      elif event.key == pygame.K_LEFT:
          ship.moving_left = False
  
  def fire_bullet(ai_settings,screen,ship,bullets):
      #创建一颗子弹，并将其加到编组bullets中
      if len(bullets) < ai_settings.bullet_allowed:
          new_bullet = Bullet(ai_settings,screen,ship)
          bullets.add(new_bullet)   
  
  def check_high_score(stats,sb):
      '''检查是否诞生了最高得分'''
      if stats.score > stats.high_score:
          stats.high_score = stats.score
          sb.prep_high_score()
  
  def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
      '''更新子弹的位置，并消除已消失的子弹'''
      bullets.update()
  
      # 删除已消失的子弹
      for bullet in bullets.copy():
          if bullet.rect.bottom <= 0:
              bullets.remove(bullet)
  
      check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
  
  def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
      # 检查是否有子弹击中了外星人，若有就删除外星人和子弹
      collisios = pygame.sprite.groupcollide(bullets,aliens,True,True)
      # 模拟高能子弹，后两个参数设置为 False,True
      if collisios:
          for alien in collisios.values():
              stats.score += ai_settings.alien_points
              sb.prep_score()
          check_high_score(stats,sb)
  
      #打完外星人后新建一批
      if(len(aliens) == 0):
          # 如果这批外星人都被消灭，就提高一个等级
          # 删除现有的子弹并新建一群外星人
          bullets.empty()
          ai_settings.increase_speed()
  
          # 提高等级
          stats.level += 1
          sb.prep_level()
          create_fleet(ai_settings,screen,ship,aliens)
  
  def create_fleet(ai_settings,screen,ship,aliens):
      '''创建外星人群'''
      alien = Alien(ai_settings,screen)
      number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
      number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
      for row_number in range(number_rows):
          #创建第一行外星人
          for alien_number in range(number_aliens_x):
              #创建一个外星人并将其加入到当前行
              create_alien(ai_settings,screen,aliens,alien_number,row_number)
  
  def create_alien(ai_settings,screen,aliens,alien_number,row_number):
      '''创建一个外星人并将其放在当前行'''
      alien = Alien(ai_settings,screen)
      alien_width = alien.rect.width
      alien.x = alien_width + 2 * alien_width * alien_number
      alien.rect.x = alien.x
      alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
      aliens.add(alien)
  
  def get_number_aliens_x(ai_settings,alien_width):
      '''计算每行可以容纳多少个人外星人'''
      available_space_x = ai_settings.screen_width - 2 * alien_width
      number_aliens_x = int(available_space_x / (2 * alien_width))
      return number_aliens_x
  
  def get_number_rows(ai_settings,ship_height,alien_height):
      '''计算屏幕可容纳多少行外星人'''
      available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
      number_rows = int(available_space_y / (2 * alien_height))
      return number_rows
  
  def check_fleet_edges(ai_settings,aliens):
      '''有外星人到达边缘时需要采取的相应措施'''
      for alien in aliens.sprites():
          if alien.check_edges():
              change_fleet_direction(ai_settings,aliens)
              break
  
  def change_fleet_direction(ai_settings,aliens):
      '''将整群外星人群下移，并改变它们的方向'''
      for alien in aliens.sprites():
          alien.rect.y += ai_settings.fleet_drop_speed
      ai_settings.fleet_direction *= -1
  
  def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
      '''更新外星人群中所有外星人的位置'''
      check_fleet_edges(ai_settings,aliens)
      aliens.update()
  
      # 检测外星人和飞船之间的碰撞
      if pygame.sprite.spritecollideany(ship,aliens):
          ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
  
      # 检查是否有外星人到达屏幕底端
      check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)
  
  def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
      '''响应被外星人撞到的飞船'''
      if stats.ships_left > 0:
          # 将 ships_left 减 1
          stats.ships_left -= 1
  
          # 更新记分牌
          sb.prep_ships()
  
          # 清空外星人列表和子弹列表
          aliens.empty()
          bullets.empty()
  
          #创建一群新的外星人，并将飞船放到屏幕底端中央
          create_fleet(ai_settings,screen,ship,aliens)
          ship.center_ship()
  
          # 暂停
          sleep(0.5)
      else:
          stats.game_active = False
          pygame.mouse.set_visible(True)
  
  def  check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
      '''检查是否有外星人到达了屏幕底端'''
      screen_rect = screen.get_rect()
      for alien in aliens.sprites():
          if alien.rect.bottom >= screen_rect.bottom:
              # 像飞船被撞到那样处理
              ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
              break
       
  
  def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
      '''更新屏幕上的图像并切换到新屏幕'''
      #用背景色填充屏幕
      screen.fill(ai_settings.bg_color)
      #在飞船和外星人后面重绘所有子弹
      for bullet in bullets.sprites():
          bullet.draw_bullet()
      ship.blitme()
      aliens.draw(screen)
      #alien.blitme()
      # 显示得分
      sb.show_score()
      
      # 如果游戏处于非活动状态，就绘制 Play 按钮
      if not stats.game_active:
          play_button.draw_button()
  
      #让最近绘制的屏幕可见
      pygame.display.flip()
  
  
  ```

----

- 设置类：用于设置游戏的各项参数

  ```python
  class Settings():
      '''
      该类用于存储游戏中的所有设置
      '''
  
      def __init__(self):
          '''初始化游戏设置'''
          #屏幕设置
          self.screen_width = 1200
          self.screen_height = 800
          self.bg_color = (230,230,230)
  
          #飞船的设置
          self.ship_speed_factor = 1.5
          self.ship_limit = 3
  
          #子弹的设置
          self.bullet_speed_factor = 1
          self.bullet_width = 3
          self.bullet_height = 15
          self.bullet_color = 60,60,60
          self.bullet_allowed = 20
  
          #外星人的设置
          self.alien_speed_factor = 1
          self.fleet_drop_speed = 10
          # fleet_direction 为1表示向右移，为-1表示向左移
          self.fleet_direction = 1
  
          # 游戏速度倍率
          self.speedup_scale = 1.1
  
          # 外星人点数的提高速度
          self.score_scale = 1.5
  
  
          self.initialize_dynamic_settings()
  
      def initialize_dynamic_settings(self):
          '''初始化随游戏进行而变化的设置'''
          self.ship_speed_factor = 1.5
          self.bullet_speed_factor = 3
          self.alien_speed_factor = 1
  
          # 1向右，-1向左
          self.fleet_direction = 1
  
          # 计分
          self.alien_points = 50
  
      def increase_speed(self):
          '''提高速度设置'''
          self.ship_speed_factor *= self.speedup_scale
          self.bullet_speed_factor *= self.speedup_scale
          self.alien_speed_factor *= self.speedup_scale
          self.alien_points = int(self.alien_points * self.score_scale)
  
  ```

----

- 子弹类：飞船发射的子弹

  ```python
  import pygame
  from pygame.sprite import Sprite
  
  class Bullet(Sprite):
      '''一个对飞船发射的子弹进行管理的类'''
  
      def  __init__(self,ai_settings,screen,ship):
          '''在飞船所处的位置创建一个子弹对象'''
          Sprite.__init__(self)
          #super(Bullet,self).__init__()# 调用super()来继承.__inti__()
          self.screen = screen
  
          # 在(0,0)创建一个表示子弹的矩形，再设置正确的位置
          self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
          self.rect.centerx = ship.rect.centerx
          self.rect.top = ship.rect.top
  
          #存储用小数表示的子弹位置
          self.y = float(self.rect.y)
  
          self.color = ai_settings.bullet_color
          self.speed_factor = ai_settings.bullet_speed_factor
  
      def update(self):
          '''向上移动子弹'''
          #更新表示子弹位置的小数值
          self.y -= self.speed_factor
          #更新表示子弹的rect的位置
          self.rect.y = self.y
  
      def draw_bullet(self):
          '''在屏幕上绘制子弹'''
          pygame.draw.rect(self.screen,self.color,self.rect)
  ```

----

- 游戏统计信息的类

  ```python
  class GameStats():
      '''跟踪游戏统计信息'''
      def __init__(self,ai_settings):
          '''初始化统计信息'''
          self.ai_settings = ai_settings
          self.rest_stats()
  
          # 历史最高分
          self.high_score = 0
  
          # 游戏刚启动时处于活动状态
          self.game_active = False
  
      def rest_stats(self):
          '''初始化在游戏运行期间可能变化的统计信息'''
          self.ships_left = self.ai_settings.ship_limit
          self.score = 0
          self.level = 1
  ```

----

- 记分板类：将统计的当前分数、历史最高分数和等级显示在屏幕上

  ```python
  import pygame.font
  from pygame.sprite import Group
  from ship import Ship
  
  class Scoreboard():
      '''显示得分信息的类'''
      
      def __init__(self,ai_settings,screen,stats):
          '''初始化显示得分需要设置的属性'''
          self.screen = screen
          self.screen_rect = screen.get_rect()
          self.ai_settings = ai_settings
          self.stats = stats
  
          # 显示得分信息时使用的字体设置
          self.text_color = (30,30,30)
          self.font = pygame.font.SysFont(None,48)
  
          # 准备初始和历史最高得分、等级、飞船图像
          self.prep_score()
          self.prep_high_score()
          self.prep_level()
          self.prep_ships()
  
  
  
      def prep_score(self):
          ''' 将得分转换为一幅渲染的图像'''
  
          # 圆整，第二个参数为负数指圆整到最近的10、100、1000等整数倍
          rounded_score = int(round(self.stats.score,-1))
          score_str = 'current score ' +  "{:,}".format(rounded_score)
          self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
  
          # 将得分放在屏幕右上角
          self.score_rect = self.score_image.get_rect()
          self.score_rect.right = self.screen_rect.right - 20
          self.score_rect.top = 20
  
      def prep_high_score(self):
          ''' 将历史最高得分转换为一幅渲染的图像'''
  
          # 圆整，第二个参数为负数指圆整到最近的10、100、1000等整数倍
          rounded_score = int(round(self.stats.high_score,-1))
          high_score_str = "High score " + "{:,}".format(rounded_score)
          self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
  
          # 将得分放在屏幕顶部中央
          self.high_score_rect = self.high_score_image.get_rect()
          self.high_score_rect.centerx = self.screen_rect.centerx
          self.high_score_rect.top = 20
  
      def prep_level(self):
          ''' 将等级渲染为图像'''
          level_str = str("{}".format(self.stats.level))
          self.level_image = self.font.render(level_str,True,self.text_color,self.ai_settings.bg_color)
          # 将得分放在得分下方
          self.level_rect = self.level_image.get_rect()
          self.level_rect.right = self.screen_rect.right - 20
          self.level_rect.top = self.score_rect.bottom + 10
  
      def prep_ships(self):
          '''显示还剩余多少飞船'''
          self.ships = Group()
          for ship_number in range(self.stats.ships_left):
              ship = Ship(self.ai_settings,self.screen)
              ship.rect.x = 10 + ship_number * ship.rect.width
              ship.rect.y = 10
              self.ships.add(ship)
  
      def show_score(self):
          '''显示得分'''
          self.screen.blit(self.score_image,self.score_rect)
          self.screen.blit(self.high_score_image,self.high_score_rect)
          self.screen.blit(self.level_image,self.level_rect)
  
          #绘制飞船
          self.ships.draw(self.screen)
  ```

----

- 按钮类：设置Play按钮

  ```python
  import pygame.font
  
  class Button():
  
      def __init__(self,ai_settings,screen,msg):
          '''初始化按钮的属性'''
          self.screen = screen
          self.ai_settings = ai_settings
          self.screen_rect = screen.get_rect()
  
          # 设置按钮的尺寸和其它属性
          self.width,self.height = 200,50
          self.button_color = (0,255,0)
          self.text_color = (255,0,0)
          self.font = pygame.font.SysFont(None,48) 
  
          # 创建按钮的rect对象，并使其居中
          self.rect = pygame.Rect(0,0,self.width,self.height)
          self.rect.center = self.screen_rect.center
  
          # 按钮的标签只需创建一次
          self.prep_msg(msg)
  
      def prep_msg(self,msg):
          '''将msg渲染为图像，并使其在按钮上居中'''
          self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
          self.msg_image_rect = self.msg_image.get_rect()
          self.msg_image_rect.center = self.rect.center
  
      def draw_button(self):
          # 绘制一个用颜色填充的按钮，再绘制文本
          self.screen.fill(self.button_color,self.rect)
          self.screen.blit(self.msg_image,self.msg_image_rect)
  ```

----

