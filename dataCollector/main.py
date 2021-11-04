import inspect
import os
import sys

from Controller import Controller

if __name__ == "__main__":
    print("System started...")
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    controller = Controller()
    controller.start()
