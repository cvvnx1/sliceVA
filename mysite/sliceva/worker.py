from threading import Thread, Event, local
import Queue

class Worker(Thread):
    def __init__(self, queue, event_dict, work, result):
        Thread.__init__(self)
        self.queue = queue
        self.event_dict = event_dict
        self.work = work
        self.result = result

    def run(self):
        while True:
            try:
                x, hostname, username, password = self.queue.get(True, 1)
            except Queue.Empty:
                break
            self.event_dict[x] = Event()
            self.event_dict[x].clear()
            self.result[hostname] = self.work.run(hostname=hostname, username=username, password=password)
            self.event_dict[x].set()

def Assignment(work, username, password, hosts, thread_num):
    """
    Input work class & target devices list
    Return dict for all thread result
    """
    Q = Queue.Queue()
    threads = []
    event_dict = {}
    result = {}
    x = 0
    for host in hosts:
        Q.put([x, host, username, password])
        x += 1
    for i in range(0, thread_num):
        threads.append(Worker(Q, event_dict, work, result))
        threads[i].setDaemon(True)
        threads[i].start()
    for thread in threads:
        thread.join()
    return result

