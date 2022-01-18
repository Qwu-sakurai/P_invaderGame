import pygame
from pygame.sprite import Sprite
import random
from speedup import SpeedUp
from barrier import Barrier
from twin import Twin

class Item(Sprite):
    """アイテムを管理するクラス"""

    def __init__(self,ai_game,bullet):
        super().__init__()
        self.screen = ai_game.screen
        self.scree_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 生成するアイテムの種類を選択
        speed = SpeedUp()
        barrier = Barrier()
        twin = Twin()
        item_kinds = [speed,twin,barrier]
        self.item_object = random.choice(item_kinds)
        self.image = pygame.image.load(self.item_object.item_kinds)
        self.rect = self.image.get_rect()

        # 生成される位置を設定
        self.rect.top = bullet.rect.top
        self.rect.x = bullet.rect.x

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """画面上のアイテムを移動させる"""

        # 弾の浮動小数点での位置を更新する
        self.y += self.settings.a_bullet_speed

        # rectの位置を更新する
        self.rect.y = self.y

    def draw_item(self):
        """画面にアイテムを描画する"""
        self.screen.blit(self.image, self.rect)

    def item_do(self,ai_game):
        self.item_object.item_do(ai_game)

