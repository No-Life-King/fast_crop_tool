import os
import cv2


mouse_x = 0
mouse_y = 0
rect_scale = 1
make_crop = False

def mouse_rectangle(event, x, y, flags, param):
    global mouse_x, mouse_y, rect_scale, make_crop
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y = y
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0 and rect_scale > 1:
            rect_scale -= .3
        elif flags < 0:
            rect_scale += .3
    elif event == cv2.EVENT_LBUTTONUP:
        make_crop = True


filenames = os.listdir('dudes_undetected')
index = 0
key_code = 0
cv2.namedWindow("Crop Tool")
cv2.setMouseCallback('Crop Tool', mouse_rectangle)


def show_image(index):
    image = cv2.imread('dudes_undetected/' + filenames[index])

    height, width = image.shape[:2]

    if height > 800:
        image = cv2.resize(image, None, 0, 800/height, 800/height)

    if width > 1600:
        image = cv2.resize(image, None, 0, 1600/width, 1600/width)

    height, width = image.shape[:2]
    image = cv2.copyMakeBorder(image, int((800-height)/2), int((800-height)/2), int((1600-width)/2), int((1600-width)/2), cv2.BORDER_CONSTANT, value=(153,136,119))

    image_top_x = int((1600-width)/2)
    image_top_y = int((800-height)/2)

    top_x = mouse_x - int(100*rect_scale) - 1
    top_y = mouse_y - int(120*rect_scale) - 1

    top_x = image_top_x if top_x < image_top_x else top_x
    top_y = image_top_y if top_y < image_top_y else top_y

    bottom_x = top_x + int(200 * rect_scale) + 1
    bottom_y = top_y + int(240 * rect_scale) + 1

    if bottom_x > image_top_x + width:
        top_x = image_top_x + width - int(200 * rect_scale)
        bottom_x = image_top_x + width

    if bottom_y > image_top_y + height:
        top_y = image_top_y + height - int(240 * rect_scale)
        bottom_y = image_top_y + height

    cv2.rectangle(image, (top_x, top_y),
                          (bottom_x, bottom_y), (0, 255, 0), 1)
    cv2.imshow('Crop Tool', image)

    global make_crop
    if make_crop:
        crop = image[top_y:bottom_y, top_x:bottom_x]
        crop = cv2.resize(crop, (200, 240))
        counter = 0
        extension = ''

        while os.path.isfile('dudes_cropped_unclean/' + filenames[index].split('.')[0] + extension + '.png'):
            extension = '_' + str(counter)
            counter += 1

        cv2.imwrite('dudes_cropped_unclean/' + filenames[index].split('.')[0] + extension + '.png', crop)
        make_crop = False

    key_code = cv2.waitKey(1)

    return key_code

while True and key_code != ord('q'):
    if key_code == ord('a'):
        index -= 1
        key_code = show_image(index)
    elif key_code == ord('d'):
        index += 1
        key_code = show_image(index)
    elif key_code == ord('w'):
        os.remove('dudes_undetected/' + filenames[index])
        filenames.pop(index)
        key_code = 0
    else:
        key_code = show_image(index)

