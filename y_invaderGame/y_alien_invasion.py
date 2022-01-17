import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from b_bullet import B_Bullet


class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        """ゲームを初期化し、ゲームのリソースを作成する"""

        # インポートしたpygameのモジュールを初期化
        pygame.init()

        # ウインドウサイズ、背景色が設定されたクラスを読み込む
        self.settings = Settings()

        # ウインドウサイズ、背景色、タイトルをまとめて設定
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
        """
        フルスクリーンにする場合
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """

        pygame.display.set_caption("エイリアン侵略")

        # 宇宙船を表示する
        self.ship = Ship(self)

        # 弾丸グループを作成
        self.bullets = pygame.sprite.Group()

        # ビット用の弾丸グループを作成
        self.b_bullets = pygame.sprite.Group()

    def run_game(self):
        """ゲームのメインループを開始する"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
            # キーボードとマウスのイベントに対応する
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # キー入力
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:    # キー入力止め
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """キーを押すイベントに対応する"""
        if event.key == pygame.K_RIGHT:     # 右向き矢印
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:    # 左向き矢印
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:      # 上向き矢印
            self.ship.moving_top = True
        elif event.key == pygame.K_DOWN:    # 下向き矢印
            self.ship.moving_bottom = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self._b_fire_bullet()

    def _check_keyup_events(self, event):
        """キーを離すイベントに対応する"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False

    def _fire_bullet(self):
        """新しい弾を作成し、bulletsグループに追加する"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _b_fire_bullet(self):
        """ビットの新しい弾を作成し、bulletsグループに追加する"""
        if len(self.b_bullets) < self.settings.bullet_allowed:
            new_bullet = B_Bullet(self)
            self.b_bullets.add(new_bullet)

    def _update_bullets(self):
        """弾の位置を更新し、古い弾を廃棄する"""
        # 弾の位置を更新する
        self.bullets.update()
        self.b_bullets.update()

        # 見えなくなった弾を廃棄する
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().width:
                self.bullets.remove(bullet)

        for bullet in self.b_bullets:
            if bullet.rect.left >= self.screen.get_rect().width:
                self.b_bullets.remove(bullet)


    def _update_screen(self):
            # 画面上の画像を更新し、新しい画面に切り替える
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.b_bullets.sprites():
                bullet.draw_bullet()

            # 最新の状態の画面を表示する
            pygame.display.flip()

if __name__ == '__main__':
    # ゲームのインスタンスを作成し、ゲームを実行する
    ai = AlienInvasion()
    ai.run_game()

