import cv2


def show(win_name, img, scale=0.6):
    im = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)),
                    interpolation=cv2.INTER_LINEAR)
    cv2.imshow(win_name, im)
