# live_session.py
import cv2
import time
from datetime import datetime

class LiveSession:
    def __init__(self):
        self.active = False
        self.start_time = None
        self.video_writer = None
        self.output_filename = None
        self.latest_frame = None  # Store the latest frame for streaming

    def start(self, frame):
        self.active = True
        self.start_time = time.time()
        height, width = frame.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_filename = f"videos/live_{timestamp}.avi"
        self.video_writer = cv2.VideoWriter(self.output_filename, fourcc, 10.0, (width, height))
        print(f"Started new live session, saving video to {self.output_filename}")

    def update(self, frame):
        if not self.active:
            self.start(frame)
        self.video_writer.write(frame)
        self.latest_frame = frame  # Save the latest frame for streaming
        if time.time() - self.start_time >= 120:
            self.end()

    def end(self):
        if self.active:
            self.video_writer.release()
            print(f"Live session ended. Video saved as {self.output_filename}")
            self.active = False
            self.start_time = None
            self.video_writer = None
            self.output_filename = None
            self.latest_frame = None

    def get_latest_frame(self):
        return self.latest_frame
