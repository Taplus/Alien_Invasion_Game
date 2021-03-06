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