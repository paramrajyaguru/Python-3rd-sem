import threading
import queue
import time

# Buffer capacity
BUFFER_SIZE = 5

# Total producers and consumers
NUM_PRODUCERS = 4
NUM_CONSUMERS = 2

# Requests per producer
REQUESTS_PER_PRODUCER = 5

# Shared buffer
buffer = queue.Queue(maxsize=BUFFER_SIZE)

# Semaphores
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

# Mutex lock
mutex = threading.Lock()

# Counters
request_id = 1
produced = 0
consumed = 0

# Counter lock
counter_lock = threading.Lock()

# Total requests
TOTAL_REQUESTS = NUM_PRODUCERS * REQUESTS_PER_PRODUCER


# Producer function
def producer(producer_id):

    global request_id, produced

    for _ in range(REQUESTS_PER_PRODUCER):

        # Wait for empty space
        empty.acquire()

        with counter_lock:
            current_id = request_id
            request_id += 1

        # Create examination request
        request = {
            "id": current_id,
            "marks": 70 + (current_id * 3) % 31
        }

        # Critical section
        with mutex:
            buffer.put(request)

            with counter_lock:
                produced += 1

            print(
                f"Producer {producer_id}: "
                f"Enqueued Request ID: {request['id']} | "
                f"Marks: {request['marks']}"
            )

        # Signal available item
        full.release()

        time.sleep(0.1)


# Consumer function
def consumer(consumer_id):

    global consumed

    while True:

        # Wait for available item
        full.acquire()

        # Critical section
        with mutex:
            request = buffer.get()

            if request is None:
                print(f"Consumer {consumer_id}: Stopping.")
                empty.release()
                break

            with counter_lock:
                consumed += 1

            print(
                f"Consumer {consumer_id}: "
                f"Dequeued Request ID: {request['id']} | "
                f"Marks: {request['marks']}"
            )

        # Signal empty space
        empty.release()

        time.sleep(0.2)


# Main function
def main():

    print("\n==========================================")
    print(" UNIVERSITY EXAMINATION APPLICATION")
    print(" PRODUCER-CONSUMER USING SEMAPHORES")
    print("==========================================\n")

    producers = []
    consumers = []

    # Create consumer threads
    for i in range(NUM_CONSUMERS):
        t = threading.Thread(
            target=consumer,
            args=(i + 1,)
        )
        consumers.append(t)
        t.start()

    # Create producer threads
    for i in range(NUM_PRODUCERS):
        t = threading.Thread(
            target=producer,
            args=(i + 1,)
        )
        producers.append(t)
        t.start()

    # Wait for all producers
    for t in producers:
        t.join()

    # Send termination signals
    for _ in range(NUM_CONSUMERS):
        empty.acquire()

        with mutex:
            buffer.put(None)

        full.release()

    # Wait for all consumers
    for t in consumers:
        t.join()

    # Final output
    print("\n==========================================")
    print("              FINAL SUMMARY")
    print("==========================================")

    print("Total Producers      :", NUM_PRODUCERS)
    print("Total Consumers      :", NUM_CONSUMERS)
    print("Total Requests       :", TOTAL_REQUESTS)
    print("Total Produced       :", produced)
    print("Total Consumed       :", consumed)
    print("Remaining in Buffer  :", buffer.qsize())

    if produced == consumed == TOTAL_REQUESTS:
        print("\nStatus: All requests processed successfully.")
    else:
        print("\nStatus: Processing incomplete.")

    print("==========================================\n")


if __name__ == "__main__":
    main()
