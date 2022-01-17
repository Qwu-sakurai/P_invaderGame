import pygame
from pygame.sprite import Sprite
import random
from speedup import Speedup

class Item(Sprite):
    """アイテムを管理するクラス"""

    def __init__(self,ai_game,bullet):
        super().__init__()
        self.screen = ai_game.screen
        self.scree_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 生成するアイテムの種類を選択
        speed = Speedup()
        item_kinds = [speed,'images/twin.png','images/barrier.png']
        image_name = random.choice(item_kinds)
        self.image = pygame.image.load(image_name)
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
        """画面に弾を描画する"""
        self.screen.blit(self.image, self.rect)

    def speed_up(self):
        self.settings.ship_speed += 0.2

    def twin_shot(self,ship):
        self.settings.bullet_allowed *= 2
        self.settings.twin_shot = True

    def barrier(self):
        self.settings.barrier = True

