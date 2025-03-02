from colored import Fore, Style

# make an enum for log levels
class LogLevel:
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4

def log(level, message):
    if level == LogLevel.DEBUG:
        print(f"{Fore.CYAN}[DEBUG] {Style.RESET_ALL}{message}")
    elif level == LogLevel.INFO:
        print(f"{Fore.GREEN}[INFO] {Style.RESET_ALL}{message}")
    elif level == LogLevel.WARN:
        print(f"{Fore.YELLOW}[WARN] {Style.RESET_ALL}{message}")
    elif level == LogLevel.ERROR:
        print(f"{Fore.RED}[ERROR] {Style.RESET_ALL}{message}")
    elif level == LogLevel.FATAL:
        print(f"{Fore.RED}[FATAL] {Style.RESET_ALL}{message}")
    else:
        print(f"{Fore.WHITE}[OTHER] {Style.RESET_ALL}{message}")