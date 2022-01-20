import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from a_bullet import A_Bullet
from alien import Alien
from star import Star
from button import Button
from scoreboard import Scoreboard
from item import Item
import random

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
        self.bg = pygame.image.load('images/sora.jpg').convert_alpha()
        self.rect_bg = self.bg.get_rect()

        pygame.display.set_caption("エイリアン侵略")

        # ゲーム統計情報を格納するインスタンスを生成
        self.stats = GameStats(self)

        # 星作成
        self.stars = pygame.sprite.Group()
        for i in range(self.settings.star_num):
            self._create_star()

        # 宇宙船を表示する
        self.ship = Ship(self)

        # 弾丸グループを作成
        self.bullets = pygame.sprite.Group()

        # エイリアン艦隊を作成
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # エイリアン用弾丸グループ作成
        self.a_bullets = pygame.sprite.Group()

        # アイテム用グループ作成
        self.items = pygame.sprite.Group()

        # Playボタンを作成する
        self.play_button = Button(self, "Play")

        # Exitボタンを作成
        self.exit_button = Button(self, "Exit")
        self.exit_button.rect.y += 100
        self.exit_button.msg_image_rect.y += 100

        # GAME OVER表示用ボタン（押せない）
        self.gameover = Button(self, "GAME OVER",size=(300,50),color=(255,0,0),text_color=(255,255,255))
        self.gameover.rect.y -= 150
        self.gameover.msg_image_rect.y -= 150

        # TITLE表示用ボタン（押せない）
        self.title = Button(self,"Alien Invasion",size=(500,100),color=(0,0,255),text_color=(0,0,0))
        self.title.rect.y -= 200
        self.title.msg_image_rect.y -= 200

        # NextStage表示用ボタン
        self.nextstage = Button(self, "NextStage", size=(500, 100), color=(0, 0, 255), text_color=(0, 0, 0))
        self.nextstage.rect.y -= 150
        self.nextstage.msg_image_rect.y -= 150

        # CLEAR表示用ボタン(押せない)
        self.clear = Button(self, "CLEAR!", size=(500, 100), color=(0, 0, 255), text_color=(0, 0, 0))
        self.clear.rect.y += 100
        self.clear.msg_image_rect.y += 100


        # scoreboardを作成
        self.score = Scoreboard(self)



    def run_game(self):
        """ゲームのメインループを開始する"""
        while True:
            self._check_events()
            # 使用できる宇宙船が存在する場合はゲームを続行する
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._a_update_bullets()
                self._update_aliens()
                self._update_item()

            # 画面を再描画する
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
                elif event.type == pygame.MOUSEBUTTONDOWN:  # マウスクリック
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    self._check_exit_button(mouse_pos)
                    self._check_nextstage_button(mouse_pos)

    def _check_exit_button(self,mouse_pos):
        """プレイヤーがexitボタンをクリックしたらゲームを終了する"""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #ゲームを終了する
            sys.exit()

    def _check_play_button(self,mouse_pos):
        """プレイヤーがPlayボタンをクリックしたら新規ゲームを開始する"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # ゲームの設定値をリセットする
            self.settings.initialize_dynamic_settings()

            # ゲームの統計情報をリセットする
            self.stats.reset_stats()
            self.stats.game_active = True
            self.score.prep_score()
            self.score.prep_level()
            self.score.prep_ships()

            # 残ったエイリアンと弾を廃棄する
            self.aliens.empty()
            self.bullets.empty()

            # 新しい艦隊を作成し宇宙船を中央に配置する
            self._create_fleet()
            self.ship.center_ship()

            # マウスカーソルを非表示にする
            # pygame.mouse.set_visible(False)

    def _check_nextstage_button(self,mouse_pos):
        """プレイヤーがボタンをクリックしたら次のステージへ進む"""
        button_clicked = self.nextstage.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.game_active = True
            self.stats.stage_clear = False


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
        if self.settings.twin_shot_flag:
            if len(self.bullets) < self.settings.bullet_allowed*2:
                new_bullet_l = Bullet(self)
                new_bullet_r = Bullet(self)
                new_bullet_l.x -= (self.ship.image.get_width()//2)
                new_bullet_l.rect.x = new_bullet_l.x
                new_bullet_r.x += (self.ship.image.get_width()//2)
                new_bullet_r.rect.x = new_bullet_r.x
                self.bullets.add(new_bullet_r)
                self.bullets.add(new_bullet_l)
        else:
            """新しい弾を作成し、bulletsグループに追加する"""
            if len(self.bullets) < self.settings.bullet_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)

    def _update_bullets(self):
        """弾の位置を更新し、古い弾を廃棄する"""
        # 弾の位置を更新する
        self.bullets.update()

        # 見えなくなった弾を廃棄する
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 弾とエイリアンの衝突に対応する
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # この一文でself.bulletsとself.aliensの衝突を感知するとそれを削除するようになる
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            self.stats.score += self.settings.point
            self.score.prep_score()
            self.score.check_high_score()
            if self.settings.item_drop >= random.randint(0,100):
                for bullet in collisions:
                    item = Item(self, bullet)
                    self.items.add(item)

        # エイリアンが０になったらステージクリアとし、ボタンを押したら再スタートする
        if not self.aliens:

            self.stats.game_active = False
            self.stats.stage_clear = True

            # 存在する弾を破壊し、新しい艦隊を作成する
            self.bullets.empty()
            self.a_bullets.empty()
            self.items.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # レベルを増やす
            self.stats.level += 1
            self.score.prep_level()

    def _update_item(self):
        """アイテムの位置を更新し、古い弾を廃棄する"""
        # 弾の位置を更新する
        if self.items:
            self.items.update()

        # 見えなくなったアイテムを廃棄する
        for item in self.items:
            if item.rect.top >= self.screen.get_height():
                self.bullets.remove(item)

        # アイテムと宇宙船の衝突に対応する
        self._check_item_ship_collisions()

    def _check_item_ship_collisions(self):
        # この一文でself.itemsとself.shipの衝突を感知するとそれを削除するようになる
        collisions = pygame.sprite.spritecollide(
            self.ship, self.items, True)

        if collisions:
            for item in collisions:
                item.item_do(self)


    def _update_aliens(self):
        """
        艦隊が画面の端にいるか確認してから、
        艦隊にいる全エイリアンの位置を更新する
        """
        self._alien_fire()
        self._check_fleet_edges()
        self.aliens.update()


        # エイリアン艦と宇宙船の衝突を探す
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        # 画面の一番下に到達したエイリアンを探す
        self._check_aliens_bottom()

    def _alien_fire(self):
        for alien in self.aliens:
            if self.settings.a_bullet_area >= random.randint(0,100):
                self._a_fire_bullet(alien)

    def _a_fire_bullet(self,alien):
        """alienの新しい弾を作成し、bulletsグループに追加する"""
        if len(self.a_bullets) < int(self.settings.a_bullet_allowed):
            new_bullet = A_Bullet(self,alien)
            self.a_bullets.add(new_bullet)

    def _a_update_bullets(self):
        """alienの弾の位置を更新し、古い弾を廃棄する"""
        # 弾の位置を更新する
        self.a_bullets.update()

        # 見えなくなった弾を廃棄する
        for bullet in self.a_bullets:
            if bullet.rect.bottom >= self.screen.get_rect().height :
                self.a_bullets.remove(bullet)

        # 弾と宇宙船の衝突に対応する
        self._check_bullet_ship_collisions()

    def _check_bullet_ship_collisions(self):
        # この一文でself.bulletsとself.aliensの衝突を感知するとそれを削除するようになる
        collisions = pygame.sprite.spritecollide(
            self.ship,self.a_bullets, True)

        if collisions:
            if not self.settings.barrier_flag:
                self._ship_hit()
            else:
                self.settings.barrier_flag = False
                self.ship.image = pygame.image.load('images/ship.png')

    def _check_aliens_bottom(self):
        """エイリアンが画面の一番下に到達したかを確認する"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 宇宙船に衝突した時と同じように扱う
                self._ship_hit()
                break


    def _ship_hit(self):
        """エイリアンと宇宙船の衝突に対応する"""
        self.ship.hit()
        self._update_screen()
        self.settings.reset_ship_settings()

        if self.stats.ships_left > 0:
            # 残りの宇宙船の数を減らす
            self.stats.ships_left -= 1
            print(f'残機：{self.stats.ships_left}')
            self.score.prep_ships()

            # 残ったエイリアンと弾を廃棄する
            self.aliens.empty()
            self.bullets.empty()
            self.a_bullets.empty()
            self.items.empty()

            # 新しい艦隊を生成し、宇宙船を中央に配置する
            self._create_fleet()
            self.ship.center_ship()

            # 一時停止する
            sleep(0.5)

        else:
            sleep(0.5)
            self.stats.game_active = False
            self.stats.game_over = True

    def _create_fleet(self):
        """エイリアンの艦隊を作成する"""
        # エイリアンを１匹作成し、１列のエイリアンの数を求める
        # 各エイリアンの間にはエイリアン１匹分のスペースを空ける
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # 画面両端をエイリアン１匹分あける
        available_space_x = self.settings.screen_width - (2 * alien_width)

        # 水平方向に収まるエイリアンの数を計算する
        number_aliens_x = available_space_x // (2 * alien_width)
        print(f'１列のエイリアン感の数：{number_aliens_x}')

        # 画面に収まるエイリアン艦隊の列を決定する
        # y方向の有効スペース = 画面の高さ - エイリアン艦３匹分の高さ - 宇宙船の高さ
        # 画面に収まる艦隊の列数 = y方向の有効スペース / エイリアン艦２匹分の高さ
        ship_height = self.ship.rect.height     # 宇宙船の高さ　
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_aliens_y = available_space_y // (2 * alien_height)
        print(f'y方向の有効スペース：{available_space_y} 画面に収まるエイリアン列数：{number_aliens_y}')


        # 最初の列のエイリアン艦隊を作成
        for y_number in range(number_aliens_y):
            for x_number in range(number_aliens_x):
                self._create_alien(x_number,y_number)

    def _create_alien(self, x_number, y_number):
        """エイリアン艦を１隻作成し列の中に配置する"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * x_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + (2 * alien.rect.height * y_number)
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """エイリアンが画面端に達した場合に適切な処理を行う"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """艦隊を下に移動し、横移動の方向を変更する"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_star(self):
        star = Star(self)
        star.x = random.randint(0, self.settings.screen_width)
        star.rect.x = star.x
        star.rect.y = random.randint(0, self.settings.screen_height)
        self.stars.add(star)

    def _update_screen(self):
            # 画面上の画像を更新し、新しい画面に切り替える
            self.screen.fill(self.settings.bg_color)

            # 宇宙背景描画
            self.screen.blit(self.bg,self.rect_bg)
            # 星描画
            self.stars.draw(self.screen)

            if self.stats.game_active:

                # 宇宙船描画
                self.ship.blitme()

                # アイテム描画
                for item in self.items.sprites():
                    item.draw_item()

                # 弾丸描画
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()

                for bullet in self.a_bullets.sprites():
                    bullet.draw_bullet()

                # エイリアン艦隊描画
                self.aliens.draw(self.screen)

                # スコア描画
                self.score.show_score()

            # ゲームが非アクティブ状態の時に「Play」「Exit」ボタンを描画する
            else:
                if self.stats.stage_clear:
                    self.nextstage.draw_button()
                    self.clear.draw_button()
                else:
                    self.play_button.draw_button()
                    self.exit_button.draw_button()

                    if self.stats.game_over:
                        self.gameover.draw_button()
                        self.score.show_score()
                    else:
                        self.title.draw_button()

            # 最新の状態の画面を表示する
            pygame.display.flip()

if __name__ == '__main__':
    # ゲームのインスタンスを作成し、ゲームを実行する
    ai = AlienInvasion()
    ai.run_game()

