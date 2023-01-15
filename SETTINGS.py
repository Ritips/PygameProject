settings_file_name = 'data/SETTINGS.txt'
with open(settings_file_name) as f:
    size = width, height = list(map(int, f.readlines()))

FPS = 60

player_speed = int(2 * height / 600)
player_width = int(50 * width // 800)
player_height = int(50 * height // 600)

slime_speed = int(1 * height / 600)
slime_width = int(15 * width // 800)
slime_height = int(15 * height // 600)

meteor_width = int(34 * width / 800)
meteor_height = int(34 * height / 600)
magic_ball_width = int(20 * width / 800)
magic_ball_height = int(11 * height / 600)

hp_bar_height = 5 * height // 600

button_width = int(200 * width / 800)
button_height = int(50 * height / 600)

font_size = int(50 * width / 800)

tile_width = int(50 * width / 800)
tile_height = int(50 * height / 600)

level_first = 'first_level.txt'

black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
purple = (63, 18, 75)
dark_grey = (73, 77, 78)
light_grey = (128, 128, 128)
btn_start_game_color = (0, 0, 200)
