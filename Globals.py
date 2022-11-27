
class Globals:
    is_smth = True;
    def is_active(self):
        return self.is_smth
    def change(self, top):
        self.is_smth = top

is_abilities = Globals()
is_passive = Globals()
is_ally_tips = Globals()
is_enemy_tips = Globals()
is_found = Globals()
