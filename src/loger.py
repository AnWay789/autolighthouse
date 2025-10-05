import time
import functools
import asyncio
from colorama import Fore, Style, init
from enum import Enum

# инициализация цветного вывода на Windows/Unix
init(autoreset=True)

class LogLevel(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARN"
    ERORR = "ERORR"
    SUCCESS = "SUCCESS"


def log_msg(message, level="info"):
    colors = {
        "INFO": Fore.CYAN,
        "DEBUG": Fore.BLUE,
        "WARN": Fore.YELLOW,
        "ERORR": Fore.RED,
        "SUCCESS" : Fore.GREEN
    }
    prefix = f"{colors.get(level, Fore.WHITE)}[{level.upper()}]{Style.RESET_ALL}"
    print(f"[MESSAGE]   -   {prefix} {message}")

def log_call(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        print(
            f"{Fore.CYAN}[CALL]{Style.RESET_ALL} {func.__name__}("
            f"{Fore.YELLOW}args={args}{Style.RESET_ALL}, "
            f"{Fore.YELLOW}kwargs={kwargs}{Style.RESET_ALL})"
        )
        try:
            result = await func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            print(
                f"{Fore.GREEN}[RETURN]{Style.RESET_ALL} {func.__name__} -> "
                f"{Fore.MAGENTA}{result}{Style.RESET_ALL} "
                f"({duration:.2f} ms)"
            )
            return result
        except Exception as e:
            duration = (time.time() - start) * 1000
            print(
                f"{Fore.RED}[ERROR]{Style.RESET_ALL} {func.__name__} "
                f"({duration:.2f} ms): {e}"
            )
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        print(
            f"{Fore.CYAN}[CALL]{Style.RESET_ALL} {func.__name__}("
            f"{Fore.YELLOW}args={args}{Style.RESET_ALL}, "
            f"{Fore.YELLOW}kwargs={kwargs}{Style.RESET_ALL})"
        )
        try:
            result = func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            print(
                f"{Fore.GREEN}[RETURN]{Style.RESET_ALL} {func.__name__} -> "
                f"{Fore.MAGENTA}{result}{Style.RESET_ALL} "
                f"({duration:.2f} ms)"
            )
            return result
        except Exception as e:
            duration = (time.time() - start) * 1000
            print(
                f"{Fore.RED}[ERROR]{Style.RESET_ALL} {func.__name__} "
                f"({duration:.2f} ms): {e}"
            )
            raise

    # выбираем правильный обёртчик для sync/async
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
