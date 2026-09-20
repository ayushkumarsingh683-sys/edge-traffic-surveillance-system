import cv2
import threading
import time

class ThreadedVideoStream:
    """Non-blocking threaded video frame reader for 40+ FPS throughput."""
    def __init__(self, src, queue_size=2):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, queue_size)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.lock = threading.Lock()
        
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while not self.stopped:
            if not self.stream.isOpened():
                break
            grabbed, frame = self.stream.read()
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame
            if not grabbed:
                self.stopped = True
                break
            time.sleep(0.005)

    def read(self):
        with self.lock:
            return self.grabbed, self.frame.copy() if self.frame is not None else None

    def release(self):
        self.stopped = True
        self.thread.join(timeout=1.0)
        self.stream.release()
