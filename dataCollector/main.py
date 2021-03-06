import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Controller import Controller
from keys import keys
from logger import err_log

if __name__ == "__main__":
    print("System started...")
    controller = Controller(keys, err_log)
    controller.start()
