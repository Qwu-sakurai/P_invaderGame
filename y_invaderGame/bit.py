import pygame

class Bit:
    """BITを管理するクラス"""

    def __init__(self, ai_game):
        """BITを初期化し、開始時の位置を設定する"""

        # ai_gameはpygameのモジュール
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 宇宙船の画像を読み込み、サイズを取得する
        self.image = pygame.image.load('images/bit.png')
        self.rect = self.image.get_rect()

        # 新しい宇宙船を画面左部の中央に配置する
        self.rect.midleft = self.screen_rect.midleft

        # 宇宙船の水平位置の浮動小数点数を格納する
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移動フラグ
        self.moving = False


    def update(self,x_list,y_list):
        """移動フラグによって宇宙船の位置を更新する"""

        # self.xからrectオブジェクトの位置を更新する
        self.rect.x = x_list[0]
        self.rect.y = y_list[0]

    def blitme(self):
        """宇宙船を現在位置に描画する"""
        self.screen.blit(self.image, self.rect)
