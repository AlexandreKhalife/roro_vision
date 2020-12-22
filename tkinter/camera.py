import cv2
import time


def input_resolution(cam, width, height):
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    return cam


def windows(name):
    cv2.namedWindow(name, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(name, 1000, 800)
    return name


cam = cv2.VideoCapture(0)
cam = input_resolution(cam, 1920, 1080)

frame_nb = 0
frame_max = 10
win = windows('test')

while True:
    if frame_nb == 0:
        now = time.time()
    # read frames from stream
    ret, frame = cam.read()
    frame = cv2.resize(frame, (1312, 738))
    # Show output window
    cv2.imshow(win, frame)
    # Calculate fps
    frame_nb += 1
    if frame_nb == frame_max:
        frame_nb = 0
        duration = (time.time() - now)
        fps = frame_max / duration
        print("fps = ", fps)
    # check for 'q' key if pressed
    key = cv2.waitKey(1)
    if key & 0xFF == 27:
        cam.release()
        cv2.destroyAllWindows()
        quit()
