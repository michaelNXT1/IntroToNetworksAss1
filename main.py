import random

from webServiceSimulator import WebServiceSimulator


# Example of usage:
def example_processing_time_func():
    return random.uniform(0.1, 0.5)


queue_types = [
    "FIFO",
    "SJF",
    # "EDF",
    "LIFO",
    "RoundRobin"]
results_dict = {}

for queue_type in queue_types:
    simulator = WebServiceSimulator(arrival_rate=10, processing_time_func=example_processing_time_func, deadline=2,
                                    queue_type=queue_type)
    simulator.run(duration=10)
    results = simulator.get_results()
    successful_requests = len([r for r in results if r.completion_status == "successful"])
    failed_requests = len([r for r in results if r.completion_status == "failed"])
    results_dict[queue_type] = (successful_requests, failed_requests)

for queue_type, results in results_dict.items():
    successful, failed = results
    print(f"Queue type: {queue_type}")
    print(f"Successful requests: {successful}")
    print(f"Failed requests: {failed}\n")
