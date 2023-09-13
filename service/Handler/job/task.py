
import time

class TaskState:

    def __init__(self):
        self.counter = 0

    def background_work(self):
        while True:
            self.counter += 1
            time.sleep(1)
            if self.counter > 10:
                break

    def get_state(self):
        return self.counter
