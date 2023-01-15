from SETTINGS import *

size = width, height = normal_width, normal_height

FPS = 60

level_first = 'first_level.txt'

black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
purple = (63, 18, 75)
btn_start_game_color = (0, 0, 200)

constants_height = [
    normal_player_speed, normal_player_height, normal_slime_speed, normal_slime_height,
    normal_meteor_height, normal_magic_ball_height, normal_hp_bar_height, normal_tile_height, normal_button_height
]

constants_width = [
    normal_player_width, normal_slime_width, normal_meteor_width, normal_magic_ball_width,
    normal_button_width, normal_font_size, normal_tile_width
]


def rebase_size(new_size):
    global size, width, height
    size = width, height = new_size
    print(new_size)
    rebase_constants()


def rebase_constants():
    global constants_width, constants_height

    constants_width = list(map(lambda x: x * width // 800, constants_width))
    constants_height = list(map(lambda x: x * height // 600, constants_height))


rebase_size(size)

player_speed, player_height, slime_speed, \
    slime_height, meteor_height, magic_ball_height, hp_bar_height, tile_height, button_height = constants_height

player_width, slime_width, meteor_width, magic_ball_width, button_width, font_size, tile_width = constants_width
