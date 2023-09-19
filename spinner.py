import threading
import time

class Spinner:
    def __init__(self):
        self.spinner = threading.Thread(target=self._spin)
        self.spinner.daemon = True
        self.spinning = False
        self.freezeframe = 3

    def start(self):
        self.spinning = True
        self.spinner.start()

    def stop(self):
        self.spinning = False
        self.spinner.join()

    def _spin(self):
        while self.spinning:
            print('\rAn old silent pond     ', end='')
            time.sleep(self.freezeframe)
            print('\rA frog jumps into the pond—', end='')
            time.sleep(self.freezeframe)
            print('\rSplash! Silence again.     ', end='')
            time.sleep(self.freezeframe)
            print('\r', end='')

if __name__ == '__main__':
    spinner = Spinner()

    spinner.start()

    # Do some work here
    time.sleep(5)
    spinner.stop()
