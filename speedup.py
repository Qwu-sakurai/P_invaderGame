class SpeedUp:

    def __init__(self):
        self.item_kinds = "images/speedup.png"
        self.speedup = 0.2

    def item_do(self,ai_game):
        if ai_game.settings.ship_speed < ai_game.settings.ship_max_speed:
            ai_game.settings.ship_speed += self.speedup