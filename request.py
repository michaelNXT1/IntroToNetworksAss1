class Request:
    def __init__(self, arrival_time, processing_time, deadline):
        self.arrival_time = arrival_time
        self.processing_time = processing_time
        self.deadline = deadline
        self.completion_status = None  # None, "successful", "failed"