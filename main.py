import cv2
import numpy as np
from utils import show

from radiograph_standard import RadiographInfo


def get_slices_params2(radiograph_info: RadiographInfo) -> tuple[int, int]:
    radiograph = radiograph_info.get_radiograph()
    lower_frontier_count = radiograph.max_count * radiograph_info.lower_frontier_coefficient
    upper_frontier_count = radiograph.max_count * radiograph_info.upper_frontier_coefficient
    first = second = None
    for i in range(len(radiograph.counts) - 1, 0, -1):
        if radiograph.counts[i] >= upper_frontier_count and first is None:
            first = int(radiograph.values[i])
        if radiograph.counts[i] >= lower_frontier_count and second is None:
            second = int(radiograph.values[i])
    return first, second
    #
    #
    #
    # i = 0
    # while i < len(radiograph.counts) and radiograph.counts[i] < lower_frontier_count:
    #     i += 1
    # if i >= len(radiograph.counts):
    #     return (0, 0), (0, 0)
    # first = int(radiograph.counts[i])
    # while i < len(radiograph.counts) and radiograph.counts[i] < upper_frontier_count:
    #     i += 1
    # if i >= len(radiograph.counts):
    #     return (0, 0), (0, 0)
    # second = int(radiograph.counts[i])
    #
    # while i < len(radiograph.counts) and radiograph.counts[i] > upper_frontier_count:
    #     i += 1
    # if i >= len(radiograph.counts):
    #     return (0, 0), (0, 0)
    # third = int(radiograph.counts[i])
    # while i < len(radiograph.counts) and radiograph.counts[i] > lower_frontier_count:
    #     i += 1
    # if i >= len(radiograph.counts):
    #     return (0, 0), (0, 0)
    # forth = int(radiograph.counts[i])
    # return (first, second), (third, forth)


def get_slices_params(counts: list[int], values: list[int], percent=0.1825) -> list[tuple[int, int]]:
    if len(values) != len(counts):
        raise Exception(f'Counts and values should have equals lengths. {len(values)} != {len(counts)}')
    frontier_value = np.max(counts) * percent
    result = []
    last_added_idx = 0
    is_found_high = False
    for i in range(len(counts)):
        if counts[i] > frontier_value and not is_found_high:
            result.append((int(values[i]), 0))
            is_found_high = True
        if counts[i] <= frontier_value and is_found_high:
            result[last_added_idx] = (result[last_added_idx][0], int(values[i]))
            last_added_idx += 1
            is_found_high = False
    return result[0: -1]


def main():
    for i in range(1, 4):
        radiograph = cv2.imread(f'{i}.JPG')
        radiograph = cv2.cvtColor(radiograph, cv2.COLOR_BGR2GRAY)
        rad_info = RadiographInfo(radiograph)
        slices_params = get_slices_params2(rad_info)
        show(f'init{i}', radiograph)
        show(f'slice{i}', cv2.inRange(radiograph, slices_params[0], slices_params[1]))

    # radiograph = cv2.cvtColor(radiograph, cv2.COLOR_BGR2GRAY)
    # show('initial', radiograph)
    #
    # histogram = np.histogram(radiograph, 100)
    # counts = histogram[0][1:]
    # values = histogram[1][2:]
    #
    # slice_options = get_slices_params(counts, values)
    #
    # result_img = cv2.inRange(radiograph, *slice_options[0])
    # for slice_option in slice_options:
    #     result_img = cv2.bitwise_or(result_img, cv2.inRange(radiograph, *slice_option))
    #
    # show('result', result_img)
    # show('neg_result', cv2.bitwise_not(result_img))
    # show('prev', cv2.inRange(radiograph, 150, 180))
    # show('result3', cv2.bitwise_and(cv2.bitwise_not(result_img), radiograph))
    # plot.plot(values, counts)
    # plot.show()
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
