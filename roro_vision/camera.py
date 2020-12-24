# webcam zoom
# python3 / cv2

import cv2
import numpy as np
import pickle
import time


def test_open_cam():
    connected_cam = []
    for port in range(0, 10):
        try:
            cam = cv2.VideoCapture(port)
            if cam.isOpened():
                connected_cam.append(port)
        except:
            continue
    return(connected_cam)


def get_default_cam(connected_cam):
    try:
        default_port = pickle.load(open('config/config', "rb"))
        if default_port in connected_cam:
            cam_no = connected_cam.index(default_port)
        else:
            cam_no = 0
    except:
        cam_no = 0
        default_port = 'Null'
        pickle.dump(default_port, open('config/config', "wb+"))
    return cam_no


def save_default_cam(cam_no):
    pickle.dump(cam_no, open('config/config', "wb"))


def windows_propreties(windows):
    cv2.namedWindow(windows, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(windows, 1000, 608)
    return windows


def input_resolution(cam, width, height):
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    return cam


def move_detection(frame, previous_frame, change_limit):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(frame, previous_frame)
    diff = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
    h, w = diff.shape
    pixel_deviation = np.count_nonzero(diff == 255)
    change_ratio = (pixel_deviation/(h*w))
    if change_ratio > change_limit:
        change_statut = 1
    else:
        change_statut = 0
    previous_frame = frame.copy()
    return change_statut, previous_frame


def change_menu(key, menu, total_menu):
    if key == 83:  # right array
        menu += 1
        if menu > total_menu:
            menu = 1
    if key == 81:  # left array
        menu -= 1
        if menu == 0:
            menu = total_menu
    else:
        menu = menu
    return menu


def change_scale(key, scale):
    if key == 84:  # up array
        scale = min(scale + 0.1, 1)
    if key == 82:  # down array
        scale = max(scale - 0.1, 0.1)
    if key == 32:  # space key
        scale = 1
    return scale


def scale_video(frame, height, width, scale):
    # calcul de la plage à afficher
    centerX, centerY = int(height/2), int(width/2)
    radiusX, radiusY = int(centerX*scale), int(centerY*scale)
    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY
    cropped = frame[minX:maxX, minY:maxY]
    # affichage de l'image zoomée
    resized_cropped = cv2.resize(cropped, (width, height))
    return resized_cropped


def color_video(frame, menu, scale):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.adaptiveThreshold(
                frame, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                29, 15
                )
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    if menu == 2:
        frame[np.where((frame == [0, 0, 0]).all(axis=2))] = [254, 254, 254]
        frame[np.where((frame == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
    if menu == 3:
        frame[np.where((frame == [0, 0, 0]).all(axis=2))] = [0, 240, 240]
        frame[np.where((frame == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
    return frame


def video_capture(connected_cam, cam_no):
    total_cam = len(connected_cam)
    current_cam = cam_no
    windows = windows_propreties('Roro Software')
    # Loop for changing cam index
    while (cv2.getWindowProperty(windows, 0) >= 0):
        cam = cv2.VideoCapture(connected_cam[current_cam])
        cam = input_resolution(cam, 1920, 1080)
        # init values for menu and zoom
        scale = 1
        total_menu = 3
        menu = 1
        key = -1
        # parameters for mouvment detection
        current_frame = 0
        previous_frame = 0
        change_limit = 0.005
        change_statut = 1
        # paramters for fps calculation
        frame_nb = 0
        frame_max = 10
        # get, modify and display frame
        while cam.isOpened():
            # init fps calculation
            if frame_nb == 0:
                now = time.time()
            # capture video stream
            ret, frame = cam.read()
            # detect mouvment to improve threshold output
            change_statut, previous_frame = move_detection(frame,
                                                           previous_frame,
                                                           change_limit)
            # Action on current_frame
            height, width, channels = frame.shape
            frame = scale_video(frame, height, width, scale)
            if menu != 1:
                frame = color_video(frame, menu, scale)
            if change_statut == 1 or key != -1:
                current_frame = frame
            cv2.imshow(windows, current_frame)
            # Calculate fps
            frame_nb += 1
            if frame_nb == frame_max:
                frame_nb = 0
                duration = (time.time() - now)
                fps = frame_max / duration
                print("fps = ", fps)

            key = cv2.waitKey(1)

            # increment menu and scale variable
            menu = change_menu(key, menu, total_menu)
            scale = change_scale(key, scale)
            if key & 0xFF == ord('c'):
                cam.release()
                if current_cam == total_cam - 1:
                    current_cam = 0
                else:
                    current_cam += 1
            # quit if key & 0xFF == 27:  # escape
            if cv2.getWindowProperty(windows, cv2.WND_PROP_VISIBLE) < 1:
                save_default_cam(connected_cam[current_cam])
                cam.release()
                cv2.destroyAllWindows()
                quit()


if __name__ == '__main__':
    connected_cam = test_open_cam()
    cam_no = get_default_cam(connected_cam)
    video_capture(connected_cam, cam_no)
