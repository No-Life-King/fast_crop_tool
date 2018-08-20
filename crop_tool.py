import os
import cv2
import ctypes
import tkinter as tk

from tkinter import filedialog


# create the window for parameter selection
window = tk.Tk()
#window.minsize(450, 200)
window.title('Fast Crop Tool')

# source selection
src_dir = tk.StringVar()
tk.Label(window, text="Choose Source Folder:", justify=tk.LEFT).grid(row=1, column=1)
src_textbox = tk.Entry(window, textvariable=src_dir, width=40)
src_textbox.grid(row=1, column=2)

# destination selection
dest_dir = tk.StringVar()
tk.Label(window, text="Choose Destination Folder:").grid(row=2, column=1)
dest_textbox = tk.Entry(window, textvariable=dest_dir, width=40)
dest_textbox.grid(row=2, column=2)

# width selection
tk.Label(window, text="Width:").grid(row=3, column=1)
width_textbox = tk.Entry(window, textvariable=dest_dir, width=5)
width_textbox.grid(row=3, column=2)

# height selection
tk.Label(window, text="Height:").grid(row=4, column=1)
height_textbox = tk.Entry(window, textvariable=dest_dir, width=5)
height_textbox.grid(row=4, column=2)

# instructions and start button
directions = 'Directions:\nChoose source and destination folders. Images in the source folder will be displayed one-by-one ' \
             'so that you can crop them. The resulting cropped images will be save to the destination folder.'
tk.Label(window, text=directions, wraplength=300, padx=5, pady=5, justify=tk.LEFT).grid(row=5, column=1)
tk.Button(window, text='Start Cropping', command=window.destroy).grid(row=5, column=2)

def set_src():
    global src_dir, src_label
    #src_dir = filedialog.askdirectory()
    #src_label = tk.Label(window, text=src_dir).grid(row=2, column=1
    src_textbox.delete(0, tk.END)
    src_textbox.insert(0, filedialog.askdirectory())


def set_dest():
    global dest_dir, dest_label
    #dest_dir = filedialog.askdirectory()
    #dest_label = tk.Label(window, text=dest_dir).grid(row=4, column=1)
    dest_textbox.delete(0, tk.END)
    dest_textbox.insert(0, filedialog.askdirectory())


src_button = tk.Button(window, text='  ...  ', command=set_src).grid(row=1, column=3)
dest_button = tk.Button(window, text='  ...  ', command=set_dest).grid(row=2, column=3)

tk.mainloop()

src_dir = src_dir.get() + '/'
dest_dir = dest_dir.get() + '/'

mouse_x = 0
mouse_y = 0
rect_scale = 1
make_crop = False
button_down = False
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def mouse_rectangle(event, x, y, flags, param):
    global mouse_x, mouse_y, rect_scale, make_crop, button_down
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y = y
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0 and rect_scale > 1:
            rect_scale -= .2
        elif flags < 0:
            rect_scale += .2
    elif event == cv2.EVENT_LBUTTONDOWN:
        button_down = True
    elif event == cv2.EVENT_LBUTTONUP:
        make_crop = True
        button_down = False


filenames = os.listdir(src_dir)
index = 0
key_code = 0
cv2.namedWindow("Fast Crop Tool")
cv2.setMouseCallback('Fast Crop Tool', mouse_rectangle)


def show_image(index):
    image = cv2.imread(src_dir + filenames[index])

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

    color = (0, 255, 0)

    if button_down:
        color = (255, 0, 0)

    cv2.rectangle(image, (top_x, top_y),
                          (bottom_x, bottom_y), color, 1)
    cv2.imshow('Fast Crop Tool', image)

    global make_crop
    if make_crop:
        crop = image[top_y:bottom_y, top_x:bottom_x]
        crop = cv2.resize(crop, (200, 240))
        counter = 0
        extension = ''

        while os.path.isfile(dest_dir + filenames[index].split('.')[0] + extension + '.png'):
            extension = '_' + str(counter)
            counter += 1

        cv2.imwrite(dest_dir + filenames[index].split('.')[0] + extension + '.png', crop)
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
        os.remove(src_dir + filenames[index])
        filenames.pop(index)
        key_code = 0
    else:
        key_code = show_image(index)

