import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """宇宙船から発射される弾を管理するクラス"""

    def __init__(self, ai_game):
        """宇宙船の現在の位置から玉のオブジェクトを生成する"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        """弾のrectを(0,0)の位置に生成してから、正しい位置を設定"""
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 弾の位置を浮動小数点で保存する
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """画面上の玉を移動させる"""

        # 弾の浮動小数点での位置を更新する
        self.y -= self.settings.bullet_speed

        # rectの位置を更新する
        self.rect.y = self.y

    def draw_bullet(self):
        """画面に弾を描画する"""
        pygame.draw.rect(self.screen, self.color, self.rect)