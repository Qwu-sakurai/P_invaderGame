class Settings:
    """エイリアン侵略の全設定を格納するクラス"""

    def __init__(self):
        """ゲームの初期設定"""

        # 画面に関する設定
        self.screen_width = 800
        self.screen_height = 640
        self.bg_color = (0, 0, 0)

        # 宇宙船の設定
        self.ship_speed = 0.8

        # 弾の設定
        self.bullet_speed = 1.0     # 弾の速さ
        self.bullet_width = 15     # 弾の幅
        self.bullet_height = 3     # 弾の高さ
        self.bullet_color = (60, 60, 60)  # 弾の色
        self.bullet_allowed = 3     # 一度に発射できる弾の上限値
