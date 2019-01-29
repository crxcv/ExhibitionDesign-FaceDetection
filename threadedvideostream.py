import cv2
from threading import Thread


class ThreadedVideoStream:
    def __init__(self, path, frame_width=None, frame_height=None, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not

        self.videostream = cv2.VideoCapture(path)

        if frame_width is not None:
            self.videostream.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            self.videostream.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        (self.grabbed, self.frame) = self.videostream.read()
        self.stopped = False

        # initialize the queue used to store frames read from
        # the video file
        # self.Q = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        print("starting thread")
        t.daemon = True
        t.start()
        return self

    def update(self):
        # print("videostream update")
        # if not self.Q.full():
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.videostream.read()
            # if not ret:
            #     self.stop()
            #     return
            # self.Q.put(frame)

    def read(self):
        # print("videostream read. stopped {}".format(self.stopped))
        return self.frame

    # def more(self):
    #     # return True if there are still frames in the queue
    #     return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.videostream.release()
