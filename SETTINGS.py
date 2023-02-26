settings_file_name = 'data/SETTINGS.txt'
with open(settings_file_name) as f:  # load file with settings
    size = width, height = list(map(int, f.readlines()))

FPS = 60

player_speed = int(2 * height / 600)
player_width = int(50 * width // 800)
player_height = int(50 * height // 600)

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

wizard_ball_width = int(20 * width / 800)
wizard_ball_height = int(15 * height / 600)

wizard_speed = int(2 * height / 600)
wizard_width = int(10 * width // 800)
wizard_height = int(15 * height // 600)

second_level = 'slime_level.txt'
level_first = 'first_level.txt'
start_level = 'start_level.txt'
finish_level = 'finish_level.txt'

black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
purple = (63, 18, 75)
dark_grey = (73, 77, 78)
light_grey = (128, 128, 128)
btn_start_game_color = (0, 0, 200)
