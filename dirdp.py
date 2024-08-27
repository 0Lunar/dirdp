import urllib3
import os
import sys
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

GREEN = "\x1b[1;32m"
RED = "\x1b[1;31m"
YELLOW = "\x1b[1;33m"
BLUE = "\x1b[1;34m"
MAGENTA = "\x1b[1;35m"
CYAN = "\x1b[1;36m"
RESET = "\x1b[0m"

OK = "\x1b[1;32m[\x1b[0m+\x1b[1;32m] "
ERROR = "\x1b[1;31m[\x1b[0m!\x1b[1;31m] "
WARNING = "\x1b[1;33m[\x1b[0m-\x1b[1;33m] "
INFO = "\x1b[1;34m[\x1b[0mI\x1b[1;34m] "

banner_ascii = """
   ccee88oo                    
  C8O8O8Q8PoOb o8oo            
 dOB69QO8PdUOpugoO9bD                 _ _         __
CgggbU8OU qOp qOdoUOdcb          ____/ (_)_______/ /___
    6OuU  /p u gcoUodpP        / __  / / ___/ __  / __ \\
      \\\//  /douUP            / /_/ / / /  / /_/ / /_/ /
        \\\////                \\__,_/_/_/   \\__,_/ .___/ 
         |||/\                                 /__/    
         |||\/                 
         |||||                 
   .....//||||\....            
"""

def clean():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def banner():
    colors = [GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN]
    print(random.choice(colors) + banner_ascii + RESET)

def checkArgs():
    if len(sys.argv) != 4:
        print("\n" + ERROR + "Usage: python3 dirdp.py url wordlist threads\n\nif you want max threads, set 0 to threads arg")
        sys.exit()

def check():
    if "://" not in sys.argv[1]:
        print("\n" + ERROR + "Invalid url")
        sys.exit()
    
    if "." not in sys.argv[1]:
        print("\n" + ERROR + "Invalid domain")
        sys.exit()
    
    if not sys.argv[1].endswith("/"):
        sys.argv[1] += "/"
    
    if not os.path.isfile(sys.argv[2]):
        print("\n" + ERROR + "Can't find wordlist " + sys.argv[2])
        sys.exit()

def init():
    clean()
    banner()
    checkArgs()
    check()

def fetch_url(word, url, http):
    s = (url + word).replace("\n", "")
    try:
        response = http.request('GET', s)
        if response.status < 400:
            space = " " * (20 - len(word))
            print(OK + (word + space + "(" + s + ")").replace("\n", ""))
    except urllib3.exceptions.HTTPError as e:
        pass
    except Exception as e:
        print(ERROR + f"An error occurred: {e}")

def fuzzUrl():
    url = sys.argv[1]
    max_threads = int(sys.argv[3]) or None

    start = time.time()
    http = urllib3.PoolManager()

    with open(sys.argv[2], "rt") as wordlist, ThreadPoolExecutor(max_workers=max_threads) as executor:
        for word in wordlist:
            if not word.startswith("#") and word.strip():
                executor.submit(fetch_url, word.strip(), url, http) 

    print("\n\n" + INFO + "search time: " + str(int(time.time() - start)) + " sec")

if __name__ == "__main__":
    init()
    fuzzUrl()
