import cv2
import numpy as np

__DEFAULT_LOWER_FRONTIER = 155
__DEFAULT_UPPER_FRONTIER = 181


def sigmoid(x, a, b):
    return 1 / (1 + np.exp(-a * x + b))


def sigm_calc(vec, a, b):
    for j in range(len(vec)):
        vec[j] = sigmoid(j / len(vec), a, b)


def horizontal_gradient(in_image, space_window_width, a=15, b=10):
    img = in_image.copy()
    for i in range(img.shape[0]):
        vec1 = np.zeros((img.shape[1] - space_window_width) // 2)
        sigm_calc(vec1, a, b)
        vec3 = vec1[::-1]
        must_have = img.shape[1] - (img.shape[1] + space_window_width) // 2
        if len(vec1) < must_have:
            space_window_width += must_have - len(vec1)
        vec2 = ([1] * space_window_width)
        vec2 = np.array(vec2)
        vec2 = np.concatenate((vec2, vec3))
        vec1 = np.concatenate((vec1, vec2))
        line_copy = np.float64(img[i])
        line_copy *= vec1
        img[i] = np.uint8(line_copy)
    return img


def get_bias_img(img):
    left = img[:, 0:img.shape[1] // 2]
    right = img[:, img.shape[1] // 2:img.shape[1]]
    means = [np.mean(left), np.mean(right)]
    asymp_xs = [0, img.shape[1]]
    if abs(means[0] - means[1]) > 7:
        if np.argmax(means) == 0:
            asymp_xs[1] = img.shape[1] - right.shape[1] // 4
        else:
            asymp_xs[0] = left.shape[1] // 4
    return img[:, asymp_xs[0]:asymp_xs[1]], asymp_xs


def get_x_asymptote(img):
    asymp_xs = [img.shape[0], 0]
    for line_num in range(img.shape[0]):
        line = img[line_num]
        for j in range(0, len(line) - 1):
            if j < asymp_xs[0] and line[j] == 0 and line[j + 1] != 0:
                asymp_xs[0] = j
                break
        for i in range(len(line) - 1, 1, -1):
            if i > asymp_xs[1] and line[i - 1] != 0 and line[i] == 0:
                asymp_xs[1] = i
                break
    return asymp_xs


def boxes_clean(boxes):
    out_boxes = []
    for i in range(len(boxes)):
        flag = True
        for j in range(len(boxes)):
            if boxes[i][0].item() < boxes[j][0].item() and boxes[i][1].item() < boxes[j][1].item() \
                    and boxes[i][2].item() > boxes[j][2].item() and boxes[i][3].item() > boxes[j][3].item():
                flag = False
                break
        if flag:
            out_boxes.append([boxes[i][0].item(), boxes[i][1].item(), boxes[i][2].item(), boxes[i][3].item()])
    return out_boxes


def get_spine(image, lower: int | None = 155, upper: int | None = 181):
    if lower is None:
        lower = __DEFAULT_LOWER_FRONTIER
    if upper is None:
        upper = __DEFAULT_UPPER_FRONTIER
    img = image.copy()
    orig = image.copy()
    img, bias_xs = get_bias_img(img)
    range1 = cv2.inRange(img, lower, upper)
    range1 = horizontal_gradient(range1, int(0.15 * img.shape[1]))
    range1 = cv2.inRange(range1, lower, upper)
    asymp_xs = get_x_asymptote(range1)
    img = orig[:, bias_xs[0] + asymp_xs[0]:asymp_xs[1] + bias_xs[0]]
    return img, bias_xs
