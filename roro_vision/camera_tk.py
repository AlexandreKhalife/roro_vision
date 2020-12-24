import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk


class App:
    def __init__(self, win, win_title, video_source=0, res=(800, 600)):
        # Set main grid propreties
        self.win = win
        self.win.geometry("1500x800")
        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(0, weight=1)
        self.video_source = video_source
        self.res = res

        # Set frist sub grid propreties (video)
        self.frame_vid = tk.Canvas(self.win)
        self.frame_vid.grid(row=0, column=0, sticky='EWNS')
        self.frame_vid.rowconfigure(0, weight=1)
        self.frame_vid.columnconfigure(0, weight=1)

        # Set second sub grid propreties (btn)
        self.frame_ctrl = tk.Frame(self.win)
        self.frame_ctrl.grid(row=1, column=0)

        # Create btn on second grid
        self.btn_zoom = tk.Scale(
                                 self.frame_ctrl,
                                 orient='horizontal',
                                 length=500,
                                 width=50,
                                 from_=1,
                                 to=10,
                                 resolution=1
                                 )
        self.btn_zoom.set(1)
        self.btn_zoom.grid(row=0, column=2,  padx=(10), pady=10)

        # open video source
        self.vid = MyVideoCapture(self.video_source)

        # called every delay milliseconds
        self.delay = 20

        # get the vid canvas size to resize the video stream and fit canvas
        def update_event(event):
            self.res = (event.width, event.height)
        self.frame_vid.bind('<Configure>', update_event)

        self.update()
        self.win.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            frame = self.scale_video(frame)
            frame = self.vid_resize(frame)
            self.photo = PIL.ImageTk.PhotoImage(
                         image=PIL.Image.fromarray(frame))
            self.frame_vid.create_image(self.res[0]/2,
                                        self.res[1]/2,
                                        image=self.photo)
        self.frame_vid.after(self.delay, self.update)

    def scale_video(self, frame):
        transco = {1: 1,
                   2: 0.9,
                   3: 0.8,
                   4: 0.7,
                   5: 0.6,
                   6: 0.5,
                   7: 0.4,
                   8: 0.3,
                   9: 0.2,
                   10: 0.1}
        select = self.btn_zoom.get()
        scale = transco[select]
        # calcul de la plage à afficher
        centerX, centerY = int(self.vid.height/2), int(self.vid.width/2)
        radiusX, radiusY = int(centerX*scale), int(centerY*scale)
        minX, maxX = centerX - radiusX, centerX + radiusX
        minY, maxY = centerY - radiusY, centerY + radiusY
        cropped = frame[minX:maxX, minY:maxY]
        return cropped

    def vid_resize(self, frame):
        ratio_width = (self.vid.width/self.res[0])
        ratio_height = (self.vid.height/self.res[1])
        max_ratio = max(ratio_height, ratio_width)
        x = int(self.vid.width / max_ratio)
        y = int(self.vid.height / max_ratio)
        frame = cv2.resize(frame, (x, y))
        return frame


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.vid.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


App(tk.Tk(), "Tkinter and OpenCV")
