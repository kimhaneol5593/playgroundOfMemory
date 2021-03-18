from enum import Enum


class Color(Enum):
    GAME_OVER = (111, 247, 229)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    TEAL = (0, 255, 255)
    ORANGE = (255, 165, 0)
    GOLD = (255, 215, 0)
    PURPLE = (138, 43, 226)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (122, 122, 255)
    FIREBRICK = (178, 34, 34)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)


colors_by_number = {
    1: Color.GAME_OVER,
    2: Color.WHITE,
    3: Color.BLACK,
    4: Color.TEAL,
    5: Color.ORANGE,
    6: Color.GOLD,
    7: Color.PURPLE,
    8: Color.BLUE,
    9: Color.LIGHT_BLUE,
    10: Color.FIREBRICK,
    11: Color.GREEN,
    12: Color.RED
}


def get_color_by_number(number):
    return colors_by_number.get(number)


colors_by_name = {
    'GAME_OVER': 1,
    'WHITE': 2,
    'BLACK': 3,
    'TEAL': 4,
    'ORANGE': 5,
    'GOLD': 6,
    'PURPLE': 7,
    'BLUE': 8,
    'LIGHT_BLUE': 9,
    'FIREBRICK': 10,
    'GREEN': 11,
    'RED': 12
}


def get_color_number_by_name(colour_str):
    return colors_by_name.get(colour_str)
