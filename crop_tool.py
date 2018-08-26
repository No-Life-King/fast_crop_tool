import os
import cv2
import ctypes
import tkinter as tk

from tkinter import filedialog, messagebox


# create the window for parameter selection
window = tk.Tk()
#window.minsize(450, 200)
window.title('Fast Crop Tool')

# source selection
src_dir = tk.StringVar()
tk.Label(window, text="Choose Source Folder:", justify=tk.RIGHT).grid(row=1, column=1)
src_textbox = tk.Entry(window, textvariable=src_dir, width=40)
src_textbox.grid(row=1, column=2)

# open a file picker and set the chosen path in the source text field
def set_src():
    src_textbox.delete(0, tk.END)
    src_textbox.insert(0, filedialog.askdirectory())

src_button = tk.Button(window, text='  ...  ', command=set_src).grid(row=1, column=3)

# destination selection
dest_dir = tk.StringVar()
tk.Label(window, text="Choose Destination Folder:", justify=tk.RIGHT).grid(row=2, column=1)
dest_textbox = tk.Entry(window, textvariable=dest_dir, width=40)
dest_textbox.grid(row=2, column=2)

# open a file picker and set the chosen path in the destination text field
def set_dest():
    dest_textbox.delete(0, tk.END)
    dest_textbox.insert(0, filedialog.askdirectory())

dest_button = tk.Button(window, text='  ...  ', command=set_dest).grid(row=2, column=3)

# width selection
crop_width = tk.IntVar()
tk.Label(window, text="Crop Width:", justify=tk.RIGHT).grid(row=3, column=1)
width_textbox = tk.Entry(window, textvariable=crop_width, width=5)
width_textbox.delete(0, tk.END)
width_textbox.insert(tk.END, '200')
width_textbox.grid(row=3, column=2)


# height selection
crop_height = tk.IntVar()
tk.Label(window, text="Crop Height:", justify=tk.RIGHT).grid(row=4, column=1)
height_textbox = tk.Entry(window, textvariable=crop_height, width=5)
height_textbox.delete(0, tk.END)
height_textbox.insert(tk.END, '240')
height_textbox.grid(row=4, column=2)

def validate():
    """
    Checks for any errors in the form before proceeding.
    """
    if src_dir.get() == '':
        messagebox.showerror('Error', 'You must set a source directory.')
    elif dest_dir.get() == '':
        messagebox.showerror('Error', 'You must set a destination directory.')
    elif src_dir.get() == dest_dir.get():
        messagebox.showerror('Error', 'Your source and destination directories must be different.')
    elif not os.path.isdir(src_dir.get()):
        messagebox.showerror('Error', 'Please choose a valid source path.')
    elif not os.path.isdir(dest_dir.get()):
        messagebox.showerror('Error', 'Please choose a valid destination path.')
    elif crop_width.get() <= 0 or crop_height.get() <= 0:
        messagebox.showerror('Error', 'You must choose valid crop dimensions. Crop width and height must be at least 1x1.')
    else:
        # close this window and pass on the parameters to the crop tool
        window.destroy()

# instructions and start button
directions = 'Directions:\nChoose source and destination folders. Images in the source folder will be displayed one-by-one ' \
             'so that you can crop them. The resulting cropped images will be save to the destination folder.'
tk.Label(window, text=directions, wraplength=300, padx=5, pady=5, justify=tk.LEFT).grid(row=5, column=1)
tk.Button(window, text='Start Cropping', command=validate).grid(row=5, column=2)

# run the GUI
tk.mainloop()

src_dir = src_dir.get() + '/'
dest_dir = dest_dir.get() + '/'
crop_width = int(crop_width.get())
crop_height = int(crop_height.get())

mouse_x = 0
mouse_y = 0
rect_scale = 1
make_crop = False
button_down = False

# get user's screen size
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# handle mouse events
def mouse_handler(event, x, y, flags, param):
    global mouse_x, mouse_y, rect_scale, make_crop, button_down

    # if the mouse moves, set its new coordinates so that the rectangle can move
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y = y

    # increase/decrease the size of the rectangle upon scroll
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0 and rect_scale > 1:
            rect_scale -= .2
        elif flags < 0:
            rect_scale += .2

    # set a flag that tells the script to draw a blue rectangle when the left mouse button is held down
    elif event == cv2.EVENT_LBUTTONDOWN:
        button_down = True

    # on release of the left mouse button, make the crop and start drawing a green rectangle again
    elif event == cv2.EVENT_LBUTTONUP:
        make_crop = True
        button_down = False


# load images from the source directory
filenames = os.listdir(src_dir)
image_names = []

for filename in filenames:
    file_extension = filename.split('.')[-1].lower()
    if file_extension == 'bmp' or file_extension == 'dib' or file_extension == 'jpeg' or file_extension == 'jpg' or \
        file_extension == 'jpe' or file_extension == 'jp2' or file_extension == 'png' or file_extension == 'webp' or \
        file_extension == 'pbm' or file_extension == 'pgm' or file_extension == 'ppm' or file_extension == 'sr' or \
        file_extension == 'ras' or file_extension == 'tiff' or file_extension == 'tif': image_names.append(filename)

index = 0
key_code = 0
cv2.namedWindow('Fast Crop Tool')
cv2.setMouseCallback('Fast Crop Tool', mouse_handler)

def show_image(index):
    """
    This is the function that handles rendering each image in a window. The image is redrawn every time the mouse is moved.
    :param index: The index of the image in the list of image names.
    :return: A key code if a key is pressed.
    """

    # open sesame
    image = cv2.imread(src_dir + image_names[index])

    # set the window size
    max_image_width = screen_width
    max_image_height = screen_height - 60

    # get image height and width
    height, width = image.shape[:2]

    # resize the image if it is too large to fit on the screen
    if height > max_image_height:
        image = cv2.resize(image, None, 0, max_image_height/height, max_image_height/height)

    if width > max_image_width:
        image = cv2.resize(image, None, 0, max_image_width/width, max_image_width/width)

    height, width = image.shape[:2]

    # pad the image out to the max size
    image = cv2.copyMakeBorder(image, int((max_image_height - height)/2),
                               int((max_image_height - height)/2),
                               int((max_image_width - width)/2),
                               int((max_image_width - width)/2),
                               cv2.BORDER_CONSTANT, value=(153,136,119))

    image_top_x = int((max_image_width-width)/2)
    image_top_y = int((max_image_height-height)/2)

    # set the top (x, y) coordinate of the rectangle
    top_x = mouse_x - int(crop_width / 2 * rect_scale) - 1
    top_y = mouse_y - int(crop_height / 2 * rect_scale) - 1

    top_x = image_top_x if top_x < image_top_x else top_x
    top_y = image_top_y if top_y < image_top_y else top_y

    # set the bottom (x, y) coordinate of the rectangle
    bottom_x = top_x + int(crop_width * rect_scale) + 2
    bottom_y = top_y + int(crop_height * rect_scale) + 2

    if bottom_x > image_top_x + width:
        top_x = image_top_x + width - int(crop_width * rect_scale)
        bottom_x = image_top_x + width

    if bottom_y > image_top_y + height:
        top_y = image_top_y + height - int(crop_height * rect_scale)
        bottom_y = image_top_y + height

    # color of the rectangle is green
    rect_color = (0, 255, 0)

    # if the left mouse button is held down, change the color of the rectangle to be blue
    if button_down:
        rect_color = (255, 0, 0)

    # draw the rectangle
    cv2.rectangle(image, (top_x, top_y),
                          (bottom_x, bottom_y), rect_color, 1)

    # draw the image in the window
    cv2.imshow('Fast Crop Tool', image)

    global make_crop

    # take a crop when the left mouse button is released
    if make_crop:
        crop = image[top_y+1:bottom_y, top_x+1:bottom_x]
        crop = cv2.resize(crop, (crop_width, crop_height))
        counter = 0
        extension = ''

        # if a file already exists with the current filename, keep looping through until a unique name is found
        while os.path.isfile(dest_dir + image_names[index].split('.')[0] + extension + '.png'):
            extension = '_' + str(counter)
            counter += 1

        # write the image to a file
        cv2.imwrite(dest_dir + image_names[index].split('.')[0] + extension + '.png', crop)
        make_crop = False

    # get the key code of any pressed key
    key_code = cv2.waitKey(1)

    return key_code

# keep displaying images until the 'q' key is pressed or until there are no more images in the source folder
while key_code != ord('q') and len(image_names) > 0:

    # go back to the previous image when the 'a' key is pressed
    if key_code == ord('a'):
        index -= 1
        key_code = show_image(index)

    # advance to the next image if the 'd' key is pressed
    elif key_code == ord('d'):
        index += 1
        key_code = show_image(index)

    # delete the current image and advance to the next image
    elif key_code == ord('w'):
        os.remove(src_dir + image_names[index])
        image_names.pop(index)
        key_code = 0

    # keep showing the same image
    else:
        key_code = show_image(index)

if len(image_names) == 0:
    print('Source folder contains no image files.')