import time
import random
from queue import Queue, PriorityQueue, LifoQueue
from threading import Thread, Event

from request import Request

class WebServiceSimulator:
    def __init__(self, arrival_rate, processing_time_func, deadline, queue_type="FIFO", time_slice=0.1):
        self.arrival_rate = arrival_rate
        self.processing_time_func = processing_time_func
        self.deadline = deadline
        self.queue_type = queue_type
        self.time_slice = time_slice
        self.requests = self._init_queue(queue_type)
        self.stop_event = Event()
        self.processed_requests = []

    def _init_queue(self, queue_type):
        if queue_type == "FIFO":
            return Queue()
        elif queue_type == "SJF":  # Shortest Job First
            return PriorityQueue()
        elif queue_type == "EDF":  # Earliest Deadline First
            return PriorityQueue()
        elif queue_type == "LIFO":  # Last In First Out
            return LifoQueue()
        elif queue_type == "RoundRobin":
            return Queue()
        else:
            raise ValueError("Unsupported queue type")

    def generate_request(self):
        while not self.stop_event.is_set():
            time.sleep(random.expovariate(self.arrival_rate))
            arrival_time = time.time()
            processing_time = self.processing_time_func()
            request = Request(arrival_time, processing_time, self.deadline)
            if self.queue_type == "FIFO" or self.queue_type == "LIFO" or self.queue_type == "RoundRobin":
                self.requests.put(request)
            elif self.queue_type == "SJF":
                self.requests.put((processing_time, request))
            elif self.queue_type == "EDF":
                self.requests.put((request.deadline, request))

    def process_requests(self):
        if self.queue_type == "RoundRobin":
            while not self.stop_event.is_set():
                if not self.requests.empty():
                    request = self.requests.get()
                    start_time = time.time()
                    remaining_time = request.processing_time
                    while remaining_time > 0 and time.time() - start_time < self.time_slice:
                        time.sleep(min(self.time_slice, remaining_time))
                        remaining_time -= self.time_slice
                    if time.time() - request.arrival_time <= request.deadline:
                        request.completion_status = "successful"
                    else:
                        request.completion_status = "failed"
                    self.processed_requests.append(request)
                    if remaining_time > 0:
                        self.requests.put(request)
        else:
            while not self.stop_event.is_set():
                # print('here')
                if not self.requests.empty():
                    if self.queue_type == "FIFO" or self.queue_type == "LIFO":
                        request = self.requests.get()
                    else:
                        _, request = self.requests.get()
                    start_time = time.time()
                    if start_time + request.processing_time <= request.arrival_time + request.deadline:
                        time.sleep(request.processing_time)  # Simulate processing
                        request.completion_status = "successful"
                    else:
                        time.sleep(request.processing_time)  # Simulate processing
                        request.completion_status = "failed"
                    self.processed_requests.append(request)

    def run(self, duration):
        generator_thread = Thread(target=self.generate_request)
        processor_thread = Thread(target=self.process_requests)
        generator_thread.start()
        processor_thread.start()
        time.sleep(duration)
        self.stop_event.set()
        generator_thread.join()
        processor_thread.join()

    def get_results(self):
        return self.processed_requests