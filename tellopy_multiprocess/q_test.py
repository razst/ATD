import queue
import threading
import time

def do_stuff(q):
  name = threading.currentThread().getName()
  while True:
    n = q.get()
    time.sleep(0.2)
    print (name,n)
    time.sleep(0.2)
    q.task_done()

q = queue.Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
  worker = threading.Thread(name = "origThread-"+str(i), target=do_stuff, args=(q,))
  worker.setDaemon(True)
  worker.start()

for x in range(100):
  q.put(x)

q.join()