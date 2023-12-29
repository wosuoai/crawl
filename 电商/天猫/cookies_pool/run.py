import sys
from schedule import Scheduler
import multiprocessing

if __name__ == "__main__":
    s1=Scheduler()
    s1.run("tmall")