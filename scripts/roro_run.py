import argparse

from roro_vision.lib import App
from roro_vision.camera import test_open_cam
from roro_vision.camera import get_default_cam
from roro_vision.camera import video_capture

if __name__ == '__main__':
    usage = '%(prog)s'
    description = 'Roro Reading System'
    parser = argparse.ArgumentParser(description=description, usage=usage)
    parser.add_argument("-tk", "--use_tk", action="store_true",
                        help="Call tk version", default=False)
    args = parser.parse_args()
    print('=> ', args)

    if args.use_tk:
        App("Tkinter and OpenCV")
    else:
        print('=> no Tk, call camera.py')
        connected_cam = test_open_cam()
        cam_no = get_default_cam(connected_cam)
        video_capture(connected_cam, cam_no)
