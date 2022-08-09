import pynput


def lock(aims, mouse, x, y):
    mouse_pos_x, mouse_pos_y = mouse.position
    dist_list = []
    for det in aims:
        _, x_c, y_c, _, _ = det
        dist = (x * float(x_c) - mouse_pos_x) ** 2 + (y * float(y_c) - mouse_pos_y) ** 2
        dist_list.append(dist)

    det = aims[dist_list.index(min(dist_list))]

    tag, x_center, y_center, width, height = det
    tag = int(tag)
    x_center, width = x * float(x_center), x * float(width)
    y_center, height = y * float(y_center), y * float(height)
    if tag == 2:
        mouse.position = (x_center, y_center)
    elif tag == 3:
        mouse.position = (x_center, y_center - 1 / 6 * height)


import csv
import time


def recoil_control():
    f = csv.reader(open('./ammo_path/ak47.csv', encoding='utf-8'))
    ak_recoil = []
    for i in f:
        ak_recoil.append(i)
    ak_recoil[0][0] = '0'
    ak_recoil = [[float(i) for i in x] for x in ak_recoil]
    print(ak_recoil)
    k = -1
    mouse = pynput.mouse.Controller()
    flag = 0
    recoil_mode = False # mouse.button.x1
    with pynput.mouse.Events() as events:
        for event in events:
            if isinstance(event, pynput.mouse.Events.Click):
                if event.button == event.button.left:
                    if event.pressed:
                        flag = 1
                    else:
                        flag = 0
                if event.button == event.button.x1 and event.pressed:
                    recoil_mode = not recoil_mode
                    print('recoil mode', 'on' if recoil_mode else 'off')

            if flag and recoil_mode:
                i = 0
                a = next(events)
                while True:
                    mouse.move(ak_recoil[i][0] * k, ak_recoil[i][1] * k)
                    i += 1
                    if i == 30:
                        break
                    if a is not None and isinstance(a, pynput.mouse.Events.Click) and a.button == a.button.left and not a.pressed:
                        break
                    a = next(events)
                    while a is not None and not isinstance(a, pynput.mouse.Events.Click):
                        a = next(events)
                    time.sleep(ak_recoil[i][2] / 1000)
                flag = 0
