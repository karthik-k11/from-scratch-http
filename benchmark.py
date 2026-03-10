import requests
import threading
import time

URL = "http://127.0.0.1:8080/hello"

TOTAL_REQUESTS = 100
THREADS = 10


def send_request():
    try:
        r = requests.get(URL)
        print(r.status_code)
    except Exception as e:
        print("Request failed:", e)


def worker():
    for _ in range(TOTAL_REQUESTS // THREADS):
        send_request()


start = time.time()

threads = []

for _ in range(THREADS):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end = time.time()

print("\nBenchmark complete")
print("Total requests:", TOTAL_REQUESTS)
print("Time taken:", round(end - start, 2), "seconds")
print("Requests/sec:", round(TOTAL_REQUESTS / (end - start), 2))