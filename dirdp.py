import urllib3
import os
import sys
import time
import random
import threading


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

max_threads = 0
threads = 0
event = threading.Event()


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
        print("\n" + ERROR + "Usage: python3 dirdp.py url worlist threads\n\nif you want max threads, set 0 to threads arg")
        sys.exit()


def check():
    if "://" not in sys.argv[1]:
        print("\n" + ERROR + "Invalid url")
        sys.exit()
    
    if "." not in sys.argv[1]:
        print("\n" + ERROR + "Invalid domain")
        sys.exit()
    
    if sys.argv[1].endswith("/") == False:
        sys.argv[1] += "/"
    
    if os.path.isfile(sys.argv[2]) == False:
        print("\n" + ERROR + "Can't find wordlist " + sys.argv[2])
        sys.exit()


def init():
    global max_threads

    clean()
    banner()
    checkArgs()
    check()

    max_threads = int(sys.argv[3])


def fuzzUrl():
    global threads, max_threads

    url = sys.argv[1]
    wordlist = open(sys.argv[2], "rt")

    word = wordlist.readline()

    start = time.time()

    http = urllib3.PoolManager()

    while word != "":

        if word.startswith("#") == False and word != "\n":

            threading.Thread(target=find, args=(word, url, http,)).start()
            
            threads += 1

            if threads == max_threads:
                event.wait()
                event.clear()

        word = wordlist.readline()
    
    while threads != 0:
        pass

    print("\n\n" + INFO + "search time: " + str(int(time.time() - start)) + " sec")


def find(word, url, http: urllib3.PoolManager):
    global threads

    s = (url + word).replace("\n", "")

    try:
        code = http.request('GET', s).status

        if code < 400:

            space = " " * (20-len(word))

            print(OK + (word + space + "(" + s + ")").replace("\n", ""))     
        
    except:
        pass

    threads -= 1
    event.set()


if __name__ == "__main__":
    init()
    fuzzUrl()