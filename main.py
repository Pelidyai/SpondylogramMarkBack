import os

import cv2

from extraction import get_spine
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


# def main():
#     for i in range(1, 4):
#         radiograph = cv2.imread(f'{i}.JPG')
#         radiograph = cv2.cvtColor(radiograph, cv2.COLOR_BGR2GRAY)
#         rad_info = RadiographInfo(radiograph)
#         slices_params = get_slices_params2(rad_info)
#         show(f'init{i}', radiograph)
#         show(f'slice{i}', cv2.inRange(radiograph, *slices_params))
#     cv2.waitKey(0)


def main():
    files = os.listdir('images/side')
    for file in files:
        print(file)
        radiograph = cv2.imread(os.path.join('images/side', file))
        radiograph = cv2.cvtColor(radiograph, cv2.COLOR_BGR2GRAY)
        rad_info = RadiographInfo(radiograph)
        slices_params = get_slices_params2(rad_info)
        spine_image, _ = get_spine(radiograph, *slices_params)
        if spine_image.shape[0] > 0 and spine_image.shape[1] > 0:
            cv2.imwrite(os.path.join('results/side', file), spine_image)

    # radiograph = cv2.imread(os.path.join('images/front', '16.png'))
    # radiograph = cv2.cvtColor(radiograph, cv2.COLOR_BGR2GRAY)
    # rad_info = RadiographInfo(radiograph)
    # slices_params = get_slices_params2(rad_info)
    # spine_image, _ = get_spine(radiograph, *slices_params)
    # show('res', spine_image)
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
