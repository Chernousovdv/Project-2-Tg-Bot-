class Globals:
    is_info = True;
    def is_active(self):
        return self.is_info
    def change(self, top):
        self.is_info = top


is_abilities = Globals()
is_passive = Globals()
is_ally_tips = Globals()
is_enemy_tips = Globals()
is_found = Globals()
is_found.change(False)

