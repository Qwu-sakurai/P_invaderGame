import pygame
from pygame.sprite import Sprite
import random

class Star(Sprite):
    """背景用の星"""

    def __init__(self, ai_game):
        """星を初期化し、開始時の位置を設定する"""
        super().__init__()
        self.screen = ai_game.screen

        # 星のリスト
        y_star = 'images/star/star.png'
        g_star = 'images/star/g_star.png'
        r_star = 'images/star/r_star.png'
        b_star = 'images/star/b_star.png'
        star_list = [y_star,g_star,r_star,b_star]

        # 星の画像を読み込み、サイズを取得する
        self.image = pygame.image.load(random.choice(star_list))
        self.rect = self.image.get_rect()

        # 新しい星を画面の左上らへんに配置する
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 星の実際の位置を格納する
        self.x = float(self.rect.x)