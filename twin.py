class Twin:

    def __init__(self):
        self.item_kinds = "images/twin.png"

    def item_do(self,ai_game):
        ai_game.settings.twin_shot_flag = True