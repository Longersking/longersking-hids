import requests
import threading
import time

# 设置目标URL
url = "https://www.xiaodu0.com"

# 请求的数量
num_requests = 1000

# 并发线程数
num_threads = 10

# 定义每个线程要执行的请求函数
def send_requests():
    for _ in range(num_requests // num_threads):
        try:
            response = requests.get(url)
            print(f"Response Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# 创建线程并启动
threads = []
start_time = time.time()

for i in range(num_threads):
    thread = threading.Thread(target=send_requests)
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")
