from SettingsRebase import level_first
from LoadLevel import load_level


class QueenLevel:
    def __init__(self):
        self.current_level = 1
        self.finished = False
        self.level = load_level(level_first)

    def get_level(self):
        return self.level, self.current_level


class Levels:
    def __init__(self):
        self.all_levels = [None, QueenLevel()]
        with open('data/levels.txt') as f:
            self.available_levels = list(map(int, map(str.strip, f.readlines())))
        self.current_level_index = None
        self.current_level = None

    def finish_level(self):
        if self.current_level:
            self.current_level.finish_level()
            with open('data/levels.txt', 'a') as f:
                print(self.current_level_index, file=f)
            self.available_levels.append(self.current_level_index)

    def chose_level(self, level_chosen=None):
        if not self.available_levels:
            self.current_level_index = 1
        elif not level_chosen:
            self.current_level_index = 1
        else:
            self.current_level_index = level_chosen
        self.current_level = self.all_levels[self.current_level_index]

    def get_level(self):
        return self.all_levels[self.current_level_index]


LEVELS = Levels()
