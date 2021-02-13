import threading
from multiprocessing import Process

def func(args):
    while True:
        x = 100 * 45 / 5 + 90
        # print("test")


p = Process(name = "finalThread",target=func, args=(1,))
p.start()

# t = threading.Thread(target=func, args=(1,))
# t.daemon = True
# t.start()

# t2 = threading.Thread(target=func, args=(1,))
# t2.daemon = True
# t2.start()

func(1)