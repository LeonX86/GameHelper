from grabscreen import grab_screen
import pynput
import cv2
import os

x, y = (1920, 1080)

img = grab_screen(region=(0, 0, x, y))

num = 1


dir_name = 'dir'
if not os.path.exists('./dir'):
    os.mkdir('./' + dir_name)


def on_press(key):
    global num
    if key == pynput.keyboard.KeyCode(char='a'):
        img = grab_screen(region=(0, 0, x, y))
        cv2.imwrite('./' + dir_name + '/' + str(num) + '.jpg', img)
        num += 1


def on_release(key):
    pass


listener = pynput.keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    pass