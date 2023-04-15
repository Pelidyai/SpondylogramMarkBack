import cv2
import numpy as np


class _Radiograph:
    def __init__(self, radiograph_image):
        self.__image = radiograph_image
        self.mean: float = float(np.mean(radiograph_image))
        self.median: float = float(np.median(radiograph_image))
        self.std: float = float(np.std(radiograph_image))
        histogram = np.histogram(radiograph_image, 100)
        self.counts: list[float] = histogram[0][4:-10].tolist()
        self.values: list[float] = histogram[1][5:-10].tolist()
        self.max_count = np.max(self.counts)


class _ReferenceRadiograph:
    __radiograph_instance: _Radiograph = None
    upper_frontier_coefficient = 0.3466
    lower_frontier_coefficient = 0.0655

    def __init__(self):
        raise RuntimeError('Call get_radiograph_instance() instead')

    @classmethod
    def get_radiograph_instance(cls):
        if cls.__radiograph_instance is None:
            cls.__radiograph_instance = _Radiograph(cv2.imread('1.JPG'))
        return cls.__radiograph_instance


class _RadiographComparator:
    @classmethod
    def compare(cls, to_compare: _Radiograph, reference: _Radiograph) -> float:
        result_coefficient = 1.0
        result_coefficient *= cls.__calc_coefficient(to_compare.mean, reference.mean)
        result_coefficient *= cls.__calc_coefficient(to_compare.median, reference.median)
        result_coefficient *= cls.__calc_coefficient(to_compare.std, reference.std)
        return result_coefficient

    @staticmethod
    def __calc_coefficient(to_compare: float, reference: float) -> float:
        return 1 + abs(to_compare - reference) / reference


class RadiographInfo:
    def __init__(self, radiograph_image):
        self.__radiograph = _Radiograph(radiograph_image)
        compared_coefficient =\
            _RadiographComparator.compare(self.__radiograph, _ReferenceRadiograph.get_radiograph_instance())
        self.upper_frontier_coefficient = _ReferenceRadiograph.upper_frontier_coefficient * compared_coefficient
        self.lower_frontier_coefficient = _ReferenceRadiograph.lower_frontier_coefficient * compared_coefficient

    def get_radiograph(self) -> _Radiograph:
        return self.__radiograph
