class GameStats:
    """エイリアン侵略ゲームの統計情報を記録する"""

    def __init__(self,ai_game):
        """統計情報を初期化する"""
        self.settings = ai_game.settings
        self.reset_stats()

        # エイリアン侵略ゲームをアクティブな状態で開始する
        self.game_active = False

        # GAMEOVERフラグ
        self.game_over = False

        # ハイスコア
        self.high_score = 0

    def reset_stats(self):
        """ ゲーム中に変更される統計情報を初期化する"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1