class Settings:
    """エイリアン侵略の全設定を格納するクラス"""

    def __init__(self):
        """ゲームの初期設定"""

        # 画面に関する設定
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # 宇宙船の設定
        self.ship_speed = 0.8
        self.ship_max_speed = 2.0
        self.ship_limit = 3

        # 弾の設定
        self.bullet_speed = 1.0     # 弾の速さ
        self.bullet_width = 3       # 弾の幅
        self.bullet_height = 15     # 弾の高さ
        self.bullet_color = (60, 60, 60)  # 弾の色
        self.bullet_allowed = 3     # 一度に発射できる弾の上限値

        # 星の数
        self.star_num = 15

        # エイリアンの設定
        self.alien_speed = 0.25
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.a_bullet_color = (0, 255, 0)
        self.a_bullet_speed = 0.75
        self.a_bullet_width = 5
        self.a_bullet_height = 5
        self.a_bullet_allowed = 5
        self.a_bullet_area = 10
        self.point = 100

        self.speedup_scale = 1.1

        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # アイテム関係の設定
        self.item_drop = 10
        self.twin_shot = False
        self.barrier = False
        self.item_speed = 0.5

    def initialize_dynamic_settings(self):
        """ゲーム中に変更される設定値を初期化する"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.fleet_direction = 1
        self.alien_speed = 0.25

        self.alien_points = 50

    def increase_speed(self):
        """速度の設定値を増やす"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.a_bullet_allowed += 1

        self.alien_points = int(self.alien_points * self.score_scale)