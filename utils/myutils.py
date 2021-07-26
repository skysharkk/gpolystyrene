from collections import namedtuple
import math
import ctypes
from array import array


def round_half_up(n, decimals=0, int_result=True):
    multiplier = 10 ** decimals
    result = math.floor(n * multiplier + 0.5) / multiplier
    if int_result:
        return int(result)
    else:
        return result


def get_corner_coordinates(coordinates_tuple):
    print(coordinates_tuple)
    Points = namedtuple("Points", ["min_x", "max_x", "min_y", "max_y"])
    x_coordinates_list = []
    y_coordinates_list = []
    for index in range(len(coordinates_tuple)):
        if index % 2 == 0:
            x_coordinates_list.append(coordinates_tuple[index])
        else:
            y_coordinates_list.append(coordinates_tuple[index])
    max_x = max(x_coordinates_list)
    min_x = min(x_coordinates_list)
    max_y = max(y_coordinates_list)
    min_y = min(y_coordinates_list)
    return Points(min_x, max_x, min_y, max_y)


def get_rectangle_sizes(coordinates_tuple, scale):
    coordinates = get_corner_coordinates(coordinates_tuple)
    width = abs(round_half_up(
        (coordinates.max_x - coordinates.min_x) * scale))
    height = abs(round_half_up(
        (coordinates.max_y - coordinates.min_y) * scale))
    return [width, height]


def compare_list_or_tuple(first_list, second_list):
    return set(first_list) == set(second_list)


def is_elem_exist_in_collection(elem, collection):
    for item in collection:
        if compare_list_or_tuple(item.coord, elem):
            return True
    return False


def show_error_window(error_message, window_name=u"Ошибка"):
    ctypes.windll.user32.MessageBoxW(
        0, error_message, window_name, 0)


def create_array_of_double(converted_list):
    return array("d", converted_list)


def two_dimension_list_to_list(converted_list):
    formatted_list = []
    for item in converted_list:
        formatted_list.extend(item)
    return formatted_list
