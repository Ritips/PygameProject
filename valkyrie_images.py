from LoadImage import load_image
import pygame
from SETTINGS import width, height


def transform_image(image):
    x, y = image.get_size()
    x, y = int(width * (x + 1) / 800), int(height * (y + 1) / 600)
    return pygame.transform.scale(image, (x, y))


def transform_images(dictionary):
    for key in dictionary:
        dictionary[key] = transform_image(dictionary[key])


valkyrie_side_active_1 = load_image('ValkyrieSide1.png')
valkyrie_side_active_2 = load_image('ValkyrieSide2.png')
valkyrie_side_active_reverse_1 = load_image('ValkyrieSideReverse1.png')
valkyrie_side_active_reverse_2 = load_image('ValkyrieSideReverse2.png')
valkyrie_back_active_1 = load_image('ValkyrieBack1.png')
valkyrie_back_active_2 = load_image('ValkyrieBack2.png')
valkyrie_front_active_1 = load_image('ValkyrieFront1.png')
valkyrie_front_active_2 = load_image('ValkyrieFront2.png')


valkyrie_images = {
    'side1': valkyrie_side_active_1,
    'side2': valkyrie_side_active_2,
    'side_reverse1': valkyrie_side_active_reverse_1,
    'side_reverse2': valkyrie_side_active_reverse_2,
    'back1': valkyrie_back_active_1,
    'back2': valkyrie_back_active_2,
    'front1': valkyrie_front_active_1,
    'front2': valkyrie_front_active_2
}

transform_images(valkyrie_images)
