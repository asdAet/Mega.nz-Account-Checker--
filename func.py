import os
import colorama
from colorama import init, Fore, Back, Style
colorama.init(autoreset = True)

GREEN = '\033[92m'
RESET = '\033[0m'

def hit():
    string = ("[   HIT   ] ")
    return string

def fail():
    string = (Fore.RED + "[   FAIL  ] ")
    return string

def custom():
    string = (Fore.YELLOW + "[  CUSTOM ] ")
    return string

def error():
    string = (Fore.MAGENTA + "[  ERROR  ] ")
    return string


def logo():
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'

    print(f"""{CYAN}
  ____   _                     _             
 / ___| | |__     ___    ___  | | __  ___   _ __ 
| |     | |_ \   / _ \  / __| | |/ / / _ \ | '__|
| |___  | | | | |  __/ | (__  |   < |  __/ | |   
 \____| |_| |_|  \___|  \___| |_|\_\ \___| |_| 
 
  {MAGENTA}           -Mega.nz Account Checker
        -Coded By And Discord - 23XT and Methodllo {RESET} 
        """)
    
