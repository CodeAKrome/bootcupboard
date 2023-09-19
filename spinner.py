import threading
import time

class Spinner:
    def __init__(self):
        self.spinner = threading.Thread(target=self._spin)
        self.spinner.daemon = True
        self.spinning = False

    def start(self):
        self.spinning = True
        self.spinner.start()

    def stop(self):
        self.spinning = False
        self.spinner.join()

    def _spin(self):
        while self.spinning:
            print('\rLoading...', end='')
            time.sleep(0.1)
            print('\rLoading..', end='')
            time.sleep(0.1)
            print('\rLoading...', end='')
            time.sleep(0.1)
            print('\r', end='')

if __name__ == '__main__':
    spinner = Spinner()

    spinner.start()

    # Do some work here
    time.sleep(5)
    spinner.stop()
